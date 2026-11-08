# Gældende metodevalg og review

Dato: 2026-11-08. Tidligere udgaver af struktur og kode findes i Git; denne fil beskriver de gældende valg.

## Bevar kun det, der har en konkret funktion

Efter brugerens præcisering er rådata fladet ud til ét uændret JSON-svar pr. CVR og ét fælles indeks med URL, hentetid og hash. Kun seneste gyldige svar beholdes i arbejdsstrukturen. HTTP-headers, fejlede forsøg, gamle kørsler, profiler, kodekopier og den redundante BFE-liste er fjernet. Git bevarer committede versioner.

De to fælles CSV-filer er den anvendelige relationstabel og konkrete kontrolfund. Generelle forbehold står i DATA_MODEL.md. Nye filer kræver en konkret anvendelse; der foretages ikke generel arkivering af alt tilgængeligt materiale.

## Bevar kildeindhold og betydning

Pilotens 7.476 kildebytes og SHA-256 er uændrede efter flytning til `27736033.json`. Indeksets hentetid er det oprindeligt registrerede afslutningstidspunkt. Alle 42 relationer er sammenlignet felt for felt med den tidligere tabel. De to konkrete forskelle i ejerandele er bevaret som kontrolfund.

Faktiske og tinglyste andele bevares særskilt. Nul, manglende og ugyldige værdier skelnes. Datoerne fortolkes ikke som start-/slutdatoer. Kandidatlisten er ikke en verificeret selskabsstruktur; Næstved Forsyning `46837592` sidestilles ikke med NK-Forsyning `28118465` ud fra navnet.

## Kontrol og review

Den tidligere JSON-risiko med dublerede nøgler er fortsat dækket af streng indlæsning og regressionstest. Nye svar må først erstatte sidste gode svar efter HTTP 200, kendt struktur og JSON-kontrol. Indeks og CVR-filer skal stemme fuldstændigt før samlet bearbejdning.

Underagenten `method_review` gennemgik forslaget og de færdige filer og godkendte den enklere løsning som teknisk pilot uden væsentlige fund. Reviewet kontrollerede bevarede data, deterministisk genkørsel og de to aftalte outputfiler. Underagenten `official_sources` godkendte kildebelæg, den oprindelige hentetid, uændrede råbytes og alle 42 relationer uden væsentlige indvendinger. Den aktuelle testsuite har 14 beståede tests, herunder kontrol af CVR i kilde-URL, sidste gode svar, indeksafstemning og gendannelse ved skrivefejl.

Underagenten `pilot_scope_review` gennemgik planen for indsamling efter den tekniske pilot. Reviewet førte til, at første runde kun omfatter CVR-numre, der er valgt til ejendomsopslag, at opslagsudfald registreres særskilt fra råsvar, og at relevante anlægskilder skal gennemgås i hver sektor.

## Arbejdsproces

Nødvendig offentlig research og lokal eksekvering er tilladt. Væsentlige beslutninger og leverancer reviewes. Arbejdet committes og synkroniseres ved passende milepæle; kildeindeks, kildesvar og genbyggede tabeller hører sammen i samme commit. Begrænsningerne for interne data og systemer gælder fortsat.

Underagenten `direct_sources_review` gennemgik instruksen om direkte kildesvar og kontrollerede begge adgangsveje mod kilderegisteret. Reviewet førte til, at tilladt adgang blev gjort eksplicit, og at Matriklen Labs-opslaget blev afgrænset til de CVR-numre, der er valgt til ejendomsindsamlingen. Reviewet fandt ingen væsentlige fejl.

## Historik for Matriklen Labs' CVR-opslag

Labs-forsidens arkivkopi fra 13. oktober 2025 har et værktøjskatalog uden link til `/ejerskaber`. Kopien fra 11. november 2025 viser »Ejerskaber« som prototype og linker til værktøjet. Værktøjssiden er arkiveret 9. december 2025. Dens daværende JavaScript-modul kunne ikke hentes fra arkivet. Datoerne viser, hvad der er bevaret i arkivet. Se S058–S060 i [kilderegisteret](sources.csv).

Søgningen 8. november 2026 fandt ingen dateret reference til `CvrEjerskaber` fra før værktøjets omtale. Webarkivets indeks gav ingen fund på det konkrete endepunkt (S061). Det tidligste verificerede belæg i projektet for API-kaldet er det aktuelle Labs-modul (S057). Endepunktets første udgivelsesdato og oprindelige formål står åbne. Underagenten `api_history_review` søgte uafhængigt efter ældre referencer og fandt ingen til det konkrete endepunkt.

## CVR-kontrol af selskabskandidater

Den 8. november 2026 blev C001–C020 kontrolleret i Erhvervsstyrelsens offentlige CVR. Alle 20 opslag gav en entydig CVR-post: 16 med status »Normal« og fire med status »Opløst efter fusion«. C021 (Cerius A/S) er den nytilføjede kandidat og stod også som »Normal«. Dækningen gælder denne navngivne liste på opslagsdatoen. Den siger ikke, om alle relevante selskaber er fundet.

