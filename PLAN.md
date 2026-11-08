# Fase 1: selskaber, ejendomme og anlæg

Statusdato: 2026-11-08. Planen gælder det offentlige datagrundlag. Arbejdet er i pilotfasen, og ingen samlet dataleverance er endelig.

## Mål og afgrænsning

Kortlæg relevante juridiske enheder, deres dokumenterede relationer samt ejendomme og anlæg, de ejer, administrerer eller driver. Det skal fremgå, hvad der er aktuelt, historisk, besluttet, forventet og uafklaret.

Bevar kun kildeindhold, der konkret bruges som belæg eller til nødvendig bearbejdning. Historiske oplysninger i relevante svar bevares, men der oprettes ikke arkiver af alle opslag. Følg tidligere navne, CVR-numre, fusioner og frasalg, når de kan forklare en tilknytning. Registrer uafklarede spor som åbne spørgsmål frem for at udfylde huller ved gæt.

Kommuner, medejere og samarbejdsselskaber kan indgå som kontekst i selskabsstrukturen. Deres øvrige selskaber omfattes ikke automatisk af ejendomsindsamlingen. Udvidelser skal begrundes med en dokumenteret forbindelse til den aftalte kortlægning. Særligt FIT og det mulige nye Næstved Forsyning skal undersøges, før deres rolle fastlægges.

Fasen omfatter ikke interne data, integrationer, DocuNote-opsætning, dokumenthåndteringsstruktur eller udvikling af en app/database. Kildedokumenter kan bruges som belæg for data; det er ikke en opgave om dokumenthåndtering.

## Leverancer og rækkefølge

| Trin | Leverance | Status | Afslutningskriterium |
|---|---|---|---|
| 1. Kilder og søgepunkter | Kilderegister og selskabskandidater | Første version skrevet: 20 kandidater, 30 kilder | Kandidater har kildehenvisning, evidensstatus og næste kontrol. Nye relevante kilder tilføjes løbende |
| 2. Selskabsstruktur | CVR-enheder, navnehistorik, P-enheder og selskabsrelationer | Åben; aktuel CVR-kontrol ikke udført | Alle identificerede kandidater behandlet; relationer og fravalg dokumenteret; nye kandidater fulgt |
| 3. Ejendomspilot | Ét CVR-svar, fælles relationstabel og konkrete kontrolfund | Teknisk gennemført for 27736033; faglige kontroller åbne | Format, roller, datoer og begrænsninger undersøgt; stikprøver mod relevante kilder og mindst ét anlægsspor |
| 4. Ejendomsindsamling | Samme dokumenterede metode på omfattede CVR-numre | Afventer pilotens metodekontrol og selskabsafgrænsning | Alle omfattede CVR har registreret udfald og kildehenvisning; historik og administration særskilt |
| 5. Anlæg og krydskontrol | Anlægsoversigt og koblinger til selskaber/ejendomme | Åben | Relevante anlægskilder gennemgået; anlæg uden ejendomsfund og ejendomme uden anlæg håndteret |
| 6. Samlet kvalitetssikring | Sammenhængende CSV/JSON, dækningsbeskrivelse og review | Åben | Kontroller afstemt, huller beskrevet, reviewbemærkninger håndteret og processen gentagelig |

Trin 2 og pilotens faglige kontrol kan fortsætte parallelt. Brede ejendomsudtræk skal vente på, at piloten har afklaret de væsentlige metodeproblemer. Der kræves ikke, at alle historiske spørgsmål er løst, men deres betydning og status skal være synlig.

## Næste konkrete opgaver

