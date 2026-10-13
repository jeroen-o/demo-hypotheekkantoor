/* Demo Hypotheek kantoor — documentvenster.
   Toont de modeldocumenten uit de <template>-elementen op documenten.html
   en print ze via een eigen venster (window.print() wordt in iframes,
   o.a. Google Sites, geblokkeerd). */
(function () {
  "use strict";

  var DOCS = {
    otd:   { titel: "Opdracht tot dienstverlening — modelversie", versie: "modelversie 1.0, 13 oktober 2026" },
    av:    { titel: "Algemene voorwaarden",                       versie: "versie 1.0, 13 oktober 2026" },
    dw:    { titel: "Dienstenwijzer",                             versie: "versie 1.0, 13 oktober 2026" },
    beheer:{ titel: "Beheerovereenkomst — modelversie",           versie: "modelversie 1.0, 13 oktober 2026" },
    dvd:   { titel: "Dienstverleningsdocument — voorbeeld",       versie: "voorbeeldversie 1.0, 13 oktober 2026" },
    vgk:   { titel: "Vergelijkingskaart aanbieders",              versie: "versie 1.0, 13 oktober 2026" }
  };

  var ov      = document.getElementById("ov");
  var ovbody  = document.getElementById("ovbody");
  var ovtitle = document.getElementById("ovtitle");
  if (!ov || !ovbody || !ovtitle) return;

  var huidig = null;
  var vorigeFocus = null;

  function focusbaar() {
    return Array.prototype.filter.call(
      ov.querySelectorAll('a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])'),
      function (el) { return el.offsetParent !== null; }
    );
  }

  function openDoc(id, viaHash) {
    var tpl = document.getElementById("doc-" + id);
    if (!tpl || !DOCS[id]) return;
    vorigeFocus = document.activeElement;
    huidig = id;
    ovtitle.textContent = DOCS[id].titel;
    ovbody.innerHTML = "";
    ovbody.appendChild(tpl.content.cloneNode(true));
    ovbody.scrollTop = 0;
    ov.classList.add("open");
    document.body.style.overflow = "hidden";
    var eersten = focusbaar();
    if (eersten.length) eersten[0].focus();
    if (!viaHash && history.replaceState) history.replaceState(null, "", "#" + id);
  }

  function closeDoc() {
    if (!ov.classList.contains("open")) return;
    ov.classList.remove("open");
    document.body.style.overflow = "";
    huidig = null;
    if (history.replaceState) history.replaceState(null, "", location.pathname + location.search);
    if (vorigeFocus && vorigeFocus.focus) vorigeFocus.focus();
  }

  function printDoc() {
    if (!huidig) return;
    var d = DOCS[huidig];
    var w = window.open("", "_blank");
    if (!w) { alert("Sta pop-ups toe om dit document te kunnen printen."); return; }
    var css =
      "body{font-family:Georgia,'Times New Roman',serif;color:#333;line-height:1.55;font-size:11pt;" +
      "max-width:17cm;margin:0 auto;padding:18mm 0}" +
      "h1{font-size:19pt;color:#003057;font-weight:400;margin:0 0 4px;border-bottom:3px solid #003057;padding-bottom:10px}" +
      ".kopregel{font-size:9pt;color:#78848f;margin:0 0 22px}" +
      "h3{font-size:12pt;color:#003057;margin:20px 0 7px;page-break-after:avoid}" +
      ".n{font-size:9.5pt;font-weight:700;color:#8a6212;letter-spacing:.05em;text-transform:uppercase;" +
      "margin:20px 0 3px;page-break-after:avoid}" +
      "p{margin:0 0 9px}ol,ul{margin:0 0 11px 20px}li{margin-bottom:5px}" +
      "table{width:100%;border-collapse:collapse;font-size:10pt;margin:11px 0 16px;page-break-inside:avoid}" +
      "th{text-align:left;padding:7px 9px;border-bottom:2px solid #dde5ec;color:#003057}" +
      "td{padding:7px 9px;border-bottom:1px solid #dde5ec;vertical-align:top}" +
      "table.kv td:first-child{font-weight:700;width:36%}" +
      ".box{border-left:3px solid #003057;padding:11px 15px;margin:12px 0;background:#fafcfd}" +
      ".box p:last-child{margin-bottom:0}.lead{font-size:9.5pt;color:#78848f}" +
      ".meta{font-size:8.5pt;color:#78848f;border-top:1px solid #dde5ec;padding-top:12px;margin-top:24px}" +
      "@page{margin:18mm 16mm}";
    w.document.write("<!DOCTYPE html><html lang='nl'><head><meta charset='utf-8'><title>" + d.titel + "</title>");
    w.document.write("<style>" + css + "</style></head><body>");
    w.document.write("<h1>" + d.titel + "</h1>");
    w.document.write("<div class='kopregel'>Demo Hypotheek kantoor B.V. &middot; AFM 99999999 &middot; Kifid 999.999999 &middot; " +
      d.versie + " &middot; fictief voorbeelddocument</div>");
    w.document.write(ovbody.innerHTML);
    w.document.write("</body></html>");
    w.document.close();
    w.focus();
    setTimeout(function () { w.print(); }, 350);
  }

  /* knoppen die een document openen */
  document.querySelectorAll("[data-doc]").forEach(function (el) {
    el.addEventListener("click", function (e) {
      e.preventDefault();
      openDoc(el.getAttribute("data-doc"));
    });
  });

  ov.querySelectorAll("[data-ov-close]").forEach(function (b) {
    b.addEventListener("click", closeDoc);
  });
  ov.querySelectorAll("[data-ov-print]").forEach(function (b) {
    b.addEventListener("click", printDoc);
  });
  ov.addEventListener("click", function (e) { if (e.target === ov) closeDoc(); });

  document.addEventListener("keydown", function (e) {
    if (!ov.classList.contains("open")) return;
    if (e.key === "Escape") { closeDoc(); return; }
    if (e.key !== "Tab") return;
    var items = focusbaar();
    if (!items.length) return;
    var eerste = items[0], laatste = items[items.length - 1];
    if (e.shiftKey && document.activeElement === eerste) { e.preventDefault(); laatste.focus(); }
    else if (!e.shiftKey && document.activeElement === laatste) { e.preventDefault(); eerste.focus(); }
  });

  /* deeplink: documenten.html#dvd opent dat document direct */
  var hash = location.hash.replace("#", "");
  if (hash && DOCS[hash]) openDoc(hash, true);
})();
