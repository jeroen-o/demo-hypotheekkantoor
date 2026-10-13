#!/usr/bin/env python3
"""Controleert de site op structuur, verwijzingen en — belangrijker — op samenhang
tussen de publieksteksten en de modeldocumenten.

De fout die in dit project het vaakst voorkwam, is dat een wijziging één kant raakte:
de documenten werden dichtgezet terwijl de publieksteksten een dienst bleven beloven,
of omgekeerd. Dit script legt beide kanten per thema naast elkaar.

    python3 tools/controle.py        # exitcode 1 bij fouten
"""
import json, os, pathlib, re, sys
from html.parser import HTMLParser

WD = pathlib.Path(__file__).resolve().parent.parent
os.chdir(WD)

LEEG = {"meta", "link", "br", "img", "input", "hr", "source", "area", "base", "col",
        "embed", "param", "track", "wbr", "path", "rect", "circle", "line", "polyline",
        "polygon", "ellipse", "use", "stop", "iframe"}


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.fouten, self.ids, self.links = [], [], set(), []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if d.get("id"):
            self.ids.add(d["id"])
        if tag == "a" and d.get("href"):
            self.links.append(d["href"])
        if tag == "iframe" or tag in LEEG:
            return
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in LEEG:
            return
        if not self.stack or self.stack[-1] != tag:
            self.fouten.append((tag, tuple(self.stack[-3:])))
        else:
            self.stack.pop()


# Publieksteksten tegenover de documenten. Elke regel: patroon, waar het niet mag
# staan, en waarom het een probleem is.
SAMENHANG = [
    (r"[Bb]ewaking van het financieringsvoorbehoud", "publiek",
     "belooft termijnbewaking die OTD onderdeel 4 en AV artikel 4a uitsluiten"),
    (r"bewaken wij de (afgesproken )?termijn", "publiek",
     "belooft termijnbewaking die OTD onderdeel 4 en AV artikel 4a uitsluiten"),
    (r"bewaken de termijnen", "beide",
     "belooft termijnbewaking die OTD onderdeel 4 en AV artikel 4a uitsluiten"),
    (r"[Aa]ctief onderhoud", "beide",
     "suggereert een bewakingsdienst; het abonnement is een kortingsafspraak"),
    (r"Een controle is inbegrepen", "beide",
     "belooft een controle die de beheerovereenkomst uitsluit"),
    (r"jullie vragenlijst|(?<![Gg]een )periodieke check|Signaal verstuurd met opties", "beide",
     "veronderstelt periodieke signalering die het kantoor niet levert"),
    (r"wij beoordelen uw polisvoorwaarden|lezen ze en vertalen wat er", "publiek",
     "belooft het beoordelen van bestaande voorzieningen, dat meerwerk is"),
    (r"vergelijkingskaart die u bij het advies", "beide",
     "de kaart gaat vóór het adviesgesprek, niet erbij"),
    (r"<code>|LEESMIJ", "publiek",
     "instructie aan een implementerend kantoor in een consumententekst"),
    (r"Gebruikt u de tools niet, dan wordt er niets geladen", "publiek",
     "onjuist zolang een rekenhulp automatisch laadt"),
]


