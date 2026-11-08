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

## Visuelt datakort

`datakort.html` viser, hvad hver kilde og funktion leverer, og forbinder pilotens CVR, ejendomsrelation og BFE. Det er ét lokalt overblik med links til de eksisterende filer og offentlige kilder. Underagenten `datakort_review` kontrollerede pilotens eksempel, dataflow og skellet mellem indsamlede data og åbne arbejdsspor. Bemærkningerne om CVR-linket og afstemningen i `load_sources()` er indarbejdet.

## Arbejdsproces

Nødvendig offentlig research og lokal eksekvering er tilladt. Væsentlige beslutninger og leverancer reviewes. Arbejdet committes og synkroniseres ved passende milepæle; kildeindeks, kildesvar og genbyggede tabeller hører sammen i samme commit. Begrænsningerne for interne data og systemer gælder fortsat.
