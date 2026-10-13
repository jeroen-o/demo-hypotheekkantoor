/* Sitebrede zoekfunctie. Laadt de index pas bij het eerste gebruik,
   zodat een gewoon paginabezoek niet zwaarder wordt. */
(function () {
  "use strict";
  var veld = document.getElementById("zoekveld");
  var uitvoer = document.getElementById("zoekuitvoer");
  if (!veld || !uitvoer) return;

  var index = null, bezig = false;

  function laad(daarna) {
    if (index) { daarna(); return; }
    if (bezig) return;
    bezig = true;
    fetch("assets/zoekindex.json")
      .then(function (r) { return r.json(); })
      .then(function (data) { index = data; bezig = false; daarna(); })
      .catch(function () { bezig = false; uitvoer.innerHTML = "<p>Zoeken lukt nu even niet.</p>"; uitvoer.hidden = false; });
  }

  function normaliseer(t) {
    return t.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  }

  function zoek() {
    var vraag = normaliseer(veld.value.trim());
    if (vraag.length < 2) { uitvoer.hidden = true; uitvoer.innerHTML = ""; return; }
    var woorden = vraag.split(/\s+/);
    var treffers = [];
    index.forEach(function (r) {
      var hooi = normaliseer(r.t + " " + r.o + " " + r.b);
      var score = 0;
      for (var i = 0; i < woorden.length; i++) {
        var pos = hooi.indexOf(woorden[i]);
        if (pos === -1) return;
        score += pos < 40 ? 3 : 1;
        if (normaliseer(r.t).indexOf(woorden[i]) !== -1) score += 4;
      }
      treffers.push({ r: r, score: score });
    });
    treffers.sort(function (a, b) { return b.score - a.score; });

    if (!treffers.length) {
      uitvoer.innerHTML = '<p class="geen">Niets gevonden voor &ldquo;' +
        veld.value.replace(/[<>&]/g, "") + '&rdquo;. Probeer een ander woord, of stel uw vraag via ' +
        '<a href="contact.html">contact</a>.</p>';
      uitvoer.hidden = false;
      return;
    }
    var lijst = treffers.slice(0, 8).map(function (x) {
      return '<li><a href="' + x.r.p + '"><b>' + x.r.t + '</b>' +
        (x.r.o ? '<span>' + x.r.o + '</span>' : '') +
        '<em>' + x.r.b + '</em></a></li>';
    }).join("");
    uitvoer.innerHTML = '<ul>' + lijst + '</ul>' +
      (treffers.length > 8 ? '<p class="meer">' + treffers.length + ' resultaten; de acht beste staan hierboven.</p>' : '');
    uitvoer.hidden = false;
  }

  var wacht;
  veld.addEventListener("input", function () {
    clearTimeout(wacht);
    wacht = setTimeout(function () { laad(zoek); }, 160);
  });
  veld.addEventListener("focus", function () { laad(function () {}); });
  veld.closest("form").addEventListener("submit", function (e) { e.preventDefault(); laad(zoek); });
  document.addEventListener("click", function (e) {
    if (!uitvoer.contains(e.target) && e.target !== veld) uitvoer.hidden = true;
  });
  veld.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { uitvoer.hidden = true; veld.blur(); }
  });

  /* Een zoekopdracht in de url, zodat ?q=... rechtstreeks een resultaat toont.
     Dat maakt de zoekfunctie ook bruikbaar vanuit een zoekmachine of een
     antwoordmachine die een zoek-url volgt. */
  try {
    var vraag = new URLSearchParams(window.location.search).get("q");
    if (vraag) {
      veld.value = vraag;
      laad(zoek);
    }
  } catch (e) {}
})();
