# AGENTS.md

## Projektets formål

Projektet skal kortlægge og kvalitetssikre oplysninger om ejendomme og anlæg relateret til Envafors.

På længere sigt skal resultaterne kunne understøtte dokumentstruktur og integration med DocuNote.

Første fase omfatter alene indsamling, dokumentation og validering af offentligt tilgængelige data.

## Arbejdsmiljø og sikkerhed

LLM-assisteret arbejde foregår på en Mac Mini, der er adskilt fra Envafors' IT-miljø.

Ingen interne, fortrolige eller ikke-godkendte virksomhedsdata må indføres i dette miljø, repoet eller eksterne LLM-tjenester.

Der må ikke automatisk udføres scripts, shellkommandoer, API-kald eller dataudtræk. Agenten må researche offentlige kilder, analysere dokumentation og udarbejde forslag, men al egentlig eksekvering og dataindsamling skal udføres manuelt af brugeren.

Kode må ikke køres på Envafors' arbejdscomputere uden den nødvendige godkendelse.

## Principper for datakvalitet

Kilder skal angives med URL og dato. Usikre oplysninger skal markeres som usikre.

Originale data skal bevares uændret. Bearbejdede data skal placeres separat.

Enhver transformation skal kunne reproduceres og efterprøves.

Ingen oplysninger må opfindes, udfyldes ved gæt eller behandles som verificerede alene på baggrund af en LLM's vurdering.

Manglende resultater må ikke automatisk fortolkes som dokumentation for, at der ikke findes relevante ejendomme.

## Udviklingsprincipper

Foretræk den enkleste løsning, der opfylder behovet.

Undgå tredjepartsafhængigheder, frameworks og installationer, medmindre der er dokumenteret et konkret behov.

Windows 11 uden installation af yderligere programmer er målmiljøet for eventuel fremtidig anvendelse. MacOS er det primære udviklingsmiljø.

CSV og JSON foretrækkes som udvekslingsformater.

Agenten skal fremlægge kommandoer og kode til manuel gennemgang før eksekvering og forklare deres input, output, eventuelle sideeffekter og fejlmuligheder.

## Arbejdsproces

Arbejd i små, kontrollerbare trin.

Begynd med at identificere officielle datakilder og forstå deres datastruktur.

Udarbejd derefter en metode til udtræk, validering og transformation.

Afprøv metoden på et enkelt CVR-nummer, før den anvendes på flere selskaber.

Hold research, rådata, transformationer og kvalitetssikring tydeligt adskilt.

Enhver endelig leverance skal ledsages af en beskrivelse, der gør det muligt for brugeren selvstændigt at gentage og kontrollere processen.

## Begrænsning

Projektet må ikke udvikle integrationer til Envafors' interne systemer uden særskilt godkendelse. Offentlige ejendomsdata er et foreløbigt kortlægningsgrundlag, ikke et autoritativt register over alle Envafors' faciliteter.
