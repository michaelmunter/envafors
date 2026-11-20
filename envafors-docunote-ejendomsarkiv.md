# Ejendomsarkiv i DocuNote

**Envafors · Forslag til pilot · Version 0.2 · 20. november 2026**

Læg ejendomssagen direkte i ejerens selskabsmappe. Brug selskabets registrerede navn og CVR som mappenavn. Begynd sagstitlen med BFE-nummeret, og tilføj kendenavn eller kort adresse, når det er kendt. For hver BFE med en dokumenteret, gældende ejer i arkivet bruges én hovedsag af typen **Ejendom** med ni faste emnemapper. Herfra skal brugeren kunne finde skøde, aftaler, tilladelser og tegninger, også når originalen ligger på en fælles sag eller i et fagsystem.

## Hovedsag, medejere og tidligere ejere

**Gældende** og **historisk** angiver, om selskabet stadig har rollen på den pågældende BFE. **Primær** angiver, hvilken ejer der fører hovedsagen i arkivet. Registrér dette selskabs CVR én gang på hovedsagen. Ved sameje kan en ejer altså være **gældende og ikke-primær**.

| Selskabets forhold til ejendommen | Placering i selskabsmappen |
|---|---|
| Gældende ejer, som fører sagen | Læg BFE-hovedsagen direkte i roden. Ved sameje aftaler de omfattede ejere, hvem der fører sagen. Registrér hver ejers andel på ejerforholdet. |
| Gældende medejer, når en anden ejer fører sagen | Vis en genvej direkte i roden, fx **BFE … · medejer**. Hvis to medejere bytter sagsansvar, bytter hovedsag og genvej plads. Begge ejerforhold er stadig gældende. Ejendommen tæller én gang i den samlede portefølje. |
| Tidligere ejer | Opret **Tidligere ejendomme** ved det første historiske ejerforhold. Vis den tidligere ejers afsluttede sag med egne dokumenter, eller en historisk reference, hvis der kun foreligger registeroplysninger. Tilføj en genvej til den aktuelle hovedsag, når den findes i arkivet. |
| Gældende administrator, lejer, rettighedshaver eller driftsansvarlig | Knyt rollen og dens belæg til BFE. En genvej i roden kan mærkes med rollen, fx **BFE … · lejer**. På fremmed grund uden hovedsag i arkivet peger henvisningen på den relevante aftale- eller rettighedssag. Ejeroversigten medtager alene gældende, dokumenterede ejere. |

