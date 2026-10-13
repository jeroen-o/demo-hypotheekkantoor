# Logo's van geldverstrekkers

Deze map bevat de logo's van de geldverstrekkers die op de homepage worden getoond.
De bestanden zijn overgenomen uit het aanbiedersoverzicht van fierhypotheken.nl.

De logo's zijn eigendom van de betreffende aanbieders. Ze staan hier om te laten zien
met welke partijen wordt samengewerkt.

## Zelf logo's beheren

1. Zet per aanbieder een bestand in deze map, bij voorkeur SVG of PNG met een
   transparante achtergrond. Gebruik een nette bestandsnaam zonder spaties,
   bijvoorbeeld `aanbieder-naam.png`.
2. Voeg in `index.html` een regel toe aan de lijst met klasse `logos`:

   ```html
   <li><img src="logos/aanbieder-naam.png" alt="Aanbieder Naam" loading="lazy" width="120" height="40"></li>
   ```

3. Geef elk logo een `alt` met de naam van de aanbieder, zodat de strook ook
   bruikbaar is voor wie de afbeeldingen niet ziet.

## Waar u op moet letten

- Gebruik alleen logo's waarvoor u toestemming heeft. Veel aanbieders stellen een
  merkhandboek beschikbaar met regels over kleur, witruimte en minimale afmeting.
- Toon geen logo's van partijen waar u feitelijk niet mee werkt. Dat is misleidend
  en kan worden gelezen als een onjuiste voorstelling van uw dienstverlening.
- Houd de strook actueel. Stopt de samenwerking met een aanbieder, haal het logo
  dan weg.
- Zet bij de strook welke claim u maakt. "Een selectie van onze aanbieders" is iets
  anders dan "wij werken met alle geldverstrekkers"; het tweede moet u kunnen
  aantonen en moet overeenkomen met uw vergelijkingskaart en dienstenwijzer.
- Logo's zijn geen vervanging van de vergelijkingskaart. Die blijft verplicht.

## Social-mediaknoppen

De knoppen in de footer zijn tekstknoppen met een neutraal icoon, en verwijzen naar
placeholder-adressen met het fictieve kantoor erin. Pas twee dingen aan:

1. Vervang de URL's in het blok met klasse `social` (in elke pagina) door uw eigen
   profielen, en het WhatsApp- en telefoonnummer door uw eigen nummer.
2. Haal de kanalen weg die u niet gebruikt. Een knop die naar een leeg of verlaten
   profiel leidt, doet meer kwaad dan goed.

De officiële merklogo's van LinkedIn, Facebook, Instagram en WhatsApp staan hier
bewust niet. Elk platform stelt die zelf beschikbaar met eigen voorwaarden over
kleur, vorm en minimale afmeting; download ze daar als u ze wilt gebruiken, en
vervang dan de `<svg>` in de knop.