Gentag kontrollen med CVR-numrene fra [kandidatlisten](company_candidates.csv):

1. Start med at åbne gateway-URL'en fra [kilderegisteret](sources.csv) direkte i en browser. Brug samme adresse til gentagne opslag: skift `cvrnummer`, og behold `locale=da`. Det afprøvede `curl`-opslag gav HTTP 403; browseren kunne læse JSON. Hvis gatewayen ikke kan bruges, registrer udfaldet og slå nummeret op i den offentlige [CVR-visning](https://datacvr.virk.dk/). Gatewayen er websidens adgang til data og kan ændre sig. Erhvervsstyrelsens [system-til-system-adgang](https://erhvervsstyrelsen.dk/kom-godt-igang-med-elasticSearch) er en særskilt adgangsvej, der kræver bruger-ID og adgangskode.
2. Kontrollér `stamdata.cvrnummer` mod det søgte nummer. Læs `stamdata.navn`, `status`, `startdato`, `ophoersdato` og `udvidedeOplysninger.binavne`. På CVR.dk findes binavne under »Udvidede virksomhedsoplysninger«; brug også »Fold ud«, når den vises. Gengiv navne og status som i brugerfladen (`NORMAL` → »Normal«, `OPLØSTEFTERFUSION` → »Opløst efter fusion«). Datoerne gemmes som ISO-datoer og binavne i kildens rækkefølge. `stamdata.virkningsdato` var tom for alle 21. Gateway og brugerflade stemte overens og har samme registerophav.
3. Registrer resultatet i kandidatlisten og URL, opslagstid og udfald i kilderegisteret. Opslagene er læsning; CSV-filerne er de eneste data, der ændres ved registreringen. Hele JSON-svar gemmes ikke: de rummer bl.a. person-, kontakt- og regnskabsoplysninger uden betydning for denne kontrol. Gem det seneste gyldige resultat ved genopslag; registrer fejl som et særskilt udfald frem for at erstatte belagte værdier.
4. Åbn »Registreringshistorik« ved et konkret fusionsspor. Brug teksten »Gennemførelse af fusion eller spaltning«, og hold datoen ved registreringsteksten adskilt fra datoen, hvor teksten siger, at selskabet blev opløst. CVR's »Historiske stamdata« kan bruges til at kontrollere, hvilket navn et fortsættende selskab havde på det tidspunkt.

Fusionshistorikken i S052–S055 dokumenterer, at NKE-Elnet fusionerede med Cerius, at NK-Vejlys fusionerede med NK-Service, og at både NK-Service og Sorø Forsyningsservice fusionerede med CVR 26863902. Den viser ikke, hvilke anlæg og ejendomme der overgik. FITs eventuelle juridiske opløsning følges op særskilt.

Underagenten `cvr_review` påpegede, at den første aflæsning sprang registrerede binavne over. Alle 20 opslag blev gentaget med kontrol af binavne, og gatewayens fulde navnelister blev afstemt mod visningen for alle 21. Reviewet understregede, at et vist navn på en ophørt post ikke er et aktivt selskabsnavn, og at ophørsdato og registreringstekstens dato skal holdes adskilt. Reviewet fandt derefter ingen væsentlige mangler i den afgrænsede stamdatakontrol. Cerius er alene et opfølgningsspor for den tidligere NKE-portefølje; Fors og KLAR Forsyning er kontekst for FIT.

## NK-Forsyning og Næstved Forsyning

**Stiftelse.** CVR-opslaget 8. november 2026 viser, at NK-Forsyning A/S (`28118465`) stiftede det særskilte selskab Næstved Forsyning A/S (`46837592`). CVR's meddelelse 40115283 angiver 8. oktober 2026 som stiftelsesdato, virkningsdato og seneste vedtægtsdato. Offentliggørelsesdatoen i CVR er også 8. oktober 2026 (S045, S095).

**Legalt ejerskab.** CVR viser `28118465` med 100 % af kapitalen og 100 % af stemmerettighederne i `46837592` fra 8. oktober 2026. Ændringsdatoen er 8. oktober 2026, og der vises ingen slutdato. CVR viser samtidig Næstved Kommune som legal ejer af `28118465` med 100 % af kapitalen og stemmerettighederne fra 30. juni 2009, som også er den viste ændringsdato (S095–S096).

**Navn og drift.** Kommunen omtalte 9. oktober 2026 et planlagt navneskift omkring årsskiftet i forbindelse med NK-Forsynings udtræden af Envafors. Meddelelsen angiver ikke forsyningsselskabets CVR. Ved opslaget 8. november hed `28118465` fortsat NK-FORSYNING A/S i CVR (S016, S096). Formålet for `46837592` omfatter administrations- og driftsydelser til koncernens øvrige selskaber. Formålet og meddelelserne giver ikke belæg for en gennemført udtræden eller overførsel af konkrete aktiver og driftsroller (S014–S016, S045). `46837592` står fortsat uafklaret i ejendoms- og anlægssporene.

