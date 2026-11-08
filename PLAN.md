# Fase 1: selskaber, ejendomme og anlæg

Statusdato: 2026-11-08. CVR-stamdata og relevans for ejendomme og anlæg er vurderet for 21 kandidater. Første runde i Matriklen Labs er gennemført for de 16 valgte CVR-numre, inklusive SK Vand-piloten. Målrettet opfølgning på Cerius og faglig validering står åbne.

## Mål og afgrænsning

Kortlæg alle juridiske enheder, ejendomme og anlæg med dokumenteret relevans for Envafors. Det omfatter blandt andet vand, spildevand, varme, el og gadelys, også når et relevant selskab driver et anlæg på en andens ejendom. Ejerskab, administration og drift registreres særskilt. Det skal fremgå, hvad der er aktuelt, historisk, besluttet, forventet og uafklaret.

Bevar kun kildeindhold, der konkret bruges som belæg eller til nødvendig bearbejdning. Historiske oplysninger i relevante svar bevares, men der oprettes ikke arkiver af alle opslag. Følg tidligere navne, CVR-numre, fusioner og frasalg, når de kan forklare en tilknytning. Registrer uafklarede spor som åbne spørgsmål frem for at udfylde huller ved gæt.

Kommuner, medejere og samarbejdsselskaber kan indgå som kontekst i selskabsstrukturen. Udvidelser af ejendomsindsamlingen kræver en dokumenteret forbindelse til kortlægningen. FIT er identificeret som fælles it-selskab. CVR dokumenterer, at NK-Forsyning (28118465) stiftede og ejer Næstved Forsyning (46837592). Eventuelle ændringer i ejerskab af aktiver og driftsansvar ved udtræden af Envafors står åbne. Se [CVR-kontrollen af Næstved Forsyning](research/decisions.md#nk-forsyning-og-næstved-forsyning).

Fasen omfatter ikke interne data, integrationer, DocuNote-opsætning, dokumenthåndteringsstruktur eller udvikling af en app/database. Kildedokumenter kan bruges som belæg for data; det er ikke en opgave om dokumenthåndtering.

## Leverancer og rækkefølge

| Trin | Leverance | Status | Afslutningskriterium |
|---|---|---|---|
| 1. Kilder og søgepunkter | Kilderegister og selskabskandidater | 21 kandidater med kilder og opfølgning | Kandidater har kildehenvisning, evidensstatus og næste kontrol. Nye relevante kilder tilføjes løbende |
| 2. Selskabsstruktur | CVR-enheder, navnehistorik, P-enheder og selskabsrelationer | CVR-stamdata, fire fusioner og deres fortsættende selskaber er kontrolleret. [Fusionsopfølgningen](research/decisions.md#aktiver-og-driftsroller-ved-de-fire-fusioner) dokumenterer aftaler, drift og aktivklasser på det niveau, kilderne dækker. [P-enheder og legale ejerforhold](research/decisions.md#p-enheder-og-selskabsejerskab) er undersøgt, og FITs status er kontrolleret | Selskabsrelationer og afgrænsning pr. kandidat er dokumenteret med kilder og datoer. Nye kandidater følges op |
| 3. Teknisk ejendomspilot | CVR-opslag i Matriklen Labs, bevaret råsvar og BFE-relationer i den fælles tabel | Gennemført for SK Vand (27736033) | Råsvaret kan spores til kilden, og alle poster kan afstemmes og genskabes fra det gemte svar |
| 4. Ejendomsindsamling | CVR-opslag og målrettet opfølgning på Cerius | 16 af 16 valgte CVR-numre undersøgt pr. 8. november 2026; 10 svar med poster og seks tomme svar. Cerius følges via konkrete spor til det tidligere NKE-net | Alle valgte opslag har registreret udfald og kildehenvisning. Kildens roller og status bevares særskilt |
| 5. Anlæg og krydskontrol | Anlægsoversigt, faglige stikprøver og koblinger til selskaber og ejendomme | [Valbygård Vandværk](research/decisions.md#valbygård-vandværk-og-sk-vand-piloten) er kontrolleret mod SK Vand-piloten. [Anlægskilder og søgeafgrænsning](research/decisions.md#anlægskilder-og-søgeafgrænsning) er afprøvet på eksempler. Den bredere anlægsoversigt og de konkrete CVR-roller og aktiviteter ved [Hovsøvej](research/decisions.md#hovsøvej-1-tilladelse-roller-og-aktivitet) står åbne. | Relevante kilder er gennemgået, og søgeafgrænsning og belæg for driftsansvar er beskrevet pr. sektor. Anlæg uden ejendomsfund og ejendomme uden anlæg er håndteret |
| 6. Samlet kvalitetssikring | Sammenhængende CSV/JSON, dækningsbeskrivelse og review | Åben | Kontroller afstemt, huller beskrevet, reviewbemærkninger håndteret og processen gentagelig |

Brug [kandidatlistens opslagsmetode](DATA_MODEL.md#research) til at vælge CVR-opslag. Faglig kontrol af roller, datoer og dækning kan foregå parallelt. De indsamlede poster har status som kildeudsagn, indtil de er kontrolleret. Selskabsafgrænsningen er reviewet; indhent også underagent-review af den faglige kontrol før den endelige leverance.

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

Registrer seneste opslagsforsøg pr. CVR og kilde med URL, tidspunkt med tidszone og udfald. Skeln mellem fund, tomt svar, delvist svar, adgangsafslag og teknisk fejl. Markér også, hvad der endnu ikke er undersøgt, og om et bevaret råsvar er fra et tidligere opslag. Rapporter dækning pr. kilde og sektor samt åbne spørgsmål. Undgå en samlet fuldstændighedsprocent, når det samlede antal relevante selskaber, ejendomme eller anlæg er ukendt.

En endelig faseleverance skal have en fast referencedato, eksplicit afgrænsning, relevante kildehenvisninger, datamodel, kvalitetsstatus og dokumenteret underagent-review. Brug et fælles kildeindeks frem for metadatafiler for hvert opslag; Git versionerer committede data og kode. Væsentlige uafklarede forhold skal stå i leverancen. Et tomt søgeresultat er alene resultatet af det konkrete opslag.
