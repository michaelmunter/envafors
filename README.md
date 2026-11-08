# Envafors: offentligt datagrundlag

Første fase kortlægger offentlige oplysninger om relaterede selskaber, ejendomme og anlæg. Repoet indeholder kun aktuelle arbejdsfiler og det kildebelæg, de kræver.

## Start her

- [Plan og status](PLAN.md).
- [Arbejdskø for kommende sessioner](QUEUE.md).
- [Datamodel og kontrolforbehold](DATA_MODEL.md).
- [Selskabskandidater](research/company_candidates.csv) og [kilderegister](research/sources.csv).
- [Gældende metodevalg og review](research/decisions.md).

Kandidatlisten er ikke en verificeret eller fuldstændig koncernstruktur. Aktuel CVR-status og selskabsrelationer er endnu ikke kontrolleret.

## Kildeoverblik i browseren

Kør fra projektroden med Python 3 i udviklingsmiljøet.

```sh
python3 scripts/show_sources.py
```

Åbn adressen fra terminalen. Visningen læser kilderegister, kandidathenvisninger, råsvar, indeks og tabeller ved hver genindlæsning. Tilføj nye kilder i `research/sources.csv`, og brug deres `source_id` i kandidatlisten, når der er en henvisning. Nye Matriklen Labs-opslag kommer fra kildeindekset. Visningen læser opslagets URL med CVR-parameter, hentetid og SHA-256 fra indekset og forbinder kun en kilderegisterpost med opslaget, når URL'en er identisk.

Visningen lytter kun på den lokale computer og stoppes med Ctrl+C. Den læser de gemte filer. Ved tekniske uoverensstemmelser viser den årsagen og tilbageholder de afstemte tal. Den faglige vurdering ligger i projektets øvrige kontroller.

En browser på Windows kan åbne et eksporteret øjebliksbillede direkte. Opret filen i projektroden, hvis filhenvisningerne også skal virke i en kopi af projektet. Eksporten afbrydes ved kontrolfejl og bevarer en eventuel tidligere fil.

```sh
python3 scripts/show_sources.py --output kilder.html
```

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

## Opdatering og kontrol

Kør fra projektroden med Python 3 og systemets `curl`. Der installeres ingen afhængigheder. Scripts er researchværktøjer i det adskilte arbejdsmiljø.

```sh
python3 scripts/fetch_matriklen.py --cvr 27736033
python3 scripts/transform_matriklen.py
python3 -m unittest discover -s tests -v
```

Hentning erstatter kun CVR-filen efter HTTP 200, streng JSON-kontrol og kendt svarstruktur. Fejl går til stderr med en fejlkode og ændrer ikke sidste gode svar. Transformation kontrollerer alle CVR-filer mod indekset og genbygger de to fælles CSV-filer. Den foretager ingen netværkskald; tests bruger kun midlertidige testdata.

Hentning og genbygning køres sekventielt, fordi de opdaterer fælles filer. Genbyg efter ændringer i rådata og før data bruges eller committes. Ved afbrudt kørsel gentages operationen og kontrollen, før der arbejdes videre. Commit kildeindeks, berørte data og kode samlet ved en passende milepæl. Git gemmer committede versioner, ikke ethvert mellemliggende opslag.
