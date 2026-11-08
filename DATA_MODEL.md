# Datamodel

Pr. 8. november 2026 er der bevaret Matriklen Labs-svar for alle 21 kandidater. Metode og kode versioneres i Git.

## Hvad der forbindes

Juridiske selskaber identificeres med CVR. Selskabsrelationer skal dokumenteres særskilt; de kan ikke udledes af en navneliste. Ejendomsrelationer forbinder CVR med BFE og en bestemt rolle. Senere forbindes anlæg med selskaber og ejendomme, når der er konkret kildebelæg. Et anlæg kan omfatte flere ejendomme og omvendt. P-enheder, ejendomme og anlæg er forskellige objekter.

Der oprettes først yderligere tabeller, når vi har relevante data og en konkret anvendelse. Der gemmes ingen tomme tabeller eller alternative eksporter for mulige fremtidige behov.

## Research

- `research/company_candidates.csv`: Én række pr. kandidat med kontrolleret CVR. `cvr_registered_name` og `current_cvr_status` gengiver CVR-visningen på opslagstidspunktet, også for opløste selskaber. `cvr_secondary_names` er de viste binavne adskilt med `|`; tomt ved et vellykket opslag betyder, at CVR ikke viste nogen. `cvr_start_date` og `cvr_end_date` er CVR's start- og ophørsdato som ISO-datoer; tom ophørsdato betyder, at der ikke blev vist en dato.
- `scope_group` bruges til at finde kandidater inden for en forsyningsgruppe. Selskabsrelationer fremgår af noterne og ejertabellen.
- `property_scope` og `facility_scope` afgrænser henholdsvis faglig ejendomsopfølgning og anlægsindsamling. Begge kan være `omfattet`, `fravalgt` eller `uafklaret`. `scope_assessed_on` er vurderingsdatoen. Hvert spor har egne `*_scope_source_ids` og `*_scope_basis` med kildehenvisninger og begrundelse. Alle kandidater medtages i det ensartede CVR-opslag i Labs. Verificerede roller ved konkrete ejendomme og anlæg kræver særskilt belæg.
- `research/sources.csv`: URL, udgiver, titel og kildebegrænsninger. Andre tabeller refererer til `source_id`. Flere ID'er adskilles med `|`. `document_date` er kildens dato. `lookup_at` er opslagstidspunktet med tidszone, eller opslagsdatoen alene hvis klokkeslættet er ukendt. Datoer for regnskabsperiode, virkning og registrering holdes adskilt i noten eller kandidatfelterne. `lookup_outcome` skelner mellem fund (`found`), tomt resultat (`no_result`), delvist svar (`partial`), afslag (`access_denied`) og teknisk fejl (`technical_error`). En tom værdi betyder, at udfaldet ikke blev kodet. Noten peger på råfilen, hvis svaret er bevaret.

- `research/production_units.csv`: Én række pr. synligt P-nummer under et valgt CVR. `source_status` følger CVR-svarets lister for aktive og ophørte enheder. `registered_name`, `registered_address`, `postal_code_and_city`, `main_industry_code` og `main_industry_name` gengiver stamdata. `start_date` og `end_date` gælder enheden, ikke en bestemt adresseperiode. Adresse og branche er søgespor til videre kontrol af anlæg. De beviser ikke i sig selv ejerskab eller aktuel driftsrolle.
- `research/company_ownership.csv`: Én række pr. ejerlink og andelsperiode i den offentlige CVR-visning, hvor kapital og stemmer har samme viste periode. `company_cvr` er det selskab, som ejerforholdet gælder for. Slå nummeret op i `company_candidates.csv` under `cvr`, og kopiér `cvr_registered_name` til `registered_company_name`. Navnet gælder ved opslaget af stamdata, også når rækken viser en ældre ejerperiode. `owner_cvr` er afstemt via ejerlinket i `owner_link_source_id`. Læs den viste andelsperiode for at afgøre, om den er afsluttet. CVR kan vise afsluttede andelsperioder i panelet med aktuelle ejere. Kapital og stemmer bevares som to separate viste værdier, inklusive intervaller. `displayed_owner_change_date` er ændringsdatoen på ejerkortet, ikke startdatoen for hver andelsperiode. `disposal_date` udfyldes, når visningen angiver afhændelsesdato. Tabellen dækker CVR's offentlige legale ejere og udgør ikke en komplet ejerbog. Se [afgrænsning og kontrol](research/decisions.md#p-enheder-og-selskabsejerskab).

## Kildesvar og fælles indeks

`data/raw/matriklen-labs/<CVR>.json` er API'ets uændrede svarbytes. CVR ligger i filnavnet og føjes ikke til kildeobjekterne. `index.json` har CVR som nøgle og tre oplysninger pr. svar:

- `url`: det konkrete kildeopslag inklusive CVR-parameter.
- `retrieved_at`: afslutningstidspunkt for hentningen med tidszone. Pilotens værdi er overført fra den oprindeligt registrerede `completed_at`; tidspunktet er ikke rekonstrueret.
- `sha256`: kontrol af, at kildeindholdet er uændret i forhold til indekset.

