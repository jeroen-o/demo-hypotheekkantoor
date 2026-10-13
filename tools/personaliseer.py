#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Personaliseert de demowebsite voor een eigen kantoor.

Gebruik:
    python3 tools/personaliseer.py            toont wat er zou veranderen
    python3 tools/personaliseer.py --schrijf  past de bestanden daadwerkelijk aan

Het script leest tools/kantoor.json en vervangt de demowaarden in alle
HTML-bestanden. Er wordt niets geraden: alleen exacte tekstvervanging.
Controleer het resultaat altijd zelf voordat u de site publiceert.
"""

import json
import os
import re
import sys

BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# demowaarde -> sleutel in kantoor.json
VERVANGINGEN = [
    ("Demo Hypotheek kantoor B.V.", "kantoornaam_juridisch"),
    ("Demo Hypotheek kantoor", "kantoornaam"),
    ("Demostraat 12", "straat"),
    ("1234 AB Demostad", "postcode_plaats"),
    ("Demostad", "plaats"),
    ("085 - 000 00 00", "telefoon"),
    ("info@demohypotheekkantoor.nl", "email"),
    ("Demo Schadeverzekeringen N.V.", "bav_verzekeraar"),
    ("NL00ZZZ999999990000", "incassant_id"),
    ("KvK 99999999", "kvk", "KvK {}"),
    ("AFM 99999999", "afm", "AFM {}"),
    ("Kifid 999.999999", "kifid", "Kifid {}"),
    ("999.999999", "kifid"),
    ("18 geldverstrekkers", "aantal_geldverstrekkers", "{} geldverstrekkers"),
    ("7 verzekeraars", "aantal_verzekeraars", "{} verzekeraars"),
    ("&euro; 2.950,&ndash;", "tarief_hypotheek", "&euro; {},&ndash;"),
    ("€ 2.950,–", "tarief_hypotheek", "€ {},–"),
    ("&euro; 495,&ndash;", "tarief_orv", "&euro; {},&ndash;"),
    ("&euro; 1.450,&ndash;", "tarief_aov", "&euro; {},&ndash;"),
    ("&euro; 695,&ndash;", "tarief_woonlasten", "&euro; {},&ndash;"),
    ("&euro; 1.750,&ndash;", "tarief_oversluiten", "&euro; {},&ndash;"),
    ("&euro; 1.250,&ndash;", "tarief_ontslag_ha", "&euro; {},&ndash;"),
    ("&euro; 250,&ndash;", "tarief_bankgarantie", "&euro; {},&ndash;"),
    ("&euro; 145,&ndash;", "uurtarief", "&euro; {},&ndash;"),
    ("€ 7,50", "abonnement_basis", "€ {}"),
    ("&euro; 7,50", "abonnement_basis", "&euro; {}"),
    ("€ 17,50", "abonnement_plus", "€ {}"),
    ("&euro; 17,50", "abonnement_plus", "&euro; {}"),
    ("€ 29,50", "abonnement_compleet", "€ {}"),
    ("&euro; 29,50", "abonnement_compleet", "&euro; {}"),
    ("13 oktober 2026", "documentdatum"),
]

# Blijft altijd staan tenzij u het bewust weghaalt: zie README.
WAARSCHUWING = """
LET OP — controleer deze punten zelf voordat u publiceert:
  1. De demobalk bovenaan elke pagina moet weg.
  2. De regel <meta name="robots" content="noindex, nofollow"> moet uit elke
     pagina, en robots.txt moet worden aangepast.
  3. Vervang in elke pagina de canonical- en og:url-waarde door uw eigen domein.
  4. Het contactformulier opent nu de mailclient van de bezoeker. Koppel het aan
     uw eigen formulierverwerking en leg de bewaartermijn vast.
  5. De modeldocumenten zijn niet juridisch getoetst. Laat ze nakijken.
  6. Vervang de fictieve aanbieders in de vergelijkingskaarten door uw eigen
     selectie, en controleer of alle tarieven kloppen.
"""


def laad():
    pad = os.path.join(BASIS, "tools", "kantoor.json")
    with open(pad, encoding="utf-8") as f:
        gegevens = json.load(f)
    return {k: v for k, v in gegevens.items() if not k.startswith("_")}


def bestanden():
    for naam in sorted(os.listdir(BASIS)):
        if naam.endswith(".html"):
            yield os.path.join(BASIS, naam)


def main():
    schrijven = "--schrijf" in sys.argv
    gegevens = laad()
    totaal = 0

    for pad in bestanden():
        with open(pad, encoding="utf-8") as f:
            inhoud = origineel = f.read()

        for regel in VERVANGINGEN:
            zoek, sleutel = regel[0], regel[1]
            sjabloon = regel[2] if len(regel) > 2 else "{}"
            waarde = gegevens.get(sleutel, "")
            if not waarde:
                continue
            vervang = sjabloon.format(waarde)
            if vervang == zoek:
                continue
            aantal = inhoud.count(zoek)
            if aantal:
                inhoud = inhoud.replace(zoek, vervang)
                totaal += aantal

        if inhoud != origineel:
            naam = os.path.basename(pad)
            if schrijven:
                with open(pad, "w", encoding="utf-8") as f:
                    f.write(inhoud)
                print("aangepast: %s" % naam)
            else:
                print("zou aanpassen: %s" % naam)

    print("\n%d vervangingen %s." % (totaal, "doorgevoerd" if schrijven else "gevonden"))
    if not schrijven:
        print("Draai opnieuw met --schrijf om de bestanden aan te passen.")
    print(WAARSCHUWING)


if __name__ == "__main__":
    main()
