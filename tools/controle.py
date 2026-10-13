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

BASE = "https://demo-hypotheek-kantoor.nl/"

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
    (r"Onderhoud Basis|Onderhoud Plus|Onderhoud Compleet|onderhoudsabonnement", "beide",
     "de pakketnaam belooft onderhoud; het product is een kortingsafspraak"),
    (r"[Bb]eheerovereenkomst", "beide",
     "de naam belooft beheer; het product is een servicekortingsovereenkomst"),
    (r"na indiening van de aanvraag het volledige tarief", "beide",
     "de klant betaalt dan 100% voordat de begeleiding tot het passeren is geleverd"),
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
        if 'content="index, follow' not in txt:
            fouten.append(f"{f}: staat niet op index, follow")
        verwacht = BASE if f == "index.html" else f"{BASE}{f}"
        if f'rel="canonical" href="{verwacht}"' not in txt:
            fouten.append(f"{f}: canonical wijst niet naar {verwacht}")
        if "og:image" not in txt:
            fouten.append(f"{f}: geen og:image")

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

    telwoord = {19: "negentien", 20: "twintig", 21: "eenentwintig", 22: "tweeentwintig"}.get(len(templates))
    if telwoord:
        for f in ("index.html", "documenten.html", "README.md"):
            txt = pathlib.Path(f).read_text(encoding="utf-8").lower()
            for mis, woord in {19: "negentien", 20: "twintig", 21: "eenentwintig"}.items():
                if mis != len(templates) and re.search(rf"(?<![a-z]){woord} model", txt):
                    fouten.append(f"{f}: noemt '{woord} modellen' terwijl er {len(templates)} zijn")

    # elke inhoudelijke hoofdpagina hoort in het hoofdmenu te staan
    # elke inhoudelijke hoofdpagina hoort in de header te staan: in het hoofdmenu of,
    # voor de stukken die daar niet meer bij passen, in de snelkoppelingen van de topbalk
    menu = ("werkwijze.html", "diensten.html", "risicos.html", "tools.html", "nazorg.html",
            "kosten.html", "documenten.html", "vragen.html")
    for f in paginas:
        if f.startswith("rekenhulp-") or f in ("404.html", "en.html", "de.html", "pl.html", "es.html", "fr.html"):
            continue
        txt = pathlib.Path(f).read_text(encoding="utf-8")
        if '<div class="nav-links"' not in txt:
            continue
        begin = txt.index('<div class="nav-links"')
        blok = txt[begin:txt.index("</div>", begin)]
        if '<div class="snel">' in txt:
            top = txt.index('<div class="snel">')
            blok += txt[top:txt.index("</div>", top)]
        for doel in menu:
            if f'href="{doel}"' not in blok:
                fouten.append(f"{f}: {doel} ontbreekt in de header")

    for bestand, eis in (("CNAME", "demo-hypotheek-kantoor.nl"),
                         ("robots.txt", "Sitemap: https://demo-hypotheek-kantoor.nl/sitemap.xml"),
                         ("llms.txt", "demo-hypotheek-kantoor.nl"),
                         ("sitemap.xml", "<lastmod>")):
        pad = pathlib.Path(bestand)
        if not pad.exists():
            fouten.append(f"{bestand} ontbreekt")
        elif eis not in pad.read_text(encoding="utf-8"):
            fouten.append(f"{bestand}: '{eis}' ontbreekt")
    sitemap = pathlib.Path("sitemap.xml").read_text(encoding="utf-8")
    for f in paginas:
        if f == "404.html":
            continue
        verwacht = f"<loc>{BASE}</loc>" if f == "index.html" else f"<loc>{BASE}{f}</loc>"
        if verwacht not in sitemap:
            fouten.append(f"sitemap.xml mist {f}")
    if "jeroen-o.github.io" in sitemap:
        fouten.append("sitemap.xml verwijst nog naar het oude domein")

    # alle Nederlandse pagina's horen exact hetzelfde hoofdmenu te hebben; de vijf
    # taalpagina's hebben bewust een eigen, kort menu
    navs = {}
    for f in paginas:
        if f in ("en.html", "de.html", "pl.html", "es.html", "fr.html"):
            continue
        txt = pathlib.Path(f).read_text(encoding="utf-8")
        m = re.search(r'<div class="nav-links" id="navlinks">.*?</div>', txt, re.S)
        if m:
            navs.setdefault(m.group(0), []).append(f)
    if len(navs) > 1:
        grootste = max(navs.values(), key=len)
        for blok, bestanden in navs.items():
            if bestanden is grootste:
                continue
            fouten.append(f"afwijkend hoofdmenu op: {', '.join(bestanden)}")

    # de twee risicocategorieen staan niet in de header maar als kaart op de risicopagina;
    # die route moet dan wel blijven bestaan
    risicos = pathlib.Path("risicos.html").read_text(encoding="utf-8")
    for doel in ("woning-risicos.html", "fiscale-risicos.html"):
        if f'href="{doel}"' not in risicos:
            fouten.append(f"risicos.html verwijst niet naar {doel}; die pagina is dan alleen via de footer te vinden")

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
