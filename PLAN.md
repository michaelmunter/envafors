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
| 3. Ejendomspilot | Ét CVR-svar, fælles relationstabel og konkrete kontrolfund | Teknisk gennemført for 27736033; faglige kontroller åbne | Format, roller, datoer og begrænsninger undersøgt. Stikprøver mod relevante kilder og kontrol af mindst ét SK Vand-anlæg |
| 4. Ejendomsindsamling | Samme dokumenterede metode på omfattede CVR-numre | Afventer pilotens metodekontrol og selskabsafgrænsning | Alle omfattede CVR har registreret udfald og kildehenvisning; historik og administration særskilt |
| 5. Anlæg og krydskontrol | Anlægsoversigt og koblinger til selskaber/ejendomme | Åben | Relevante anlægskilder gennemgået; anlæg uden ejendomsfund og ejendomme uden anlæg håndteret |
| 6. Samlet kvalitetssikring | Sammenhængende CSV/JSON, dækningsbeskrivelse og review | Åben | Kontroller afstemt, huller beskrevet, reviewbemærkninger håndteret og processen gentagelig |

Trin 2 og pilotens faglige kontrol kan fortsætte parallelt. Brede ejendomsudtræk kan begynde, når selskabsafgrænsningen er på plads, piloten har afklaret de væsentlige metodeproblemer, og en underagent har gennemgået pilotens faglige metode. Historiske spørgsmål kan stå åbne, hvis deres betydning og status fremgår.

## Arbejdskø

De konkrete opgaver for kommende sessioner ligger i [QUEUE.md](QUEUE.md).

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
