# Ejendomsarkiv i DocuNote

**Envafors · Forslag til pilot · Version 0.1**

Behold den aftalte struktur med juridisk selskab (CVR) og ejendom (BFE). Brug en fælles sagstype **Ejendom** med stamdata og ni standardmapper under hvert BFE. Ejendomssagen skal give medarbejderen adgang til skødet, de gældende aftaler og tilladelser samt relevante tegninger, også når dokumenterne ligger på en fælles sag eller i et fagsystem.

## Standardmapper under hvert BFE

| Mappe | Indhold |
|---|---|
| **01 Ejerskab og registrering** | Skøder, køb og salg, tingbogsattester, matrikelkort, gennemførte udstykninger og arealoverførsler, skelforhold samt daterede BBR-meddelelser og ejendomsdatarapporter. |
| **02 Servitutter og rettigheder** | Servitutter, deklarationer, ledningsrettigheder, vej- og adgangsrettigheder samt relevante rådighedsbegrænsninger. Omfatter både selskabets rettigheder og byrder på ejendommen. |
| **03 Leje, udlejning og brugsaftaler** | Lejekontrakter, grundleje, forpagtning og andre brugsaftaler med tillæg, opsigelser og afleveringsaftaler. Tinglyste lejekontrakter placeres også her. |
| **04 Plan- og byggesager** | Relevante lokalplaner, landzonetilladelser, byggetilladelser, dispensationer, færdigmeldinger og ibrugtagningstilladelser. Ansøgninger og væsentlig korrespondance følger byggesagen eller plansagen. |
| **05 Miljø, jord og forsyningstilladelser** | Miljøgodkendelser, indvindings- og udledningstilladelser, jordforureningsundersøgelser, jordhåndtering samt myndighedstilsyn, påbud og opfølgning på miljøvilkår. |
| **06 Bygninger, anlæg og tegninger** | Gældende situationsplaner og tegninger, dokumentation for det udførte anlæg, tekniske beskrivelser, tilstandsrapporter, energimærker og væsentlig afleveringsdokumentation. |
| **07 Drift og vedligehold** | Driftsvejledninger, serviceaftaler, garantier, eftersyn, vedligeholdelsesplaner og væsentlig servicehistorik. Henvisning til driftssystemet, hvor materialet vedligeholdes dér. |
| **08 Forsikring og skader** | Ejendomsspecifik dækningsdokumentation, forsikringsvurderinger, skadesager med bilag og afgørelser samt henvisninger til fælles policer. |
| **09 Vurdering, skatter og ejendomsøkonomi** | Ejendomsvurderinger, vurderingsklager, ejendomsskatter, ejendomsrelaterede afgifter og særlige hæftelses- eller finansieringsdokumenter. Henvisning til økonomisystemet for løbende bogføring. |

- **Lad dokumenterne følge sagen.** En landzonetilladelse til udstykning hører til i 04. Dokumentation for den gennemførte matrikulære ændring hører til i 01. Den samlede tingbogsattest ligger i 01, og den enkelte servitut ligger i 02.
- **Bevar historikken ved emnet.** Behold en erstattet tilladelse som et selvstændigt dokument. Registrér den nye afgørelse, hvilken afgørelse den erstatter, og hvornår den nye gælder, hvis det er kendt.
- **Opret undermapper efter behov.** Et større anlæg kan få undermapper efter bygning eller anlæg under 06. Brug kun **99 Til afklaring** under indlæsning af ældre materiale, og udpeg en ansvarlig for at få dokumenterne placeret.

## Stamdata på ejendomssagen

| Felt | Udfyldelse |
|---|---|
| **BFE og selskab/CVR** | Genbrug den eksisterende BFE- og selskabstilknytning. |
| **BFE-type** | Hent fra kilden, hvis muligt. Samlet fast ejendom, ejerlejlighed eller bygning på fremmed grund. |
| **Beliggenhed og matrikler** | Genbrug officiel beliggenhedsadresse og matrikelnummer med ejerlav, hvor kilden findes. Understøt flere matrikler under samme BFE. Brug kortreference, hvis beliggenhedsadressen er upraktisk i felten. |
| **Kendenavn** | Angiv det navn, medarbejderne bruger, fx navnet på en pumpestation eller et vandværk. |
| **Selskabets relation til ejendommen** | Angiv ejer, lejer, rettighedshaver eller driftsansvarlig efter behov. Tilføj datoer og eventuel ejerandel, hvor relevant. Angiv den juridiske ejer særskilt, hvis ejendommen ejes af en anden. Ved salg afsluttes ejerrelationen, mens BFE fortsat identificerer ejendommen. |
| **Ejendomsansvarlig** | Angiv den rolle, der holder oplysningerne ajour. |
| **Kilde og opdatering** | Registrér kilde og seneste import eller kontrol for oplysninger, som skal holdes ajour. |