**Gentagelse og review.** Åbn `46837592` i CVR, læs »Registreringshistorik« → »Nye selskaber« og »Ejerforhold« → »Legale ejere«, og følg ejerlinket for at afstemme ejerens CVR. Den ældre ejerliste i gatewayens stamdatasvar var tom, selv om enhedsvisningen viste den legale ejer. Brug derfor enhedsvisningen til ejerandelen; de to visninger har samme registerophav. Underagenten `naestved_review` kontrollerede stiftelse, ejerlink og ejerandel direkte i CVR og bekræftede skellet mellem det dokumenterede ejerskab, det varslede navneskift og de åbne spørgsmål om aktiver og drift. Kilderegisteret angiver de konkrete URL'er og opslagstider.

## Afgrænsning af ejendomsopslag og anlæg

Vurderingen dækker C001–C021 pr. 8. november 2026. [Kandidatlisten](company_candidates.csv) viser dato, kilde og begrundelse for hvert spor. `omfattet` vælger et søgespor; `fravalgt` gælder denne indsamling og kan ændres ved nyt belæg; `uafklaret` kræver en konkret opfølgning, før sporet kan vælges. Ingen af statusserne er et fund eller et tomt resultat fra et ejendoms- eller anlægsregister.

| Spor | Omfattet | Fravalgt | Uafklaret |
|---|---:|---:|---:|
| Ejendomme | 17 (16 CVR-opslag og én målrettet opfølgning) | 3 | 1 |
| Anlæg | 16 | 3 | 2 |

Gentag vurderingen ved at kontrollere kandidatens CVR og læse kilderne i de to felter med kilde-ID'er. I årsrapporterne ligger de afgørende oplysninger i ledelsesberetning, selskabets egen balance og noter om drift; koncerntal kan ikke bruges som moderselskabets aktiver. Sammenhold dokumentdato, regnskabsperiode og virkning eller registrering, før et forhold beskrives som aktuelt eller historisk. Gem ændrede vurderinger i kandidatlisten og kildeoplysningerne i [kilderegisteret](sources.csv). Denne vurdering er dokumentresearch og ændrer ikke de indsamlede ejendomsrelationer.

- **Ejendomme:** Vælg ét CVR-opslag ved belæg for egen ejendomsaktivitet, direkte teknisk forsyningsrolle eller en historisk teknisk rolle og fusion ind i den omfattede selskabskæde. Det sidste kriterium holder relevante ophørte CVR-numre søgbare. Et sådant opslag undersøger eventuelle ejendomsroller; teknisk drift, lejemål og anlæg på fremmed grund beviser hverken ejerskab eller registreret administration. SK Forsyning og NK-Forsyning har egne grunde og bygninger ifølge deres moderselskabsbalancer (S063, S064). Sorø Forsynings moderselskabsbalance giver ikke samme grundlag (S066).
- **Anlæg:** Vælg et spor ved belæg for direkte teknisk forsyningsaktivitet, fysisk drift, vedligeholdelse eller en relevant kontraktrolle. Følg drift og ejerskab hver for sig, også på fremmed grund. NK-Forsyning har en særskilt vejlysaktivitet. NK-Service oplyser, at selskabet solgte vejlys- og signalaftalen til NK-Forsyning ultimo 2021, før CVR-fusionen i 2022 (S064, S065, S053). Beslutningen om NK-Forsynings udtræden af Envafors daterer ikke gennemførelsen (S014, S015).
- **Cerius:** Brug NKE-Elnets historiske CVR, netudviklingsplan og fusionsoplysninger (S074, S052, S007). Find konkrete BFE-, matrikel- eller anlægsidentifikatorer i NKE-sporet, og efterprøv Cerius' rolle og eventuel overdragelse for hver post. NKE-kortet afgrænser søgningen geografisk; en placering i området dokumenterer ikke NKE-tilknytning. Cerius' øvrige portefølje indgår ikke i indsamlingen.

Underagenten `scope_review` kontrollerede kilderne uafhængigt og afstemte alle 21 beslutninger og deres kildehenvisninger. Reviewet fandt, at SK Forsyning og NK-Forsyning skal med i ejendomssporet på grund af deres egne balancer, og at NK-Forsyning også skal med i anlægssporet på grund af vejlysrollen. Reviewet identificerede den tidligere overdragelse af vejlysaftalen, FITs skel mellem it-/SRO-systemdrift og fysisk drift samt miljøgodkendelsen ved Hovsøvej. Godkendelsen viser to CVR-numre og en særskilt grundejer; Sorø Forsynings rolle og den faktiske aktivitet står åbne (S075). Næstved Forsyning `46837592` er fortsat uafklaret i begge spor. Konkrete ejendomme, anlæg og driftsroller skal valideres i de næste trin.
