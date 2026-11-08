"""Lav sporbare pilot-CSV'er og kvalitetsprofil fra ét bevaret Labs-svar."""

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile


VERSION = "1"
ROLES = ("administrerer", "ejer")
RELATION_FIELDS = [
    "relation_id", "cvr", "bfe", "bfe_state", "role", "source_status",
    "virkning_fra_original", "actual_share_state", "actual_share_numerator",
    "actual_share_denominator", "registered_share_state", "registered_share_numerator",
    "registered_share_denominator", "source_capture_id", "source_pointer",
    "source_sha256", "verification_status",
]
PROPERTY_FIELDS = [
    "bfe", "relation_count", "relation_ids", "source_capture_id", "source_sha256",
    "verification_status",
]
ISSUE_FIELDS = ["issue_id", "severity", "code", "source_pointer", "bfe", "message"]


def digest(content):
    return hashlib.sha256(content).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def transform(capture, output):
    capture, output = capture.resolve(), output.resolve()
    if output.exists():
        raise ValueError("Output findes allerede; vælg en ny mappe. Eksisterende kørsler overskrives ikke.")
    if output == capture or capture in output.parents or output in capture.parents:
        raise ValueError("Output skal ligge separat fra rådata.")
    request_bytes = (capture / "request.json").read_bytes()
    meta = json.loads(request_bytes)
    if meta.get("status") != "http_success" or meta.get("http_status") != 200:
        raise ValueError("Hentningen er ikke et HTTP 200-svar; fejl må ikke blive til tomme data.")
    if not re.fullmatch(r"[0-9]{8}", str(meta.get("request_parameters", {}).get("cvr", ""))):
        raise ValueError("Manifestet mangler et entydigt CVR på otte cifre.")
    name = meta.get("response_file")
    if not isinstance(name, str) or Path(name).name != name or name in (".", ".."):
        raise ValueError("Manifestets response_file skal være et filnavn i rådatamappen.")
    raw = (capture / name).read_bytes()
    sha = digest(raw)
    if sha != meta.get("response_sha256"):
        raise ValueError("Råsvarets SHA-256 stemmer ikke med manifestet.")
    data = json.loads(raw)
    if not isinstance(data, dict) or set(data) != set(ROLES):
        raise ValueError("Ukendt svarstruktur; forventede præcis administrerer og ejer.")
    if any(not isinstance(data[role], list) for role in ROLES):
        raise ValueError("Ukendt svarstruktur: begge roller skal være lister.")
    if any(not isinstance(row, dict) for role in ROLES for row in data[role]):
        raise ValueError("Ukendt svarstruktur: hver relation skal være et objekt.")

    issues = []

    def issue(code, pointer="", bfe="", severity="warning", message=""):
        issues.append(dict(zip(ISSUE_FIELDS, [
            "Q" + str(len(issues) + 1).zfill(4), severity, code, pointer, bfe, message,
        ])))

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
                    issue("unusual_share", pointer + "/" + key, bfe, message="Usædvanlig brøk; originalen er bevaret.")
                return "present", numerator, denominator
        issue("invalid_share", pointer + "/" + key, bfe, message="Brøken kan ikke normaliseres; se originalen.")
        return "invalid", "", ""

    issue("date_semantics_unresolved", severity="info", message="virkningFra bevares ufortolket; ingen start- eller slutdato udledes.")
    issue("coverage_unverified", severity="info", message="Ét CVR-opslag; API-historik, paginering og fuldstændighed er ikke dokumenteret.")
    rows, by_bfe = [], defaultdict(list)
    role_profile = {}
    cvr = str(meta["request_parameters"]["cvr"])
    for role in ROLES:
        seen, statuses, fields = set(), Counter(), Counter()
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
                issue("invalid_or_missing_bfe", pointer + "/bfe", message="Relationen bevares; intet ejendoms-ID oprettes.")
            status = original.get("status")
            if not isinstance(status, str):
                status = ""
            if status not in ("gældende", "historisk"):
                issue("unknown_source_status", pointer + "/status", bfe, message="Kildestatus er ukendt; se originalen.")
            date = original.get("virkningFra")
            if not isinstance(date, str):
                date = ""
                issue("invalid_or_missing_date", pointer + "/virkningFra", bfe, message="Datoværdi mangler eller har ukendt type; se originalen.")
            actual = share(original, "faktiskEjerandel", pointer, bfe)
            registered = share(original, "tinglystEjerandel", pointer, bfe)
            if actual[0] == registered[0] == "present" and actual[1] * registered[2] != registered[1] * actual[2]:
                issue("different_share_values", pointer, bfe, message="Faktisk og tinglyst ejerandel er forskellige; ingen af dem vælges som facit.")
            if role == "ejer" and actual[0] != "present":
                issue("missing_actual_share", pointer, bfe, message="Ejerpost uden normaliserbar faktisk ejerandel.")
            fingerprint = json.dumps(original, sort_keys=True, ensure_ascii=False)
            if fingerprint in seen:
                issue("duplicate_source_row", pointer, bfe, message="Identisk kildepost gentaget; begge rækker bevares.")
            seen.add(fingerprint)
            unknown = set(original) - {"bfe", "status", "virkningFra", "faktiskEjerandel", "tinglystEjerandel"}
            if unknown:
                issue("unknown_fields", pointer, bfe, message="Ekstra kildefelter findes kun i originalen: " + ", ".join(sorted(unknown)))
            relation_id = capture.name + ":" + role + ":" + str(index)
            row = dict(zip(RELATION_FIELDS, [
                relation_id, cvr, bfe, bfe_state, role, status, date,
                *actual, *registered, capture.name, pointer, sha, "source_only",
            ]))
            rows.append(row)
            if bfe:
                by_bfe[bfe].append(relation_id)
            statuses[status] += 1
            fields.update(original.keys())
        role_profile[role] = {
            "source_rows": len(data[role]), "rows_by_source_status": dict(statuses),
            "field_occurrences": dict(fields), "exact_duplicate_rows": len(data[role]) - len(seen),
        }
    if len(rows) != sum(len(data[role]) for role in ROLES):
        raise ValueError("Afstemning fejlede: ikke alle kilderelationer er bevaret.")
    properties = [dict(zip(PROPERTY_FIELDS, [
        bfe, len(ids), "|".join(ids), capture.name, sha, "source_only",
    ])) for bfe, ids in sorted(by_bfe.items(), key=lambda pair: int(pair[0]))]
    script_sha = digest(Path(__file__).read_bytes())
    profile = {
        "input_sha256": sha, "roles": role_profile, "source_relation_rows": len(rows),
        "output_relation_rows": len(rows), "unique_valid_bfe": len(properties),
        "relations_without_valid_bfe": sum(not row["bfe"] for row in rows),
        "issue_counts": dict(Counter(item["code"] for item in issues)),
        "technical_validation": "passed_with_findings" if issues else "passed",
        "verification_status": "source_only", "coverage_status": "unverified",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".matriklen-stage-", dir=output.parent))
    try:
        (stage / "processed").mkdir()
        (stage / "quality").mkdir()
        write_csv(stage / "processed/relations.csv", RELATION_FIELDS, rows)
        write_csv(stage / "processed/properties.csv", PROPERTY_FIELDS, properties)
        write_json(stage / "quality/profile.json", profile)
        write_csv(stage / "quality/issues.csv", ISSUE_FIELDS, issues)
        files = {str(path.relative_to(stage)): digest(path.read_bytes()) for path in sorted(stage.rglob("*")) if path.is_file()}
        manifest = {
            "status": "complete", "result_state": "empty_result" if not rows else "nonempty_result",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "input_capture": os.path.relpath(capture, Path(__file__).resolve().parents[1]),
            "source_url": meta["request_url"], "request_parameters": meta["request_parameters"],
            "source_completed_at": meta.get("completed_at"), "input_sha256": sha,
            "request_manifest_sha256": digest(request_bytes), "transform_version": VERSION,
            "transform_sha256": script_sha, "output_sha256": files,
            "verification_status": "source_only", "coverage_status": "unverified",
        }
        write_json(stage / "manifest.json", manifest)
        # Mappen bliver først synlig som et færdigt run, når alle filer er skrevet.
        if output.exists():
            raise ValueError("Output blev oprettet af en anden proces; ingen overskrivning udført.")
        stage.rename(output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return profile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Mappe med request.json og originalsvar")
    parser.add_argument("--output", required=True, type=Path, help="Ny, separat kørselsmappe")
    args = parser.parse_args()
    try:
        profile = transform(args.input, args.output)
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps({"output": str(args.output), **profile}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
