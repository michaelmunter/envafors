# Envafors: offentligt datagrundlag

Første fase kortlægger offentlige oplysninger om relaterede selskaber, ejendomme og anlæg. Repoet indeholder kun aktuelle arbejdsfiler og det kildebelæg, de kræver.

## Start her

- [Plan og status](PLAN.md).
- [Arbejdskø for kommende sessioner](QUEUE.md).
- [Datamodel og kontrolforbehold](DATA_MODEL.md).
- [Selskabskandidater](research/company_candidates.csv) og [kilderegister](research/sources.csv).
- [CVR-registrerede P-enheder](research/production_units.csv) og [legale ejerandele](research/company_ownership.csv).
- [Gældende metodevalg og review](research/decisions.md).

Pr. 8. november 2026 har alle 21 kandidater kontrollerede CVR-stamdata og en særskilt vurdering af relevans for ejendomme og anlæg. Der er gennemført Matriklen Labs-opslag for 18 CVR-numre. Cerius følges via konkrete spor til det tidligere NKE-net, mens SK Energi og FIT kun indgår i selskabsoversigten. Se [grundlaget for opslagene](research/decisions.md#afgrænsning-af-ejendomsopslag-og-anlæg).

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

Den 8. november 2026 gav ti opslag poster, og otte gav tomme svar. De bevarede svar giver [415 kildeposter](data/relations.csv) fordelt på 408 ejerposter og syv administratorposter. [16 kontrolfund](data/issues.csv) vedrører forskellige faktiske og tinglyste ejerandele. Se [de faglige forbehold](DATA_MODEL.md#faglige-forbehold) før brug.

## Læs og kontrollér rådata

Kør `python3 scripts/preview_matriklen.py` fra projektroden, og åbn mappen, kommandoen udskriver, i VS Code. Den indeholder én indrykket JSON-kopi pr. CVR. Kommandoen kontrollerer først råsvarene mod kildeindekset og stopper ved fejl. Den læser lokale filer og skriver kun kopierne i systemets midlertidige mappe. Kør den igen efter et nyt opslag. Formatering af en fil under `data/raw/` ændrer dens checksum, selv om oplysningerne er de samme.

Brug BFE til at finde en ejendom og CVR til at finde selskabet. Et kontrolfund for BFE `2539366` og CVR `27736033` kan læses i relationstabellen eller kontrolleres ved at søge efter `2539366` i `27736033.json` under den angivne rolle. [Samlet relationstabel](DATA_MODEL.md#samlet-relationstabel).

## Direkte kildesvar

| Opgave | Brug denne adgangsvej |
|---|---|
| CVR-stamdata | Åbn [CVR-gatewayen, eksempel med Envafors](https://datacvr.virk.dk/gateway/virksomhed/hentVirksomhed?cvrnummer=26863902&locale=da) direkte i browseren. Skift `cvrnummer`, og behold `locale=da`. Det afprøvede `curl`-opslag gav 403. Se [felter, kontrol og alternativ adgang](research/decisions.md#cvr-kontrol-af-selskabskandidater). |
| Ejendomsrelationer med BFE | Brug [Matriklen Labs `CvrEjerskaber`, eksempel med SK Vand](https://api.labs.matriklen.dk/CvrEjerskaber?cvr=27736033) via scriptet nedenfor. Vælg kun CVR-numre med `property_lookup_mode=cvr` i [kandidatlisten](research/company_candidates.csv). Svaret indeholder listerne `ejer` og `administrerer` med BFE-numre. Geodatastyrelsen mærker webværktøjet som prototype. API'ets egen driftsstatus er uafklaret. [Forbehold om API, roller og dækning](DATA_MODEL.md#faglige-forbehold). |
| Kontrol af ejer- og administratorposter pr. BFE | Brug [Matriklen.dk `BfeEjer`, eksempel med SK Vand som administrator](https://api.matriklen.dk/api/v3.4/BfeEjer?bfe=2532386). Skift `bfe`, og tilføj eventuelt `virkningstid` som ISO-tidspunkt med tidszone for en historisk stikprøve. Sammenhold `ejere` og eventuel `administrator` med Labs-posten. Se [stikprøver og fælles registerophav](research/decisions.md#stikprøver-af-ejere-og-administratorer-i-matriklendk). |

De konkrete Labs-opslag og deres udfald står i [kilderegisteret](research/sources.csv) under S030, S080–S094 og S205–S206.

## Opdatering og kontrol

Kør fra projektroden med Python 3 og systemets `curl`. Der installeres ingen afhængigheder. Scripts er researchværktøjer i det adskilte arbejdsmiljø.

```sh
python3 scripts/fetch_matriklen.py --cvr 27736033
python3 scripts/transform_matriklen.py
python3 -m unittest discover -s tests -v
```

Hentning erstatter kun CVR-filen efter HTTP 200, streng JSON-kontrol og kendt svarstruktur. Fejl går til stderr med en fejlkode og ændrer ikke sidste gode svar. Transformation kontrollerer alle CVR-filer mod indekset og genbygger de to fælles CSV-filer. Den foretager ingen netværkskald; tests bruger kun midlertidige testdata.

Brug `fetch_matriklen.py` én gang pr. valgt CVR og registrér udfaldet i kilderegisteret. Aflæs tidspunkt og URL fra scriptets JSON ved et gyldigt svar. Notér forsøgets afslutningstid med tidszone og den konkrete fejlkode eller fejltekst ved et mislykket opslag. Hentning og genbygning køres sekventielt, fordi de opdaterer fælles filer. Genbyg efter ændringer i rådata og før data bruges eller committes. Ved afbrudt kørsel gentages operationen og kontrollen, før der arbejdes videre. Commit kildeindeks, berørte data og kode samlet ved en passende milepæl. Git gemmer committede versioner, ikke ethvert mellemliggende opslag.
