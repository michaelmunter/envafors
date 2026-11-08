"""Vis kilderegister og afstemte dataforløb fra de aktuelle projektfiler."""

import argparse
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote, urlsplit

from fetch_matriklen import REPO, replace_files
from source_overview_data import read_catalog, read_matriklen


CATALOG = "research/sources.csv"
CANDIDATES = "research/company_candidates.csv"
LABS_RAW = "data/raw/matriklen-labs"
INDEX = LABS_RAW + "/index.json"
TRANSFORM = "scripts/transform_matriklen.py"
RELATIONS = "data/relations.csv"
ISSUES = "data/issues.csv"
LINKED_FILES = {CATALOG, CANDIDATES, INDEX, TRANSFORM, RELATIONS, ISSUES}
SOURCE_TYPES = {
    "primary_company_page": "Selskabets egen side",
    "primary_documentation": "Dokumentation",
    "primary_municipal_page": "Kommunens egen side",
    "primary_public_document": "Offentligt dokument",
    "prototype_api_response": "API-prototype",
    "secondary_company_profile": "Sekundær selskabsprofil",
    "secondary_document_copy": "Gengivelse af et dokument",
}

STYLE = """
:root { color: #202721; background: #f8f8f2; font: 1rem/1.55 Georgia, serif; }
body { margin: 0; }
main { max-width: 76rem; margin: auto; padding: 2rem clamp(1rem, 4vw, 3rem); }
h1, h2, h3, p { margin: 0 0 .65rem; }
h1 { font-size: clamp(2rem, 5vw, 3rem); }
section { margin-block: 2rem; }
a { color: #24533f; text-underline-offset: .15em; overflow-wrap: anywhere; }
code { overflow-wrap: anywhere; }
details { margin-top: .35rem; }
summary { cursor: pointer; }
.notice { border-left: .35rem solid #994122; background: #fff1e6; padding: .85rem 1rem; }
.lookup { margin-block: 1.3rem; }
.flow { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1.4rem;
        list-style: none; padding: 0; margin: .7rem 0; }
.flow li { position: relative; background: #fff; border: 1px solid #c6cdc3; padding: .7rem; }
.flow li + li::before { content: '→'; position: absolute; left: -1.2rem; color: #415844; }
.flow.unchecked li + li::before { content: '⇢'; color: #994122; }
.flow strong { display: block; }
.table { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
th, td { text-align: left; vertical-align: top; border-bottom: 1px solid #c6cdc3; padding: .65rem; }
thead { background: #e9ede4; }
tbody th { min-width: 12rem; }
tbody td { min-width: 10rem; }
small { display: block; font-size: .85rem; }
ul { padding-left: 1.3rem; }
@media (max-width: 48rem) {
    .flow { grid-template-columns: 1fr; }
    .flow li + li::before { content: '↓'; left: .7rem; top: -1.45rem; }
    .flow.unchecked li + li::before { content: '⇣'; }
}
"""


def external_link(url, label):
    try:
        parts = urlsplit(url)
        if (parts.scheme in {"http", "https"} and parts.hostname and parts.username is None
                and not any(character.isspace() or ord(character) < 32 for character in url)
                and "\\" not in url):
            return f'<a href="{escape(url)}">{escape(label)}</a>'
    except ValueError:
        pass
    return f"{escape(label)} <small>URL kan ikke åbnes · {escape(url)}</small>"


