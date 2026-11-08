"""Regressionskontrol af datatab, sidste gode svar og den flade datastruktur."""

from contextlib import redirect_stderr, redirect_stdout
import csv
import hashlib
from io import StringIO
import json
from pathlib import Path
from types import SimpleNamespace
import sys
import tempfile
import unittest
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import fetch_matriklen as FETCH
import transform_matriklen as MODULE


class MatriklenDataIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.raw = self.root / "raw"
        self.raw.mkdir()
        self.output = self.root / "output"

    def save_source(self, payload, cvr="27736033"):
        self.save_raw(json.dumps(payload, ensure_ascii=False).encode("utf-8"), cvr)

    def save_raw(self, raw, cvr="27736033"):
        (self.raw / (cvr + ".json")).write_bytes(raw)
        path = self.raw / "index.json"
        index = json.loads(path.read_bytes()) if path.exists() else {}
        index[cvr] = {
            "url": FETCH.API_URL + "?cvr=" + cvr,
            "retrieved_at": "2026-11-08T10:56:21.029183+00:00",
            "sha256": hashlib.sha256(raw).hexdigest(),
        }
        path.write_text(json.dumps(index), encoding="utf-8")

    def read_csv(self, name):
        with (self.output / name).open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def test_repeated_and_missing_bfe_do_not_drop_relations(self):
        row = {"bfe": 123, "status": "gældende", "virkningFra": "original"}
        self.save_source({"administrerer": [row, row], "ejer": [{"status": "historisk"}]})
        summary = MODULE.transform(self.raw, self.output)
        self.assertEqual(summary["relation_rows"], 3)
        self.assertEqual(summary["unique_bfe"], 1)
        rows = self.read_csv("relations.csv")
        self.assertEqual([(row["role"], row["bfe"]) for row in rows],
                         [("administrerer", "123"), ("administrerer", "123"), ("ejer", "")])
        findings = {row["finding"] for row in self.read_csv("issues.csv")}
        self.assertIn("Identisk kildepost gentaget.", findings)
        self.assertIn("BFE-feltet mangler.", findings)

    def test_zero_null_and_missing_shares_and_historical_date_remain_distinct(self):
        date = "2018-01-01T00:00:00+01:00[Europe/Copenhagen]"
        self.save_source({"administrerer": [], "ejer": [
            {"bfe": 1, "status": "historisk", "virkningFra": date,
             "faktiskEjerandel": {"tæller": 0, "nævner": 1},
             "tinglystEjerandel": {"tæller": 1, "nævner": 1}},
            {"bfe": 2, "status": "gældende", "virkningFra": date,
             "faktiskEjerandel": None},
        ]})
        MODULE.transform(self.raw, self.output)
        rows = self.read_csv("relations.csv")
        self.assertEqual(rows[0]["actual_share_numerator"], "0")
        self.assertEqual(rows[0]["registered_share_numerator"], "1")
        self.assertEqual(rows[0]["virkning_fra_original"], date)
        self.assertNotIn("start_date", rows[0])
        self.assertNotIn("end_date", rows[0])
        self.assertEqual(rows[1]["actual_share_state"], "null")
        self.assertEqual(rows[1]["registered_share_state"], "missing")
        self.assertTrue(any(row["bfe"] == "1" and "ejerandel er forskellige" in row["finding"]
                            for row in self.read_csv("issues.csv")))

    def test_modified_raw_bytes_are_rejected_without_output(self):
        self.save_source({"administrerer": [], "ejer": []})
        with (self.raw / "27736033.json").open("ab") as handle:
            handle.write(b" ")
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            MODULE.transform(self.raw, self.output)
        self.assertFalse(self.output.exists())

    def test_unknown_shape_is_not_an_empty_success(self):
        self.save_source({"error": "service unavailable"})
        with self.assertRaisesRegex(ValueError, "Ukendt svarstruktur"):
            MODULE.transform(self.raw, self.output)
        self.assertFalse(self.output.exists())

    def test_duplicate_json_keys_cannot_hide_source_rows(self):
        self.save_raw(b'{"administrerer":[],"ejer":[{"bfe":123}],"ejer":[]}')
        with self.assertRaisesRegex(ValueError, "Dubleret JSON"):
            MODULE.transform(self.raw, self.output)
        self.assertFalse(self.output.exists())

    def test_non_json_numeric_constants_are_rejected(self):
        self.save_raw(b'{"administrerer":[],"ejer":[{"bfe":NaN}]}')
        with self.assertRaisesRegex(ValueError, "Ugyldigt JSON-tal"):
            MODULE.transform(self.raw, self.output)
        self.assertFalse(self.output.exists())

    def test_valid_empty_result_is_explicit_and_repeat_is_identical(self):
        self.save_source({"administrerer": [], "ejer": []})
        summary = MODULE.transform(self.raw, self.output)
        self.assertEqual(summary["result_state"], "empty_result")
        before = {path.name: path.read_bytes() for path in self.output.iterdir()}
        MODULE.transform(self.raw, self.output)
        self.assertEqual({path.name: path.read_bytes() for path in self.output.iterdir()}, before)
        self.assertEqual(set(before), {"relations.csv", "issues.csv"})

    def test_same_bfe_can_have_relations_to_multiple_cvrs(self):
        payload = {"administrerer": [{"bfe": 123, "status": "gældende", "virkningFra": "original"}], "ejer": []}
        self.save_source(payload)
        self.save_source(payload, "26863902")
        summary = MODULE.transform(self.raw, self.output)
        self.assertEqual(summary["cvr_count"], 2)
        self.assertEqual(summary["relation_rows"], 2)
        rows = self.read_csv("relations.csv")
        self.assertEqual({(row["cvr"], row["bfe"], row["role"]) for row in rows},
                         {("27736033", "123", "administrerer"), ("26863902", "123", "administrerer")})

    def test_index_and_file_mismatch_does_not_replace_previous_output(self):
        self.save_source({"administrerer": [], "ejer": []})
        MODULE.transform(self.raw, self.output)
        before = (self.output / "relations.csv").read_bytes()
        (self.raw / "27736033.json").unlink()
        with self.assertRaisesRegex(ValueError, "stemmer ikke"):
            MODULE.transform(self.raw, self.output)
        self.assertEqual((self.output / "relations.csv").read_bytes(), before)

    def test_unregistered_file_cannot_be_silently_ignored(self):
        self.save_source({"administrerer": [], "ejer": []})
        (self.raw / "26863902.json").write_bytes(b'{}')
        with self.assertRaisesRegex(ValueError, "stemmer ikke"):
            MODULE.transform(self.raw, self.output)
        self.assertFalse(self.output.exists())

    def test_source_url_cannot_assign_another_cvrs_answer(self):
        self.save_source({"administrerer": [], "ejer": []})
        path = self.raw / "index.json"
        index = json.loads(path.read_bytes())
        index["27736033"]["url"] = FETCH.API_URL + "?cvr=26863902"
        path.write_text(json.dumps(index), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "matcher ikke CVR"):
            MODULE.transform(self.raw, self.output)
        self.assertFalse(self.output.exists())

    def test_failed_fetch_keeps_last_good_answer_and_index(self):
        self.save_source({"administrerer": [], "ejer": []})
        before = {path.name: path.read_bytes() for path in self.raw.iterdir()}
        for http_status, payload in [("503", b'outage'), ("200", b'{"error":"outage"}'), ("200", b'{"ejer":[],"ejer":[],"administrerer":[]}')]:
            with self.subTest(http_status=http_status, payload=payload):
                def fake_curl(command, **kwargs):
                    Path(command[command.index("--output") + 1]).write_bytes(payload)
                    return SimpleNamespace(returncode=0, stdout=http_status, stderr="")
                with patch.object(FETCH.subprocess, "run", side_effect=fake_curl):
                    with self.assertRaises(ValueError):
                        FETCH.fetch("27736033", self.raw)
                self.assertEqual({path.name: path.read_bytes() for path in self.raw.iterdir()}, before)

    def test_successful_refresh_replaces_payload_without_reformatting_or_archive(self):
        self.save_source({"administrerer": [], "ejer": []})
        payload = b'{ "ejer": [], "administrerer": [] }\n'
        def fake_curl(command, **kwargs):
            Path(command[command.index("--output") + 1]).write_bytes(payload)
            return SimpleNamespace(returncode=0, stdout="200", stderr="")
        with patch.object(FETCH.subprocess, "run", side_effect=fake_curl):
            FETCH.fetch("27736033", self.raw)
        self.assertEqual((self.raw / "27736033.json").read_bytes(), payload)
        index = json.loads((self.raw / "index.json").read_bytes())
        self.assertEqual(index["27736033"]["sha256"], hashlib.sha256(payload).hexdigest())
        self.assertEqual({path.name for path in self.raw.iterdir()}, {"27736033.json", "index.json"})

    def test_candidate_refresh_keeps_empty_results_and_reports_failed_lookups(self):
        candidates = self.root / "candidates.csv"
        candidates.write_text(
            "cvr,property_scope\n25133374,fravalgt\n27736033,omfattet\n28113285,omfattet\n",
            encoding="utf-8",
        )
        self.save_source({"administrerer": [], "ejer": [{"bfe": 456}]})
        old_response = (self.raw / "27736033.json").read_bytes()
        old_entry = FETCH.read_index(self.raw)["27736033"]
        empty_response = b'{"administrerer":[],"ejer":[]}'
        populated_response = b'{"administrerer":[],"ejer":[{"bfe":123}]}'

        def fake_curl(command, **kwargs):
            cvr = command[-1].split("=")[-1]
            if cvr == "27736033":
                return SimpleNamespace(returncode=0, stdout="503", stderr="")
            payload = empty_response if cvr == "25133374" else populated_response
            Path(command[command.index("--output") + 1]).write_bytes(payload)
            return SimpleNamespace(returncode=0, stdout="200", stderr="")

        stdout, stderr = StringIO(), StringIO()
        argv = ["fetch_matriklen.py", "--all-candidates", "--raw-root", str(self.raw)]
        with patch.object(sys, "argv", argv), patch.object(FETCH, "CANDIDATES", candidates), \
                patch.object(FETCH.subprocess, "run", side_effect=fake_curl), \
                redirect_stdout(stdout), redirect_stderr(stderr):
            self.assertEqual(FETCH.main(), 1)

        summaries = [json.loads(line) for line in stdout.getvalue().splitlines()]
        self.assertEqual([(row["cvr"], row["rows"]) for row in summaries],
                         [("25133374", 0), ("28113285", 1)])
        failure = json.loads(stderr.getvalue())
        self.assertEqual(failure["cvr"], "27736033")
        self.assertIn("503", failure["error"])
        self.assertEqual((self.raw / "25133374.json").read_bytes(), empty_response)
        self.assertEqual((self.raw / "28113285.json").read_bytes(), populated_response)
        self.assertEqual((self.raw / "27736033.json").read_bytes(), old_response)
        self.assertEqual(FETCH.read_index(self.raw)["27736033"], old_entry)

    def test_write_failure_restores_both_previous_outputs(self):
        self.save_source({"administrerer": [], "ejer": []})
        MODULE.transform(self.raw, self.output)
        before = {path.name: path.read_bytes() for path in self.output.iterdir()}
        original_replace = Path.replace
        def fail_second_file(path, target):
            if path.name == "issues.csv":
                raise OSError("simuleret skrivefejl")
            return original_replace(path, target)
        with patch.object(Path, "replace", fail_second_file):
            with self.assertRaises(OSError):
                MODULE.transform(self.raw, self.output)
        self.assertEqual({path.name: path.read_bytes() for path in self.output.iterdir()}, before)


if __name__ == "__main__":
    unittest.main()
