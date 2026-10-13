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
| `adviesproces.html` | Het adviestraject in detail: CBI-benadering, 50%-AO-scenario en de omgang met bestaande voorzieningen |
| `diensten.html` | Waarover wel en niet wordt geadviseerd, met drie fictieve voorbeeldsituaties |
| `verduurzaming.html` | Energielabel en leenruimte, financiering van maatregelen, funderingsrisico (`#fundering`) |
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
| `assets/favicon.svg` | Browser-icoon |
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

## Documenten in de demo

`documenten.html` bevat twintig modellen, elk deeplinkbaar (`documenten.html#beheer`):

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