def main():
    fouten, ids, links = [], {}, {}
    paginas = sorted(p.name for p in WD.glob("*.html"))
    publiek = [f for f in paginas if f not in ("documenten.html", "documenten-tekst.html", "404.html")]

    for f in paginas:
        txt = pathlib.Path(f).read_text(encoding="utf-8")
        p = Parser()
        p.feed(txt)
        if p.fouten or p.stack:
            fouten.append(f"{f}: structuur {p.fouten[:2]} open={p.stack}")
        ids[f], links[f] = p.ids, p.links
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', txt, re.S):
            try:
                json.loads(m.group(1))
            except Exception as e:
                fouten.append(f"{f}: JSON-LD ongeldig: {e}")
        for ac in re.findall(r'aria-controls="([^"]+)"', txt):
            if ac not in p.ids:
                fouten.append(f"{f}: aria-controls '{ac}' zonder doel")
        if f != "404.html" and len(re.findall(r"<h1", txt)) != 1:
            fouten.append(f"{f}: {len(re.findall(r'<h1', txt))} h1-koppen")
        if 'rel="alternate"' not in txt:
            fouten.append(f"{f}: geen hreflang in de head")
        if "noindex" not in txt:
            fouten.append(f"{f}: geen noindex (demo met fictieve vergunningnummers)")

    for f, lijst in links.items():
        for h in lijst:
            if h.startswith(("http", "mailto:", "tel:")) or not h:
                continue
            pad, _, fragment = h.partition("#")
            if h.startswith("#"):
                if fragment and fragment not in ids[f]:
                    fouten.append(f"{f}: anker {h} bestaat niet")
                continue
            if pad and not pathlib.Path(pad).exists():
                fouten.append(f"{f}: dode link {h}")
            elif fragment and pad in ids and fragment not in ids[pad]:
                fouten.append(f"{f}: anker {h} bestaat niet")

    index = json.loads(pathlib.Path("assets/zoekindex.json").read_text(encoding="utf-8"))
    for r in index:
        pad, _, fragment = r["p"].partition("#")
        if not pathlib.Path(pad).exists() or (fragment and fragment not in ids.get(pad, set())):
            fouten.append(f"zoekindex verwijst naar {r['p']}")

    doc = pathlib.Path("documenten.html").read_text(encoding="utf-8")
    js = pathlib.Path("assets/docs.js").read_text(encoding="utf-8")
    templates = re.findall(r'<template id="doc-([a-z]+)">', doc)
    for k in templates:
        if not re.search(r"\b%s\s*:\s*\{" % k, js):
            fouten.append(f"docs.js mist de sleutel {k}")
    # versie in de printkop moet gelijk zijn aan de versie in de documentvoet
    for m in re.finditer(r'<template id="doc-([a-z]+)">(.*?)</template>', doc, re.S):
        k, body = m.group(1), m.group(2)
        v = re.search(r"(modelversie|voorbeeldversie|algemene voorwaarden versie|versie) ([0-9.]+), (\d+ \w+ \d{4})", body)
        if not v:
            continue
        soort = "versie" if v.group(1) == "algemene voorwaarden versie" else v.group(1)
        verwacht = f"{soort} {v.group(2)}, {v.group(3)}"
        j = re.search(r'\b%s\s*:\s*\{[^}]*?versie:\s*"([^"]*)"' % k, js)
        if j and j.group(1) != verwacht:
            fouten.append(f"docs.js {k}: '{j.group(1)}' tegenover '{verwacht}' in de template")

    for patroon, waar, waarom in SAMENHANG:
        doelen = publiek if waar == "publiek" else paginas
        for f in doelen:
            txt = pathlib.Path(f).read_text(encoding="utf-8")
            if re.search(patroon, txt):
                fouten.append(f"SAMENHANG {f}: '{patroon}' — {waarom}")

    tarieven = pathlib.Path("kosten.html").read_text(encoding="utf-8")
    knoppen = re.findall(r'aria-controls="(t-[^"]+)"', tarieven)
    rijen = re.findall(r'<tr class="toelichting" id="(t-[^"]+)"', tarieven)
    if sorted(knoppen) != sorted(rijen):
        fouten.append("kosten.html: i-knoppen en toelichtingsrijen lopen niet gelijk")

    print(f"pagina's {len(paginas)} | zoekindex {len(index)} | modellen {len(templates)} | "
          f"diensten {len(knoppen)} | "
          f"FAQ {len(re.findall(r'class=.acc-item.', pathlib.Path('vragen.html').read_text(encoding='utf-8')))}")
    if fouten:
        print(f"{len(fouten)} FOUTEN:")
        for x in fouten:
            print(" -", x)
        return 1
    print("GEEN FOUTEN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
