# demo-hypotheekkantoor

Demo-website van een hypotheekadvieskantoor met **volledig fictieve gegevens**. Naam, adres,
telefoonnummer, tarieven en de AFM-, KvK- en Kifid-nummers zijn verzonnen en niet geldig. Er is geen
vergunning, geen Kifid-aansluiting en geen dienstverlening. Het contactformulier verstuurt niets.

Live: https://demo-hypotheek-kantoor.nl/

## Waar de demo over gaat

De site laat zien hoe een kantoor zijn dienstverlening richting de consument begrijpelijk en controleerbaar
kan maken: wat je krijgt, wat het kost, waar de opdracht ophoudt en wat er na het passeren van de akte
gebeurt. Het onderscheid tussen **kosteloze wettelijke nazorg** en **betaald onderhoud** is daarbij
expliciet uitgewerkt op `nazorg.html`.

## Structuur

| Bestand | Inhoud |
| --- | --- |
| `index.html` | Home met samenvatting van werkwijze, diensten, kosten en nazorg |
| `werkwijze.html` | De vijf stappen, per stap wat wij doen, wat u aanlevert en wat u krijgt |
| `adviesproces.html` | Het adviestraject in detail: CBI-benadering, 50%-AO-scenario en de omgang met bestaande voorzieningen |
| `diensten.html` | Waarover wel en niet wordt geadviseerd, met drie fictieve voorbeeldsituaties |
| `verduurzaming.html` | Energielabel en leenruimte, labelherziening (EPBD IV), renovatiepaspoort, financiering van maatregelen |
| `woning-risicos.html` | Bouwkundige staat, waarde, onderhoud (`#onderhoud`), fundering (`#fundering`), klimaat (`#klimaat`) en de EBA-richtsnoeren voor geldverstrekkers (`#geldverstrekker`) |
| `nazorg.html` | Wettelijke nazorg (gratis) versus drie onderhoudsabonnementen, met vergelijkingstabel |
| `kosten.html` | Volledige tarievenlijst, annuleringsstaffel, meerwerk, nazorgprijzen en kosten van derden |
| `documenten.html` | Twaalf modeldocumenten in een overlay, te printen of op te slaan als PDF |
| `over-ons.html` | Kantoor, toezichtgegevens, privacy (`#privacy`) en klachten (`#klachten`) |
| `vragen.html` | Veelgestelde vragen in accordeons |
| `contact.html` | Contactformulier; opent de mailclient van de bezoeker |
| `404.html` | Foutpagina voor GitHub Pages |
| `robots.txt` | Houdt de demo uit zoekmachines |
| `assets/style.css` | Gedeelde stijl |
| `assets/site.js` | Menu, accordeons, cookiemelding, formulier |
| `assets/docs.js` | Documentvenster, focusbeheer en printen |
| `assets/favicon.svg`, `favicon.ico`, `assets/favicon-32.png`, `assets/apple-touch-icon.png`, `assets/icon-192.png`, `assets/icon-512.png` | Browser- en app-iconen |
| `site.webmanifest` | Naam, themakleur en iconen voor mobiel |
| `tools/kantoor.json` | Gegevens van uw eigen kantoor |
| `tools/personaliseer.py` | Vervangt de demowaarden door die uit `kantoor.json` |

## Technische uitgangspunten

- Statische HTML, geen build-step, geen externe scripts of API's.
- Alle interne links zijn relatief, zodat de site werkt vanaf het submap-pad van GitHub Pages.
- Printen gebeurt via `window.open()` en niet via `window.print()`, omdat dat laatste in een iframe
  (bijvoorbeeld een embed in Google Sites) wordt geblokkeerd.
- Geen `localStorage`. De cookiemelding gebruikt `sessionStorage` met `try/catch`; wordt die geblokkeerd,
  dan werkt de site gewoon door.
- Toegankelijkheid: skip-link, zichtbare focus, `aria-expanded` op menu en accordeons, een dialoog met
  `role="dialog"`, focus-trap en Escape, en `prefers-reduced-motion`.
- Documenten zijn deeplinkbaar: `documenten.html#beheer` opent dat model direct.

## De demo overnemen voor een eigen kantoor

