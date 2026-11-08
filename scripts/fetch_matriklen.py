"""Gem seneste gyldige Labs-svar som <CVR>.json og opdater fælles kildeindeks."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile


REPO = Path(__file__).resolve().parents[1]
RAW_ROOT = REPO / "data/raw/matriklen-labs"
API_URL = "https://api.labs.matriklen.dk/CvrEjerskaber"
ROLES = ("administrerer", "ejer")


def digest(content):
    return hashlib.sha256(content).hexdigest()


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


def validate_payload(data):
    if not isinstance(data, dict) or set(data) != set(ROLES):
        raise ValueError("Ukendt svarstruktur; forventede præcis administrerer og ejer.")
    if any(not isinstance(data[role], list) for role in ROLES):
        raise ValueError("Ukendt svarstruktur: begge roller skal være lister.")
    if any(not isinstance(row, dict) for role in ROLES for row in data[role]):
        raise ValueError("Ukendt svarstruktur: hver relation skal være et objekt.")


def read_index(raw_root):
    path = raw_root / "index.json"
    index = parse_json(path.read_bytes()) if path.exists() else {}
    if not isinstance(index, dict) or any(not re.fullmatch(r"[0-9]{8}", key) for key in index):
        raise ValueError("Kildeindekset skal være et objekt med CVR-numre som nøgler.")
    files = {path.stem for path in raw_root.glob("*.json") if path.name != "index.json"}
    if files != set(index):
        raise ValueError("Kildeindeks og CVR-filer stemmer ikke; ingen filer må stiltiende udelades.")
    return index


def replace_files(contents):
    """Forbered alle filer før erstatning; gendan ved håndterbare skrivefejl."""
    parent = next(iter(contents)).parent
    if any(path.parent != parent for path in contents):
        raise ValueError("Filerne skal have samme mappe.")
    parent.mkdir(parents=True, exist_ok=True)
    previous = {path: path.read_bytes() if path.exists() else None for path in contents}
    replaced = []
    with tempfile.TemporaryDirectory(prefix=".tmp-", dir=parent) as temporary:
        stage = Path(temporary)
        for path, content in contents.items():
            (stage / path.name).write_bytes(content)
        try:
            for path in contents:
                (stage / path.name).replace(path)
                replaced.append(path)
        except BaseException:
            for path in reversed(replaced):
                if previous[path] is None:
                    path.unlink()
                else:
                    restore = stage / path.name
                    restore.write_bytes(previous[path])
                    restore.replace(path)
            raise


def fetch(cvr, raw_root=RAW_ROOT):
    if not re.fullmatch(r"[0-9]{8}", cvr):
        raise ValueError("CVR skal være otte cifre; dette kontrollerer ikke registreringsstatus.")
    raw_root = Path(raw_root)
    index = read_index(raw_root)
    url = API_URL + "?cvr=" + cvr
    with tempfile.TemporaryDirectory(prefix="envafors-fetch-") as temporary:
        body_path = Path(temporary) / "response"
        command = [
            "curl", "--silent", "--show-error", "--location", "--max-time", "45",
            "--header", "Accept: application/json",
            "--user-agent", "Envafors-Public-Data-Research/0.1",
            "--output", str(body_path), "--write-out", "%{http_code}", url,
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=50)
        except (OSError, subprocess.TimeoutExpired) as error:
            raise ValueError("Transportfejl: " + str(error)) from error
        if result.returncode:
            raise ValueError("Transportfejl: " + result.stderr.strip())
        if result.stdout.strip() != "200":
            raise ValueError("HTTP-fejl: " + result.stdout.strip())
        raw = body_path.read_bytes()
        data = parse_json(raw)
        validate_payload(data)
    entry = {"url": url, "retrieved_at": datetime.now(timezone.utc).isoformat(), "sha256": digest(raw)}
    index[cvr] = entry
    replace_files({
        raw_root / (cvr + ".json"): raw,
        raw_root / "index.json": (json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    })
    return {"cvr": cvr, "rows": sum(len(data[role]) for role in ROLES), **entry}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cvr", required=True)
    parser.add_argument("--raw-root", type=Path, default=RAW_ROOT)
    args = parser.parse_args()
    try:
        summary = fetch(args.cvr, args.raw_root)
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
