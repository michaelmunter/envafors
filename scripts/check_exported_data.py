"""Kontrollér leverede CVR-filer lokalt og eventuelt mod BfeEjer på en valgt virkningstid."""
import argparse
import csv
import subprocess
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from fractions import Fraction
from urllib.parse import urlencode
from zoneinfo import ZoneInfo

from fetch_matriklen import REPO, parse_json, validate_payload

SHARES = ("faktiskEjerandel", "tinglystEjerandel")


def read_folder(name):
    files = sorted((REPO / "data" / name).glob("*.json"))
    if not files:
        raise ValueError(f"Ingen JSON-filer i {name}")
    return {p.stem: parse_json(p.read_bytes()) for p in files}


def share(row, field):
    if field not in row:
        return None
    value = row[field]
    n, d = value["tæller"], value["nævner"]
    if type(n) is not int or type(d) is not int or not 0 <= n <= d or d <= 0:
        raise ValueError(f"Ugyldig {field}: {value}")
    return Fraction(n, d)


def labs_time(row):
    stamp, zone = row["virkningFra"].split("[")
    dt = datetime.fromisoformat(stamp)
    if dt.utcoffset() is None or not zone.endswith("]"):
        raise ValueError(f"Ufuldstændig tid i {row}")
    zoned = dt.astimezone(ZoneInfo(zone[:-1]))
    if dt.utcoffset() != zoned.utcoffset():
        raise ValueError(f"Tidszone og offset afviger i {row}")
    return zoned


def read_exports():
    labs, virk = read_folder("labs.matriklen"), read_folder("virk")
    print("Kun i Labs:", sorted(labs.keys() - virk.keys()), "Kun i Virk:", sorted(virk.keys() - labs.keys()))
    dates = {}
    with (REPO / "research/production_units.csv").open(encoding="utf-8", newline="") as f:
        prior_units = {r["p_number"]: r for r in csv.DictReader(f) if r["cvr"] in virk}
    units = set()
    unit_counts = Counter()
    for cvr, company in virk.items():
        master = company["stamdata"]
        if len(cvr) != 8 or not cvr.isascii() or not cvr.isdecimal() or master["cvrnummer"] != cvr:
            raise ValueError(f"CVR afviger fra filnavnet {cvr}")
        dates[cvr] = master["startdato"]
        end_date = master["ophoersdato"]
        if end_date and date.fromisoformat(end_date) < date.fromisoformat(dates[cvr]):
            raise ValueError(f"Ophørsdato før start for CVR {cvr}")
        if (master["status"] == "NORMAL" and end_date) or (master["status"].startswith("OPLØST") and not end_date):
            print("Kontrollér CVR-status og ophør:", cvr, master["status"], end_date)
        for group, closed in [("aktiveProduktionsenheder", False), ("ophoerteProduktionsenheder", True)]:
            for unit in company["produktionsenheder"][group]:
                s = unit["stamdata"]
                p, end = s["pnummer"], s["ophoersdato"]
                if p in units or len(p) != 10 or not p.isdecimal() or s["cvrnummer"] != cvr:
                    raise ValueError(f"Kontrollér P-nr. {p} ved CVR {cvr}")
                industry = s["hovedbranche"] or {}
                fields = dict(cvr=cvr, source_status="closed" if closed else "active",
                              registered_name=s["navn"], registered_address=s["adresse"],
                              postal_code_and_city=s["postnummerOgBy"], main_industry_code=industry.get("branchekode"),
                              main_industry_name=industry.get("titel"), start_date=s["startdato"], end_date=end)
                baseline = prior_units.get(p, {})
                if any((value or "") != baseline.get(key) for key, value in fields.items()):
                    print("Afvigelse fra tidligere P-opslag:", cvr, p)
                units.add(p)
                unit_counts[group] += 1
                if bool(end) != closed or (end and end < s["startdato"]):
                    raise ValueError(f"Status og datoer for P-nr. {p} er uforenelige")
                if s["startdato"] < dates[cvr]:
                    print("P-start før CVR-start:", cvr, p, s["startdato"], dates[cvr])
    if prior_units.keys() - units:
        print("Tidligere P-nr. mangler i Virk-udtræk:", sorted(prior_units.keys() - units))
    print("P-enheder:", dict(unit_counts))
    # S035 daterer SK Varme, hvis CVR-fil mangler i den leverede mappe.
    with (REPO / "research/company_candidates.csv").open(encoding="utf-8", newline="") as f:
        for source in csv.DictReader(f):
            dates.setdefault(source["cvr"], source["cvr_start_date"])

    properties = defaultdict(list)
    counts = Counter()
    for cvr, data in labs.items():
        validate_payload(data)
        for role, rows in data.items():
            for row in rows:
                bfe, status = row["bfe"], row["status"]
                if type(bfe) is not int or bfe <= 0 or status not in {"gældende", "historisk"}:
                    raise ValueError(f"Ugyldig BFE eller status: {cvr}, {row}")
                actual, registered = (share(row, k) for k in SHARES)
                if role == "ejer" and actual is None:
                    raise ValueError(f"Manglende faktisk andel: {cvr}, {bfe}")
                if role == "administrerer" and any(k in row for k in SHARES):
                    raise ValueError(f"Ejerandel på administratorpost: {cvr}, {bfe}")
                counts[role, status, actual, registered] += 1
                stamp = labs_time(row).date().isoformat()
                if dates.get(cvr) and stamp < dates[cvr]:
                    print("Labs-dato før CVR-start:", cvr, bfe, status, stamp, dates[cvr])
                properties[bfe].append((cvr, role, row))
    for pattern, count in counts.items():
        print("Andelsmønster:", *pattern, count)
    shared = 0
    for bfe, rows in sorted(properties.items()):
        keys = [(cvr, role, row["status"]) for cvr, role, row in rows]
        if len(set(keys)) != len(keys):
            print("Gentagen CVR/rolle/status:", bfe, keys)
        if len({cvr for cvr, _, _ in rows}) > 1:
            shared += 1
            print("Delt BFE:", bfe, keys)
        for field in SHARES:
            known = [share(row, field) for _, role, row in rows if role == "ejer" and row["status"] == "gældende"]
            if sum(v for v in known if v is not None) > 1:
                print("Over 100 procent:", bfe, field)
    print("Antal BFE:", len(properties), "Heraf under flere CVR:", shared)
    return properties, dates, set(labs)