```bash
# 1. Vul tools/kantoor.json met uw eigen gegevens
# 2. Bekijk wat er zou veranderen
python3 tools/personaliseer.py
# 3. Voer het door
python3 tools/personaliseer.py --schrijf
```

Het script doet alleen exacte tekstvervanging; het raadt niets. Daarna blijft handwerk over, en het script
herinnert daar na afloop aan:

1. **Demobalk verwijderen** uit elke pagina (het rode blok bovenaan).
2. **`noindex` weghalen** uit elke pagina én `robots.txt` aanpassen. Zolang die erin staan, blijft de site
   onvindbaar — bewust, want fictieve AFM- en Kifid-nummers horen niet in Google.
3. **Canonical en `og:url`** naar het eigen domein zetten.
4. **Contactformulier koppelen** aan echte formulierverwerking, met bewaartermijn en verwerkersovereenkomst.
5. **Modeldocumenten juridisch laten toetsen** en de fictieve aanbieders vervangen door de eigen selectie.
6. **Tarieven controleren** — alle bedragen in deze demo zijn verzonnen.
7. **Logo's vervangen.** Zet uw eigen bestanden in `logos/` en lees eerst `logos/LEESMIJ.md`: daar staat welke
   logo's u wel en niet mag plaatsen en waarom.
8. **Reviewblok koppelen** op de homepage (`index.html`, sectie "Ervaringen"). Koppel een onafhankelijk platform
   waarop klanten zelf beoordelen, met een link naar de bron. Niet toegestaan: zelf geschreven of geselecteerde
   citaten als klantervaring presenteren, een gemiddelde tonen zonder het aantal beoordelingen, of beoordelingen
   filteren op gunstigheid. Dat is een misleidende handelspraktijk (afdeling 6.3.3A BW) en valt onder het toezicht
   van de ACM.
9. **Fiscale pagina jaarlijks nalopen** (`fiscale-risicos.html`). De teksten bevatten bewust geen percentages of
   jaartallen, maar de regels rond aftrek, eigenwoningforfait en box 3 wijzigen jaarlijks.
10. **Cyberverzekering regelen.** De AV sluiten cyberschade uit, maar AVG-boetes en de kosten van een datalek
    zijn dwingend recht en vallen buiten elke exoneratie. De beroepsaansprakelijkheidsverzekering dekt dit niet:
    het is geen beroepsfout in de hoedanigheid van financieel adviseur.

## Publicatie en domeinnaam

De site draait op GitHub Pages onder **demo-hypotheek-kantoor.nl**. Het bestand `CNAME` in de
hoofdmap bevat die naam; GitHub leest dat bij elke publicatie.

Eenmalig in te stellen buiten deze repository:

1. **DNS bij de domeinregistrar.** Voor het hoofddomein vier A-records naar `185.199.108.153`,
   `185.199.109.153`, `185.199.110.153` en `185.199.111.153`, en vier AAAA-records naar
   `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153` en `2606:50c0:8003::153`.
   Voor `www` een CNAME naar `jeroen-o.github.io` (zonder de repositorynaam).
2. **GitHub → Settings → Pages.** Custom domain op `demo-hypotheek-kantoor.nl`, wachten tot de
   DNS-controle groen is, daarna **Enforce HTTPS** aanzetten.
3. **Google Search Console en Bing Webmaster Tools.** Domein toevoegen en
   `https://demo-hypotheek-kantoor.nl/sitemap.xml` indienen.

### Wat er aan staat voor zoekmachines en antwoordmachines

- `index, follow` op alle pagina's behalve `404.html`, met `max-snippet:-1` en
  `max-image-preview:large`.
- `robots.txt` staat alle crawlers toe en noemt de crawlers van taalmodellen afzonderlijk
  (GPTBot, ClaudeBot, PerplexityBot, Google-Extended en andere), zodat de site ook in
  antwoordmachines bruikbaar is.
- `sitemap.xml` met `lastmod`, `changefreq`, `priority` en `xhtml:link`-taalvarianten.
- `llms.txt` met een samenvatting van het model en een inhoudsopgave, inclusief de
  uitdrukkelijke instructie dat de vergunningnummers fictief zijn en nooit als bestaand mogen
  worden gepresenteerd.