Kun seneste gyldige svar pr. CVR ligger i arbejdsstrukturen. Git bevarer committede versioner. Fejl og headers er ikke selvstændige datafiler. Manglende indeksført CVR-fil, uregistreret fil, forkert hash, dublerede JSON-nøgler, ugyldige JSON-tal eller ukendt svarstruktur stopper bearbejdningen. Hvert gyldigt svar med to tomme lister gemmes og giver ingen rækker i relationstabellen. Når ingen kildesvar er bevaret, stopper bearbejdningen med en fejl. Kilderegisteret beskriver det seneste opslag. Et bevaret råsvar kan være fra et tidligere vellykket opslag.

## Samlet relationstabel

`data/relations.csv` har én række pr. kildeobjekt i `ejer` eller `administrerer`, samlet for alle registrerede CVR-numre. Den viser Labs-observationer, også hvor forbindelsen til Envafors på ejendomsniveau er uafklaret. Dubletter og poster med manglende BFE bevares. Rækkeantal afstemmes mod kilderne.

| Felter | Betydning |
|---|---|
| `cvr` | Selskabets CVR og råsvarets filnavn |
| `bfe` | Ejendommens BFE som tekst. Tomt, når kilden ikke giver et gyldigt BFE |
| `role`, `source_status` | Kildens rolle (`ejer`/`administrerer`) og status (`gældende`/`historisk`) bevares |
| `virkning_fra_original` | Hele Labs-feltet `virkningFra`. Læs datoen sammen med `source_status` og `role` efter [Labsværktøjets visningsregler](#faglige-forbehold) |
| `actual_share_state`, `actual_share_numerator`, `actual_share_denominator` | Faktisk ejerandel som tilstand og særskilt brøk |
| `registered_share_state`, `registered_share_numerator`, `registered_share_denominator` | Tinglyst ejerandel, uafhængigt af den faktiske |

Andelstilstande er `present`, `missing`, `null` og `invalid`. Nul som tæller bevares; en manglende andel er ikke nul. Ukendte felter og værdier markeres til kontrol og findes fortsat i originalen. En særskilt liste med forskellige BFE-numre kan udledes af tabellen og gemmes ikke som en dublet.

Brug CVR, BFE og rolle til at sammenholde en observation med råsvaret. Flere observationer kan vedrøre samme ejendom og selskab. Tabellen gengiver Labs' oplysninger. Faglige stikprøver er dokumenteret særskilt i [research/decisions.md](research/decisions.md).

`data/issues.csv` angiver CVR, BFE, rolle og en forklaring af hvert fund. Hvis et BFE mangler eller er ugyldigt, er BFE-feltet tomt, og fundet forklarer årsagen. Begge CSV-filer genbygges fra råsvarene.

## Faglige forbehold

I Matriklen Labs vises `virkningFra` under »Virkning« for både ejere og administratorer. Labs beskriver den tilsigtede betydning som første overtagelsesdato ved status `gældende` og som datoen, hvor CVR-nummeret ophørte som ejer eller administrator, ved status `historisk` (S020, S057, S139). Visningen kan bruge teksten »Siden d.« ved begge statusser, når svaret kun indeholder `virkningFra`. Betydningen skal kontrolleres for den konkrete post. For SK Forsynings gældende ejerpost ved BFE `5367067` falder Labs-datoen 20.05.2026 sammen med Matriklen.dk's viste tinglysningsdato, mens Matriklen.dk viser overtagelsesdatoen 01.01.2026 (S081, S143). Labs-datoen kan derfor ikke bruges som en sikker overtagelsesdato, en tinglysnings- eller registreringsdato eller til at rekonstruere en fuld periode. Vi bevarer hele datostrengen og udleder ingen særskilte fra- eller til-felter.

Faktisk og tinglyst ejerandel bevares særskilt. Administrator betyder ikke automatisk ejer eller driftsansvarlig. Flere visninger af samme register er ikke uafhængige bekræftelser.

Geodatastyrelsen mærker webværktøjet »Ejendomme ejet af virksomhed« som prototype. Webværktøjets JavaScript kalder `CvrEjerskaber` på `api.labs.matriklen.dk`. Ved kontrol 8. november 2026 fandt vi ingen særskilt offentlig dokumentation for API'ets driftsstatus, versionspolitik eller stabilitetsgarantier. Se S020, S030 og S057 i [kilderegisteret](research/sources.csv).

Første runde indeholder både gældende og historiske poster, men startgrænsen og dækningen af historikken er ukendte. Det offentlige Labs-værktøj henter én respons pr. CVR og følger ingen paginering. Det afprøvede eksempel gav 168 poster i én respons. Eventuelle servergrænser er uafklarede. Se [kontrollen af historik og resultatgrænser](research/decisions.md#historik-og-resultatgrænser-i-matriklen-labs). Et tomt svar beskriver det konkrete opslag og kan ikke bruges til at udelukke relevante ejendomme.

CSV er UTF-8 med komma og én overskriftsrække. Identifikatorer importeres som tekst. Ukendte værdier forbliver tomme og forklares af tilstand, kontrolfund eller kildehenvisning. JSON er UTF-8. Opslagstid, dokumentdato og virknings-/registreringsdato holdes adskilt.
