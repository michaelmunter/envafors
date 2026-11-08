"""Check that the source overview follows the files and exposes mismatches."""

from contextlib import redirect_stderr, redirect_stdout
import csv
from html.parser import HTMLParser
from io import StringIO
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from fetch_matriklen import API_URL, digest
from show_sources import main, render
from source_overview_data import read_catalog, read_matriklen
from transform_matriklen import transform


SOURCE_FIELDS = (
    "source_id", "title", "publisher", "url", "document_date", "researched_on",
    "source_type", "origin_system", "capture_status", "notes",
)
CANDIDATE_FIELDS = (
    "candidate_id", "cvr", "name", "scope_group", "candidate_kind", "source_ids",
    "evidence_status", "current_cvr_status", "relation_status", "next_check", "notes",
)


class PageLinks(HTMLParser):
    def __init__(self, page):
        super().__init__()
        self.hrefs = []
        self.feed(page)

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs.extend(value for name, value in attrs if name == "href")


class SourceOverviewTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.research = self.root / "research"
        self.research.mkdir()
        self.raw = self.root / "data" / "raw" / "matriklen-labs"
        self.raw.mkdir(parents=True)
        self.output = self.root / "data"
        self.sources = self.research / "sources.csv"
        self.candidates = self.research / "company_candidates.csv"
        self.write_csv(self.sources, SOURCE_FIELDS, [self.source("S001", "Kendt kilde")])
        self.write_csv(self.candidates, CANDIDATE_FIELDS, [])

    @staticmethod
    def write_csv(path, fields, rows):
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fields)
            writer.writeheader()
            writer.writerows(rows)

    @staticmethod
    def source(source_id, title, url="https://example.com/kilde"):
        return {
            "source_id": source_id, "title": title, "url": url, "publisher": "Udgiver",
            "researched_on": "2026-11-08", "source_type": "test_type",
            "origin_system": "Testsystem", "capture_status": "researched_not_archived",
            "notes": "Kildens oplysninger",
        }

    @staticmethod
    def candidate(source_ids):
        return {"candidate_id": "C001", "cvr": "11111111", "name": "Ny kandidat", "source_ids": source_ids}

    def save_lookup(self, cvr, owners):
        content = json.dumps({"administrerer": [], "ejer": owners}, ensure_ascii=False).encode("utf-8")
        (self.raw / f"{cvr}.json").write_bytes(content)
        path = self.raw / "index.json"
        index = json.loads(path.read_bytes()) if path.exists() else {}
        index[cvr] = {
            "url": API_URL + "?cvr=" + cvr,
            "retrieved_at": "2026-11-08T10:56:21+00:00",
            "sha256": digest(content),
        }
        path.write_text(json.dumps(index), encoding="utf-8")

    def test_new_source_and_its_candidate_links_come_from_csv(self):
        before, _ = render(self.root)
        self.assertNotIn("Ny kilde", before)
        self.write_csv(self.sources, SOURCE_FIELDS, [
            self.source("S001", "Kendt kilde"),
            self.source("S099", "Ny kilde", "https://example.com/ny?kilde=099"),
        ])
        self.write_csv(self.candidates, CANDIDATE_FIELDS, [self.candidate("S001|S099")])

        sources, references = read_catalog(self.root)
        self.assertEqual({source["source_id"] for source in sources}, {"S001", "S099"})
        self.assertEqual(references["S099"][0]["candidate_id"], "C001")
        page, _ = render(self.root)
        self.assertIn("Ny kilde", page)
        self.assertIn("Ny kandidat", page)
        self.assertIn("https://example.com/ny?kilde=099", PageLinks(page).hrefs)

    def test_unknown_candidate_source_is_an_explicit_error(self):
        self.write_csv(self.candidates, CANDIDATE_FIELDS, [self.candidate("S404")])
        with self.assertRaisesRegex(ValueError, "S404"):
            read_catalog(self.root)

    def test_new_cvr_from_index_is_visible_before_and_after_regeneration(self):
        owner = {"bfe": 123, "status": "gældende", "virkningFra": "original"}
        self.save_lookup("11111111", [])
        transform(self.raw, self.output)
        self.save_lookup("22222222", [owner])

        lookups, problem = read_matriklen(self.root)
        self.assertIsNotNone(problem)
        self.assertEqual({lookup["cvr"] for lookup in lookups}, {"11111111", "22222222"})
        self.assertTrue(all(lookup["relation_count"] is None for lookup in lookups))

        transform(self.raw, self.output)
        lookups, problem = read_matriklen(self.root)
        self.assertIsNone(problem)
        self.assertEqual({row["cvr"]: row["relation_count"] for row in lookups}, {
            "11111111": 0, "22222222": 1,
        })
        page, problem = render(self.root)
        self.assertIsNone(problem)
        self.assertIn(API_URL + "?cvr=22222222", PageLinks(page).hrefs)

    def test_changed_raw_bytes_suppress_counts(self):
        self.save_lookup("11111111", [])
        transform(self.raw, self.output)
        with (self.raw / "11111111.json").open("ab") as handle:
            handle.write(b" ")

        lookups, problem = read_matriklen(self.root)
        self.assertIn("SHA-256", problem)
        self.assertIsNone(lookups[0]["relation_count"])
        self.assertIsNone(lookups[0]["issue_count"])
        page, problem = render(self.root)
        self.assertIn("SHA-256", page)
        self.assertIsNotNone(problem)

    def test_changed_relation_value_fails_with_original_hash_and_row_count(self):
        owner = {"bfe": 123, "status": "gældende", "virkningFra": "original"}
        self.save_lookup("11111111", [owner])
        transform(self.raw, self.output)
        relations = self.output / "relations.csv"
        content = relations.read_bytes()
        altered = content.replace(b",123,", b",999,")
        self.assertNotEqual(altered, content)
        relations.write_bytes(altered)

        lookups, problem = read_matriklen(self.root)
        self.assertIn("relations.csv", problem)
        self.assertIsNone(lookups[0]["relation_count"])

    def test_failed_export_preserves_the_last_valid_snapshot(self):
        self.save_lookup("11111111", [])
        transform(self.raw, self.output)
        snapshot = self.root / "kilder.html"
        stderr = StringIO()

        with (
            patch("show_sources.REPO", self.root),
            patch.object(sys, "argv", ["show_sources.py", "--output", str(snapshot)]),
            redirect_stdout(StringIO()),
            redirect_stderr(stderr),
        ):
            main()
            original = snapshot.read_bytes()
            with (self.raw / "11111111.json").open("ab") as handle:
                handle.write(b" ")
            with self.assertRaises(SystemExit) as failure:
                main()

        self.assertEqual(failure.exception.code, 1)
        self.assertIn("SHA-256", stderr.getvalue())
        self.assertEqual(snapshot.read_bytes(), original)

    def test_catalog_text_is_escaped_and_unsafe_urls_are_inert(self):
        self.write_csv(self.sources, SOURCE_FIELDS, [
            self.source("S001", "<script>payload</script>", "javascript:alert(1)"),
        ])

        page, _ = render(self.root)
        self.assertIn("&lt;script&gt;payload&lt;/script&gt;", page)
        self.assertNotIn("<script>payload</script>", page)
        self.assertNotIn("javascript:alert(1)", PageLinks(page).hrefs)


if __name__ == "__main__":
    unittest.main()