def role_rows(data, role):
    if not isinstance(data["ejere"], list):
        raise ValueError("Ukendt ejerstruktur i BfeEjer")
    if role == "ejer":
        return data["ejere"]
    return [data["administrator"]] if data.get("administrator") else []


def fetch_bfe(bfe, stamp):
    url = "https://api.matriklen.dk/api/v3.4/BfeEjer?" + urlencode({"bfe": bfe, "virkningstid": stamp.isoformat()})
    result = subprocess.run(["curl", "--fail", "--silent", "--show-error", "--max-time", "30", url],
                            capture_output=True, check=True)
    return parse_json(result.stdout)


def check_register(properties, dates, scope, as_of, fetch=fetch_bfe):
    counts = Counter()

    def lookup(bfe, stamp):
        try:
            data = fetch(bfe, stamp)
            role_rows(data, "ejer")
            return data
        except (OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError) as error:
            print("Opslag uafklaret:", bfe, stamp.isoformat(), error)
            counts["uafklarede opslag"] += 1
            return None

    for bfe, rows in sorted(properties.items()):
        current = lookup(bfe, as_of)
        for role in ("ejer", "administrerer"):
            if current is None:
                break
            expected = {cvr for cvr, r, row in rows if r == role and row["status"] == "gældende"}
            visible = {str(q.get("cvr")) for q in role_rows(current, role)} & scope
            if visible != expected:
                print("Rolleafvigelse:", bfe, role, sorted(expected), sorted(visible))
                counts["rolleafvigelser"] += 1
        for cvr, role, row in rows:
            checks = [("gældende", current, True)]
            if row["status"] == "historisk":
                end = labs_time(row)
                checks = [("før", lookup(bfe, end - timedelta(seconds=1)), True), ("ved", lookup(bfe, end), False)]
            for label, data, expected in checks:
                if data is None:
                    continue
                matched = [q for q in role_rows(data, role) if str(q.get("cvr")) == cvr]
                if len(matched) != int(expected):
                    print("Statusafvigelse:", bfe, cvr, role, label, len(matched))
                    counts["statusafvigelser"] += 1
                    continue
                if matched and role == "ejer":
                    if any(share(row, k) != share(matched[0], k) for k in SHARES):
                        print("Andelsafvigelse:", bfe, cvr, label)
                        counts["andelsafvigelser"] += 1
                        continue
                    if label == "gældende":
                        day = labs_time(row).date().isoformat()
                        matching = [k for k in ("overtagelsesdato", "tinglysningsdato") if day == matched[0].get(k)]
                        counts["Labs-dato matcher " + (" og ".join(matching) or "ingen af datoerne")] += 1
                        if not matching:
                            print("Labs-dato afviger fra begge ejendomsdatoer:", cvr, bfe, day,
                                  matched[0].get("overtagelsesdato"), matched[0].get("tinglysningsdato"))
                        for field in ("overtagelsesdato", "tinglysningsdato"):
                            value = matched[0].get(field)
                            if value and dates.get(cvr) and value < dates[cvr]:
                                print("BfeEjer før CVR-start:", cvr, bfe, field, value, dates[cvr])
                                counts[field + " før CVR-start"] += 1
                counts[role + " " + label] += 1
    print("BfeEjer:", dict(counts))
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bfe-at", type=datetime.fromisoformat, help="Virkningstid med offset til afstemning af gældende rækker")
    args = parser.parse_args()
    properties, dates, scope = read_exports()
    if args.bfe_at:
        if args.bfe_at.utcoffset() is None:
            parser.error("Angiv tidszone i --bfe-at")
        counts = check_register(properties, dates, scope, args.bfe_at)
        if counts["uafklarede opslag"]:
            raise SystemExit(2)
        if any(counts[k] for k in ("rolleafvigelser", "statusafvigelser", "andelsafvigelser")):
            raise SystemExit(1)