def source_row(source, candidates, lookup_cvr, link):
    source_id = escape(source["source_id"])
    use = []
    if candidates:
        names = "".join(
            f'<li>{escape(row["name"])} · {escape(row["cvr"])}</li>' for row in candidates
        )
        use.append(
            f'<details><summary>Henvisninger fra kandidatlisten ({len(candidates)})</summary>'
            f'<ul>{names}</ul>{link(CANDIDATES, "Åbn kandidatlisten")}</details>'
        )
    if lookup_cvr:
        use.append(f'<p><a href="#opslag-{escape(lookup_cvr)}">Registreret API-opslag</a></p>')
    if source["source_type"] == "primary_documentation":
        use.append('<p>Dokumentation for et register eller en adgangsmetode.</p>')

    capture = {
        "researched_not_archived": "Råkopi er ikke gemt",
        "archived_raw": "Råkopi registreret",
    }.get(source["capture_status"], source["capture_status"] or "Arkivstatus ukendt")
    source_type = source["source_type"]
    type_label = SOURCE_TYPES.get(source_type, source_type or "Kildetype ukendt")
    return f"""<tr id="kilde-{source_id}">
  <th scope="row"><small>{source_id} · {escape(source['origin_system'])}</small>
    {external_link(source['url'], source['title'])}<small>{escape(source['publisher'])} · {escape(type_label)}</small></th>
  <td>{escape(source['notes'] or 'Ingen beskrivelse registreret.')}
    <small>Researchdato {escape(source['researched_on'] or 'ukendt')} · Dokumentdato {escape(source['document_date'] or 'ukendt')}</small></td>
  <td>{''.join(use) or '<p>Ingen kobling registreret i visningens datagrundlag.</p>'}
    <small>{escape(capture)}</small></td>
</tr>"""


def lookup_flow(lookup, matching_sources, link):
    cvr = escape(lookup["cvr"])
    raw = link(f"{LABS_RAW}/{lookup['cvr']}.json", f"{lookup['cvr']}.json")
    source_links = ", ".join(
        f'<a href="#kilde-{quote(source_id, safe="")}">{escape(source_id)}</a>' for source_id in matching_sources
    )
    if source_links:
        source_links = f"<small>Kilderegister {source_links}</small>"
    if lookup["relation_count"] is None:
        flow_class = "flow unchecked"
        outputs = f'{link(RELATIONS)} og {link(ISSUES)}<small>Afstemning mangler</small>'
    else:
        flow_class = "flow"
        outputs = f'{link(RELATIONS)} · {lookup["relation_count"]} kilderelationer<br>'
        outputs += f'{link(ISSUES)} · {lookup["issue_count"]} kontrolfund'
        if lookup["relation_count"] == 0:
            outputs += "<small>Gyldigt tomt opslag</small>"
    return f"""<article class="lookup" id="opslag-{cvr}">
  <h3>CVR {cvr}</h3>
  <ol class="{flow_class}" role="list" aria-label="Dataforløb for CVR {cvr}">
    <li><strong>Opslag</strong>{external_link(lookup['url'], 'Matriklen Labs · CvrEjerskaber')}
        {source_links}<small>Hentet {escape(lookup['retrieved_at'] or 'ukendt')}</small></li>
    <li><strong>Råsvar</strong>{raw} og {link(INDEX, 'kildeindeks')}
        <small>Ejer- og administratorposter. Bearbejdede felter omfatter BFE, kildestatus, dato og ejerandele.</small>
        <details><summary>SHA-256 i indekset</summary><code>{escape(lookup['sha256'] or 'ukendt')}</code></details></li>
    <li><strong>Bearbejdning</strong>{link(TRANSFORM, 'Matriklen-transformation')}
        <small>Én række pr. kildepost. Afvigelser samles særskilt.</small></li>
    <li><strong>Brug i projektet</strong>{outputs}</li>
  </ol>
</article>"""


