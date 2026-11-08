# Envafors: offentligt datagrundlag

Projektet kortlægger offentlige oplysninger om relaterede selskaber, ejendomme og anlæg. Første fase er dataindsamling og kvalitetssikring. DocuNote og dokumenthåndtering indgår ikke.

## Start her

- [Faseplan og aktuel status](PLAN.md): opgaver, afhængigheder og kriterier for afslutning.
- [Datamodel](DATA_MODEL.md): hvad tabellerne betyder, hvordan de forbindes, og hvilke oplysninger der endnu mangler.
- [Selskabskandidater](research/company_candidates.csv): 20 søgepunkter med evidensstatus og næste kontrol.
- [Kilderegister](research/sources.csv): kildehenvisninger fra den hidtidige research. Registeret er foreløbigt.
- [Beslutninger og review](research/decisions.md): væsentlige valg og håndtering af reviewbemærkninger.

De 20 kandidater er ikke en verificeret eller fuldstændig koncernstruktur. Aktuel CVR-status og selskabsrelationer står som `not_checked`. Indtil videre er kun ét CVR afprøvet i ejendoms-API'et.

## Arbejdsstruktur

```text
AGENTS.md                         Regler for arbejdet
PLAN.md                           Plan, status og afslutningskriterier
DATA_MODEL.md                     Datakontrakt og koblinger
research/
  sources.csv                     Kilder og evidensbegrænsninger
  company_candidates.csv          Selskaber, der skal undersøges
  decisions.md                    Metodevalg og review
scripts/
  fetch_matriklen.py               Hent ét CVR og bevar originalsvar
  transform_matriklen.py           Reproducerbar bearbejdning og kontrol
tests/
  test_matriklen.py                Kontrol af væsentlige fejlsituationer
data/
  raw/matriklen-labs/<capture>/    Uændret svar, svarheaders og hentningsmanifest
  runs/matriklen-labs/<run>/
    manifest.json                 Input, kodeversion, outputhash og kørselsstatus
    processed/relations.csv       Alle rårelationer, struktureret til CSV
    processed/properties.csv      Afledt liste over forskellige gyldige BFE-numre
    quality/profile.json          Optælling og tekniske kontroller
    quality/issues.csv            Konkrete fund og uafklarede forhold
    method/transform_matriklen.py  Den præcise kodeversion til kørslen
```

Mapperne under `data` er til researchdata, bearbejdning og kontrol. Der oprettes ingen struktur til virksomhedens dokumenthåndtering.

## Første pilot

Den 8. november 2026 gav opslag på SK Vand, CVR `27736033`, HTTP 200 og gyldig JSON. [Originalsvaret](data/raw/matriklen-labs/20261108T105618531332Z_27736033/response.body) er bevaret med [hentningsoplysninger](data/raw/matriklen-labs/20261108T105618531332Z_27736033/request.json).

[Pilotens bearbejdede data og kontrol](data/runs/matriklen-labs/pilot-27736033-v2/manifest.json) indeholder 42 relationer og 42 forskellige BFE-numre: 34 ejerposter mærket `gældende`, fem mærket `historisk` og tre administratorposter mærket `gældende`. Dette er en optælling af kildens svar, ikke en selvstændig bekræftelse af ejerskab eller fuldstændighed. Faktiske og tinglyste ejerandele er forskellige på to poster. Feltet `virkningFra` fortolkes ikke som start- eller slutdato. Den tidligere tekniske kørsel `pilot-27736033-v1` er bevaret; v2 er den gældende bearbejdningsversion.

## Gentag bearbejdningen

Kør fra projektroden med Python 3. Scripts bruger kun standardbiblioteket. Hentning bruger desuden systemets `curl`. De er researchværktøjer til det adskilte arbejdsmiljø; ingen installation eller kørsel på Envafors' arbejdscomputere forudsættes.

```sh
python3 scripts/transform_matriklen.py --input data/raw/matriklen-labs/20261108T105618531332Z_27736033 --output data/runs/matriklen-labs/pilot-27736033-v2-gentaget
python3 -m unittest discover -s tests -v
```

Input er det bevarede råsvar og dets manifest. Output er en ny kørselsmappe med CSV, kvalitetsprofil og manifest. Eksisterende output afvises. Hentningsfejl, ændret råfil eller ukendt svarstruktur må ikke fremstå som tomme, vellykkede data. Der foretages ingen netværkskald under transformation eller test.

For et nyt opslag:

```sh
python3 scripts/fetch_matriklen.py --cvr 27736033
```

Kommandoen foretager ét offentligt læseopslag og opretter en ny rådatamappe. Fejl og eventuelle fejlsvar bevares også. Et nyt opslag kan afvige fra det tidligere, fordi kilden kan være ændret. Scriptet gennemgår ikke selskabskoncernen eller eventuelle yderligere resultatsider.