Foreslåede manuelle felter ved oprettelse er **kendenavn, selskabets relation og ejendomsansvarlig**. Tilføj anvendelse, arealer, BBR- og anlægs-ID, GIS-reference og særskilt driftsansvarligt selskab, hvis der er behov i søgning eller opfølgning. Hvis miljødata indgår, registreres V1/V2-kortlægning og områdeklassificering særskilt med kilde og dato på det relevante areal eller matrikelniveau. [Geodatastyrelsen om BFE](https://admin.gst.dk/ansvarsomraader/matrikel-og-ejendomsregistrering/matriklen/bfe-nummer) · [Miljøstyrelsen om kortlægning og områdeklassificering](https://mst.dk/erhverv/rent-miljoe-og-sikker-forsyning/jord/forurenede-grunde/kortlaegning-og-omraadeklassificering)

## Metadata på dokumenter og sager

Brug **titel, dokumentkategori og dokumentdato** som fælles udgangspunkt. Hent selskab og BFE fra sagstilknytningen, hvor opsætningen understøtter det. Brug få dokumentkategorier til søgning på tværs, fx skøde, servitut, lejekontrakt, tilladelse, tegning og forsikringspolice.

På aftaler, policer og tilladelser registreres efter behov status, gyldighed, næste frist, ansvarlig og reference som policenummer eller myndighedens sagsnummer. Registrér hver aftale, police eller tilladelse på dokumentet eller den tilhørende sag, så samme ejendom kan have flere af hver type.

## Fælles dokumenter og fagsystemer

| Situation | Placering og adgang |
|---|---|
| **Police for flere BFE’er eller selskaber** | Gem policen én gang på aftalesagen hos det selskab, der har indgået policen. Ved flere aftaleparter aftales, hvilket selskab der vedligeholder sagen. Registrér de omfattede selskaber og BFE’er, og gør policen findbar via 08 på de relevante ejendomme. Hvis direkte relationer mangler, brug en henvisning med selskab, sagsnummer og policenummer. |
| **Leje eller ledningsret på fremmed grund** | Hvis fremmed grund indgår i arkivet, placeres dokumentet på aftale- eller rettighedssagen hos det selskab, der er juridisk part. Registrér grundens BFE som reference. Har en registreret bygning på grunden eget BFE, registreres det særskilt fra grundens. |
| **Projekt på flere ejendomme eller dokumentation i et fagsystem** | Behold dokumentet på projektsagen eller i fagsystemet, hvor det vedligeholdes. Gør gældende tilladelser, tegninger og driftsdokumentation findbare fra de relevante BFE’er via en direkte henvisning til sagen, dokumentet eller anlægget. |

## Pilot i DocuNote

Afprøv sagstypen på 5–10 forskellige ejendomme, fx en administrationsbygning, et større teknisk anlæg, en pumpestation og et ubebygget areal. Brug konkrete dokumenter til at teste følgende arbejdsgange.

1. **Fælles police.** Kan en medarbejder med relevant adgang finde én gældende police fra hvert omfattet BFE, også på tværs af selskaber?
2. **Erstattet tilladelse.** Kan medarbejderen se den gældende afgørelse og dens historik? Næstved Kommunes landzonetilladelse fra 2025 til en NK-Spildevand-pumpestation erstattede en tidligere tilladelse på samme placering. [Næstved Kommunes afgørelse](https://www.naestved.dk/media/cxbdf4rm/2025-03-08_4_sneslevvej_41_4250.pdf)
3. **Ledningsret på fremmed grund.** Kan medarbejderen finde aftalen ud fra både det juridiske selskab og den berørte grunds BFE?

Bed administratoren demonstrere, hvordan mapper og metadata knyttes til sagstypen, hvilke eksisterende aftale- og projektsager der kan genbruges, og hvordan henvisninger og adgang virker på tværs af BFE’er. Aftal i piloten, hvem der ajourfører data og følger op på frister. IntraNote beskriver sagstyper med dokumentmapper og metadata samt gemte og delte søgninger. Den konkrete kobling mellem flere BFE’er og ét dokument skal afprøves i Envafors’ opsætning. [IntraNotes superbrugerkursus](https://www.intranote.dk/arrangementer-for-kunder/docunote-superbruger-kursus) · [IntraNotes vejledning til søgning](https://www.intranote.dk/blog/konsulentchefens-tips-til-sogning)

## Inspiration fra praksis

- **Boligflow** dokumenterer fælles standardmapper, som kan sættes op særskilt for selskaber, ejendomme, lejemål og lejeforhold. Det viser, hvordan en ejendomsskabelon kan genbruges på tværs af selskaber. [Boligflow om standardmapper](https://support.boligflow.dk/product/koncern/standardmapper)
- **BIOFOS** beskriver en genkendelig mappestruktur i DocuNote og en strukturworkshop. Casen fremhæver kontrakter, anlægsprojekter og miljø- og plandokumenter som relevante områder. [IntraNotes BIOFOS-case](https://www.intranote.dk/inspiration/cases/biofos)
- **Envafors** har allerede brugt DocuNote til aftaler og projektstyring ifølge leverandørens case. Den eksisterende opsætning er et naturligt udgangspunkt for piloten. [IntraNotes Envafors-case](https://www.intranote.dk/inspiration/cases/envafors)
- **Bygningsstyrelsen** anbefaler en ensartet mappestruktur, filnavngivning, metadata og versionering i byggeprojekter. [Bygningsstyrelsens vejledning](https://bygst.dk/byggeri/ikt/vejledning-til-ikt-ydelser-og-implementering/digital-kommunikation-og-etablering-af-kommunikationsplatform/)
