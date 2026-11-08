# AGENTS.md

## Projektets formål

Projektet skal kortlægge og kvalitetssikre oplysninger om ejendomme og anlæg relateret til Envafors.

På længere sigt skal resultaterne kunne understøtte dokumentstruktur og integration med DocuNote.

Første fase omfatter alene indsamling, dokumentation og validering af offentligt tilgængelige data.

Scope i første fase er data. Opsætning af DocuNote, mappestruktur til dokumenthåndtering og integrationer indgår ikke i denne fase.

## Arbejdsmiljø og sikkerhed

LLM-assisteret arbejde foregår på en Mac Mini, der er adskilt fra Envafors' IT-miljø.

Ingen interne, fortrolige eller ikke-godkendte virksomhedsdata må indføres i dette miljø, repoet eller eksterne LLM-tjenester.

Agenten må selvstændigt udføre nødvendig research og dataindsamling fra offentlige kilder, herunder køre scripts, shellkommandoer, API-kald og dataudtræk, hente og gemme rådata samt bearbejde og kontrollere data i projektets adskilte arbejdsmiljø. Det kræver ikke manuel eksekvering eller godkendelse af hver enkelt kommando.

Brugeren er den eneste person, agenten må kontakte. Hvis offentlige kilder ikke afklarer et spørgsmål, registrerer agenten hullet og tager det om nødvendigt op med brugeren.

Friheden til eksekvering ændrer ikke kravene til datakvalitet eller begrænsningerne for interne data og systemer. Formålet er et efterprøveligt datagrundlag, hvor kilder, usikkerheder og kontrol er tydelige.

Kode må ikke køres på Envafors' arbejdscomputere uden den nødvendige godkendelse.

## Principper for datakvalitet

Kilder skal angives med URL og opslagstidspunkt med tidszone. Kildens dokumentdato samt oplysningernes virknings- og registreringsdatoer skal registreres særskilt, når de fremgår. Ukendte datoer og usikre oplysninger skal markeres som ukendte eller usikre.

Bevar kun originalsvar, der konkret bruges som kildebelæg eller er nødvendige for at gentage den valgte bearbejdning. De bevarede svar skal være uændrede; bearbejdede data skal placeres separat. Der er ikke et generelt krav om at arkivere alle fund eller opslag.

Registrer kilde-URL med relevante søgeparametre, hentetid og reference til bevaret indhold i et fælles kildeindeks. Suppler kun med andre metadata, hvis de har et konkret kontrolformål. Ingen fund, teknisk fejl, adgangsafslag, delvist resultat, manglende feltværdi og ikke undersøgt er forskellige forhold og må ikke sammenblandes; det kræver ikke en arkivfil for hvert udfald.

Enhver transformation skal kunne reproduceres og efterprøves.

Ingen oplysninger må opfindes, udfyldes ved gæt eller behandles som verificerede alene på baggrund af en LLM's vurdering.

Hver væsentlig oplysning i det endelige datagrundlag skal kunne spores til en konkret kilde eller en dokumenteret transformation. Foreløbige kandidater og antagelser skal holdes adskilt fra kontrollerede oplysninger. En kildebaseret oplysning er ikke automatisk uafhængigt bekræftet; flere visninger af samme register tæller ikke som uafhængige kilder.

Gældende og historiske forhold samt ejerskab, administration og drift skal holdes adskilt. Modstridende oplysninger skal bevares og undersøges; de må ikke stiltiende overskrives. Et teknisk vellykket udtræk dokumenterer ikke i sig selv korrekthed eller fuldstændighed.

Brug stabile identifikatorer som CVR, P-nummer og BFE til sammenkobling, når de findes. Navne- og adressesammenfald er søgespor og må ikke alene afgøre identitet eller tilknytning.

Manglende resultater må ikke automatisk fortolkes som dokumentation for, at der ikke findes relevante ejendomme.

## Udviklingsprincipper

Foretræk den enkleste løsning, der opfylder behovet.

Undgå tredjepartsafhængigheder, frameworks og installationer, medmindre der er dokumenteret et konkret behov.

Windows 11 uden installation af yderligere programmer er målmiljøet for eventuel fremtidig anvendelse. MacOS er det primære udviklingsmiljø.

CSV og JSON foretrækkes som udvekslingsformater.

Væsentlige udtræks- og bearbejdningsmetoder skal beskrives med input, output, relevante sideeffekter og fejlmuligheder, så de kan gentages og kontrolleres. Beskrivelsen kræver ikke forhåndsgodkendelse af almindelig research eller lokal, reversibel bearbejdning.

## Begrænsning af data og filer

Hver fil i repoet skal have en konkret funktion i den aktuelle opgave: data, der skal bruges, nødvendigt kildebelæg, en aktiv kontrol eller en nødvendig arbejdsinstruktion. At noget er tilgængeligt eller måske kan blive relevant er ikke tilstrækkeligt. Undlad at hente eller gemme det uden et begrundet behov.

