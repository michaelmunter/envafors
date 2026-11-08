# Datamodel

Status: pilot pr. 2026-11-08. Kun filer med en aktuel anvendelse gemmes. Metode og kode versioneres i Git.

## Hvad der forbindes

Juridiske selskaber identificeres med CVR. Selskabsrelationer skal dokumenteres særskilt; de kan ikke udledes af en navneliste. Ejendomsrelationer forbinder CVR med BFE og en bestemt rolle. Senere forbindes anlæg med selskaber og ejendomme, når der er konkret kildebelæg. Et anlæg kan omfatte flere ejendomme og omvendt. P-enheder, ejendomme og anlæg er forskellige objekter.

Der oprettes først yderligere tabeller, når vi har relevante data og en konkret anvendelse. Der gemmes ingen tomme tabeller eller alternative eksporter for mulige fremtidige behov.

## Research

- `research/company_candidates.csv`: 20 kandidater med CVR, kilde-ID'er, evidensstatus og næste kontrol. `candidate_kind` er en researchprioritering, ikke en verificeret registreringsstatus. Alle aktuelle CVR- og relationskontroller står som `not_checked`.
- `research/sources.csv`: URL, udgiver, titel og kildebegrænsninger. `document_date` og `researched_on` er forskellige datoer. `source_ids` i kandidatlisten refererer til `source_id`; flere ID'er adskilles med `|`. En kildehenvisning medfører ikke et krav om at hente og arkivere hele kilden.

## Kildesvar og fælles indeks

`data/raw/matriklen-labs/<CVR>.json` er API'ets uændrede svarbytes. CVR ligger i filnavnet og føjes ikke til kildeobjekterne. `index.json` har CVR som nøgle og tre oplysninger pr. svar:

- `url`: det konkrete kildeopslag inklusive CVR-parameter.
- `retrieved_at`: afslutningstidspunkt for hentningen med tidszone. Pilotens værdi er overført fra den oprindeligt registrerede `completed_at`; tidspunktet er ikke rekonstrueret.
- `sha256`: kontrol af, at kildeindholdet er uændret i forhold til indekset.

Kun seneste svar pr. CVR ligger i arbejdsstrukturen. Git bevarer committede versioner. Fejl og headers er ikke selvstændige datafiler. Manglende CVR-fil, uregistreret fil, forkert hash, dublerede JSON-nøgler, ugyldige JSON-tal eller ukendt svarstruktur stopper bearbejdningen. Et gyldigt svar med to tomme lister er et tomt kildeopslag; ingen indsamlede svar er en fejl.

## Samlet relationstabel

`data/relations.csv` har én række pr. kildeobjekt i `ejer` eller `administrerer`, samlet for alle registrerede CVR-numre. Dubletter og poster med manglende BFE bevares. Rækkeantal afstemmes mod kilderne.

| Felter | Betydning |
|---|---|
| `cvr`, `source_pointer`, `source_sha256` | CVR-fil og kildeobjekt, fx `/ejer/0`, samt kontrol mod indeksets hash. CVR + pointer identificerer en observation i denne kildeversion |
| `bfe`, `bfe_state` | BFE som tekst; tilstand `present`, `missing`, `null` eller `invalid` |
| `role`, `source_status` | Kildens rolle (`ejer`/`administrerer`) og status (`gældende`/`historisk`) bevares |
| `virkning_fra_original` | Hele kildens datostreng; ingen start-/slutdato udledes |
| `actual_share_state`, `actual_share_numerator`, `actual_share_denominator` | Faktisk ejerandel som tilstand og særskilt brøk |
| `registered_share_state`, `registered_share_numerator`, `registered_share_denominator` | Tinglyst ejerandel, uafhængigt af den faktiske |
| `verification_status` | `source_only`: kildeudsagn, ikke uafhængig bekræftelse |

Andelstilstande er `present`, `missing`, `null` og `invalid`. Nul som tæller bevares; en manglende andel er ikke nul. Ukendte felter og værdier markeres til kontrol og findes fortsat i originalen. En særskilt liste med forskellige BFE-numre kan udledes af tabellen og gemmes ikke som en dublet.

`data/issues.csv` indeholder kun konkrete fund med `cvr`, `code`, `source_pointer`, `bfe`, `message` og `source_sha256`. Piloten har to fund af typen `different_share_values`. Optællinger skrives til terminalen og gemmes ikke som profilfiler. Begge CSV-filer genbygges; de vedligeholdes ikke manuelt.

## Faglige forbehold

`virkningFra` er ikke sikkert koblet til dokumentationens visningsfelt »Virkning« og fortolkes derfor ikke som en fra-/til-dato. Faktisk og tinglyst ejerandel må ikke erstatte hinanden. Administrator betyder ikke automatisk ejer eller driftsansvarlig. Flere visninger af samme register er ikke uafhængige bekræftelser.

API'ets historikdækning og eventuelle resultatgrænser er uafklarede. Et teknisk gyldigt svar dokumenterer ikke fuldstændighed, og et tomt svar dokumenterer ikke fravær af relevante ejendomme. Disse generelle begrænsninger gentages ikke som kontrolrækker for hvert opslag.

CSV er UTF-8 med komma og én overskriftsrække. Identifikatorer importeres som tekst. Ukendte værdier forbliver tomme og forklares af tilstand, kontrolfund eller kildehenvisning. JSON er UTF-8. Opslagstid, dokumentdato og virknings-/registreringsdato holdes adskilt.
