# Kontrol af Matriklen- og Virk-udtræk, 20. november 2026

Alle 15 ejendomme, som optræder under to CVR-numre, har én gældende og én historisk ejerpost. Kontrollen fandt ingen modstrid mellem den viste status, selskabets rolle og ejerandelene. Der er derimod datoer, som kræver yderligere belæg, hvis de skal bruges til at fastslå, hvornår et bestemt selskab overtog en ejendom.

Kontrollen omfatter præcis de 24 JSON-filer i [Git-version dd06ea4](https://github.com/michaelmunter/envafors/tree/dd06ea474e077fcbaf3b99f2c1332408fbce5cdf/data). Begge mapper har 12 CVR-numre, med 11 fælles. SK Varme (27736904) findes kun i Labs-mappen og NK-Vejlys (29193304) kun i Virk-mappen. Fem af de 12 leverede Labs-svar har to tomme lister. De oprindelige hentetider er ukendte. Git-versionen identificerer det undersøgte indhold. Tidspunkterne i [kildeindekset](sources.csv) fra S226 og frem gælder genopslagene.

## Status og andele

Matriklen Labs bruger status til at angive, om selskabet har rollen på opslagstidspunktet. En historisk post kan derfor godt vise en positiv andel. Faktisk og tinglyst andel beskriver hvert sit forhold og kan ændre sig på forskellige tidspunkter. En kontrol, der kan afsløre en modstrid, er at summere hver andelstype for sig for samme BFE på samme tidspunkt eller sammenholde en gældende rolle med den daterede ejendomsvisning. En sum over 100 procent kræver afklaring. En lavere sum i et udvalg af CVR-numre kan skyldes andre ejere eller uoplyste andele. [Labs' feltbeskrivelse](https://labs.matriklen.dk/ejerskaber) og [Ejerfortegnelsens datamodel](https://grunddatamodel.datafordeler.dk/objekttypekatalog/Ejerfortegnelsen/Ejerskab.html).

| Status for ejerpost | Faktisk | Tinglyst | Poster |
|---|---|---|---:|
| Gældende | 1/1 | 1/1 | 179 |
| Gældende | 1/1 | 0/1 | 4 |
| Gældende | 1/1 | Felt udeladt | 9 |
| Historisk | 1/1 | Felt udeladt | 22 |
| Historisk | 1/1 | 0/1 | 4 |
| Historisk | 0/1 | 1/1 | 2 |

De 220 ejerposter og 6 administratorposter vedrører 211 forskellige BFE-numre. Der var ingen gentagne kombinationer af CVR, BFE, rolle og status, ugyldige brøker eller aktuelle andelssummer over 100 procent. Alle 12 Labs-filer stemte ved genopslag på deres CVR-nummer efter JSON-parsning. Det afprøver også koblingen mellem filnavn og selskab, da Labs' svar ikke selv indeholder det søgte CVR-nummer.

**BFE 5367067** viser forskellen. Umiddelbart inden 20. maj 2026 kl. 00.00 dansk tid viste BfeEjer SK Forsyning (25797981) med faktisk 1/1 og tinglyst 0/1, og SK Vand (27736033) med faktisk 0/1 og tinglyst 1/1. Fra det undersøgte skiftetidspunkt viste ejendomsopslaget SK Forsyning med begge andele 1/1. De leverede Labs-filer viser SK Forsyning som gældende og SK Vand som historisk. Begge visninger bygger på Ejerfortegnelsen. Se S273, S349 og S512 samt de [tidligere daterede stikprøver](decisions.md#stikprøver-af-ejere-og-administratorer-i-matriklendk).

Ved virkningstid 20. november 2026 kl. 00.00 dansk tid viste BfeEjer alle 192 gældende ejere med begge andelsfelter som i filerne, også når det tinglyste felt var udeladt. Alle fire gældende administratorer stemte. Ingen af de 30 historiske relationer var vist som aktuelle, og ingen yderligere aktuelle roller for de 12 undersøgte CVR-numre blev fundet på de 211 ejendomme. For samtlige 28 historiske ejerposter og to historiske administratorposter viste et opslag ét sekund før Labs-tidspunktet den angivne rolle og, for ejerne, de angivne andele. Ved selve tidspunktet var rollen ophørt i visningen. Datoerne er virkningstid i den tilgængelige registerhistorik. De oplyser ikke, hvornår en ændring blev indberettet.

## Datoer, der kræver afklaring

| Selskab (CVR) | CVR-start | Labs-dato før CVR-start¹ | Overtagelsesdato i BfeEjer før CVR-start² |
|---|---|---:|---:|
| Zeanet (26863899) | 06.11.2002 | 6 | 29 |
| SK Vand (27736033) | 05.05.2004 | 6 | 26 |
| SK Varme (27736904) | 05.05.2004 | 0 | 4 |
| SK Spildevand (28483708) | 04.02.2005 | 0 | 11 |
| Sorø Spildevand (33053738) | 23.06.2010 | 2 | 10 |
| Sorø Vand (33053770) | 23.06.2010 | 0 | 4 |
| **I alt** | | **14** | **84** |

¹ Kalenderdatoen i `virkningFra` på alle 220 ejerposter. 10 af de 14 er gældende og 4 historiske.

² Det særskilte felt `overtagelsesdato` på de 192 gældende ejerposter i ejendomsvisningen. De to kolonner kan omfatte samme BFE. For SK Varme stammer CVR-start fra det tidligere Virk-opslag S035. For de øvrige selskaber er den kontrolleret i den leverede Virk-fil.

Fire af de 84 ejendomme viser også en tinglysningsdato før CVR-start. Det gælder BFE 2539862 (Zeanet) samt 2538076, 2531485 og 2539366 (SK Vand). For eksempel viser BFE 2539862 både overtagelses- og tinglysningsdato 01.01.1950, faktisk andel 1/1 og tinglyst andel 0/1. En tinglysningsdato er derfor heller ikke tilstrækkelig til at fastslå en positiv tinglyst andel. Udtrækkene kan ikke afgøre årsagen til de tidlige datoer eller identificere en eventuel tidligere ejer.

**Hvilken dato viser Labs?** For de 192 gældende ejerposter falder Labs-datoen i 168 tilfælde alene sammen med tinglysningsdatoen, i 11 alene med overtagelsesdatoen og i 7 med begge. For 6 matcher den ingen af dem. Det gælder BFE 7894780, 2506176, 2531352, 5367073, 5369474 og 7358872. Eksempelvis viser BFE 2531352 overtagelse 01.01.2002, tinglysning 22.06.2004 og en Labs-dato på 23.02.2009. Bevar de tre felter særskilt ved brug af data til historik. Se S325 og den [leverede Labs-fil](../data/labs.matriklen/27736033.json).

## Selskabsdata fra Virk

Samtlige 12 CVR-numre stemmer med filnavnene. 11 selskaber har status NORMAL uden ophørsdato. NK-Vejlys er registreret opløst efter fusion den 27.06.2018 og har én ophørt P-enhed. De 43 P-numre er forskellige, og selskabets CVR stemmer på hver post. De 35 aktive og 8 ophørte P-enheder ligger i den forventede liste i forhold til ophørsdatoen. Navn, adresse, postnummer/by, branche og start-/ophørsdato stemte også med [de tidligere P-opslag](production_units.csv) for disse 12 selskaber.

- **Ét P-nummer er ældre end selskabet.** P-nr. 1008965397 starter 01.12.2001 og ligger under SK Spildevand, hvis CVR starter 04.02.2005. P-enhedens startdato alene daterer ikke dens tilknytning til dette selskab. Se [Virk-filen](../data/virk/28483708.json).
- **Én oplysning afveg ved genopslag.** Alle 12 selskabers fulde stamdata og alle P-enheder stemte med Virk ved sammenligning på identifikator. I FIT A/S' fil er `udvidedeOplysninger.email` null, mens feltet var udfyldt ved genopslaget. Ændringstidspunktet er ukendt. De øvrige forskelle i de fulde svar var rækkefølgen af SK Vands aktive P-enheder samt almindelige og hårde mellemrum i registrerings- eller tegningsregeltekst. Otte af 12 svar var ens efter JSON-parsning uden normalisering. Se S226–S237 i [kildeindekset](sources.csv).
- **De tomme ejerlister har begrænset dækning.** Alle 12 selskabsudtræk har tomme lister for aktuelle og ophørte legale ejere. Virks særskilte ejervisninger, tidligere dokumenteret for de samme 12 selskaber, viser tilsammen 17 andelsperioder. Brug den særskilte ejervisning til spørgsmål om, hvem der ejer selskabet. Se [legale ejerandele](company_ownership.csv).

## Sådan gentages kontrollen

Kør fra projektroden med Python 3.9 eller nyere, tidszonedata for Europe/Copenhagen og systemets curl. Første kommando læser kun lokale filer. Den anden foretager også offentlige BfeEjer-opslag og skriver resultater til terminalen. Ingen af kommandoerne opdaterer kildefiler eller registre.

```sh
python3 scripts/check_exported_data.py
python3 scripts/check_exported_data.py --bfe-at 2026-11-20T00:00:00+01:00
```

Filnavnene angiver CVR. For hvert BFE sammenholdes roller og de to andele hver for sig. Kørslen udskriver de konkrete BFE-numre ved datofund, gentagelser, andels- og statusafvigelser. En manglende andel holdes adskilt fra en oplyst nulandel. For historiske rækker anvendes hele `virkningFra` med sekunder og tidszone. Tekniske fejl registreres særskilt. Et opslag uden viste ejere giver ingen konklusion om alle ejere. For BFE 5356220 var ejerlisten tom i alle tre opslag, mens administratorfeltet kunne sammenlignes. Se S365–S366 og S515. Tolv opslag på selve skiftetidspunktet fik først timeout. Alle tolv lykkedes ved genopslag (S521–S532).

For at gentage sammenligningen af hele kildesvar hentes Labs med `CvrEjerskaber?cvr=<CVR>` og Virk i en almindelig browser med `hentVirksomhed?cvrnummer=<CVR>&locale=da`. De konkrete URL'er og hentetider står i [kildeindekset](sources.csv). Kontrollér først ét CVR. Sammenlign de parsede JSON-objekter med de versionsbundne filer. Ved forskelle i Virk sammenlignes P-enheder på P-nummer inden for hver statusliste og tekster med almindeligt og hårdt mellemrum adskilt. En senere kørsel kan vise nye værdier eller rettet historik.

To uafhængige gennemgange efterregnede andelsmønstrene, de 15 delte BFE-numre, de 14 tidlige Labs-datoer og Virks stam- og P-data. Slutreviewet efterregnede også de 84 overtagelsesdatoer, de fire tinglysningsdatoer, fordelingen af de 192 Labs-datoer og alle 30 historiske skift mod de konkrete ejendomssvar. Reviewet fremhævede den udeladte tinglyste andel, de tomme legale ejerlister og manglende oprindelige hentetider. De forhold indgår i resultaterne ovenfor. Kontrollen afprøver de angivne relationer og felter i udvalget. En fuldstændig fortegnelse over selskabernes ejendomme og en juridisk dokumenteret adkomsthistorik kræver yderligere kilder.
