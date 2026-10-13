# Logo's van geldverstrekkers

Deze map is leeg. In de demo staan bewust geen logo's van echte geldverstrekkers:
het kantoor op deze website is fictief, en logo's van bestaande partijen zouden
een samenwerking suggereren die niet bestaat.

## Zelf logo's plaatsen

Een kantoor dat deze opzet overneemt, kan hier zijn eigen bestanden neerzetten:

1. Zet per aanbieder een bestand in deze map, bij voorkeur SVG of PNG met een
   transparante achtergrond. Gebruik een nette bestandsnaam zonder spaties,
   bijvoorbeeld `aanbieder-naam.svg`.
2. Vervang in `index.html` het blok met de placeholders door `<img>`-elementen:

   ```html
   <li><img src="logos/aanbieder-naam.svg" alt="Aanbieder Naam" loading="lazy"></li>
   ```

3. Geef elk logo een `alt` met de naam van de aanbieder, zodat de strook ook
   bruikbaar is voor wie de afbeeldingen niet ziet.

## Waar u op moet letten

- Gebruik alleen logo's waarvoor u toestemming heeft. Veel aanbieders stellen een
  merkhandboek beschikbaar met regels over kleur, witruimte en minimale afmeting.
- Toon geen logo's van partijen waar u feitelijk niet mee werkt. Dat is misleidend
  en kan worden gelezen als een onjuiste voorstelling van uw dienstverlening.
- Zet bij de strook welke claim u maakt. "Een selectie van onze aanbieders" is iets
  anders dan "wij werken met alle geldverstrekkers"; het tweede moet u kunnen
  aantonen en moet overeenkomen met uw vergelijkingskaart en dienstenwijzer.
- Logo's zijn geen vervanging van de vergelijkingskaart. Die blijft verplicht.
