# Envafors: offentligt datagrundlag

Første fase kortlægger offentlige oplysninger om relaterede selskaber, ejendomme og anlæg. Repoet indeholder kun aktuelle arbejdsfiler og det kildebelæg, de kræver.

## Start her

- [Plan og status](PLAN.md).
- [Arbejdskø for kommende sessioner](QUEUE.md).
- [Datamodel og kontrolforbehold](DATA_MODEL.md).
- [Selskabskandidater](research/company_candidates.csv) og [kilderegister](research/sources.csv).
- [Gældende metodevalg og review](research/decisions.md).

Pr. 8. november 2026 har alle 21 kandidater kontrollerede CVR-stamdata og en særskilt vurdering af relevans for ejendomme og anlæg. Første runde af Matriklen Labs-opslag dækker alle 16 CVR-numre, der er valgt til ejendomsopslag, herunder den bevarede SK Vand-pilot. Cerius følges kun via konkrete spor til det tidligere NKE-net. Se [metoden, reviewet og de åbne spørgsmål](research/decisions.md#afgrænsning-af-ejendomsopslag-og-anlæg).

## Datafiler

```text
data/
  raw/matriklen-labs/
    <CVR>.json        Uændret kildeindhold for hvert bevaret svar
    index.json        Fælles URL, hentetid og hash for hvert CVR-svar
  relations.csv       Én samlet arbejdstabel for alle indsamlede CVR
  issues.csv          Kun konkrete kontrolfund
```

Vi gemmer kun seneste gyldige kildesvar pr. CVR. Historik for committede data og kode ligger i Git. Headers, fejlede forsøg, kodekopier og kørselsarkiver gemmes ikke. Et samlet JSON-eksportformat kan genereres senere, hvis det får en konkret anvendelse; det gemmes ikke som endnu en kopi nu.

Den 8. november 2026 gav ti opslag poster og seks to tomme lister. Der var ingen afslag eller tekniske fejl i runden. De bevarede svar giver [415 kildeposter](data/relations.csv) fordelt på 408 ejerposter og syv administratorposter. [16 kontrolfund](data/issues.csv) vedrører forskellige faktiske og tinglyste ejerandele. Se [de faglige forbehold](DATA_MODEL.md#faglige-forbehold) før brug.

## Direkte kildesvar

| Opgave | Brug denne adgangsvej |
|---|---|
| CVR-stamdata | Åbn [CVR-gatewayen, eksempel med Envafors](https://datacvr.virk.dk/gateway/virksomhed/hentVirksomhed?cvrnummer=26863902&locale=da) direkte i browseren. Skift `cvrnummer`, og behold `locale=da`. Det afprøvede `curl`-opslag gav 403. Se [felter, kontrol og alternativ adgang](research/decisions.md#cvr-kontrol-af-selskabskandidater). |
| Ejendomsrelationer med BFE | Brug [Matriklen Labs `CvrEjerskaber`, eksempel med SK Vand](https://api.labs.matriklen.dk/CvrEjerskaber?cvr=27736033) via scriptet nedenfor. Vælg kun CVR-numre med `property_lookup_mode=cvr` i [kandidatlisten](research/company_candidates.csv). Svaret indeholder listerne `ejer` og `administrerer` med BFE-numre. Geodatastyrelsen mærker webværktøjet som prototype. API'ets egen driftsstatus er uafklaret. [Forbehold om API, roller og dækning](DATA_MODEL.md#faglige-forbehold). |

De konkrete opslag og deres udfald står i [kilderegisteret](research/sources.csv), S030 og S080–S094 for denne runde.

## Opdatering og kontrol

Kør fra projektroden med Python 3 og systemets `curl`. Der installeres ingen afhængigheder. Scripts er researchværktøjer i det adskilte arbejdsmiljø.

```sh
python3 scripts/fetch_matriklen.py --cvr 27736033
python3 scripts/transform_matriklen.py
python3 -m unittest discover -s tests -v
```

Hentning erstatter kun CVR-filen efter HTTP 200, streng JSON-kontrol og kendt svarstruktur. Fejl går til stderr med en fejlkode og ændrer ikke sidste gode svar. Transformation kontrollerer alle CVR-filer mod indekset og genbygger de to fælles CSV-filer. Den foretager ingen netværkskald; tests bruger kun midlertidige testdata.

Brug `fetch_matriklen.py` én gang pr. valgt CVR og registrér udfaldet i kilderegisteret. Aflæs tidspunkt og URL fra scriptets JSON ved et gyldigt svar. Notér forsøgets afslutningstid med tidszone og den konkrete fejlkode eller fejltekst ved et mislykket opslag. Hentning og genbygning køres sekventielt, fordi de opdaterer fælles filer. Genbyg efter ændringer i rådata og før data bruges eller committes. Ved afbrudt kørsel gentages operationen og kontrollen, før der arbejdes videre. Commit kildeindeks, berørte data og kode samlet ved en passende milepæl. Git gemmer committede versioner, ikke ethvert mellemliggende opslag.
