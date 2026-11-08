"""Genbyg én samlet relationstabel og konkrete kontrolfund fra alle CVR-svar."""

import argparse
from collections import Counter
import csv
from datetime import datetime
import io
import json
from pathlib import Path
import re

from fetch_matriklen import API_URL, RAW_ROOT, REPO, ROLES, digest, parse_json, read_index, replace_files, validate_payload


RELATION_FIELDS = [
    "cvr", "bfe", "role", "source_status", "virkning_fra_original",
    "actual_share_state", "actual_share_numerator", "actual_share_denominator",
    "registered_share_state", "registered_share_numerator", "registered_share_denominator",
]
ISSUE_FIELDS = ["cvr", "bfe", "role", "finding"]


def csv_bytes(fields, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def load_sources(raw_root, *, index=None):
    """Kontrollér råsvar mod et kildeindeks læst med read_index."""
    if index is None:
        index = read_index(raw_root)
    if not index:
        raise ValueError("Ingen registrerede kildesvar; det er ikke et tomt CVR-resultat.")
    sources = []
    for cvr, meta in sorted(index.items()):
        if not isinstance(meta, dict) or not all(isinstance(meta.get(key), str) for key in ("url", "retrieved_at", "sha256")):
            raise ValueError("Mangelfulde kildeoplysninger for CVR " + cvr)
        if meta["url"] != API_URL + "?cvr=" + cvr:
            raise ValueError("Kilde-URL matcher ikke CVR " + cvr)
        if not re.fullmatch(r"[0-9a-f]{64}", meta["sha256"]):
            raise ValueError("Ugyldigt kildehash for CVR " + cvr)
        if datetime.fromisoformat(meta["retrieved_at"]).utcoffset() is None:
            raise ValueError("Hentetid mangler tidszone for CVR " + cvr)
        raw = (raw_root / (cvr + ".json")).read_bytes()
        if digest(raw) != meta["sha256"]:
            raise ValueError("Råsvarets SHA-256 stemmer ikke med indekset for CVR " + cvr)
        data = parse_json(raw)
        validate_payload(data)
        sources.append((cvr, data))
    return sources


def normalize(cvr, data):
    rows, issues = [], []

    def issue(bfe, role, finding):
        issues.append(dict(cvr=cvr, bfe=bfe, role=role, finding=finding))

    def share(row, key, bfe, role):
        if key not in row:
            return "missing", "", ""
        value = row[key]
        if value is None:
            return "null", "", ""
        if isinstance(value, dict):
            numerator, denominator = value.get("tæller"), value.get("nævner")
            if type(numerator) is int and type(denominator) is int and numerator >= 0 and denominator > 0:
                if numerator > denominator or set(value) != {"tæller", "nævner"}:
                    issue(bfe, role, f"Usædvanlig brøk i {key}.")
                return "present", numerator, denominator
        issue(bfe, role, f"Ugyldig brøk i {key}.")
        return "invalid", "", ""

    for role in ROLES:
        seen = set()
        for original in data[role]:
            value = original.get("bfe")
            bfe = ""
            if "bfe" not in original:
                issue(bfe, role, "BFE-feltet mangler.")
            elif value is None:
                issue(bfe, role, "BFE er angivet som null.")
            elif (type(value) is int and value > 0) or (isinstance(value, str) and re.fullmatch(r"[0-9]+", value) and int(value) > 0):
                bfe = str(value)
            else:
                issue(bfe, role, "BFE-værdien er ugyldig.")
            status = original.get("status")
            if not isinstance(status, str):
                status = ""
            if status not in ("gældende", "historisk"):
                issue(bfe, role, "Ukendt kildestatus.")
            date = original.get("virkningFra")
            if not isinstance(date, str):
                date = ""
                issue(bfe, role, "Feltet virkningFra mangler eller har ukendt type.")
            actual = share(original, "faktiskEjerandel", bfe, role)
            registered = share(original, "tinglystEjerandel", bfe, role)
            if actual[0] == registered[0] == "present" and actual[1] * registered[2] != registered[1] * actual[2]:
                issue(bfe, role, "Faktisk og tinglyst ejerandel er forskellige.")
            if role == "ejer" and actual[0] == "missing":
                issue(bfe, role, "Faktisk ejerandel mangler.")
            elif role == "ejer" and actual[0] == "null":
                issue(bfe, role, "Faktisk ejerandel er angivet som null.")
            fingerprint = json.dumps(original, sort_keys=True, ensure_ascii=False)
            if fingerprint in seen:
                issue(bfe, role, "Identisk kildepost gentaget.")
            seen.add(fingerprint)
            unknown = set(original) - {"bfe", "status", "virkningFra", "faktiskEjerandel", "tinglystEjerandel"}
            if unknown:
                issue(bfe, role, "Ekstra kildefelter: " + ", ".join(sorted(unknown)))
            rows.append(dict(zip(RELATION_FIELDS, [
                cvr, bfe, role, status, date, *actual, *registered,
            ])))
    if len(rows) != sum(len(data[role]) for role in ROLES):
        raise ValueError("Afstemning fejlede for CVR " + cvr)
    return rows, issues


def build_outputs(sources):
    rows, issues = [], []
    for cvr, data in sources:
        source_rows, source_issues = normalize(cvr, data)
        rows.extend(source_rows)
        issues.extend(source_issues)
    files = {
        "relations.csv": csv_bytes(RELATION_FIELDS, rows),
        "issues.csv": csv_bytes(ISSUE_FIELDS, issues),
    }
    return files, rows, issues


def transform(raw_root=RAW_ROOT, output=REPO / "data"):
    raw_root, output = Path(raw_root).resolve(), Path(output).resolve()
    if output == raw_root or raw_root in output.parents:
        raise ValueError("Bearbejdede filer skal ligge uden for rådatamappen.")
    # Alle kilder kontrolleres, og begge output beregnes, før eksisterende filer røres.
    sources = load_sources(raw_root)
    files, rows, issues = build_outputs(sources)
    replace_files({output / name: content for name, content in files.items()})
    return {
        "cvr_count": len(sources), "relation_rows": len(rows),
        "unique_bfe": len({row["bfe"] for row in rows if row["bfe"]}),
        "rows_by_role_and_source_status": dict(Counter(row["role"] + ":" + row["source_status"] for row in rows)),
        "issue_count": len(issues), "result_state": "nonempty_result" if rows else "empty_result",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=RAW_ROOT, help="Flad mappe med CVR-JSON og index.json")
    parser.add_argument("--output", type=Path, default=REPO / "data", help="Mappe med de to fælles CSV-filer")
    args = parser.parse_args()
    try:
        summary = transform(args.input, args.output)
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
