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

Friheden til eksekvering ændrer ikke kravene til datakvalitet eller begrænsningerne for interne data og systemer. Formålet er et efterprøveligt datagrundlag, hvor kilder, usikkerheder og kontrol er tydelige.

Kode må ikke køres på Envafors' arbejdscomputere uden den nødvendige godkendelse.

## Principper for datakvalitet

Kilder skal angives med URL og opslagstidspunkt med tidszone. Kildens dokumentdato samt oplysningernes virknings- og registreringsdatoer skal registreres særskilt, når de fremgår. Ukendte datoer og usikre oplysninger skal markeres som ukendte eller usikre.

Originale data skal bevares uændret. Bearbejdede data skal placeres separat.

Ved dataudtræk skal søgeparametre uden adgangsoplysninger, svarstatus, eventuel paginering og henvisning til det bevarede originalsvar registreres. Ingen fund, teknisk fejl, adgangsafslag, delvist resultat, manglende feltværdi og ikke undersøgt er forskellige forhold og må ikke sammenblandes.

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

## Arbejdsproces

Arbejd i små, kontrollerbare trin.

Begynd med at identificere officielle datakilder og forstå deres datastruktur.

Udarbejd derefter en metode til udtræk, validering og transformation.

Afprøv metoden på et enkelt CVR-nummer, før den anvendes på flere selskaber.

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
