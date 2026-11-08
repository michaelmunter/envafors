"""Hent ét offentligt CVR-opslag og bevar svar og metadata uden normalisering."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


REPO = Path(__file__).resolve().parents[1]
API_URL = "https://api.labs.matriklen.dk/CvrEjerskaber"
VERSION = "1"


def parse_json(content):
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Dubleret JSON-nøgle: " + key)
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError("Ugyldigt JSON-tal: " + value)

    return json.loads(content, object_pairs_hook=unique_keys, parse_constant=invalid_constant)


def fetch(cvr, raw_root):
    if not re.fullmatch(r"[0-9]{8}", cvr):
        raise ValueError("CVR skal være otte cifre. Dette kontrollerer ikke registreringen i CVR.")
    started = datetime.now(timezone.utc)
    folder = raw_root / (started.strftime("%Y%m%dT%H%M%S%fZ") + "_" + cvr)
    folder.mkdir(parents=True, exist_ok=False)
    body_path = folder / "response.body"
    headers_path = folder / "response.headers"
    meta = {
        "request_url": API_URL + "?cvr=" + cvr,
        "request_method": "GET",
        "request_parameters": {"cvr": cvr},
        "started_at": started.isoformat(),
        "collector_version": VERSION,
        "collector_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "fetch_method": "curl; TLS verification; redirects followed; maximum 45 seconds",
        "validation_status": "unreviewed",
        "pagination_status": "not_documented_not_followed",
        "status": "not_completed",
    }
    command = [
        "curl", "--silent", "--show-error", "--location", "--max-time", "45",
        "--header", "Accept: application/json",
        "--user-agent", "Envafors-Public-Data-Research/0.1",
        "--dump-header", str(headers_path), "--output", str(body_path),
        "--write-out", "%{http_code}\n%{url_effective}\n%{content_type}\n",
        meta["request_url"],
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=50)
        fields = result.stdout.splitlines()
        code = int(fields[0]) if fields and fields[0].isdigit() else None
        meta.update({
            "curl_exit_code": result.returncode,
            "http_status": code,
            "final_url": fields[1] if len(fields) > 1 else None,
            "content_type": fields[2] if len(fields) > 2 else None,
            "status": "transport_error" if result.returncode else (
                "http_success" if code and 200 <= code < 300 else "http_error"
            ),
        })
        if result.stderr:
            meta["error"] = result.stderr.strip()
    except (OSError, subprocess.TimeoutExpired) as error:
        meta.update({"status": "transport_error", "error": str(error)})
    finally:
        if headers_path.exists():
            meta["response_headers_file"] = headers_path.name
        if body_path.exists():
            body = body_path.read_bytes()
            meta.update({
                "response_file": body_path.name,
                "response_bytes": len(body),
                "response_sha256": hashlib.sha256(body).hexdigest(),
            })
            try:
                parsed = parse_json(body)
                meta["json_valid"] = True
                meta["json_root_type"] = type(parsed).__name__
                if isinstance(parsed, (dict, list)):
                    meta["json_top_level_count"] = len(parsed)
                if isinstance(parsed, dict):
                    meta["json_top_level_keys"] = list(parsed)
            except (ValueError, UnicodeDecodeError) as error:
                meta.update({"json_valid": False, "json_error": str(error)})
        meta["completed_at"] = datetime.now(timezone.utc).isoformat()
        (folder / "request.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return folder, meta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cvr", required=True)
    parser.add_argument("--raw-root", type=Path, default=REPO / "data/raw/matriklen-labs")
    args = parser.parse_args()
    try:
        folder, meta = fetch(args.cvr, args.raw_root)
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps({"capture": str(folder), **meta}, ensure_ascii=False, indent=2))
    return 0 if meta["status"] == "http_success" and meta.get("json_valid") else 1


if __name__ == "__main__":
    sys.exit(main())
