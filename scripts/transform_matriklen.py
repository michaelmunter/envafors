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
    "cvr", "bfe", "bfe_state", "role", "source_status", "virkning_fra_original",
    "actual_share_state", "actual_share_numerator", "actual_share_denominator",
    "registered_share_state", "registered_share_numerator", "registered_share_denominator",
    "source_pointer", "source_sha256", "verification_status",
]
ISSUE_FIELDS = ["cvr", "code", "source_pointer", "bfe", "message", "source_sha256"]


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
        sources.append((cvr, meta["sha256"], data))
    return sources


def normalize(cvr, sha, data):
    rows, issues = [], []

    def issue(code, pointer, bfe, message):
        issues.append(dict(zip(ISSUE_FIELDS, [cvr, code, pointer, bfe, message, sha])))

    def share(row, key, pointer, bfe):
        if key not in row:
            return "missing", "", ""
        value = row[key]
        if value is None:
            return "null", "", ""
        if isinstance(value, dict):
            numerator, denominator = value.get("tæller"), value.get("nævner")
            if type(numerator) is int and type(denominator) is int and numerator >= 0 and denominator > 0:
                if numerator > denominator or set(value) != {"tæller", "nævner"}:
                    issue("unusual_share", pointer + "/" + key, bfe, "Usædvanlig brøk; se originalen.")
                return "present", numerator, denominator
        issue("invalid_share", pointer + "/" + key, bfe, "Brøken kan ikke normaliseres; se originalen.")
        return "invalid", "", ""

    for role in ROLES:
        seen = set()
        for index, original in enumerate(data[role]):
            pointer = "/" + role + "/" + str(index)
            value = original.get("bfe")
            if "bfe" not in original:
                bfe_state, bfe = "missing", ""
            elif value is None:
                bfe_state, bfe = "null", ""
            elif (type(value) is int and value > 0) or (isinstance(value, str) and re.fullmatch(r"[0-9]+", value) and int(value) > 0):
                bfe_state, bfe = "present", str(value)
            else:
                bfe_state, bfe = "invalid", ""
            if bfe_state != "present":
                issue("invalid_or_missing_bfe", pointer + "/bfe", bfe, "Relationen bevares uden et gyldigt BFE.")
            status = original.get("status")
            if not isinstance(status, str):
                status = ""
            if status not in ("gældende", "historisk"):
                issue("unknown_source_status", pointer + "/status", bfe, "Ukendt kildestatus; se originalen.")
            date = original.get("virkningFra")
            if not isinstance(date, str):
                date = ""
                issue("invalid_or_missing_date", pointer + "/virkningFra", bfe, "Dato mangler eller har ukendt type.")
            actual = share(original, "faktiskEjerandel", pointer, bfe)
            registered = share(original, "tinglystEjerandel", pointer, bfe)
            if actual[0] == registered[0] == "present" and actual[1] * registered[2] != registered[1] * actual[2]:
                issue("different_share_values", pointer, bfe, "Faktisk og tinglyst ejerandel er forskellige; ingen vælges som facit.")
            if role == "ejer" and actual[0] != "present":
                issue("missing_actual_share", pointer, bfe, "Ejerpost uden normaliserbar faktisk ejerandel.")
            fingerprint = json.dumps(original, sort_keys=True, ensure_ascii=False)
            if fingerprint in seen:
                issue("duplicate_source_row", pointer, bfe, "Identisk kildepost gentaget; begge rækker bevares.")
            seen.add(fingerprint)
            unknown = set(original) - {"bfe", "status", "virkningFra", "faktiskEjerandel", "tinglystEjerandel"}
            if unknown:
                issue("unknown_fields", pointer, bfe, "Ekstra kildefelter findes i originalen: " + ", ".join(sorted(unknown)))
            rows.append(dict(zip(RELATION_FIELDS, [
                cvr, bfe, bfe_state, role, status, date, *actual, *registered, pointer, sha, "source_only",
            ])))
    if len(rows) != sum(len(data[role]) for role in ROLES):
        raise ValueError("Afstemning fejlede for CVR " + cvr)
    return rows, issues


def build_outputs(sources):
    rows, issues = [], []
    for cvr, sha, data in sources:
        source_rows, source_issues = normalize(cvr, sha, data)
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