- [x] Gem planen og en eksplicit datamodel i projektet.
- [x] Gem de hidtidige selskabskandidater og kilder som CSV.
- [x] Bevar API-prøven som `data/raw/matriklen-labs/27736033.json`, med fælles URL, hentetid og hash i `index.json`.
- [x] Opret en gentagelig transformation, som bevarer alle 42 kilderelationer.
- [x] Gem én samlet `data/relations.csv` og konkrete fund i `data/issues.csv`; undlad profiler og kørselsarkiver.
- [ ] Bevar konkret kildebelæg, når det anvendes til at kontrollere kandidater eller relationer. Der er ingen generel opgave om at arkivere alle kildehenvisninger.
- [x] Udvid kilderegisteret med dokumentation for CVR, Ejerfortegnelsen, BBR, DAR, Jupiter, PULS, DMA og Plandata.
- [ ] Kontroller aktuel CVR-status og navne for de 20 kandidater via officielle oplysninger; undersøg nyfundne kandidater løbende.
- [ ] Opret selskabsrelationer med konkret belæg. Kandidatlisten er ikke koncernstrukturen.
- [ ] Afklar relationen mellem `46837592` og `28118465`; navnelighed er ikke bevis.
- [ ] Afklar fusioner/ophør og efterfølgere for tidligere service- og vejlysselskaber samt NKE-Elnet.
- [ ] Undersøg den præcise betydning af Labs-feltet `virkningFra`, især ved historiske relationer.
- [ ] Undersøg de to pilotposter med forskellige faktiske og tinglyste ejerandele: BFE `2539366` og `5367067`.
- [ ] Undersøg et udvalg af pilotens gældende/historiske ejerposter og administratorposter i Matriklen. Fælles registerophav må ikke kaldes uafhængig bekræftelse.
- [ ] Kontroller mindst ét kendt SK Vand-anlæg via anlægsbeskrivelse/Jupiter og undersøg forbindelsen til ejendomsfundene.
- [ ] Afklar API'ets historikdækning og eventuelle resultatgrænser/paginering. Én prøve kan ikke bevise fuldstændighed.
- [ ] Indhent review af pilotens faglige metode, før indsamlingen udvides.

## Prioriterede datakilder

1. **CVR og officielle selskabsoplysninger:** juridisk identitet, status, navne, P-enheder og ejerrelationer. Årsrapporter og kommunale ejeroplysninger supplerer.
2. **Matriklen Labs, Matriklen og Ejerfortegnelsen:** selskab–ejendom-relationer, BFE og ejer-/administratorroller. Behandles som potentielt samme underliggende registerophav.
3. **BBR og DAR:** bygnings-/anlægsregistreringer og officielle adressereferencer. En adresse er ikke en entydig ejendoms- eller anlægsidentitet.
4. **Jupiter og PULS:** vandindvindingsanlæg, boringer, spildevandsanlæg og udløb; kildernes særskilte identifikatorer bevares.
5. **DMA, Plandata og offentlige kommunale oplysninger:** aktivitet, myndighedsforhold, matrikler og placeringer. Planlagte forhold holdes adskilt fra eksisterende anlæg.

Kildevalg og adgangsforhold skal dokumenteres i kilderegisteret før brug. LER er et særskilt muligt senere spor, fordi en forespørgsel har andre konsekvenser end et almindeligt offentligt opslag; det er ikke en del af den første pilot.

## Kontrol og dækningsgrad

Hold fire spørgsmål adskilt: Er data hentet teknisk korrekt? Er kildeværdierne gengivet korrekt? Er deres betydning og tilknytning dokumenteret? Hvor meget af det aftalte omfang er undersøgt?

Rapporter antal kandidater behandlet, omfattede CVR undersøgt, kildeopslag gennemført, relationer fundet og åbne spørgsmål. Undgå en samlet fuldstændighedsprocent, når det samlede antal relevante selskaber, ejendomme eller anlæg er ukendt.

En endelig faseleverance skal have en fast referencedato, eksplicit afgrænsning, relevante kildehenvisninger, datamodel, kvalitetsstatus og dokumenteret underagent-review. Brug et fælles kildeindeks frem for metadatafiler for hvert opslag; Git versionerer committede data og kode. Væsentlige uafklarede forhold skal stå i leverancen. Et tomt søgeresultat er alene resultatet af det konkrete opslag.
