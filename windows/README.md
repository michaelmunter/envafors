# Genskab datagrundlaget på Windows 11

Kopiér denne vejledning og de to PowerShell-filer ad den vej, virksomheden godkender. Opret input på virksomhedens side, og hent oplysningerne fra de offentlige registre. Gem virksomhedens egne udtræk, kildesvar og kontrolresultater på virksomhedens godkendte drev. Udtrækket kræver Windows PowerShell 5.1, en almindelig browser og Excel til gennemgang.

Scripts skal være godkendt til kørsel på virksomhedens udstyr. Hvis scripts ikke er godkendt, kan browseren og Excel bruges som beskrevet under [manuel indsamling](#manuel-indsamling-i-browser-og-excel). Afklar også, hvordan data fra sammenligningsgrundlaget må bruges. Det offentlige opslag dokumenterer værdien i virksomhedens datasæt.

## Afgræns selskaberne

Opret en mappe `input` og skriv `scope.csv` i VS Code med kolonnen `cvr` og ét kontrolleret, ottecifret CVR pr. linje. Start med Envafors' offentlige selskabsoplysninger og slå selskaber, ejere og datterselskaber op i CVR. Brug også registreringshistorikken til at finde direkte forgængere. Virksomheden fastlægger selv, hvilke selskaber der skal undersøges, og gemmer begrundelsen og de konkrete kilder til udvælgelsen.

Start med ét selskab med kendte ejendoms- og P-enhedsopslag, fx SK Vand, hvis det indgår i jeres afgrænsning. Slå CVR op i den offentlige visning før indtastning. Registreringsmeddelelse 13491615 for SK Vand nævner fx Korsør Vand som tidligere fusionsselskab. Kontroller den slags fund særskilt og tilføj CVR, hvis selskabet hører med. Ved det fulde udtræk undersøges hvert CVR i listen. Vurder anlæggenes relevans efter opslaget. [SK Vand i CVR](https://datacvr.virk.dk/enhed/virksomhed/27736033)

## Hent kildesvar

**Matriklen Labs.** Scriptet kalder `https://api.labs.matriklen.dk/CvrEjerskaber?cvr=<CVR>` for hvert CVR. Hvis computeren kun må behandle lokale filer, kan originale offentlige JSON-svar hentes via en godkendt internetadgang og lægges i `input/labs/<CVR>.json`. Gem den præcise adresse og hentetid for hver fil i henteloggen nedenfor. Labs-svaret indeholder ikke det søgte CVR, så filnavnet og den noterede URL skal afstemmes ved hentningen.

**CVR og P-enheder.** Åbn `https://datacvr.virk.dk/gateway/virksomhed/hentVirksomhed?cvrnummer=<CVR>&locale=da` i en almindelig browser. Gem JSON-svaret midlertidigt som `input/cvr/<CVR>.json`. Kontrollér i VS Code, at filen indeholder JSON og det søgte `stamdata.cvrnummer`. Gem fulde gatewayfiler kun under godkendt, midlertidig behandling. De kan indeholde oplysninger ud over de felter, som udtrækket bruger. Scriptet kopierer kun de valgte felter og et hash til resultatet. Ved afslag eller et ufuldstændigt svar bruges [den offentlige enhedsvisning](#manuel-indsamling-i-browser-og-excel).

Opret `input/captures.csv` i VS Code til hentninger foretaget i browseren eller på den godkendte kildeenhed. Brug komma og UTF-8.

```csv
cvr,source,url,lookup_at,outcome
```

- `source` er `cvr` for CVR-gatewayen og `labs` for Matriklen Labs. Brug én linje pr. kilde og CVR.
- `url` er den fulde adresse med søgeparameter som vist ovenfor. `lookup_at` er det faktiske tidspunkt med tidszone, fx formatet `2026-11-08T13:14:15+01:00`. Kommandoen `Get-Date -Format o` viser det aktuelle tidspunkt.
- `outcome` er `saved` ved en gemt JSON-fil. Brug `access_denied`, `technical_error`, `partial` eller `invalid_response` ved de respektive udfald. En gemt Labs-fil med to tomme lister registreres som `saved`. Scriptet klassificerer den som `no_result` efter indlæsning. Et manglende opslag vises som `not_checked`.

## Kør og kontrollér

Åbn PowerShell i mappen med scriptet. Vælg et nyt mappenavn til resultatet ved hver kørsel.

```powershell
powershell.exe -NoProfile -File .\Build-Backbone.ps1 -InputFolder .\input -OutputFolder .\run-01
```

Tilføj `-UseSavedLabs` for kun at læse lokale filer. I den tilstand foretager scriptet ingen netværkskald. CVR-filer læses lokalt i begge tilstande. Ved fejl i enkelte opslag får de øvrige CVR'er deres resultater, og scriptet returnerer statuskode 2. Samme statuskode bruges ved P-numre, der er registreret under flere CVR'er. Læs `lookups.csv` og eventuelle advarsler før brug af udtrækket. Gentag i en ny resultatmappe efter rettelser.

| Resultat | Kontrol |
| --- | --- |
| `companies.csv` | Afstem CVR, navn, binavne, status og datoer med CVR-visningen. |
| `production_units.csv` | Sammenhold antal aktive og ophørte enheder pr. CVR med de to lister i kilden. P-enhedens datoer gælder enheden. |
| `relations.csv` | Én observation pr. objekt i `ejer` eller `administrerer`. Afstem antal med kildens lister. Rolle, kildestatus, original virkningsdato og ejerandele bevares særskilt. |
| `lookups.csv` | Én linje pr. CVR og kilde med URL, tidspunkt, udfald og relevante antal. Kontrollér, at alle CVR'er er med, og følg op på afslag, fejl og mangler. |
| `raw/matriklen-labs` | Originale Labs-filer, inklusive gyldige tomme svar. Sammenhold SHA-256 med `lookups.csv` ved behov. |

Gennemgå ét udfyldt og ét tomt Labs-svar før det fulde udtræk. Filtrér `relations.csv` efter CVR og rolle, og sammenhold med den lokale JSON-fil. En manglende tinglyst andel bevares som en særskilt tilstand. En udtrykkelig andel på 0/1 bevares med sine tal. Behold den viste dato som kildeværdi. Brug et særskilt BFE-opslag til at undersøge overtagelses- eller tinglysningsdatoen.

Brug **Data → Hent data → Fra tekst/CSV** i Excel. Vælg UTF-8 og komma, og sæt CVR, P-nummer, BFE, branchekode, viste andele og originale datoer til tekst i Power Query. Det bevarer værdierne ved dansk tal- og datoformat. [Microsofts vejledning til Power Query](https://support.microsoft.com/en-us/excel/import-data-from-data-sources-power-query)

## Manuel indsamling i browser og Excel

- **CVR og P-enheder.** Åbn `https://datacvr.virk.dk/enhed/virksomhed/<CVR>`. Kontrollér CVR, navn, binavne og selskabsdatoer. Åbn **P-enheder**, vis alle relevante poster og åbn også **Vis ophørte P-enheder**. Registrér hver enhed på sin egen række og gem URL, hentetid, udfald og antal for begge lister. Brug kolonnerne fra `companies.csv` og `production_units.csv` ovenfor, eller skriv kolonneoverskrifterne fra scriptets `$companyFields` og `$unitFields` i Excel. Før manuelt indsamlede rækker i virksomhedens arbejdsbog sammen med de afstemte udtræk.
- **Legale ejere.** Åbn **Ejerforhold** og **Ophørt ejerskab** på samme CVR-side. Registrér udfaldet for begge visninger. Brug ejerlinket til at kontrollere ejerens CVR. Bevar de viste kapital- og stemmeandele med deres perioder, ændringsdato og eventuel afhændelsesdato. En vist intervalværdi bevares som tekst. Opret én række pr. ejer og vist andelsperiode, hvor kapital og stemmer har samme periode. Hvis perioderne afviger, behold kildeoplysningerne særskilt til kontrol. Brug felterne for `company_ownership` i sammenligningsscriptet, og gem kilder og hentetider i arbejdsbogen.
- **Labs.** Hent JSON fra den offentlige adresse pr. CVR og notér udfaldet. På Excel til Windows kan JSON importeres via **Data → Hent data → Fra fil → Fra JSON**. Udvid først `ejer` og `administrerer` i hver sin tabel, tilføj CVR fra opslagslisten og den tilsvarende rolle, og saml tabellerne. Behold observationsrækker, også når samme BFE går igen. Brug råsvaret til at skelne en udeladt andel fra en andel med værdien `null`. Kontrollér antal rækker mod de to lister.

## Gennemgå afvigelser

Behold virksomhedens egne resultater og kilder som grundlag. Når en separat sammenligning er tilladt, bruges kun de sammenligningsfiler og det miljø, virksomheden har godkendt. Brug samme kolonner og angiv afgrænsning og dato for begge udtræk. PowerShell-sammenligningen kan køres helt lokalt.

```powershell
powershell.exe -NoProfile -File .\Compare-Backbone.ps1 -Table relations -CompanyCsv .\run-01\relations.csv -ComparisonCsv .\comparison\relations.csv -OutputCsv .\afvigelser-relations.csv
```

Vælg `relations`, `companies`, `production_units` eller `company_ownership`. For `companies` kan en kandidattabel med de seks tilsvarende kildefelter bruges. Begge inputfiler skal være UTF-8. Hvis Excel har eksporteret med semikolon, angives `-CompanyDelimiter ';'` eller `-ComparisonDelimiter ';'` for den relevante fil, når kommandoen køres direkte i PowerShell. Scriptet tæller forekomster af hver identisk række og viser kun forskellige antal. Filtrér i Excel på CVR, BFE, rolle og status for at se ændrede ejendomsobservationer sammen. Brug CVR og P-nummer for P-enheder og selskabs-CVR, ejer-CVR og andelsperiode for ejerposter. Afstem først, om begge sider faktisk har undersøgt samme CVR og kilde. Slå derefter afvigelsen op direkte og registrér dato, forskel og afgørelse.

For anlæg skal identitet og rolle kontrolleres i et sektorregister, en myndighedsafgørelse eller andet konkret belæg. Start fx ved et Jupiter- eller PULS-id og følg matrikel til BFE. Et CVR i en tilladelse, en P-enhed på adressen og en ejerpost er forskellige oplysninger.

## Tekniske grænser

Labs er en prototype, og dækningen af historikken er uafklaret. En ny kørsel kan afvige fra et tidligere udtræk, fordi kilden er ændret. PowerShell læser JSON med den indbyggede parser. Originalerne gør det muligt at undersøge tvetydigheder som gentagne JSON-feltnavne. Adgang til CVR-gatewayen og kørsel af scripts kan variere med virksomhedens udstyr og regler. [Microsofts vejledning til Windows PowerShell](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-windows-powershell) · [Microsofts vejledning til kørselspolitik](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-5.1)

Underagenten `review_win11_design` kontrollerede gatewayfelterne og Windows PowerShell 5.1-funktionerne. Reviewet førte til kontrol af påkrævede CVR-felter og til, at svarbytes skrives direkte fra PowerShell-svarets datastrøm. På Mac med PowerShell 7 genskabte scriptet alle 604 gemte Labs-observationer og håndterede et nyt opslag med poster og et nyt tomt opslag. Afvigelseskontrollen fandt en ekstra forekomst af en identisk række. Kør pilottrinnet på den administrerede Windows-maskine for at bekræfte lokal adgang og kørsel.
