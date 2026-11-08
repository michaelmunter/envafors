# Envafors: offentligt datagrundlag

Første fase kortlægger offentlige oplysninger om relaterede selskaber, ejendomme og anlæg. Repoet indeholder kun aktuelle arbejdsfiler og det kildebelæg, de kræver.

## Start her

- [Plan og status](PLAN.md).
- [Arbejdskø for kommende sessioner](QUEUE.md).
- [Datamodel og kontrolforbehold](DATA_MODEL.md).
- [Selskabskandidater](research/company_candidates.csv) og [kilderegister](research/sources.csv).
- [Gældende metodevalg og review](research/decisions.md).

Den 8. november 2026 blev hovednavn, binavne og status kontrolleret i CVR for de 20 oprindelige kandidater: 16 stod som »Normal« og fire som »Opløst efter fusion«. Cerius A/S blev tilføjet som kandidat til opfølgning på det tidligere NKE-net. Listen dokumenterer ikke en fuldstændig koncernstruktur. Se [CVR-metoden og de åbne spørgsmål](research/decisions.md#cvr-kontrol-af-selskabskandidater).

## Datafiler

```text
data/
  raw/matriklen-labs/
    27736033.json     Uændret kildeindhold; fremover én fil pr. undersøgt CVR
    index.json        Fælles URL, hentetid og hash for hvert CVR-svar
  relations.csv       Én samlet arbejdstabel for alle indsamlede CVR
  issues.csv          Kun konkrete kontrolfund
```

Vi gemmer kun seneste gyldige kildesvar pr. CVR. Historik for committede data og kode ligger i Git. Headers, fejlede forsøg, kodekopier og kørselsarkiver gemmes ikke. Et samlet JSON-eksportformat kan genereres senere, hvis det får en konkret anvendelse; det gemmes ikke som endnu en kopi nu.

Piloten for SK Vand `27736033` er hentet 8. november 2026 og har [42 relationer](data/relations.csv): 34 ejerposter mærket `gældende`, fem mærket `historisk` og tre administratorposter. [To kontrolfund](data/issues.csv) vedrører forskellige faktiske og tinglyste ejerandele. Det er kildeudsagn, ikke en endelig bekræftelse af ejerskab eller fuldstændighed.

## Direkte kildesvar

| Opgave | Brug denne adgangsvej |
|---|---|
| CVR-stamdata | Åbn [CVR-gatewayen, eksempel med Envafors](https://datacvr.virk.dk/gateway/virksomhed/hentVirksomhed?cvrnummer=26863902&locale=da) direkte i browseren. Skift `cvrnummer`, og behold `locale=da`. Det afprøvede `curl`-opslag gav 403. Se [felter, kontrol og alternativ adgang](research/decisions.md#cvr-kontrol-af-selskabskandidater). |
| Ejendomsrelationer med BFE | Brug [Matriklen Labs `CvrEjerskaber`, eksempel med SK Vand](https://api.labs.matriklen.dk/CvrEjerskaber?cvr=27736033) via scriptet nedenfor. Sæt `cvr` til nummeret på et selskab, der er omfattet af ejendomsindsamlingen. Svaret indeholder listerne `ejer` og `administrerer` med BFE-numre. Geodatastyrelsen mærker webværktøjet som prototype. API'ets egen driftsstatus er uafklaret. [Forbehold om API, roller og dækning](DATA_MODEL.md#faglige-forbehold). |

De konkrete opslag og deres kildehenvisninger står i [kilderegisteret](research/sources.csv).

## Opdatering og kontrol

Kør fra projektroden med Python 3 og systemets `curl`. Der installeres ingen afhængigheder. Scripts er researchværktøjer i det adskilte arbejdsmiljø.

```sh
python3 scripts/fetch_matriklen.py --cvr 27736033
python3 scripts/transform_matriklen.py
python3 -m unittest discover -s tests -v
```

Hentning erstatter kun CVR-filen efter HTTP 200, streng JSON-kontrol og kendt svarstruktur. Fejl går til stderr med en fejlkode og ændrer ikke sidste gode svar. Transformation kontrollerer alle CVR-filer mod indekset og genbygger de to fælles CSV-filer. Den foretager ingen netværkskald; tests bruger kun midlertidige testdata.

Hentning og genbygning køres sekventielt, fordi de opdaterer fælles filer. Genbyg efter ændringer i rådata og før data bruges eller committes. Ved afbrudt kørsel gentages operationen og kontrollen, før der arbejdes videre. Commit kildeindeks, berørte data og kode samlet ved en passende milepæl. Git gemmer committede versioner, ikke ethvert mellemliggende opslag.
