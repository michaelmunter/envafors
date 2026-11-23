# Ejendomsarkiv i DocuNote

**Envafors · Forslag til pilot · Version 0.6 · 23. november 2026**

**Ejendommen** har ét sæt stamdata pr. BFE-nummer. Når en gældende ejer i arkivet er dokumenteret, får ejendommen en fast plads direkte i selskabsmappen hos den ejer, der fører sagen. I piloten foreslås en DocuNote-sag af typen **Ejendom** til denne plads. Her ser brugeren ejendommens stamdata og ni emnemapper med adgang til skøder, aftaler, tilladelser og tegninger, også når originalen ligger på en fælles sag eller i et fagsystem. Brug selskabets registrerede navn og CVR som mappenavn. Begynd ejendomssagens titel med BFE-nummeret, og tilføj kendenavn eller kort adresse, når det er kendt.

## Hovedsag, medejere og tidligere ejere

**Gældende** og **historisk** angiver, om selskabet stadig har rollen på den pågældende BFE. **Primær** angiver, hvilken ejer der fører hovedsagen i arkivet. Registrér dette selskabs CVR én gang på hovedsagen. Ved sameje kan en ejer altså være **gældende og ikke-primær**.

| Selskabets forhold til ejendommen | Placering i selskabsmappen |
|---|---|
| Gældende ejer, som fører sagen | Læg BFE-hovedsagen direkte i roden. Ved sameje aftaler de omfattede ejere, hvem der fører sagen. Registrér hver ejers andel på ejerforholdet. |
| Gældende medejer, når en anden ejer fører sagen | Vis en genvej direkte i roden, fx **BFE … · medejer**. Hvis to medejere bytter sagsansvar, bytter hovedsag og genvej plads. Begge ejerforhold er stadig gældende. Ejendommen tæller én gang i den samlede portefølje. |
| Tidligere ejer | Opret **Tidligere ejendomme** ved det første historiske ejerforhold. Vis den tidligere ejers afsluttede sag med egne dokumenter, eller en historisk reference, hvis der kun foreligger registeroplysninger. Tilføj en genvej til den aktuelle hovedsag, når den findes i arkivet. |
| Gældende administrator, lejer, rettighedshaver eller driftsansvarlig | Knyt rollen og dens belæg til BFE. En genvej i roden kan mærkes med rollen, fx **BFE … · lejer**. På fremmed grund uden hovedsag i arkivet peger henvisningen på den relevante aftale- eller rettighedssag. Ejeroversigten medtager alene gældende, dokumenterede ejere. |

