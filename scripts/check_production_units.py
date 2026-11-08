"""Afstem P-enheder og opslagsdækning mod kandidatlisten og kilderegisteret."""

from collections import Counter
import csv
from pathlib import Path
import re
import sys


RESEARCH = Path(__file__).resolve().parents[1] / "research"
CVR_LOOKUP = re.compile(
    r"https://datacvr\.virk\.dk/(?:gateway/virksomhed/hentVirksomhed\?cvrnummer=([0-9]{8})&locale=da"
    r"|enhed/virksomhed/([0-9]{8})(?:\?[^#]+)?)"
)
P_COUNTS = re.compile(r"\bproduktionsenheder: ([0-9]+) aktive og ([0-9]+) ophørte\.")


def read_rows(filename):
    with (RESEARCH / filename).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def check():
    candidates = {row["cvr"] for row in read_rows("company_candidates.csv")}
    lookups = {}
    expected = Counter()
    for source in read_rows("sources.csv"):
        url = CVR_LOOKUP.fullmatch(source["url"])
        counts = P_COUNTS.search(source["notes"])
        if not url or not counts or source["lookup_outcome"] not in {"found", "no_result"}:
            continue
        cvr = url[1] or url[2]
        active, closed = map(int, counts.groups())
        if source["lookup_outcome"] == "no_result" and (active or closed):
            raise ValueError("Tomt P-opslag har registrerede enheder for CVR " + cvr)
        if cvr in lookups:
            raise ValueError("Flere registrerede P-opslag for CVR " + cvr)
        lookups[cvr] = source["source_id"]
        for status, count in (("active", active), ("closed", closed)):
            if count:
                expected[cvr, status] = count

    missing = candidates - lookups.keys()
    extra = lookups.keys() - candidates
    if missing or extra:
        raise ValueError(
            f"P-opslag stemmer ikke med kandidatlisten. Mangler: {sorted(missing)}. Ekstra: {sorted(extra)}."
        )

    rows = read_rows("production_units.csv")
    actual = Counter()
    numbers = set()
    for row in rows:
        cvr, number = row["cvr"], row["p_number"]
        if not re.fullmatch(r"[0-9]{10}", number) or number in numbers:
            raise ValueError("Ugyldigt eller gentaget P-nummer: " + number)
        if lookups.get(cvr) != row["source_id"]:
            raise ValueError(f"P-nummer {number} har forkert kilde for CVR {cvr}.")
        numbers.add(number)
        actual[cvr, row["source_status"]] += 1

    if actual != expected:
        differences = sorted(key for key in actual.keys() | expected.keys() if actual[key] != expected[key])
        details = ", ".join(f"{cvr} ({status}): {actual[cvr, status]} mod {expected[cvr, status]}"
                            for cvr, status in differences)
        raise ValueError("P-enheder stemmer ikke med kilderegisteret: " + details)
    print(f"{len(rows)} P-enheder stemmer med de registrerede opslag for {len(candidates)} CVR-numre.")


if __name__ == "__main__":
    try:
        check()
    except (OSError, ValueError) as error:
        sys.exit(str(error))
