# Beslutninger og review

Dato: 2026-11-08. Dette er en log over væsentlige metodevalg; den er ikke kildebelæg for ejerskab.

## D01: Selvstændig research og kontrol af slutdata

Brugerens præcisering tillader nødvendig eksekvering til research. AGENTS.md er ændret, så offentlig research, scripts, API-kald og lokal bearbejdning ikke kræver manuel eksekvering. Sporbarhed, rådata, usikkerhed og kontrol af slutleverancen er fortsat krav. Scope er data; DocuNote og dokumenthåndtering er udenfor.

Review: underagenterne `method_review` og `official_sources` gennemgik den faktiske AGENTS-diff. Begge havde ingen væsentlige indvendinger. Bemærkninger om rutinefrihed, kildeafhængighed, tidsdimensioner og afgrænsning af reviewkravet blev indarbejdet.

## D02: Kandidater er en selvstændig researchleverance

De 20 fundne CVR-numre gemmes som kandidater med kildehenvisning og næste kontrol. De betegnes ikke som en komplet eller aktuelt verificeret koncern. Selskabsrelationer skal have en selvstændig tabel og kildebelæg. Næstved Forsyning `46837592` må ikke sidestilles med NK-Forsyning `28118465` ud fra navnet.

Review: `method_review` påpegede, at kandidatlisten alene ikke repræsenterer selskabsstrukturen. DATA_MODEL.md definerer derfor `company_relations` særskilt, og PLAN.md har selskabsafklaringen som åben leverance. Medejere/kommuner er kontekst; deres øvrige koncerner udvider ikke automatisk ejendomssøgningen.

## D03: Bevar alle rårelationer og begge ejerandele

Piloten har 42 relationer/42 forskellige BFE. Kildestatus og rolle bevares. Faktisk og tinglyst ejerandel lagres hver for sig. Manglende brøk bliver ikke nul. En nulværdi eller status alene afgør ikke juridisk ejerskab.

Review af råsvaret: `official_sources` bekræftede optællingen og påpegede BFE `2539366` (faktisk 1/1, tinglyst 0/1) samt `5367067` (faktisk 0/1, tinglyst 1/1). Begge markeres i kvalitetsloggen. Uafhængig faglig afklaring udestår.

## D04: Datoer og fuldstændighed er ikke afklaret

API-feltet `virkningFra` bevares ufortolket. Labs' beskrivelse af visningsfeltet »Virkning« beviser ikke alene API-feltets betydning. Der udledes ingen start-/slutdato. En gyldig JSON-prøve beviser heller ikke historikdækning eller fravær af resultatgrænser.

Review: `official_sources` støttede denne fortolkning efter at have gennemgået råsvaret og dokumentationen. PLAN.md registrerer datosemantik og API-dækning som åbne opgaver.

## D05: Enkel, reproducerbar filpipeline

To små researchscripts bruger Python-standardbiblioteket og systemets curl. Rådata forbliver uændrede. En transformation skriver en samlet kørselsmappe med særskilte processed-/quality-mapper og manifest; der er ingen database eller app. Kørselsmappen vælges eksplicit og overskrives ikke. Manifestet skelner teknisk færdig bearbejdning fra faglig verifikation.

Review af forslaget: `method_review` anbefalede at skelne fejl og gyldigt tomt resultat, bevare relationer med ugyldigt BFE, afstemme kilde-/outputantal og beskytte mod delvise output. Dette er indarbejdet. Det tidligere forslag om separate kørselsmapper på tværs af processed/quality er erstattet af én samlet run-mappe med to undermapper, så hele kørslen kan publiceres samlet efter skrivning.

## D06: Konkrete fil- og kodereview

`official_sources` afstemte alle 42 pilotrelationer mod råsvaret (BFE, rolle, status, datoråstreng og begge andele) samt de 42 ejendomsreferencer og hashene. Plan og model havde ingen væsentlige faglige indvendinger. Efter udvidelsen blev kilder S020–S030 og den rettede kandidat C003 reviewet særskilt uden væsentlige indvendinger. Bemærkningen om kildeside S021's opdateringsdato er indarbejdet i kildenoten.

`method_review` genkørte transformationen i en midlertidig mappe og kontrollerede identiske outputbytes samt de oprindelige seks tests. Reviewet fandt en reel risiko: standard-JSON-indlæsning kunne stiltiende skjule poster ved dublerede objektnøgler. Metodeversion 2 afviser derfor dublerede nøgler i både råsvar og requestmanifest samt ugyldige JSON-tal. To regressionstests er tilføjet. Hentningsscriptets JSON-kontrol bruger samme strenge regler.

Den første tekniske kørsel v1 er bevaret med sin oprindelige kode arkiveret i `method/`. Den gældende bearbejdning er `pilot-27736033-v2`, som også gemmer og hasher sin præcise kodeversion. Rådata ændres ikke. Teknisk test- og reviewstatus er ikke en godkendelse af juridisk ejerskab eller fuldstændighed.

Afsluttende kontrol: `method_review` genprøvede rettelsen og godkendte v2 som teknisk pilot uden resterende væsentlige fund. Alle otte tests bestod; dublerede JSON-nøgler blev afvist uden output, input-/metadata-/outputhash og kodearkiv stemte, og en genkørsel gav identiske outputbytes. Rodagentens kontrol af de 30 kilde-ID'er, 20 unikke CVR-kandidater, fremmednøgler og lokale dokumenthenvisninger bestod også. Kontrollerne ændrede ingen rådata. Faglige spørgsmål er fortsat åbne som angivet nedenfor og i PLAN.md.

## D07: Git-synkronisering ved milepæle

Brugeren har bedt om synkronisering og om, at Git indgår i arbejdsprocessen, når det er hensigtsmæssigt. AGENTS.md kræver nu sammenhængende commits og push ved passende milepæle og før aflevering/overdragelse af afsluttet arbejde. Rutinehandlingerne kræver ikke en ny brugerbekræftelse. Remote-status, relevante kontroller, afgrænset staging og verificering af branch/upstream indgår; brugerændringer og publiceret historik skal bevares.

Review: `method_review` gennemgik både forslag og faktisk instruktionsdiff og godkendte uden væsentlige indvendinger. Bemærkninger om behovsbestemt fetch ved opgavestart, integration af remoteændringer og kontrol af upstream er indarbejdet.

Ved første staging markerede Git rå HTTP-headers og CSV-filers CRLF som whitespace. Indholdet blev bevaret uændret, og `.gitattributes` er tilføjet for at undgå linjeskiftkonvertering af rådata og hashede kørsler samt genkende CSV-linjeskift. `method_review` gennemgik valget; bemærkningen om at lade rådatareglen have sidste prioritet er indarbejdet. Kontrol af staged bytes og kørselsmanifesternes hash bestod.

## Åbne forhold

- Aktuel CVR-status, faktisk selskabsstruktur og flere historiske relationer mangler officiel kontrol.
- Kandidaternes eksterne kildebelæg er endnu ikke arkiveret som rådata.
- Kilderegisteret indeholder nu 30 poster, herunder dokumentation for de prioriterede registre. Adgang, konkret feltdækning og udtræksmetode skal fortsat afklares kilde for kilde.
- Ejendomsfundene er endnu ikke koblet til anlæg, adresser, matrikler eller BBR.
- Faglige spørgsmål i D03/D04 er åbne og forhindrer, at pilotdata betegnes som en endeligt valideret ejendomsoversigt.