Brug **tinglyst adkomst** som udgangspunkt for placering hos den formelle ejer. Vælg først rollen `ejer` og status `gældende` i Matriklen Labs. Sammenhold CVR, BFE og de faktiske og tinglyste ejerandele med det daterede ejendomsopslag. Er andelene forskellige, er den tinglyste andel uoplyst, eller er adkomsten i øvrigt uklar, oprettes en afklaringsopgave med BFE, kilde og ansvarlig i den fælles opfølgning. Det kan gøres, før der findes en hovedsag. Ejendommen medtages i ejerens portefølje, når placeringen er afklaret. [Kontrol af status, andele og datoer](research/udtraekskontrol.md#status-og-andele)

Ved ejerskifte afsluttes den gamle ejerrelation med den dokumenterede dato, hvis den kendes. Den tidligere ejers egne dokumenter og oprindelige sagsnummer bevares hos selskabet. Er den nye ejer omfattet af arkivet, vises den aktuelle hovedsag i den nye ejers rod. Hvis stamdata vedligeholdes på hovedsagen, overtager den nye hovedsag den opgave. Datoen for seneste faglige gennemgang følger ejendommen. Angiv, hvem der fremover holder oplysningerne ajour. Henvis fra den afsluttede sag til den aktuelle hovedsag, når den findes, og kontrollér de øvrige genveje til samme BFE.

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

### Sådan placeres dokumenter og sager

En sag samler dokumenter og oplysninger om et bestemt forhold eller forløb. Ved udlejning er **03 Brugsaftaler** emnemappen, hvor brugeren finder ejendommens lejeaftaler. En **aftalesag** kan samle kontrakten, senere tillæg og en opsigelse for ét bestemt lejemål. En forlængelse kan behandles på samme aftalesag. At indhente lejerens underskrift er en **opgave**. Den er løst, når underskriften er modtaget, mens lejeaftalen kan gælde i flere år endnu.

Vælg den emnemappe, hvor brugeren vil lede efter resultatet, og se først, om der allerede findes en sag om forholdet. En selvstændig sag med eget sagsnummer er relevant, når et forløb skal kunne følges og afsluttes for sig, fx en tvist om fraflytning.

| Situation | Hvad brugeren finder i emnemappen |
|---|---|
| Dokumentet er allerede journaliseret på en aftale-, projekt- eller myndighedssag eller i et fagsystem | Henvis til sagen eller dokumentet, fx fra 03 til lejemålets aftalesag i aftalearkivet. Brug sagsnummer for et helt forløb og dokumentnummer for et bestemt dokument. Knyt henvisningen til BFE og emne, så den kan findes fra ejendommen. |
| Et enkelt dokument eller et lille forløb vedrører ejendommen | Dokumenterne direkte i emnemappen, fx en skatteopgørelse i **09 Ejendomsøkonomi**. |
| Flere dokumenter hører sammen på ejendomssagen | Saml dem efter behov i en undermappe, fx **Vurderingsklage · 2026** i 09 eller **Skadesag · skadenr.** i 08. Dokumenterne hører fortsat til ejendomssagen. Brug fx forsikringsselskabets skadenummer som reference. Henvis fra andre berørte emner eller BFE’er til det samme forløb eller dokument. |

Ved en udstykning findes landzonetilladelsen fra **04 Plan- og byggesager**, og registreringen af den gennemførte matrikelændring fra **01 Ejerskab og registrering**. Føres begge dokumenter på samme projektsag, peger de to emnemapper på hver sit dokument dér. Den samlede tingbogsattest hører til i 01 og den enkelte servitut i 02.

Nye, faste underemner indføres kun i den fælles skabelon ved et tilbagevendende behov. Skabeloner til fx besigtigelsesnotater hentes fra skabelonbiblioteket, når der skal skrives et notat. Modtagne skøder, policer og afgørelser journaliseres, når de foreligger. Uafklaret materiale fra indlæsning får en ansvarlig for placeringen.

## Stamdata og ansvar

### Ejendomsstamdata for alle BFE-typer

Registrér oplysninger om hele ejendommen én gang, og vis dem samlet i ejendomsmappen. Findes der allerede en fælles ejendomspost, kan hovedsagen henvise til den med BFE-nummeret. Ellers kan felterne vedligeholdes i afsnittet **Ejendomsstamdata** på hovedsagen. Hver række nedenfor er ét felt.

De fælles felter gælder for samlet fast ejendom, ejerlejlighed og bygning på fremmed grund. En ejendom kan findes på sit BFE-nummer, også uden oplysninger om jordstykker, bygninger eller anlæg. Viser kilden et BFE-nummer uden type, beholdes nummeret, og typen står uafklaret, indtil et ejendomsopslag dokumenterer den.

| Felt | Udfyldelse |
|---|---|
| **BFE-nummer** | Ejendommens entydige nummer i Matriklen, fx `5367067`. |
| **BFE-type** | Den registrerede ejendomstype. Værdien er *samlet fast ejendom*, *ejerlejlighed* eller *bygning på fremmed grund*. [Geodatastyrelsen om BFE](https://gst.dk/ansvarsomraader/matrikel-og-ejendomsregistrering/matriklen/bfe-nummer) |
| **Beliggenhedsadresse** | Ejendommens officielle beliggenhedsadresse fra Ejendomsbeliggenhedsregistret. |
| **Kortreference til ejendommen** | Henvisning til ejendommen på et kort, når adressen er upraktisk i felten. |
| **Kendenavn** | Det navn medarbejderne bruger om ejendommen som helhed, når den har et. |
| **Anvendelse** | Hvad ejendommen bruges til, fx administrationsbygning eller ubebygget areal. Gøres søgbart. |

**Faglig opfølgning på ejendommen** registreres også én gang pr. BFE. Ændringer i en lejeaftale eller en byggesag kan følges på den konkrete sag.

| Felt | Udfyldelse |
|---|---|
| **Ejendomsansvarlig** | Den funktion, der holder ejendommens oplysninger ajour. |
| **Dato for seneste faglige gennemgang** | Datoen for den seneste samlede gennemgang af ejendommen. En tom dato betyder, at der endnu ikke er registreret en gennemgang. |

### Supplerende stamdata efter BFE-type

Brug tillægget for den registrerede type, når oplysningerne foreligger og er relevante. En samlet fast ejendom består af ét eller flere jordstykker. Registrér matrikelnummer og ejerlav sammen for hvert af dem. En ejerlejlighed og en bygning på fremmed grund har hver sit eget BFE-nummer. En henvisning til en anden BFE viser sammenhængen mellem ejendommene. Ejerskabet af hver BFE dokumenteres særskilt. [Kildeindeks med opslagstider, S536–S539](research/sources.csv)

| Felt | Gælder for | Udfyldelse |
|---|---|---|
| **Matrikelnummer** | Samlet fast ejendom, pr. jordstykke | Jordstykkets matrikelnummer fra Matriklen. |
| **Ejerlavsnummer** | Samlet fast ejendom, pr. jordstykke | Nummeret identificerer jordstykket sammen med matrikelnummeret. [Geodatastyrelsen om Matrikelregistret](https://gst.dk/data-og-kort/matrikelkort-og-data/matrikelregistret) |
| **Ejerlavsnavn** | Samlet fast ejendom, pr. jordstykke | Vis det registrerede navn sammen med matrikelnummeret. Navnet hentes ud fra ejerlavsnummeret. |
| **Jordstykkets areal** | Samlet fast ejendom, pr. jordstykke | Det registrerede areal i m² fra Matriklen, når det bruges til søgning eller opfølgning. |
| **Ejerlejlighedsnummer** | Ejerlejlighed | Lejlighedens registrerede nummer inden for hovedejendommen. |
| **Hovedejendommens BFE-nummer** | Ejerlejlighed | Henvisning til den ejendom, der er opdelt i ejerlejligheder. Det kan være en samlet fast ejendom eller en bygning på fremmed grund. [Geodatastyrelsen om ejerlejligheder](https://gst.dk/ansvarsomraader/matrikel-og-ejendomsregistrering/registrering-af-ejerlejligheder) |
| **Grundens BFE-nummer** | Bygning på fremmed grund | Henvisning til den grund, hvor bygningen eller anlægget ligger, når grundens BFE er dokumenteret. [Geodatastyrelsen om bygning på fremmed grund](https://gst.dk/ansvarsomraader/matrikel-og-ejendomsregistrering/registrering-af-bygning-paa-fremmed-grund) |

### Tilknyttede bygninger, anlæg og miljøoplysninger

Vis kun disse oplysninger, når de bruges til søgning eller opfølgning. Registrér dem på den bygning, det anlæg eller det areal, de beskriver. Fx omfatter BFE 5371653 to jordstykker. Valbygård Vandværk er knyttet til det ene, matrikel 1d. Et anlæg kan tilsvarende berøre flere BFE’er. Brug anlægs-ID, GIS-reference eller begge dele til at finde det samme anlæg fra hver berørt ejendom. [Projektets kontrol af Valbygård Vandværk](research/decisions.md#valbygård-vandværk-og-sk-vand-piloten)

| Felt | Hører til | Udfyldelse |
|---|---|---|
| **BBR-reference** | Bygning eller teknisk anlæg | Henvisning til den konkrete post i BBR. |
| **Bebygget areal** | Bygning | Bygningens bebyggede areal i m² fra BBR. |
| **Anlægsnavn** | Anlæg | Anlæggets navn, fx Valbygård Vandværk. Vis navnet fra de ejendomme, anlægget er knyttet til. |
| **Anlægs-ID** | Anlæg | Anlæggets identifikator i det relevante fagsystem. |
| **GIS-reference til anlægget** | Anlæg | Henvisning til det konkrete anlæg i GIS. |
| **Kortlægningsniveau for jordforurening** | Berørt areal | Kildens angivelse af V1 eller V2 for det konkrete areal, når det er kortlagt. |
| **Områdeklassificering** | Berørt areal | Kommunens registrering for det pågældende areal. [Miljøstyrelsen om kortlægning og områdeklassificering](https://mst.dk/erhverv/rent-miljoe-og-sikker-forsyning/jord/forurenede-grunde/kortlaegning-og-omraadeklassificering) |

### Selskaber og deres relationer til ejendommen

Vis ejendommens gældende og historiske selskabsforhold fra BFE’en. Selskabets navn og status hentes fra CVR-stamdata. Rolle, periode og eventuel ejerandel registreres for det enkelte selskabs forhold til ejendommen. Et selskab kan have flere roller på samme BFE. For begge slags ejerandel bevares en oplyst nulandel som nul, mens en uoplyst andel markeres som ukendt.

| Felt | Hører til | Udfyldelse |
|---|---|---|
| **Selskabets CVR-nummer** | Selskab | Nummeret identificerer selskabet. Hver rolle på ejendommen henviser til selskabet med dette CVR. |
| **Registreret selskabsnavn** | Selskab | Navnet fra Virk for det pågældende CVR-nummer. |
| **Selskabsstatus i Virk** | Selskab | Virks status for virksomheden på opslagstidspunktet, fx `NORMAL`. |
| **Rolle på ejendommen** | Selskabsrelation | Fx ejer, administrator, lejer, rettighedshaver eller driftsansvarlig. |
| **Relationsstatus** | Selskabsrelation | Om den konkrete rolle er gældende eller historisk. |
| **Rollens startdato** | Selskabsrelation | Den dokumenterede dato for rollens begyndelse, når den kendes. |
| **Rollens ophørsdato** | Selskabsrelation | Den dokumenterede dato for rollens ophør, når den kendes. |
| **Faktisk ejerandel** | Ejerforhold | Den faktiske andel, som kilden viser, angivet som brøk. |
| **Tinglyst ejerandel** | Ejerforhold | Den tinglyste andel, som kilden viser, angivet som brøk. |

### Kilde og ajourføring

Knyt kildebelæg til den oplysning, det underbygger. Samme kildepost kan bruges til flere oplysninger. For miljøoplysninger knyttes kilden og opslagstidspunktet til det berørte areal. Angiv også virkningsdatoen, hvis den fremgår.

| Felt | Udfyldelse |
|---|---|
| **Kildehenvisning** | Reference til det konkrete registeropslag eller dokument. For et offentligt opslag bevares URL med søgeparametre i kildeindekset. |
| **Kildens dokumentdato** | Datoen på kildedokumentet, når den fremgår. |
| **Virkningsdato** | Datoen, hvor oplysningen gælder fra, hvis kilden angiver den. |
| **Registreringstidspunkt i kilden** | Hvornår oplysningen blev registreret i kilderegistret, hvis tidspunktet fremgår. |
| **Opslagstidspunkt** | Hvornår kildesvaret blev hentet, med tidszone. |
| **Importtidspunkt** | Hvornår oplysningerne eventuelt blev indlæst i arkivet. |

Ved kontrol af ejerhistorik bevares Labs-feltet `virkningFra` og ejendomsopslagets overtagelsesdato og tinglysningsdato hver for sig i kildesvarene. Brug kun en dato som rollens start eller ophør, når kilden dokumenterer den betydning. [Projektets kontrol af datoerne i Matriklen](research/udtraekskontrol.md#datoer-der-kræver-afklaring)

## Metadata på dokumenter og sager

### Sagens egne oplysninger og henvisning til ejendommen

For et dokument eller et forløb i ejendomsmappen er placeringen tilstrækkelig, når sammenhængen med én BFE er entydig og søgbar. En aftale- eller projektsag, der føres andetsteds eller vedrører flere ejendomme, henviser til hver berørt BFE. Herfra kan brugeren finde de fælles ejendomsoplysninger uden at indtaste dem igen. Ved en aftale om fremmed grund uden ejendomspost i arkivet er det tilstrækkeligt at angive grundens BFE-nummer og henvise til registeropslaget.

| Felt | Hører til | Udfyldelse |
|---|---|---|
| **Sagsnummer i DocuNote** | Den enkelte sag | DocuNotes nummer på hovedsagen, aftalesagen eller en anden selvstændig sag. Bruges til at genfinde den konkrete sag. |
| **Sagsførende CVR** | Ejendommens hovedsag | Henvisning til det ejerselskab, som fører hovedsagen. Ved sameje vises alle ejere fra de registrerede ejerforhold. |
| **Ejendomsreference** | Sag eller dokument | Brug BFE-nummeret, når placeringen alene ikke giver en søgbar kobling til ejendommen. Gentag henvisningen ved flere BFE’er. Gælder et dokument kun nogle af dem, angives de på dokumentet. |

### Dokumenter og opgaver

Brug **titel, dokumentkategori og dokumentdato** som fælles udgangspunkt. Brug få søgbare kategorier, fx skøde, servitut, lejekontrakt, tilladelse, tegning og forsikringspolice. Angiv aftalepart eller tilladelsesindehaver efter dokumentet. Grundejeren og parten i dokumentet kan være forskellige selskaber.

På aftaler, policer og tilladelser registreres status, kendt gyldighed og en relevant reference, fx policenummer eller myndighedens sagsnummer. Flere aftaler eller tilladelser kan være gældende for samme ejendom. Hver handling med egen frist eller ansvarlig følges på den sag, hvor arbejdet udføres.

### Dokumenthistorik uden faste undermapper

Når fx en byggesag er færdigbehandlet, kan forløbet markeres **afsluttet**. Ejendomssagen kan fortsætte, og tilladelsen kan stadig gælde. Dokumenterne bliver dér, hvor de er journaliseret. Brug dokumentets versioner ved redigering af samme kladde. En ny afgørelse eller et underskrevet tillæg journaliseres som et selvstændigt dokument.

Knyt en ny afgørelse til den tidligere med dokumentnummer eller med myndighedens sagsnummer, titel og dokumentdato. Angiv, om den **erstatter** eller **supplerer** det tidligere dokument. Registrér den dokumenterede virkningsdato særskilt fra dokumentdatoen. Ved fuld erstatning markeres den tidligere afgørelse som erstattet fra det dokumenterede tidspunkt. Ved et tillæg kan begge dokumenter være gældende. Er gyldigheden uafklaret, vises den som uafklaret.

Fra BFE og emne skal en bruger kunne se både gældende og tidligere dokumenter i en liste eller søgning med dato, status og reference. Ved opslag i et fagsystem skal henvisningen føre til den bestemte udgave. Hvis systemet overskriver gamle udgaver, journaliserer den sagsansvarlige den relevante udgave én gang med kilde og dato. Henvisningen peger da på det bevarede dokument. Hvis kun omtalen af et ældre dokument findes, vises den kendte reference med bemærkningen **kun reference i arkivet**. Mappen **Tidligere ejendomme** bruges på selskabsniveau ved afsluttede ejerforhold.

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
| Selskab og arkivets top | Brug en delt liste over åbne punkter og kommende frister. Vis det valgte CVR på selskabsniveau og alle omfattede selskaber på toppen. Tæl hver opgave én gang. En søgning på ejendomme uden gennemgangsdato viser, hvilke BFE’er der mangler en første registreret gennemgang. |

## Pilot i DocuNote

Afprøv sagstypen på 5–10 forskellige ejendomme. Lad alle tre BFE-typer indgå, eventuelt som tydeligt markerede prøveeksempler. Kontrollér, at en ejendom kan findes med de fælles felter alene. Åbn en særskilt aftalesag, og kontrollér, at den fører til samme aktuelle ejendomsoplysninger som ejendomsmappen. Brug også disse arbejdsgange som acceptprøver.

1. **Ejerskifte.** Find BFE 5367067 direkte hos SK Forsyning og via **Tidligere ejendomme** hos SK Vand. Kontrollér, at en bruger med relevant adgang kan se den historiske ejerrelation og åbne den aktuelle hovedsag.
2. **Sameje (tænkt eksempel).** Lad to medejere bytte sagsansvar. Åbn samme BFE fra begge selskabers rod før og efter skiftet. Begge andele skal fortsat være synlige som gældende, og ejendommen skal tælle én gang i ledelsens samlede oversigt.
3. **Erstattet tilladelse.** Start i **05 Miljø** på BFE 5367073. Find Slagelse Kommunes afgørelse af 17. december 2020 og henvisningen til tilladelsen af 24. november 1999, som afgørelsen erstattede. Prøv først med 2020-afgørelsen direkte i 05, dernæst i en undermappe i 05 og til sidst med en henvisning fra 05 til en eksisterende sag. Ved hver prøve skal brugeren kunne finde historikken ud fra BFE og emne og se, at SK Forsyning var ansøger, mens SK Spildevand er registreret som grundejer. [Kommunens afgørelse, s. 3](https://b0301proddatasto.blob.core.windows.net/files/vrp2k3oj.pdf#page=3) · [Kobling til BFE og kilder S213, S215 og S217](research/decisions.md#krydskontrol-med-udgangspunkt-i-renseanlæg)
4. **Fælles police og ledelsesoverblik.** Vælg en police, der omfatter to BFE’er i hvert sit selskab. Find policen fra begge ejendomme. Luk en prøveopgave på aftalesagen, og kontrollér, at den forsvinder fra begge selskabers åbne punkter og fra den samlede liste. Find også en ejendom uden registreret gennemgang.
5. **Ledningsret på fremmed grund.** Find aftalen fra både selskabet, der har indgået den, og den berørte grunds BFE. Kontrollér, at grunden kun tæller som ejet, hvis der også foreligger et dokumenteret ejerforhold.

IntraNote beskriver sagstyper med dokumentmapper og metadata, et skabelonbibliotek samt gemte og delte søgninger. Afprøv genveje mellem selskaber med almindelige brugerrettigheder, koblingen mellem flere BFE’er og én sag samt selskabsfilteret i Envafors’ opsætning. Hvis en genvej kræver en anden løsning, skal sagen fortsat kunne findes på BFE og sagsnummer. [IntraNotes superbrugerkursus](https://www.intranote.dk/arrangementer-for-kunder/docunote-superbruger-kursus) · [IntraNotes vejledning til søgning](https://www.intranote.dk/blog/konsulentchefens-tips-til-sogning)

## Inspiration fra praksis

- **Boligflow** dokumenterer fælles standardmapper, som kan sættes op særskilt for selskaber, ejendomme, lejemål og lejeforhold. Det viser, hvordan en ejendomsskabelon kan genbruges på tværs af selskaber. [Boligflow om standardmapper](https://support.boligflow.dk/product/koncern/standardmapper)
- **BIOFOS** beskriver en genkendelig mappestruktur i DocuNote og en strukturworkshop. Casen fremhæver kontrakter, anlægsprojekter og miljø- og plandokumenter som relevante områder. [IntraNotes BIOFOS-case](https://www.intranote.dk/inspiration/cases/biofos)
- **Envafors** har allerede brugt DocuNote til aftaler og projektstyring ifølge leverandørens case. Den eksisterende opsætning er et naturligt udgangspunkt for piloten. [IntraNotes Envafors-case](https://www.intranote.dk/inspiration/cases/envafors)
- **Bygningsstyrelsen** anbefaler en ensartet mappestruktur, filnavngivning, metadata og versionering i byggeprojekter og henviser til Molio A104. De ni emnenavne i dette forslag er valgt til Envafors’ ejendomsarkiv. [Bygningsstyrelsens vejledning](https://bygst.dk/byggeri/ikt/vejledning-til-ikt-ydelser-og-implementering/digital-kommunikation-og-etablering-af-kommunikationsplatform/)
