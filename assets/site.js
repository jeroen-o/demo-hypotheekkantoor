/* Demo Hypotheek kantoor — gedeelde paginalogica.
   Geen externe afhankelijkheden, geen build-step. */
(function () {
  "use strict";

  /* ---- jaartal in de footer ---- */
  var jaar = document.getElementById("jaar");
  if (jaar) jaar.textContent = new Date().getFullYear();

  /* ---- mobiel menu ---- */
  var burger = document.getElementById("burger");
  var navlinks = document.getElementById("navlinks");
  if (burger && navlinks) {
    burger.addEventListener("click", function () {
      var open = navlinks.classList.toggle("open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
    navlinks.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        navlinks.classList.remove("open");
        burger.setAttribute("aria-expanded", "false");
      });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && navlinks.classList.contains("open")) {
        navlinks.classList.remove("open");
        burger.setAttribute("aria-expanded", "false");
        burger.focus();
      }
    });
  }

  /* ---- huidige pagina markeren ---- */
  var hier = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav-links a").forEach(function (a) {
    var doel = (a.getAttribute("href") || "").split("#")[0].split("/").pop();
    if (doel && doel === hier) a.setAttribute("aria-current", "page");
  });

  /* ---- accordeon ---- */
  document.querySelectorAll(".acc-head").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      var acc = btn.closest(".acc");
      if (acc) {
        acc.querySelectorAll(".acc-head").forEach(function (b) {
          b.setAttribute("aria-expanded", "false");
          var p = document.getElementById(b.getAttribute("aria-controls"));
          if (p) p.classList.remove("open");
        });
      }
      if (!open) {
        btn.setAttribute("aria-expanded", "true");
        var paneel = document.getElementById(btn.getAttribute("aria-controls"));
        if (paneel) paneel.classList.add("open");
      }
    });
  });

  /* ---- cookiemelding ----
     Keuze geldt voor deze browsersessie. Bewust geen localStorage: die wordt
     geblokkeerd wanneer de site in een iframe (bijv. Google Sites) staat. */
  var cookie = document.getElementById("cookie");
  if (cookie) {
    var KEY = "dhk-cookie-ok";
    var gezien = false;
    try { gezien = sessionStorage.getItem(KEY) === "1"; } catch (e) { gezien = false; }
    if (gezien) {
      cookie.hidden = true;
    } else {
      cookie.hidden = false;
      cookie.querySelectorAll("[data-cookie-ok]").forEach(function (b) {
        b.addEventListener("click", function () {
          cookie.hidden = true;
          try { sessionStorage.setItem(KEY, "1"); } catch (e) { /* geen opslag beschikbaar */ }
        });
      });
    }
  }

  /* ---- contactformulier (demo: verstuurt niets) ---- */
  var form = document.getElementById("contactform");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = document.getElementById("formmsg");
      if (msg) {
        msg.classList.add("show");
        msg.focus();
      }
      var knop = form.querySelector("button[type=submit]");
      if (knop) knop.disabled = true;
    });
  }
})();
