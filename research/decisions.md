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

Underagenten `pilot_scope_review` gennemgik den opdaterede plan for indsamling efter den tekniske pilot. Reviewet førte til, at første runde kun omfatter CVR-numre, der er valgt til ejendomsopslag, at opslagsudfald registreres særskilt fra råsvar, og at relevante anlægskilder skal gennemgås i hver sektor. CVR-afgrænsning og faglig kontrol står fortsat åbne.

## Arbejdsproces

Nødvendig offentlig research og lokal eksekvering er tilladt. Væsentlige beslutninger og leverancer reviewes. Arbejdet committes og synkroniseres ved passende milepæle; kildeindeks, kildesvar og genbyggede tabeller hører sammen i samme commit. Begrænsningerne for interne data og systemer gælder fortsat.

Underagenten `direct_sources_review` gennemgik instruksen om direkte kildesvar og kontrollerede begge adgangsveje mod kilderegisteret. Reviewet førte til, at tilladt adgang blev gjort eksplicit, og at Matriklen Labs-opslaget blev afgrænset til de CVR-numre, der er valgt til ejendomsindsamlingen. Reviewet fandt ingen væsentlige fejl.

## CVR-kontrol af selskabskandidater

Den 8. november 2026 blev C001–C020 kontrolleret i Erhvervsstyrelsens offentlige CVR. Alle 20 opslag gav en entydig CVR-post: 16 med status »Normal« og fire med status »Opløst efter fusion«. C021 (Cerius A/S) er den nytilføjede kandidat og stod også som »Normal«. Dækningen gælder denne navngivne liste på opslagsdatoen. Den siger ikke, om alle relevante selskaber er fundet.

Gentag kontrollen med CVR-numrene fra [kandidatlisten](company_candidates.csv):

1. Start med at åbne gateway-URL'en fra [kilderegisteret](sources.csv) direkte i en browser. Brug samme adresse til gentagne opslag: skift `cvrnummer`, og behold `locale=da`. Det afprøvede `curl`-opslag gav HTTP 403; browseren kunne læse JSON. Hvis gatewayen ikke kan bruges, registrer udfaldet og slå nummeret op i den offentlige [CVR-visning](https://datacvr.virk.dk/). Gatewayen er websidens adgang til data og kan ændre sig. Erhvervsstyrelsens [system-til-system-adgang](https://erhvervsstyrelsen.dk/kom-godt-igang-med-elasticSearch) er en særskilt adgangsvej, der kræver bruger-ID og adgangskode.
2. Kontrollér `stamdata.cvrnummer` mod det søgte nummer. Læs `stamdata.navn`, `status`, `startdato`, `ophoersdato` og `udvidedeOplysninger.binavne`. På CVR.dk findes binavne under »Udvidede virksomhedsoplysninger«; brug også »Fold ud«, når den vises. Gengiv navne og status som i brugerfladen (`NORMAL` → »Normal«, `OPLØSTEFTERFUSION` → »Opløst efter fusion«). Datoerne gemmes som ISO-datoer og binavne i kildens rækkefølge. `stamdata.virkningsdato` var tom for alle 21. Gateway og brugerflade stemte overens og har samme registerophav.
3. Registrer resultatet i kandidatlisten og URL, opslagstid og udfald i kilderegisteret. Opslagene er læsning; CSV-filerne er de eneste data, der ændres ved registreringen. Hele JSON-svar gemmes ikke: de rummer bl.a. person-, kontakt- og regnskabsoplysninger uden betydning for denne kontrol. Gem det seneste gyldige resultat ved genopslag; registrer fejl som et særskilt udfald frem for at erstatte belagte værdier.
4. Åbn »Registreringshistorik« ved et konkret fusionsspor. Brug teksten »Gennemførelse af fusion eller spaltning«, og hold datoen ved registreringsteksten adskilt fra datoen, hvor teksten siger, at selskabet blev opløst. CVR's »Historiske stamdata« kan bruges til at kontrollere, hvilket navn et fortsættende selskab havde på det tidspunkt.

Fusionshistorikken i S052–S055 dokumenterer, at NKE-Elnet fusionerede med Cerius, at NK-Vejlys fusionerede med NK-Service, og at både NK-Service og Sorø Forsyningsservice fusionerede med CVR 26863902. Den viser ikke, hvilke anlæg og ejendomme der overgik. Næstved Forsyning `46837592` og NK-Forsyning `28118465` er to forskellige CVR-poster. Deres indbyrdes relation og FITs tilknytning og opløsningsforløb følges op særskilt.

Underagenten `cvr_review` påpegede, at den første aflæsning sprang registrerede binavne over. Alle 20 opslag blev gentaget med kontrol af binavne, og gatewayens fulde navnelister blev afstemt mod visningen for alle 21. Reviewet understregede, at et vist navn på en ophørt post ikke er et aktivt selskabsnavn, og at ophørsdato og registreringstekstens dato skal holdes adskilt. Reviewet fandt derefter ingen væsentlige mangler i den afgrænsede stamdatakontrol. Cerius er alene et opfølgningsspor for den tidligere NKE-portefølje; Fors og KLAR Forsyning er kontekst for FIT.
