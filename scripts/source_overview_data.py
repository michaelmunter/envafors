"""Læs kilderegisteret og kontrollér Matriklen Labs-sporet uden at ændre data."""

from collections import Counter
import csv
from pathlib import Path

from fetch_matriklen import API_URL, RAW_ROOT, REPO, read_index
from transform_matriklen import build_outputs, load_sources


SOURCE_FIELDS = {
    "source_id", "title", "publisher", "url", "document_date", "researched_on",
    "source_type", "origin_system", "capture_status", "notes",
}
CANDIDATE_FIELDS = {"candidate_id", "cvr", "name", "source_ids"}


def read_csv(path, required_fields):
    rows = []
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, strict=True)
            fields = reader.fieldnames or []
            if len(fields) != len(set(fields)) or any(not field.strip() for field in fields):
                raise ValueError(f"{path.name} har tomme eller dublerede kolonnenavne.")
            missing = required_fields - set(fields)
            if missing:
                raise ValueError(f"{path.name} mangler kolonnerne {', '.join(sorted(missing))}.")
            for row in reader:
                if None in row or None in row.values():
                    raise ValueError(f"{path.name} har forkert antal felter ved linje {reader.line_num}.")
                rows.append(row)
    except (csv.Error, UnicodeError) as error:
        raise ValueError(f"{path.name} kan ikke læses som UTF-8 CSV. {error}") from error
    return rows


def read_catalog(root):
    research = Path(root) / "research"
    sources = read_csv(research / "sources.csv", SOURCE_FIELDS)
    candidate_refs = {}
    for source in sources:
        source_id = source["source_id"]
        if not source_id or "|" in source_id or any(char.isspace() for char in source_id):
            raise ValueError(f"sources.csv har et ugyldigt kilde-ID {source_id!r}.")
        if source_id in candidate_refs:
            raise ValueError(f"sources.csv har dubleret kilde-ID {source_id!r}.")
        candidate_refs[source_id] = []
    for candidate in read_csv(research / "company_candidates.csv", CANDIDATE_FIELDS):
        source_ids = candidate["source_ids"]
        if not source_ids:
            continue
        for source_id in dict.fromkeys(source_ids.split("|")):
            if source_id not in candidate_refs:
                raise ValueError(
                    f"Kandidat {candidate['candidate_id']} i company_candidates.csv "
                    f"henviser til ukendt kilde-ID {source_id!r}."
                )
            candidate_refs[source_id].append(candidate)
    return sources, candidate_refs


def read_matriklen(root):
    root = Path(root)
    raw_root = root / RAW_ROOT.relative_to(REPO)
    output = root / "data"
    lookups = []
    try:
        index = read_index(raw_root)
        if not index:
            if (output / "relations.csv").exists() or (output / "issues.csv").exists():
                return [], "Der findes afledte CSV-filer uden registrerede Matriklen Labs-opslag."
            return [], None
        for cvr, entry in sorted(index.items()):
            meta = entry if isinstance(entry, dict) else {}
            url = meta.get("url")
            retrieved_at = meta.get("retrieved_at")
            sha256 = meta.get("sha256")
            lookups.append({
                "cvr": cvr,
                "url": url if url == API_URL + "?cvr=" + cvr else "",
                "retrieved_at": retrieved_at if isinstance(retrieved_at, str) else "",
                "sha256": sha256 if isinstance(sha256, str) else "",
                "relation_count": None,
                "issue_count": None,
            })
        files, rows, issues = build_outputs(load_sources(raw_root, index=index))
        for name, expected in files.items():
            path = output / name
            if not path.is_file():
                return lookups, f"data/{name} mangler som almindelig fil."
            if path.read_bytes() != expected:
                return lookups, f"data/{name} stemmer ikke med transformationen af de registrerede råsvar."
    except (OSError, ValueError) as error:
        return lookups, str(error)

    relations_by_cvr = Counter(row["cvr"] for row in rows)
    issues_by_cvr = Counter(issue["cvr"] for issue in issues)
    for lookup in lookups:
        lookup["relation_count"] = relations_by_cvr[lookup["cvr"]]
        lookup["issue_count"] = issues_by_cvr[lookup["cvr"]]
    return lookups, None
