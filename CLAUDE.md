# demo-hypotheekkantoor

Voorbeeldwebsite van een **fictief** hypotheekadvieskantoor ("Demo Hypotheek kantoor"), live op
https://demo-hypotheek-kantoor.nl/ (GitHub Pages vanaf `main`, zie `CNAME`). Naam, adres, tarieven en de AFM-, KvK- en
Kifid-nummers zijn verzonnen. De site laat zien hoe een kantoor dienstverlening, kosten, grenzen en documenten vastlegt.

## Afbakening: wat hoort hier wel en niet

Dit project is **niet** hetzelfde als **"Kan ik straks nog doorstromen of mijn hypotheek verlengen?"**
(repo `jeroen-o/Kan-ik-straks-nog-doorstromen-of-mijn-hypotheek-verlengen-`, live op
https://jeroen-o.github.io/Kan-ik-straks-nog-doorstromen-of-mijn-hypotheek-verlengen-/).

| Hoort hier (demo-hypotheekkantoor) | Hoort in "Kan ik straks nog doorstromen..." |
| --- | --- |
| Het fictieve kantoor: werkwijze, diensten, kosten, nazorg, documenten, risico's, rekenhulpen | Hypotheekregels nu en straks, nieuws over bankbeleid |
| Uitleg over de woning, fundering, verduurzaming vanuit het kantoor | Toekomstscenario's (2035, stressscenario), rol van ECB en kapitaaleisen |
| Rekenhulppagina's die een externe tool na een klik laden | De gesprekshulp "Uw hypotheek in drie scenario's" |
| | De Europa-vergelijking |

- Bouw geen pagina's over regels-in-de-toekomst, scenario's of Europa in deze repo. Die gaan naar de andere repo.
- Vanuit deze site wordt alleen **gelinkt** naar de andere site (`rekenhulp-doorstromen-of-verlengen.html` laadt hem
  na een klik; `woning-risicos.html` linkt naar `…/regels.html`). Neem geen inhoud van die site over.
- Twijfel je bij een nieuwe opdracht in welke repo iets hoort? Vraag het de gebruiker voordat je bouwt.

## Werkwijze

- Statische HTML, geen build-stap, geen externe scripts of API's. Gedeelde stijl in `assets/style.css` (de laag
  "Huisstijl 2026" onderaan overschrijft oudere regels), gedrag in `assets/site.js`.
- Na elke wijziging: `python3 tools/controle.py` moet `GEEN FOUTEN` geven (structuur, links, ankers, JSON-LD,
  canonical, zoekindex, documenten).
- Nieuwe of gewijzigde pagina: werk ook `sitemap.xml`, `assets/zoekindex.json`, `llms.txt` en zo nodig de footer op
  alle pagina's bij.
- Taal: Nederlands, u-vorm (behalve `adviesproces.html`, dat je-vorm gebruikt). Nederlandse getalnotatie
  (`&euro;&nbsp;1.234,56`).
- Printen via `window.open()`, nooit `window.print()` direct (iframe/Google Sites). Geen `localStorage`.
- Metabeschrijvingen hoogstens 160 tekens. Eén `<h1>` per pagina.
- De rode demobalk blijft staan zolang de gegevens fictief zijn.

## Compliance

Benoem bij elke tekst met een AFM- of compliance-relevante claim het risico. Geen beloftes die een echt kantoor niet
waarmaakt, geen misleidende vergelijkingen, geen gesimuleerde reviews.
