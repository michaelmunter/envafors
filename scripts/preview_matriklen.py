"""Lav indrykkede JSON-kopier til læsning i en midlertidig mappe."""

import json
from pathlib import Path
import tempfile

from fetch_matriklen import RAW_ROOT, replace_files
from transform_matriklen import load_sources


def main():
    try:
        sources = load_sources(RAW_ROOT)
        folder = Path(tempfile.mkdtemp(prefix="envafors-json-"))
        replace_files({
            folder / f"{cvr}.json": (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            for cvr, data in sources
        })
    except (OSError, ValueError, TypeError) as error:
        raise SystemExit(str(error)) from error
    print(folder)


if __name__ == "__main__":
    main()
