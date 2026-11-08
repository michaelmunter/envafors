"""Regressionskontrol af datatab, fejlfortolkning og ændring af rådata."""

import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/transform_matriklen.py"
SPEC = importlib.util.spec_from_file_location("transform_matriklen", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class MatriklenDataIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.capture = self.root / "raw" / "capture"
        self.capture.mkdir(parents=True)
        self.output = self.root / "run"

    def save_capture(self, payload, status="http_success", http_status=200):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.save_raw_capture(raw, status, http_status)

    def save_raw_capture(self, raw, status="http_success", http_status=200):
        (self.capture / "response.body").write_bytes(raw)
        (self.capture / "request.json").write_text(json.dumps({
            "request_url": "https://example.invalid/?cvr=27736033",
            "request_parameters": {"cvr": "27736033"},
            "response_file": "response.body",
            "response_sha256": hashlib.sha256(raw).hexdigest(),
            "status": status, "http_status": http_status,
        }), encoding="utf-8")

    def read_csv(self, relative):
        with (self.output / relative).open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def test_repeated_and_missing_bfe_do_not_drop_relations(self):
        row = {"bfe": 123, "status": "gældende", "virkningFra": "original"}
        self.save_capture({"administrerer": [row, row], "ejer": [{"status": "historisk"}]})
        profile = MODULE.transform(self.capture, self.output)
        self.assertEqual(profile["source_relation_rows"], 3)
        self.assertEqual(profile["output_relation_rows"], 3)
        self.assertEqual(profile["unique_valid_bfe"], 1)
        self.assertEqual(profile["relations_without_valid_bfe"], 1)
        rows = self.read_csv("processed/relations.csv")
        self.assertEqual(len({row["relation_id"] for row in rows}), 3)
        self.assertEqual(rows[2]["bfe_state"], "missing")
        properties = self.read_csv("processed/properties.csv")
        self.assertEqual(properties[0]["relation_count"], "2")
        self.assertEqual(len(properties[0]["relation_ids"].split("|")), 2)

    def test_zero_null_and_missing_shares_and_historical_date_remain_distinct(self):
        date = "2018-01-01T00:00:00+01:00[Europe/Copenhagen]"
        self.save_capture({"administrerer": [], "ejer": [
            {"bfe": 1, "status": "historisk", "virkningFra": date,
             "faktiskEjerandel": {"tæller": 0, "nævner": 1},
             "tinglystEjerandel": {"tæller": 1, "nævner": 1}},
            {"bfe": 2, "status": "gældende", "virkningFra": date,
             "faktiskEjerandel": None},
        ]})
        MODULE.transform(self.capture, self.output)
        rows = self.read_csv("processed/relations.csv")
        self.assertEqual(rows[0]["actual_share_numerator"], "0")
        self.assertEqual(rows[0]["registered_share_numerator"], "1")
        self.assertEqual(rows[0]["virkning_fra_original"], date)
        self.assertNotIn("start_date", rows[0])
        self.assertNotIn("end_date", rows[0])
        self.assertEqual(rows[1]["actual_share_state"], "null")
        self.assertEqual(rows[1]["registered_share_state"], "missing")
        issues = self.read_csv("quality/issues.csv")
        self.assertTrue(any(row["code"] == "different_share_values" for row in issues))

    def test_modified_raw_bytes_are_rejected_without_output(self):
        self.save_capture({"administrerer": [], "ejer": []})
        with (self.capture / "response.body").open("ab") as handle:
            handle.write(b" ")
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            MODULE.transform(self.capture, self.output)
        self.assertFalse(self.output.exists())

    def test_http_error_is_not_an_empty_success(self):
        self.save_capture({"administrerer": [], "ejer": []}, "http_error", 503)
        with self.assertRaisesRegex(ValueError, "HTTP 200"):
            MODULE.transform(self.capture, self.output)
        self.assertFalse(self.output.exists())

    def test_unknown_shape_is_not_an_empty_success(self):
        self.save_capture({"error": "service unavailable"})
        with self.assertRaisesRegex(ValueError, "Ukendt svarstruktur"):
            MODULE.transform(self.capture, self.output)
        self.assertFalse(self.output.exists())

    def test_duplicate_json_keys_cannot_hide_source_rows(self):
        self.save_raw_capture(b'{"administrerer":[],"ejer":[{"bfe":123}],"ejer":[]}')
        with self.assertRaisesRegex(ValueError, "Dubleret JSON"):
            MODULE.transform(self.capture, self.output)
        self.assertFalse(self.output.exists())

    def test_non_json_numeric_constants_are_rejected(self):
        self.save_raw_capture(b'{"administrerer":[],"ejer":[{"bfe":NaN}]}')
        with self.assertRaisesRegex(ValueError, "Ugyldigt JSON-tal"):
            MODULE.transform(self.capture, self.output)
        self.assertFalse(self.output.exists())

    def test_valid_empty_result_is_explicit_and_existing_output_is_protected(self):
        self.save_capture({"administrerer": [], "ejer": []})
        MODULE.transform(self.capture, self.output)
        manifest = json.loads((self.output / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "complete")
        self.assertEqual(manifest["result_state"], "empty_result")
        before = (self.output / "manifest.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "findes allerede"):
            MODULE.transform(self.capture, self.output)
        self.assertEqual((self.output / "manifest.json").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
