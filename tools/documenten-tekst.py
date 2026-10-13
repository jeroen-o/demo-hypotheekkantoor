#!/usr/bin/env python3
"""Genereert documenten-tekst.html: alle modeldocumenten als doorlopende, statische
tekst. Nodig omdat de overlay op documenten.html JavaScript gebruikt; precontractuele
informatie moet ook zonder JavaScript te lezen en te printen zijn.

Draai dit script opnieuw na elke wijziging in de <template>-blokken van
documenten.html of in assets/docs.js:

    python3 tools/documenten-tekst.py
"""
import re, pathlib, sys

wd = pathlib.Path(__file__).resolve().parent.parent
doc = (wd / "documenten.html").read_text(encoding="utf-8")
js = (wd / "assets" / "docs.js").read_text(encoding="utf-8")

titels = dict(re.findall(r'\b([a-z]+)\s*:\s*\{\s*titel:\s*"([^"]*)"', js))
blokken = re.findall(r'<template id="doc-([a-z]+)">(.*?)</template>', doc, re.S)
if not blokken:
    sys.exit("geen templates gevonden in documenten.html")

kop = doc[: doc.index('<main id="main">')]
staart = doc[doc.index("</main>") :]
kop = kop.replace(
    "<title>Documenten en voorwaarden — Demo Hypotheek kantoor (demo)</title>",
    "<title>Alle documenten als doorlopende tekst — Demo Hypotheek kantoor (demo)</title>",
)
kop = re.sub(
    r'<meta name="description" content="[^"]*">',
    '<meta name="description" content="Alle twintig modeldocumenten van het kantoor als doorlopende tekst, '
    'leesbaar en printbaar zonder JavaScript. Voorbeeldwebsite met fictieve gegevens.">',
    kop, count=1)
kop = kop.replace("documenten.html\">", "documenten-tekst.html\">")

inh = "\n".join(
    f'        <li><a href="#t-{k}">{titels.get(k, k)}</a></li>' for k, _ in blokken)
secties = []
for k, body in blokken:
    body = re.sub(r"<h3>", "<h4>", body).replace("</h3>", "</h4>")
    # verwijzingen als href="#herroep" werken alleen op documenten.html; hier naar de
    # eigen sectie wijzen wanneer die bestaat, anders terug naar de overlaypagina
    ids = {k for k, _ in blokken}
    body = re.sub(
        r'href="#([a-z]+)"',
        lambda m: f'href="#t-{m.group(1)}"' if m.group(1) in ids else f'href="documenten.html#{m.group(1)}"',
        body)
    secties.append(
        f'<section class="{"alt" if len(secties) % 2 else ""}" id="t-{k}">\n  <div class="wrap">\n'
        f'    <h2>{titels.get(k, k)}</h2>\n    <div class="ovbody" style="max-height:none;overflow:visible">\n'
        f'{body}\n    </div>\n    <p style="margin-top:18px"><a href="#inhoud">Terug naar het overzicht</a></p>\n'
        f'  </div>\n</section>\n')

main = f'''<main id="main">

<header class="pagehead">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> &rsaquo; <a href="documenten.html">Documenten</a> &rsaquo;
       Doorlopende tekst</p>
    <div class="eyebrow">Alle documenten</div>
    <h1>Alle documenten als doorlopende tekst</h1>
    <p>Dezelfde {len(blokken)} modeldocumenten die u op de <a href="documenten.html">documentenpagina</a> per stuk kunt
       openen, hier achter elkaar. Deze pagina werkt zonder JavaScript en is in &eacute;&eacute;n keer te printen of
       op te slaan.</p>
  </div>
</header>

<section id="inhoud">
  <div class="wrap">
    <h2>Inhoud</h2>
    <div class="prose">
      <ol>
{inh}
      </ol>
    </div>
  </div>
</section>

{"".join(secties)}'''

(wd / "documenten-tekst.html").write_text(kop + main + staart, encoding="utf-8")
print(f"documenten-tekst.html geschreven: {len(blokken)} documenten")
