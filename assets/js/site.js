/* smokyDuck — site behaviour. Settings live in config.js */
(function () {
  "use strict";
  var C = window.SD_CONFIG || {};
  var root = document.documentElement;
  root.classList.remove("no-js");

  /* mobile menu */
  var btn = document.querySelector(".menu-btn"), mm = document.getElementById("mmenu");
  if (btn && mm) btn.addEventListener("click", function () {
    var o = mm.classList.toggle("open");
    btn.textContent = o ? "Close" : "Menu"; btn.setAttribute("aria-expanded", o);
    document.body.classList.toggle("lock", o);
  });

  /* reveal on scroll */
  var els = document.querySelectorAll(".rv");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }); }, { threshold: .15 });
    els.forEach(function (el) { io.observe(el); });
    window.SD_reveal = function (el) { io.observe(el); };
  } else els.forEach(function (el) { el.classList.add("in"); });

  /* custom cursor (fine pointers only, like the original) */
  var cur = document.querySelector(".cursor");
  if (cur && window.matchMedia("(pointer: fine)").matches && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    root.classList.add("has-cursor");
    document.addEventListener("mousemove", function (e) { cur.style.transform = "translate(" + e.clientX + "px," + e.clientY + "px)"; });
    document.addEventListener("mouseover", function (e) { cur.classList.toggle("big", !!e.target.closest("a,button,select,summary,.item,.voice")); });
  }

  /* contact details from config */
  document.querySelectorAll("[data-email]").forEach(function (a) { a.href = "mailto:" + C.email; a.textContent = C.email; });
  document.querySelectorAll("[data-wa]").forEach(function (a) {
    if (!C.whatsapp) { a.setAttribute("data-hide", ""); return; }
    a.href = "https://wa.me/" + C.whatsapp; a.target = "_blank"; a.rel = "noopener";
  });
  document.querySelectorAll("[data-social]").forEach(function (a) {
    var u = (C.social || {})[a.getAttribute("data-social")];
    if (u) { a.href = u; a.target = "_blank"; a.rel = "noopener"; } else a.setAttribute("data-hide", "");
  });
  document.querySelectorAll("[data-year]").forEach(function (s) { s.textContent = new Date().getFullYear(); });

  /* prefill form from ?voice=… or ?type=… */
  var qs = new URLSearchParams(location.search);
  document.querySelectorAll("form[data-sd-form]").forEach(function (f) {
    qs.forEach(function (v, k) { if (f.elements[k] && f.elements[k].type !== "checkbox") f.elements[k].value = v; });
  });

  /* forms → Google Apps Script, or the visitor's email app until that's set up */
  document.querySelectorAll("form[data-sd-form]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if (f.website_hp && f.website_hp.value) return;
      if (!f.checkValidity()) { f.reportValidity(); return; }
      var data = {}; new FormData(f).forEach(function (v, k) { if (k !== "website_hp") data[k] = data[k] ? data[k] + ", " + v : v; });
      data.page = location.pathname; data.submittedAt = new Date().toISOString();
      var st = f.querySelector(".status"), b = f.querySelector("[type=submit]");
      function say(t) { st.textContent = t; st.classList.add("show"); }
      if (!C.formEndpoint) {
        var body = Object.keys(data).map(function (k) { return k + ": " + data[k]; }).join("\n");
        location.href = "mailto:" + C.email + "?subject=" + encodeURIComponent((data.formType || "Enquiry") + " — " + (data.company || data.name || "")) + "&body=" + encodeURIComponent(body);
        say("Your email app should open with everything filled in. Just press send.");
        return;
      }
      b.disabled = true;
      fetch(C.formEndpoint, { method: "POST", mode: "no-cors", headers: { "Content-Type": "text/plain;charset=utf-8" }, body: JSON.stringify(data) })
        .then(function () { if (window.gtag) gtag("event", "generate_lead", { form_type: data.formType || "contact" }); f.reset(); say("Thank you. It's with us, and you'll hear back from a person shortly."); })
        .catch(function () { say("That didn't send. Please email " + C.email + "."); })
        .finally(function () { b.disabled = false; });
    });
  });

  /* analytics only after consent */
  var bn = document.getElementById("consent");
  function get() { try { return localStorage.getItem("sd_consent"); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem("sd_consent", v); } catch (e) {} }
  function ga() {
    if (!C.ga4 || window.gtag) return;
    var s = document.createElement("script"); s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + C.ga4; document.head.appendChild(s);
    window.dataLayer = window.dataLayer || []; window.gtag = function () { dataLayer.push(arguments); }; gtag("js", new Date()); gtag("config", C.ga4);
  }
  if (C.ga4 && bn) {
    if (get() === "yes") ga(); else if (get() !== "no") bn.classList.add("show");
    bn.addEventListener("click", function (e) { var v = e.target.getAttribute("data-consent"); if (!v) return; set(v); bn.classList.remove("show"); if (v === "yes") ga(); });
  }
})();