Foretræk én gældende fil pr. kilde/enhed og få fælles tabeller eller indeks. Gem ikke automatisk HTTP-headers, fejlede forsøg, mapper pr. kørsel, kodekopier, profiler eller flere udgaver af samme afledte data. Brug Git til historik over committede versioner. Midlertidige svar mellem commits er ikke et arkiv.

Fjern overflødige artefakter, og ret henvisninger, når strukturen forenkles. Generelle metodeforbehold beskrives ét sted; kontrollister skal primært vise konkrete fund. Nye tabeller og eksportformater oprettes først, når der er data og en konkret anvendelse.

## Arbejdsproces

Arbejd i små, kontrollerbare trin.

Begynd med at identificere officielle datakilder og forstå deres datastruktur.

Ved gentagne opslag: Se først efter et direkte, struktureret kildesvar, fx JSON, CSV eller et officielt dataudtræk. Foretræk en dokumenteret adgangsvej. Hvis kildens offentlige webside allerede henter de relevante felter samlet, så undersøg, om det samme svar kan læses direkte med fx CVR, P-nummer eller BFE som parameter. Brug den vej til de afgrænsede opslag, når adgangen er tilladt, og svaret er afprøvet. Brug enkeltvisninger til stikprøver og til oplysninger, som svaret ikke dækker. Se [afprøvede adgangsveje](README.md#direkte-kildesvar).

Udarbejd derefter en metode til udtræk, validering og transformation.

Afprøv metoden på et enkelt CVR-nummer, før den anvendes på flere selskaber. Kontrollér sammenhængen mellem søgt identifikator og svar, svarstruktur og nødvendige felter. Afklar, om svaret er opdelt i sider, hvis det har betydning for dækningen. Registrer afslag og fejl særskilt, og brug en anden tilladt adgangsvej ved behov.

Hold research, rådata, transformationer og kvalitetssikring tydeligt adskilt.

Enhver endelig leverance skal ledsages af en beskrivelse, der gør det muligt for brugeren selvstændigt at gentage og kontrollere processen.

Beskriv dækningsgrad i forhold til en eksplicit afgrænsning, de undersøgte kilder og en bestemt dato. Oplys kendte huller, usikkerheder og udestående kontroller.

## Git og synkronisering

Gem arbejdet i sammenhængende commits ved afsluttede delopgaver og milepæle. Synkroniser med projektets konfigurerede remote, når det er hensigtsmæssigt, og før aflevering eller overdragelse af afsluttet arbejde. Almindelig commit og push af opgavens ændringer kræver ikke særskilt bekræftelse fra brugeren. Undgå tomme commits og unødige commits for hver lille rettelse.

Kontroller arbejdsmappe, aktuel branch, upstream og remote, før der synkroniseres. Hent remote-status ved opgavestart, når den er relevant, og før synkronisering. Integrer nye remoteændringer med fast-forward, hvor det er muligt. Ved divergens skal ændringerne integreres uden at omskrive publiceret historik eller miste brugerens arbejde.

Gennemgå ændringerne og udfør de relevante kontroller før commit. Stage kun filer, der hører til opgaven, herunder relevante data, kode, plan og kontrolresultater. Bevar eksisterende brugerændringer; brug ikke force-push eller destruktiv reset som rutinemæssig synkronisering.

Efter push skal det kontrolleres, at branch og upstream peger på samme commit, og at arbejdsstatus er som forventet. Oplys den synkroniserede commit og eventuelle resterende lokale ændringer. Hvis synkronisering ikke lykkes, skal årsagen og det udestående arbejde fremgå; arbejdet må ikke beskrives som synkroniseret.

## Review fra underagenter

Indhent uafhængigt review fra mindst én underagent ved væsentlige beslutninger og løsninger, før de lægges til grund for det endelige datagrundlag. Det gælder eksempelvis afgrænsning af selskaber og kilder, datamodel, fortolkning af historik, sammenkobling af poster, dubletbehandling og valideringsmetode.

Indhent også review af væsentlige ændringer i projektets instruktioner og før en dataleverance betegnes som endelig. Rutinemæssige opslag og mindre, reversible arbejdstrin kræver ikke særskilt review.

Review skal udfordre antagelser og kontrollere, om konklusionerne understøttes af kilderne. Registrer væsentlige bemærkninger, hvordan de er håndteret, og eventuelle udeståender. Underagenters enighed erstatter ikke kildebelæg eller datavalidering. Hvis review ikke er tilgængeligt, må research fortsætte, men den berørte beslutning eller leverance skal stå som foreløbig.

## Begrænsning

Projektet må ikke udvikle integrationer til Envafors' interne systemer uden særskilt godkendelse. Offentlige ejendomsdata er et foreløbigt kortlægningsgrundlag, ikke et autoritativt register over alle Envafors' faciliteter.
