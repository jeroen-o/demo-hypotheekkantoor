/* Scenariokiezer: uw situatie in drie scenario's.
   Alles rekent in het geheugen; er wordt niets opgeslagen of verstuurd. */
(function () {
  var form = document.getElementById("sk-form");
  if (!form) return;

  var NU = 2026, FORFAIT = 0.0035, TARIEF = 0.3756;
  var SCENARIO = {
    mild: { naam: "Mild", rente: 3.5, opslagAv: 0, aftrekTot: 9999, groei: 0.02, eenmalig: 0, grens85: 0.70, avMax: 0.30,
      uitleg: "Rente bij verlengen 3,5%. Renteaftrek blijft zoals nu. Woningwaarde +2% per jaar. Grens op 85 jaar: 70% van de waarde (zoals Rabobank vanaf 2027)." },
    strakker: { naam: "Strakker", rente: 5, opslagAv: 0.5, aftrekTot: 9999, groei: 0, eenmalig: 0, grens85: 0.50, avMax: 0.30,
      uitleg: "Rente bij verlengen 5%, plus 0,5% opslag op aflossingsvrij door hogere kapitaaleisen. Aftrek blijft binnen de termijn van 30 jaar. Woningwaarde gelijk. Grens op 85 jaar: 50% (zoals ABN AMRO), marktbreed." },
    streng: { naam: "Streng", rente: 6, opslagAv: 0.75, aftrekTot: 2030, groei: 0, eenmalig: -0.15, grens85: 0, avMax: 0,
      uitleg: "Rente bij verlengen 6%, plus 0,75% opslag op aflossingsvrij. Renteaftrek afgeschaft vanaf 2030. Woningwaarde 15% lager (regio, label of fundering). Op 85 jaar volledig afgelost; geen nieuw aflossingsvrij." }
  };
  var gekozen = "strakker";

  function getal(id) {
    var v = (document.getElementById(id).value || "").replace(/\./g, "").replace(",", ".").replace(/[^\d.\-]/g, "");
    var n = parseFloat(v); return isNaN(n) ? 0 : n;
  }
  function keuze(id) { return document.getElementById(id).value; }
  function eur(n) { return "€ " + Math.round(n).toLocaleString("nl-NL"); }
  function pct(n, d) { return n.toLocaleString("nl-NL", { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }) + "%"; }
  function factor(a, b) { return b > 0 ? (a / b).toLocaleString("nl-NL", { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + "×" : "–"; }

  // euro-velden met duizendtalscheiding
  Array.prototype.forEach.call(form.querySelectorAll("input[data-euro]"), function (el) {
    el.addEventListener("input", function () {
      var cijfers = el.value.replace(/\D/g, "");
      el.value = cijfers ? parseInt(cijfers, 10).toLocaleString("nl-NL") : "";
    });
  });

  function lees() {
    var s = {
      leeftijd: getal("sk-leeftijd"), schuld: getal("sk-schuld"), av: getal("sk-av"), woz: getal("sk-woz"),
      rente: getal("sk-rente"), einde: getal("sk-einde"), start: getal("sk-start"),
      label: keuze("sk-label"), fundering: keuze("sk-fundering"), water: keuze("sk-water"), overlijden: keuze("sk-overlijden")
    };
    if (s.av > s.schuld) s.av = s.schuld;
    if (s.einde < NU) s.einde = NU;
    s.aftrekEinde = s.start && s.start < 2001 ? 2031 : (s.start || NU) + 30;
    return s;
  }

  function netto(brutoJaar, woz, aftrek) {
    if (!aftrek) return brutoJaar;
    return brutoJaar - Math.max(0, brutoJaar - woz * FORFAIT) * TARIEF;
  }

  function reken(s, sc) {
    var n = s.einde - NU;
    var woz = s.woz * Math.pow(1 + sc.groei, n) * (1 + sc.eenmalig);
    var nuBruto = s.schuld * s.rente / 100;
    var nuNetto = netto(nuBruto, s.woz, NU < s.aftrekEinde);
    var naBruto = (s.schuld - s.av) * sc.rente / 100 + s.av * (sc.rente + sc.opslagAv) / 100;
    var aftrekNa = s.einde < s.aftrekEinde && s.einde < sc.aftrekTot;
    var naNetto = netto(naBruto, woz, aftrekNa);
    var leeftijdNa = s.leeftijd + n;
    var toegestaan85 = sc.grens85 * woz;
    var avNieuwMax = Math.min(sc.avMax * woz, sc.avMax ? 150000 : 0);
    return {
      woz: woz, ltv: woz ? s.schuld / woz * 100 : 0,
      nuBruto: nuBruto / 12, nuNetto: nuNetto / 12, naBruto: naBruto / 12, naNetto: naNetto / 12,
      aftrekNa: aftrekNa, leeftijdNa: leeftijdNa,
      tekort85: Math.max(0, s.av - toegestaan85), toegestaan85: toegestaan85,
      omzetten: Math.max(0, s.av - avNieuwMax), avNieuwMax: avNieuwMax
    };
  }

  function signalen(s, sc, r, sleutel) {
    var l = [];
    if (s.leeftijd >= 52 || r.leeftijdNa >= 52)
      l.push("Uw verwachte pensioeninkomen telt mee bij een nieuwe hypotheek (Rabobank vanaf 15 jaar voor uw pensioen).");
    if (!r.aftrekNa && s.einde >= s.aftrekEinde)
      l.push("Uw aftrektermijn is in " + s.aftrekEinde + " voorbij; daarna krijgt u niets meer terug.");
    else if (!r.aftrekNa)
      l.push("In dit scenario is de renteaftrek afgeschaft voordat uw rentevaste periode afloopt.");
    if (r.tekort85 > 0)
      l.push("Bij een nieuwe hypotheek moet de schuld op 85 jaar omlaag: ongeveer " + eur(r.tekort85) + " meer aflossen dan nu gepland.");
    if (r.omzetten > 0 && r.avNieuwMax > 0)
      l.push("Bij verhuizen of oversluiten mag u hoogstens " + eur(r.avNieuwMax) + " aflossingsvrij lenen; " + eur(r.omzetten) + " moet aflossend worden.");
    else if (r.omzetten > 0)
      l.push("In dit scenario is nieuw aflossingsvrij lenen niet meer mogelijk: bij verhuizen of oversluiten moet " + eur(r.omzetten) + " aflossend worden.");
    var label = { efg: { mild: "Label E, F of G: geen extra leenruimte en hogere energielasten.", strakker: "Label E, F of G kan meewegen in waardering en rente.", streng: "Label E, F of G: lagere waarde en een opslag; verduurzamen wordt vaak een voorwaarde." },
                  cd: { mild: "", strakker: "Label C of D: verbeteren levert extra leenruimte of rentekorting op.", streng: "Label C of D: verbeteren houdt de woning financierbaar." } };
    if (label[s.label] && label[s.label][sleutel]) l.push(label[s.label][sleutel]);
    var fund = { risico: { mild: "Funderingsrisico: bij klasse D of E is aanvullend onderzoek nodig.", strakker: "Funderingsrisico: de geldverstrekker kan een herstelplan of depot eisen.", streng: "Funderingsrisico: financiering mogelijk alleen na herstel." },
                 onbekend: { mild: "", strakker: "Fundering onbekend: laat het nagaan voordat u verkoopt of verhuist.", streng: "Fundering onbekend: zonder gegevens wordt de waarde voorzichtiger ingeschat." } };
    if (fund[s.fundering] && fund[s.fundering][sleutel]) l.push(fund[s.fundering][sleutel]);
    var water = { ja: { mild: "Overstromingsgebied: lees wat uw opstalverzekering dekt.", strakker: "Overstromingsgebied: het risico kan meetellen in de taxatie.", streng: "Overstromingsgebied: lagere waarde of een rente-opslag is mogelijk." } };
    if (water[s.water]) l.push(water[s.water][sleutel]);
    var dood = { nee: { mild: "Bij overlijden kan de partner de lasten niet dragen: bespreek een overlijdensrisicoverzekering of aflossen.", strakker: "Bij overlijden kan de partner de lasten niet dragen; banken wegen dat zwaarder mee bij een nieuwe hypotheek.", streng: "Bij overlijden kan de partner de lasten niet dragen; zonder dekking wordt herfinancieren lastig." },
                 weet: { mild: "", strakker: "Zoek uit wat er bij overlijden met de lasten gebeurt (polis, nabestaandenpensioen).", streng: "Zoek uit wat er bij overlijden met de lasten gebeurt; zonder dekking wegen banken het risico zwaar." },
                 alleen: { mild: "", strakker: "Alleenstaand: bij overlijden gaat de schuld naar de erfgenamen; met weinig overwaarde moet de woning verkocht worden.", streng: "Alleenstaand: de bank weegt mee of de schuld bij overlijden uit de verkoop kan worden afgelost." } };
    if (dood[s.overlijden] && dood[s.overlijden][sleutel]) l.push(dood[s.overlijden][sleutel]);
    return l;
  }

  function toon() {
    var s = lees();
    var uit = document.getElementById("sk-uitkomst");
    var html = "";
    ["mild", "strakker", "streng"].forEach(function (k) {
      var sc = SCENARIO[k], r = reken(s, sc), sig = signalen(s, sc, r, k);
      html += '<div class="sk-kaart' + (k === gekozen ? " gekozen" : "") + '">' +
        '<div class="sk-kop"><span class="zeker ' + (k === "mild" ? "m" : k === "strakker" ? "w" : "b") + '">' + sc.naam + '</span></div>' +
        '<p class="sk-uitleg">' + sc.uitleg + '</p>' +
        '<dl class="sk-cijfers">' +
        '<dt>Rentelast nu, netto per maand</dt><dd>' + eur(r.nuNetto) + '</dd>' +
        '<dt>Na ' + s.einde + ', netto per maand</dt><dd class="groot">' + eur(r.naNetto) + ' <small>' + factor(r.naNetto, r.nuNetto) + '</small></dd>' +
        '<dt>Bruto per maand na ' + s.einde + '</dt><dd>' + eur(r.naBruto) + '</dd>' +
        '<dt>Renteaftrek in ' + s.einde + '</dt><dd>' + (r.aftrekNa ? "Ja" : "Nee") + '</dd>' +
        '<dt>Woningwaarde in ' + s.einde + '</dt><dd>' + eur(r.woz) + ' <small>schuld ' + pct(r.ltv) + '</small></dd>' +
        '</dl>' +
        (sig.length ? '<ul class="sk-signalen">' + sig.map(function (x) { return "<li>" + x + "</li>"; }).join("") + "</ul>" : "") +
        '<button type="button" class="btn ' + (k === gekozen ? "" : "ghost") + '" data-kies="' + k + '" aria-pressed="' + (k === gekozen) + '">' +
        (k === gekozen ? "Dit scenario bespreken we" : "Dit scenario bespreken") + "</button></div>";
    });
    uit.innerHTML = html;
    Array.prototype.forEach.call(uit.querySelectorAll("[data-kies]"), function (b) {
      b.addEventListener("click", function () { gekozen = b.getAttribute("data-kies"); toon(); agenda(); });
    });
    agenda();
  }

  function agendaItems() {
    var s = lees(), sc = SCENARIO[gekozen], r = reken(s, sc), sig = signalen(s, sc, r, gekozen);
    var items = [
      "Scenario: " + sc.naam + ". " + sc.uitleg,
      "Rentelast nu " + eur(r.nuNetto) + " netto per maand; na " + s.einde + " " + eur(r.naNetto) + " (" + factor(r.naNetto, r.nuNetto) + ").",
      "Wat doen we vóór " + s.einde + ": verlengen, oversluiten, extra aflossen of verhuizen?"
    ].concat(sig);
    items.push("Uw eigen situatie: pensioenoverzicht, einddatum van elk leningdeel en de polis van uw opstalverzekering meenemen.");
    return items;
  }

  function agenda() {
    var ol = document.getElementById("sk-agenda");
    ol.innerHTML = agendaItems().map(function (x) { return "<li>" + x + "</li>"; }).join("");
  }

  form.addEventListener("input", toon);
  form.addEventListener("change", toon);
  form.addEventListener("submit", function (e) { e.preventDefault(); toon(); });

  // printen via een nieuw venster (werkt ook als de pagina in een iframe staat)
  document.getElementById("sk-print").addEventListener("click", function () {
    var w = window.open("", "_blank");
    if (!w) { alert("Uw browser blokkeert het printvenster. Sta pop-ups toe voor deze pagina."); return; }
    var esc = function (t) { var d = document.createElement("div"); d.textContent = t; return d.innerHTML; };
    w.document.write('<!doctype html><html lang="nl"><head><meta charset="utf-8"><title>Gespreksagenda</title>' +
      '<style>body{font-family:Arial,sans-serif;margin:32px;color:#111;line-height:1.5}h1{font-size:22px}li{margin-bottom:8px}p{color:#555;font-size:13px}</style></head><body>' +
      "<h1>Gespreksagenda hypotheek</h1><ol>" + agendaItems().map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ol>" +
      "<p>Indicatie op basis van uw eigen invoer en vereenvoudigde aannames. Geen advies. Demo Hypotheek kantoor (fictief).</p></body></html>");
    w.document.close(); w.focus(); w.print();
  });

  toon();
})();