def render(root, base=None):
    """Læs projektfilerne på ny og returnér HTML og eventuel kontrolfejl."""
    root = Path(root).resolve()

    def link(path, label=None):
        if base is None:
            href = "/" + quote(path)
        else:
            try:
                relative = Path(os.path.relpath(root / path, base))
                href = quote(relative.as_posix())
            except ValueError:  # Drevbogstaver kan være forskellige på Windows.
                href = (root / path).as_uri()
        return f'<a href="{escape(href)}">{escape(label or path)}</a>'

    catalog_problem = None
    try:
        sources, candidates = read_catalog(root)
    except (OSError, ValueError) as error:
        sources, candidates = [], {}
        catalog_problem = f"Kilderegister og kandidatlinks kunne ikke læses. {error}"
    lookups, pipeline_problem = read_matriklen(root)

    by_url = {}
    for source in sources:
        by_url.setdefault(source["url"], []).append(source["source_id"])
    lookup_cvrs = {lookup["url"]: lookup["cvr"] for lookup in lookups if lookup["url"]}
    flows = "".join(lookup_flow(lookup, by_url.get(lookup["url"], []), link) for lookup in lookups)
    rows = "".join(
        source_row(source, candidates.get(source["source_id"], []), lookup_cvrs.get(source["url"]), link)
        for source in sources
    )
    problems = [problem for problem in (catalog_problem, pipeline_problem) if problem]
    notices = "".join(f'<p class="notice">{escape(problem)}</p>' for problem in problems)
    lookup_status = "Ingen registrerede API-opslag." if not pipeline_problem else "API-opslag kan ikke afstemmes."
    catalog_status = "Ingen kilder registreret." if not catalog_problem else "Kildelisten er utilgængelig."
    view = (
        "Genindlæs siden for at læse projektfilerne igen." if base is None
        else "Øjebliksbillede af projektfilerne ved eksport. Kør eksporten igen for at se nyere data."
    )
    page = f"""<!doctype html>
<html lang="da">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Envafors · Kildeoverblik</title>
  <style>{STYLE}</style>
</head>
<body><main>
  <h1>Kildeoverblik</h1>
  <p>Envafors · offentligt datagrundlag</p>
  <p>{view}</p>
  {notices}
  <section id="opslag" aria-labelledby="opslag-titel">
    <h2 id="opslag-titel">Registrerede API-opslag</h2>
    <p>Pilene viser vejen fra opslag til tabeller. Stiplede pile markerer et forløb med en uafklaret teknisk kontrol.</p>
    <p>Afstemning viser, at tabellerne kan genskabes fra de bevarede svar. Ejerskab og dækning kræver faglig kontrol.</p>
    {flows or f'<p>{lookup_status}</p>'}
  </section>
  <section aria-labelledby="kilder-titel">
    <h2 id="kilder-titel">Kilderegister</h2>
    <p>{link(CATALOG, 'Åbn kilderegisterets CSV-fil')}</p>
    <div class="table"><table>
      <thead><tr><th scope="col">Kilde og adgang</th><th scope="col">Data eller dokumentation</th><th scope="col">Registreret brug og råkopi</th></tr></thead>
      <tbody>{rows or f'<tr><td colspan="3">{catalog_status}</td></tr>'}</tbody>
    </table></div>
  </section>
</main></body>
</html>
"""
    return page, "\n".join(problems) or None


def serve(root):
    root = Path(root).resolve()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.headers.get("Host") != f"127.0.0.1:{self.server.server_port}":
                self.send_error(400)
                return
            path = self.path.partition("?")[0].removeprefix("/")
            if not path:
                page, _ = render(root)
                body, content_type = page.encode("utf-8"), "text/html; charset=utf-8"
            elif path in LINKED_FILES or re.fullmatch(LABS_RAW + r"/[0-9]{8}\.json", path):
                try:
                    file = (root / path).resolve()
                    file.relative_to(root)
                    body, content_type = file.read_bytes(), "text/plain; charset=utf-8"
                except (OSError, ValueError):
                    self.send_error(404)
                    return
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)

    with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
        print(f"Åbn http://127.0.0.1:{server.server_port}/ i browseren. Stop med Ctrl+C.", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Eksportér en HTML-fil i stedet for at starte livevisningen")
    args = parser.parse_args()
    try:
        if args.output is None:
            serve(REPO)
            return
        output = args.output.resolve()
        if output.suffix.lower() != ".html":
            parser.error("Outputfilen skal ende på .html.")
        page, problem = render(REPO, output.parent)
        if problem:
            parser.exit(1, problem + "\n")
        replace_files({output: page.encode("utf-8")})
        print(output)
    except OSError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
