# Genskab datagrundlaget i Excel på Windows 11

Brug Excel til at importere, forme og kontrollere data. Værktøjet hedder **Power Query** og ligger under **Data → Hent data**. I editorens liste **Anvendte trin** kan du klikke på hvert trin og se, hvordan tabellen ændrer sig. Du kan begynde med ét JSON-svar fra browseren. Det korte script `Get-Labs.ps1` kan bruges til at hente mange Labs-svar, hvis virksomheden godkender det. [Microsofts vejledning til Power Query](https://support.microsoft.com/en-us/excel/about-power-query-in-excel)

Opret arbejdsbogen og CVR-listen på virksomhedens side. Fastlæg afgrænsningen med virksomhedens egne oplysninger og offentlige opslag. Brug fx CVR's registreringshistorik til at finde direkte forgængere. Gem de offentlige kildesvar og virksomhedens kontrolnoter på et godkendt drev. Notér CVR, kilde-URL, opslagstid med tidszone, udfald og eventuelt filnavn for hvert opslag. Ved sammenligning med et andet udtræk bruges kun data og et miljø, som virksomheden har godkendt.

## Start med ét Labs-svar

1. Find et selskab i CVR. Hvis SK Vand indgår i dit udsnit, kan du prøve CVR `27736033`. Åbn [Labs-svaret for SK Vand](https://api.labs.matriklen.dk/CvrEjerskaber?cvr=27736033), og gem selve JSON-svaret som `27736033.json`. CVR fremgår af URL'en og bruges som filnavn. Kontrollér i VS Code, at filen indeholder et JSON-objekt med listerne `ejer` og `administrerer`.
2. I Excel vælger du **Data → Hent data → Fra fil → Fra JSON**. Åbn filen i Power Query-editoren. Hvis Excel allerede har foldet noget ud, kan du se råstrukturen i det første trin under **Anvendte trin**. Fjern de senere, automatisk foreslåede trin for at følge vejledningen her.
3. Gør JSON-objektet til en tabel med **Into Table**, hvis knappen vises. Alternativt kan du vise formellinjen under **Vis → Formellinje**, trykke på **fx** og sætte `Record.ToTable(...)` omkring referencen til forrige trin. Hvis Excel indsætter `= Kilde`, skriver du `= Record.ToTable(Kilde)`. Tabellen har nu to rækker og kolonnerne `Name` og `Value`. Omdøb `Name` til `role`.
4. Vælg **Tilføj kolonne → Brugerdefineret kolonne**. Navngiv kolonnen `cvr` og skriv det søgte CVR i anførselstegn, fx `"27736033"`. Tilføj også `antal` med formlen `List.Count([Value])`. Afstem antallet med begge lister. Gem denne forespørgsel som `LabsLister`, så også et svar med to tomme lister er synligt.
5. Højreklik på `LabsLister` og vælg **Reference**. Navngiv den nye forespørgsel `LabsRelationer`. Filtrér `antal` til over nul. Brug dobbeltpilen i `Value` og vælg **Udvid til nye rækker**. Du får én række pr. observation. `cvr` og `role` følger med på hver række.
6. Brug dobbeltpilen i `Value` igen og vælg `bfe`, `status`, `virkningFra`, `faktiskEjerandel` og `tinglystEjerandel`. Fjern præfiks på feltnavnene, hvis Excel tilbyder det. De to andele er hver et lille objekt. Udvid hver for sig, og behold et særskilt kolonnenavn til hver tæller og nævner. Sæt CVR, BFE og den oprindelige dato til tekst, og fjern et automatisk datatype-trin, hvis Excel har omskrevet dem.
7. Vælg **Luk og indlæs**. Tæl relationerne efter rolle, og sammenhold dem med `LabsLister`. Behold alle rækker, også når et BFE optræder flere gange. Behold `virkningFra` som kildens dato. Brug et særskilt BFE-opslag, hvis du skal kende overtagelses- eller tinglysningsdatoen.

Brug et svar med poster til første udfoldning, så Excel kan vise felterne. Afprøv derefter et gyldigt tomt svar i `LabsLister`. Det har to tællinger på nul og giver ingen relationer. Et manglende opslag, et afslag eller et svar med forkert struktur har sit eget udfald i loggen. [JSON-import i Excel](https://support.microsoft.com/en-us/excel/import-data-from-data-sources-power-query?redirectsourcepath=%252fen-us%252farticle%252fha104019829) · [Udfoldning i Power Query](https://support.microsoft.com/en-us/excel/work-with-a-list-record-or-table-structured-column-power-query)

### Bevar forskellen på udeladt felt, null og nul

Ved sammenligning med et andet udtræk skal du registrere andelens tilstand **før** trin 6. Tilføj en brugerdefineret kolonne, mens `Value` stadig indeholder én observation pr. række.

```powerquery
let
    felt = "tinglystEjerandel",
    andel = Record.FieldOrDefault([Value], felt, null)
in
    if not Record.HasFields([Value], felt) then "missing"
    else if andel = null then "null"
    else if Value.Is(andel, type record)
        and Record.HasFields(andel, {"tæller", "nævner"})
        and Value.Is(andel[tæller], type number)
        and Value.Is(andel[nævner], type number)
        and andel[tæller] >= 0 and andel[nævner] > 0
        and Number.RoundDown(andel[tæller]) = andel[tæller]
        and Number.RoundDown(andel[nævner]) = andel[nævner]
    then "present" else "invalid"
```

Giv kolonnen navnet `registered_share_state`. Gentag med `faktiskEjerandel` og navnet `actual_share_state`. En andel på 0/1 får tilstanden `present`. Undersøg `invalid` i originalen, og behold markeringen til gennemgang. Hvis en ugyldig andelsværdi hindrer udfoldning, kan den sættes til `null` i arbejdstrinnet efter markeringen. Hvis feltvælgeren i trin 6 mangler et felt, kan du først tilføje en brugerdefineret kolonne med `Record.SelectFields([Value], {"bfe", "status", "virkningFra", "faktiskEjerandel", "tinglystEjerandel"}, MissingField.UseNull)` og udfolde den i stedet. Behold tilstandene fra trinnet før dette, så et udeladt felt fortsat kan skelnes fra `null`. [Microsofts vejledning til Record.HasFields](https://learn.microsoft.com/en-us/powerquery-m/record-hasfields)

## Hent flere Labs-svar

Gem ét svar pr. CVR i en mappe, som kun rummer Labs-svar fra samme udtræk. Browseren kan bruges til hvert opslag. Ved mange opslag kan du lave en UTF-8-fil i VS Code med overskriften `cvr` og ét ottecifret CVR pr. linje. Kør derefter det godkendte hentetrin fra PowerShell i mappen med scriptet.

```powershell
powershell.exe -NoProfile -File .\Get-Labs.ps1 -ScopeCsv .\scope.csv -OutputFolder .\run-01
```

Vælg en ny resultatmappe for hver kørsel. Scriptet gemmer svarbytes i `labs` og skriver `lookups.csv` med URL, tidspunkt, HTTP-status, udfald og eventuelt filnavn og SHA-256. `downloaded` betyder HTTP 200 og en gemt fil. I Power Query kontrollerer du svarstrukturen og tæller posterne. Et afslag eller en fejl bliver registreret, og scriptet fortsætter med de øvrige CVR'er. Ved mindst én fejl returnerer det statuskode 2. Sammenhold loggen med CVR-listen, før du bruger et udtræk.

I Excel vælger du **Data → Hent data → Fra fil → Fra mappe → Transformér data**. Filtrér til filtypen `.json` og den præcise mappesti, hvis visningen også har fundet undermapper. Behold `Name` og `Content`. Tilføj `cvr` med `Text.BeforeDelimiter([Name], ".")`, og afstem filnavnene med henteloggen.

Tilføj kolonnen `Lister` med `Record.ToTable(Json.Document([Content]))`. Udvid `Lister` til `Name` og `Value` med præfiks, så filnavnets `Name` bevares. Omdøb `Lister.Name` til `role` og `Lister.Value` til `Value`. Kontrollér, at hvert svar har præcis rollerne `ejer` og `administrerer`, og at begge værdier er lister. Fortsæt med optællingen i trin 4 ovenfor. Du har allerede kolonnen `cvr`. Hvis **Fra JSON** mangler, kan du også bruge denne metode på en mappe med én fil. Ved nye kildesvar i samme mappe kan **Data → Opdatér alle** genbruge trinnene. Gem det tidligere udtræk særskilt, hvis det skal kunne genskabes. [Microsofts vejledning til mappeimport](https://support.microsoft.com/en-gb/excel/import-data-from-a-folder-with-multiple-files-power-query)

## Virk og CVR

Ét gateway-svar kan bruges til både virksomhedsoplysninger og P-enheder. Åbn `https://datacvr.virk.dk/gateway/virksomhed/hentVirksomhed?cvrnummer=<CVR>&locale=da` i browseren. Gem JSON midlertidigt i en særskilt CVR-mappe på et godkendt drev. Kontrollér `stamdata.cvrnummer` mod det søgte nummer. Gatewayen kan fungere i browseren, selv når et direkte opslag fra et andet værktøj giver adgangsafslag. Fulde svar kan indeholde flere oplysninger end dem, der bruges i arbejdsbogen.

- **Virksomheder.** Importér via **Fra JSON** for én virksomhed. Behold trinnet med det oprindelige objekt. Ved flere filer bruges samme mappemetode som for Labs, men den brugerdefinerede kolonne `Svar` har formlen `Json.Document([Content])`. Behold kildesporet pr. fil. Åbn eller udvid `stamdata`, og vælg CVR, navn, status, startdato og ophørsdato. Binavne ligger under `udvidedeOplysninger.binavne`. Behold listen, eller saml dens værdier med `Text.Combine([binavne], "|")` for at sammenligne med projektets binavne.
- **P-enheder.** Lav en selvstændig forespørgsel fra det samme oprindelige svar. Gå til `produktionsenheder`. Kontrollér og tæl både `aktiveProduktionsenheder` og `ophoerteProduktionsenheder`. Gør de to lister til separate rækker, som ved Labs. Fra en mappe kan du gøre det med `Record.ToTable(Record.SelectFields([Svar][produktionsenheder], {"aktiveProduktionsenheder", "ophoerteProduktionsenheder"}))`. Behold navnet på listen som status, og udvid listens poster til rækker. Hver post har sit eget `stamdata` med CVR, P-nummer, navn, adresse og datoer. Udvid `hovedbranche` for branchekode og titel. Kontrollér P-postens CVR mod opslaget. Brug `active` og `closed` som status ved sammenligning med projektets tabel.
- **Legale ejere.** Brug den offentlige CVR-visning `https://datacvr.virk.dk/enhed/virksomhed/<CVR>`. Åbn **Ejerforhold** og **Ophørt ejerskab**, og kontrollér ejerens CVR via ejerlinket. Registrér kapital- og stemmeandele og deres perioder manuelt. Gatewayen kan udelade ejerdata, der er synlige i disse paneler. Hvis gatewayen ikke kan læses, kan virksomhed og P-enheder også kontrolleres i enhedsvisningen. Åbn de ophørte poster særskilt og notér udfaldet for hver visning. [Eksempel på en offentlig CVR-visning](https://datacvr.virk.dk/enhed/virksomhed/27736033)

## Sammenlign i Excel

Sammenhold CVR-lister, datoer og opslagsudfald først. En manglende kilde skal gennemgås som sådan. Hvis sammenligningsfilen er en CSV, brug **Fra tekst/CSV**, vælg filens kodning og skilletegn, og behold identifikatorer og originale datoer som tekst. Vælg de samme felter, kolonnenavne og typer i de to forespørgsler. Brug samme repræsentation for tomme celler, mens andelstilstandene bevares. I projektets relationstabel hedder `status` og `virkningFra` fx `source_status` og `virkning_fra_original`. Andelens tæller og nævner hedder `actual_share_numerator` og `actual_share_denominator` for faktisk andel, og `registered_share_numerator` og `registered_share_denominator` for tinglyst andel. Brug CVR og P-nummer til at undersøge en P-enhed. For ejendomsrelationer bevares også rolle, status, virkningsdato og andele.

Hvis der kan forekomme dubletter, skal sammenligningen tælle dem. Giv rækker fra virksomhedens udtræk to brugerdefinerede talkolonner med værdierne `1` og `0`, fx `virksomhed_antal` og `reference_antal`. Brug `0` og `1` i den anden tabel. Vælg **Tilføj forespørgsler som ny**, og vælg derefter **Gruppér efter → Avanceret**. Gruppér efter alle sammenligningsfelter, og summér de to talkolonner. Tilføj `[virksomhed_antal] <> [reference_antal]`, og filtrér til sande værdier. Åbn de offentlige kilder for at afgøre hver forskel. [Tilføj forespørgsler](https://support.microsoft.com/en-us/excel/append-queries-power-query) · [Gruppér rækker](https://support.microsoft.com/en-us/excel/group-rows-of-data-power-query)

Kontrollér anlæg og driftsroller særskilt. Find fx anlæggets id i Jupiter eller PULS, og følg matriklen til BFE. Registrér hvilken rolle den konkrete kilde viser.

Excel-trinnene er gennemgået uafhængigt mod Microsofts vejledning og kildernes struktur. Hentescriptet er afprøvet med PowerShell 7 på Mac med et udfyldt svar, et tomt svar og et simuleret afslag. Pilottrinnet på virksomhedens Windows-maskine skal bekræfte menuer, adgang og kørsel.