Brug **tinglyst adkomst** som udgangspunkt for placering hos den formelle ejer. Vælg først rollen `ejer` og status `gældende` i Matriklen Labs. Sammenhold CVR, BFE og de faktiske og tinglyste ejerandele med det daterede ejendomsopslag. Er andelene forskellige, er den tinglyste andel uoplyst, eller er adkomsten i øvrigt uklar, oprettes en afklaringsopgave med BFE, kilde og ansvarlig i den fælles opfølgning. Det kan gøres, før der findes en hovedsag. Ejendommen medtages i ejerens portefølje, når placeringen er afklaret. [Kontrol af status, andele og datoer](research/udtraekskontrol.md#status-og-andele)

Ved ejerskifte afsluttes den gamle ejerrelation med den dokumenterede dato, hvis den kendes. Den tidligere ejers egne dokumenter bevares hos selskabet. Er den nye ejer omfattet af arkivet, vises den aktuelle hovedsag i den nye ejers rod. Opdatér eksisterende genveje med sagens nummer og kontrollér, at de fører til samme BFE.

**Eksempel med tidligere ejer.** Ejendomsopslaget med virkningstid 20. november 2026 kl. 00.00 CET viste SK Forsyning A/S med faktisk og tinglyst andel 1/1 på BFE 5367067. I Labs var SK Forsynings ejerpost gældende og SK Vands historisk. Alle 15 BFE-numre, der optrådte under to CVR-numre i de 12 undersøgte Labs-udtræk, havde én gældende og én historisk ejerpost. [Projektets kontrol](research/udtraekskontrol.md#status-og-andele) · [Kildeindeks med opslagstider, S273, S349 og S512](research/sources.csv)

```text
SK Forsyning A/S (25797981)
└── BFE 5367067
SK Vand A/S (27736033)
└── Tidligere ejendomme
    └── BFE 5367067 · tidligere ejer → hovedsagen hos SK Forsyning A/S
```

## De ni standardmapper på hovedsagen

| Mappe | Indhold |
|---|---|
| **01 Ejerskab og registrering** | Skøder, køb og salg, tingbogsattester, matrikelkort, gennemførte udstykninger og arealoverførsler, skelforhold samt daterede BBR-meddelelser og ejendomsdatarapporter. |
| **02 Servitutter og rettigheder** | Servitutter, deklarationer, ledningsrettigheder, vej- og adgangsrettigheder samt relevante rådighedsbegrænsninger. Omfatter både selskabets rettigheder og byrder på ejendommen. |
| **03 Brugsaftaler** | Lejekontrakter, grundleje, forpagtning og andre brugsaftaler med tillæg, opsigelser og afleveringsaftaler. Tinglyste lejekontrakter placeres også her. Angiv, om selskabet er lejer eller udlejer. |
| **04 Plan- og byggesager** | Relevante lokalplaner, landzonetilladelser, byggetilladelser, dispensationer, færdigmeldinger og ibrugtagningstilladelser. Ansøgninger og væsentlig korrespondance følger byggesagen eller plansagen. |
| **05 Miljø** | Miljøgodkendelser, indvindings- og udledningstilladelser, jordforureningsundersøgelser, jordhåndtering samt myndighedstilsyn, påbud og opfølgning på miljøvilkår. |
| **06 Teknisk dokumentation** | Gældende situationsplaner og tegninger, dokumentation for det udførte anlæg, tekniske beskrivelser, tilstandsrapporter, energimærker og væsentlig afleveringsdokumentation. |
| **07 Drift og vedligehold** | Driftsvejledninger, serviceaftaler, garantier, eftersyn, vedligeholdelsesplaner og væsentlig servicehistorik. Henvisning til driftssystemet, hvor materialet vedligeholdes dér. |
| **08 Forsikring og skader** | Ejendomsspecifik dækningsdokumentation, forsikringsvurderinger, skadesager med bilag og afgørelser samt henvisninger til fælles policer. |
| **09 Ejendomsøkonomi** | Ejendomsvurderinger, vurderingsklager, ejendomsskatter, afgifter og dokumenter om hæftelser eller finansiering. Gør tinglyst pant findbart fra 01. Henvis til økonomisystemet for løbende bogføring. |

- **Lad dokumenterne følge sagen.** En landzonetilladelse til udstykning hører til i 04. Dokumentation for den gennemførte matrikulære ændring hører til i 01. Den samlede tingbogsattest ligger i 01, og den enkelte servitut ligger i 02.
- **Bevar historikken ved emnet.** Behold en erstattet tilladelse som et selvstændigt dokument. Registrér den nye afgørelse, hvilken afgørelse den erstatter, og hvornår den nye gælder, hvis det er kendt.

### Niveauet under emnemapperne

Enkeltstående dokumenter lægges direkte i emnemappen. Når flere dokumenter hører til samme forløb, samles de i en sagsmappe under emnet eller via en henvisning til en eksisterende sag. Brug de samme navnemønstre på tværs af ejendomme, fx **Tilladelse · emne eller sagsnr.** under 05, **Skadesag · skadenr. eller dato** under 08 og **Vurderingsklage · vurderingsår** under 09. En skatteopgørelse kan ligge direkte i 09, mens en klage med korrespondance og afgørelse får sin egen sagsmappe.

Når samme underinddeling er nødvendig på flere ejendomme, indarbejdes den i den fælles sagsskabelon. I DocuNotes skabelonbibliotek kan der fx ligge en fælles skabelon til besigtigelsesnotater. Den udfyldte fil oprettes ved en besigtigelse. Modtagne skøder, policer og afgørelser journaliseres, når de foreligger. Uafklaret materiale fra indlæsning får en ansvarlig for placeringen.

## Stamdata og ansvar

| Felt | Udfyldelse |
|---|---|
| **BFE, BFE-type og sagsførende CVR** | Identificér ejendommen med BFE og hovedsagen med sagsnummer. Hent BFE-typen fra kilden, fx samlet fast ejendom, ejerlejlighed eller bygning på fremmed grund. Angiv det selskab, som fører sagen efter ejerreglen ovenfor. |
| **Beliggenhed og matrikler** | Genbrug officiel beliggenhedsadresse og matrikelnummer med ejerlav, hvor kilden findes. Understøt flere matrikler under samme BFE. Brug kortreference, hvis beliggenhedsadressen er upraktisk i felten. |
| **Kendenavn, anvendelse og anlæg** | Gør det daglige navn og anvendelsen søgbare, fx administrationsbygning eller ubebygget areal. Knyt relevante anlægs-ID’er eller GIS-referencer til sagen. En BFE kan omfatte flere anlæg, og et anlæg kan berøre flere BFE’er. |
| **Selskabets relation til BFE** | Angiv CVR, rolle, gældende eller historisk status, dokumenterede datoer og kilde med opslagstidspunkt. Registrér faktisk og tinglyst ejerandel hver for sig. En uoplyst andel markeres som ukendt, og en oplyst nulandel bevares som nul. Virks selskabsstatus hører til CVR-stamdata. |
| **Ejendomsansvarlig og seneste faglige gennemgang** | Angiv den ansvarlige funktion og datoen for den seneste gennemgang. En tom dato betyder, at der endnu ikke er registreret en gennemgang. Hentetid og eventuel importdato registreres særskilt. |

Genbrug kontrollerede registeroplysninger. Tilføj arealer og BBR-referencer, når de skal bruges til søgning eller opfølgning. Hvis miljødata indgår, registreres V1/V2-kortlægning og områdeklassificering særskilt med kilde og dato på det relevante areal eller matrikelniveau. [Geodatastyrelsen om BFE](https://gst.dk/ansvarsomraader/matrikel-og-ejendomsregistrering/matriklen/bfe-nummer) · [Miljøstyrelsen om kortlægning og områdeklassificering](https://mst.dk/erhverv/rent-miljoe-og-sikker-forsyning/jord/forurenede-grunde/kortlaegning-og-omraadeklassificering)

## Metadata på dokumenter og sager

Brug **titel, dokumentkategori og dokumentdato** som fælles udgangspunkt. Brug få søgbare kategorier, fx skøde, servitut, lejekontrakt, tilladelse, tegning og forsikringspolice. Angiv aftalepart eller tilladelsesindehaver efter dokumentet og tilknyt de berørte BFE’er. Grundejeren og parten i dokumentet kan være forskellige selskaber.

På aftaler, policer og tilladelser registreres status, kendt gyldighed og en relevant reference, fx policenummer eller myndighedens sagsnummer. Flere aftaler eller tilladelser kan være gældende for samme ejendom. Hver handling med egen frist eller ansvarlig følges på den tilhørende sag.

## Fælles dokumenter og fagsystemer

| Situation | Placering og adgang |
|---|---|
| **Police for flere BFE’er eller selskaber** | Gem policen én gang på selskabets aftalesag i det eksisterende aftalearkiv. Ved flere aftaleparter aftales, hvem der vedligeholder sagen. Registrér omfattede selskaber og BFE’er, og henvis fra 08. Hvis direkte relationer mangler, bruges selskab, sagsnummer og policenummer som reference. |
| **Leje eller ledningsret på fremmed grund** | Hvis fremmed grund indgår i arkivet, placeres dokumentet på aftale- eller rettighedssagen hos det selskab, der er juridisk part. Registrér grundens BFE som reference. Har en registreret bygning på grunden eget BFE, registreres det særskilt fra grundens. |
| **Projekt på flere ejendomme eller dokumentation i et fagsystem** | Behold dokumentet på projektsagen eller i fagsystemet, hvor det vedligeholdes. Gør gældende tilladelser, tegninger og driftsdokumentation findbare fra de relevante BFE’er via en direkte henvisning til sagen, dokumentet eller anlægget. |

## Ledelsens overblik

Registrér et åbent punkt, når en faglig gennemgang viser en mangel, eller der er en handling at følge op på. Angiv **hvad der skal ske, ansvarlig og eventuel frist**. Ved afslutning henvises til resultatet, fx det modtagne dokument.

| Niveau | Praktisk brug |
|---|---|
| BFE-sagen | En mangel, der alene vedrører ejendommen, placeres her. Fx får en manglende henvisning til et skøde en ansvarlig, som kan finde det og lukke punktet. |
| Aftale, tilladelse eller fælles selskabssag | Registrér handlingen dér, hvor ansvaret ligger. En fælles police har én fornyelsesopgave, som kan findes fra alle omfattede BFE’er. |
| Selskab og arkivets top | Brug en delt liste over åbne punkter og kommende frister. Vis det valgte CVR på selskabsniveau og alle omfattede selskaber på toppen. Tæl hver opgave én gang. En særskilt søgning på BFE-sager uden gennemgangsdato viser, hvilke ejendomme der mangler en første registreret gennemgang. |

## Pilot i DocuNote

Afprøv sagstypen på 5–10 forskellige ejendomme, fx en administrationsbygning, et teknisk anlæg og et ubebygget areal. Brug disse arbejdsgange som acceptprøver.

1. **Ejerskifte.** Find BFE 5367067 direkte hos SK Forsyning og via **Tidligere ejendomme** hos SK Vand. Kontrollér, at en bruger med relevant adgang kan se den historiske ejerrelation og åbne den aktuelle hovedsag.
2. **Sameje (tænkt eksempel).** Lad to medejere bytte sagsansvar. Åbn samme BFE fra begge selskabers rod før og efter skiftet. Begge andele skal fortsat være synlige som gældende, og ejendommen skal tælle én gang i ledelsens samlede oversigt.
3. **Erstattet tilladelse.** Åbn 05 på BFE 5367073 og find Slagelse Kommunes afgørelse af 17. december 2020 om Slagelse Renseanlæg. Den erstattede tilladelsen af 24. november 1999 og omtaler SK Forsyning som ansøger. Ejendomskontrollen viser SK Spildevand som grundejer. Kontrollér, at både ansøger og henvisning til den tidligere afgørelse kan findes fra sagen. [Kommunens afgørelse, s. 3](https://b0301proddatasto.blob.core.windows.net/files/vrp2k3oj.pdf#page=3) · [Kobling til BFE og kilder S213, S215 og S217](research/decisions.md#krydskontrol-med-udgangspunkt-i-renseanlæg)
4. **Fælles police og ledelsesoverblik.** Vælg en police, der omfatter to BFE’er i hvert sit selskab. Find policen fra begge ejendomme. Luk en prøveopgave på aftalesagen, og kontrollér, at den forsvinder fra begge selskabers åbne punkter og fra den samlede liste. Find også en ejendom uden registreret gennemgang.
5. **Ledningsret på fremmed grund.** Find aftalen fra både selskabet, der har indgået den, og den berørte grunds BFE. Kontrollér, at grunden kun tæller som ejet, hvis der også foreligger et dokumenteret ejerforhold.

IntraNote beskriver sagstyper med dokumentmapper og metadata, et skabelonbibliotek samt gemte og delte søgninger. Afprøv genveje mellem selskaber med almindelige brugerrettigheder, koblingen mellem flere BFE’er og én sag samt selskabsfilteret i Envafors’ opsætning. Hvis en genvej kræver en anden løsning, skal sagen fortsat kunne findes på BFE og sagsnummer. [IntraNotes superbrugerkursus](https://www.intranote.dk/arrangementer-for-kunder/docunote-superbruger-kursus) · [IntraNotes vejledning til søgning](https://www.intranote.dk/blog/konsulentchefens-tips-til-sogning)

## Inspiration fra praksis

- **Boligflow** dokumenterer fælles standardmapper, som kan sættes op særskilt for selskaber, ejendomme, lejemål og lejeforhold. Det viser, hvordan en ejendomsskabelon kan genbruges på tværs af selskaber. [Boligflow om standardmapper](https://support.boligflow.dk/product/koncern/standardmapper)
- **BIOFOS** beskriver en genkendelig mappestruktur i DocuNote og en strukturworkshop. Casen fremhæver kontrakter, anlægsprojekter og miljø- og plandokumenter som relevante områder. [IntraNotes BIOFOS-case](https://www.intranote.dk/inspiration/cases/biofos)
- **Envafors** har allerede brugt DocuNote til aftaler og projektstyring ifølge leverandørens case. Den eksisterende opsætning er et naturligt udgangspunkt for piloten. [IntraNotes Envafors-case](https://www.intranote.dk/inspiration/cases/envafors)
- **Bygningsstyrelsen** anbefaler en ensartet mappestruktur, filnavngivning, metadata og versionering i byggeprojekter og henviser til Molio A104. De ni emnenavne i dette forslag er valgt til Envafors’ ejendomsarkiv. [Bygningsstyrelsens vejledning](https://bygst.dk/byggeri/ikt/vejledning-til-ikt-ydelser-og-implementering/digital-kommunikation-og-etablering-af-kommunikationsplatform/)
