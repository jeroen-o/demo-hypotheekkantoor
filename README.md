# demo-hypotheekkantoor

Demo-website van een hypotheekadvieskantoor met **volledig fictieve gegevens**. Naam, adres,
telefoonnummer, tarieven en de AFM-, KvK- en Kifid-nummers zijn verzonnen en niet geldig. Er is geen
vergunning, geen Kifid-aansluiting en geen dienstverlening. Het contactformulier verstuurt niets.

Live: https://jeroen-o.github.io/demo-hypotheekkantoor/

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
| `diensten.html` | Waarover wel en niet wordt geadviseerd, met drie fictieve voorbeeldsituaties |
| `nazorg.html` | Wettelijke nazorg (gratis) versus drie onderhoudsabonnementen, met vergelijkingstabel |
| `kosten.html` | Tarieven, staffel als het niet doorgaat, nazorgprijzen en kosten van derden |
| `documenten.html` | Zes modeldocumenten in een overlay, te printen of op te slaan als PDF |
| `over-ons.html` | Kantoor, toezichtgegevens, privacy (`#privacy`) en klachten (`#klachten`) |
| `vragen.html` | Veelgestelde vragen in accordeons |
| `contact.html` | Contactformulier (demo, verstuurt niets) |
| `404.html` | Foutpagina voor GitHub Pages |
| `assets/style.css` | Gedeelde stijl |
| `assets/site.js` | Menu, accordeons, cookiemelding, formulier |
| `assets/docs.js` | Documentvenster, focusbeheer en printen |

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

## Documenten in de demo

`documenten.html` bevat zes modellen: opdracht tot dienstverlening, algemene voorwaarden, dienstenwijzer,
dienstverleningsdocument, vergelijkingskaart en beheerovereenkomst.

> **Let op:** dit zijn demoteksten, geschreven als voorbeeld van begrijpelijke kantoordocumentatie. Ze zijn
> niet juridisch getoetst en het "dienstverleningsdocument" is een vrije weergave — het wettelijke
> standaardformulier heeft een voorgeschreven vast format. Gebruik niets hiervan voor een echte
> dienstverlening zonder eigen toetsing.