- Per pagina: canonical, `og:`-blok met een eigen afbeelding van 1200×630, `twitter:card`,
  `hreflang` voor zes talen plus `x-default`, en JSON-LD met `FinancialService`, `WebPage` en
  `BreadcrumbList`. Op de homepage daarbij `WebSite` met een `SearchAction`; de zoekfunctie
  begrijpt daarom `?q=zoekterm` in de url.
- De og-afbeelding staat in `assets/og-afbeelding.png` en het vierkante logo voor de structured data in
  `assets/logo.png`. Vervang beide bij een eigen kantoor.
- Geen enkele pagina staat meer op `noindex`, ook `404.html` niet; die pagina wordt door de 404-status zelf al
  buiten de index gehouden.
- Titels blijven onder de 65 tekens en elke pagina heeft een eigen beschrijving van 70 tot 175 tekens; dat
  bewaakt `tools/controle.py` niet, dus loop het na bij een nieuwe pagina.
- Afbeeldingen hebben `width`, `height`, `loading="lazy"` en `decoding="async"`, zodat de 37 logo's op de
  homepage de laadtijd en de layout shift niet beïnvloeden.
- Extra structured data: `HowTo` met de vijf stappen op de werkwijzepagina, `OfferCatalog` met 61 geprijsde
  diensten op de kostenpagina, en op elke pagina een `FinancialService` met logo, afbeelding, talen en acht
  aanbiedingen met prijs. Dat is wat antwoordmachines uitlezen als zij een prijsvraag krijgen.
- `llms.txt` sluit af met zes veelgestelde vragen met een kort antwoord, zodat een taalmodel het model van dit
  kantoor kan citeren zonder de hele site te lezen.

**Let op bij een echt kantoor.** De demo staat nu op indexeren met fictieve AFM-, KvK- en
Kifid-nummers; die zijn in de footer uitdrukkelijk als fictief gemarkeerd en de demobalk staat op
elke pagina. Neemt u deze site over, vervang dan eerst alle nummers en de demobalk voordat u de
site laat indexeren.

## Controle na elke wijziging

```bash
python3 tools/controle.py            # structuur, verwijzingen en samenhang
python3 tools/documenten-tekst.py    # documenten-tekst.html opnieuw opbouwen
```

`tools/controle.py` toetst de HTML-structuur, alle interne links en ankers, de JSON-LD,
de zoekindex, de koppeling tussen `documenten.html` en `assets/docs.js` inclusief de
versienummers — en de **samenhang** tussen publieksteksten en modeldocumenten. Dat laatste
is de controle die in dit project het meeste heeft opgeleverd: de fout die steeds terugkwam,
was dat een wijziging één kant raakte. De documenten werden dichtgezet terwijl een pagina de
dienst bleef beloven, of een pagina werd aangepast terwijl het document de oude belofte nog
droeg. In `SAMENHANG` in dat script staat per thema welke formulering waar niet mag staan en
waarom. Voegt u een dienst of een uitsluiting toe, zet er dan een regel bij.

`tools/documenten-tekst.py` bouwt `documenten-tekst.html`: alle modeldocumenten als
doorlopende tekst, leesbaar en printbaar zonder JavaScript. Draai dit opnieuw na elke
wijziging in een `<template>`-blok, anders loopt die pagina achter.

## Documenten in de demo

`documenten.html` bevat eenentwintig modellen, elk deeplinkbaar (`documenten.html#beheer`):

| Categorie | Documenten |
| --- | --- |
| Hypotheekadvies | Opdracht tot dienstverlening, algemene voorwaarden, dienstenwijzer, dienstverleningsdocument, vergelijkingskaart |
| Verzekeringen | Dienstverleningsdocument risico's afdekken, vergelijkingskaart verzekeringen |
| Nazorg en administratie | Beheerovereenkomst, machtiging automatische incasso, identificatie en Wwft |
| Website | Disclaimer, cookieverklaring |

> **Let op:** dit zijn demoteksten, geschreven als voorbeeld van begrijpelijke kantoordocumentatie. Ze zijn
> niet juridisch getoetst en het "dienstverleningsdocument" is een vrije weergave — het wettelijke
> standaardformulier heeft een voorgeschreven vast format. Gebruik niets hiervan voor een echte
> dienstverlening zonder eigen toetsing.
