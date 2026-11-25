/* smokyDuck — renders Voices (data/artists.json) and Work (data/portfolio.json) */
(function () {
  "use strict";
  var PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg>';
  var PAUSE = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>';
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function json(u) { return fetch(u, { cache: "no-cache" }).then(function (r) { return r.json(); }); }
  function pad(i) { return (i < 9 ? "0" : "") + (i + 1); }
  function reveal(box) { box.querySelectorAll(".rv").forEach(function (el) { window.SD_reveal ? SD_reveal(el) : el.classList.add("in"); }); }

  /* ---------- one thing plays at a time (audio, video, Drive embeds) ---------- */
  var activeFrame = null, cur = null, curBtn = null;
  function stopAll(except) {
    document.querySelectorAll("video, audio").forEach(function (m) { if (m !== except && !m.paused) m.pause(); });
    if (cur && cur !== except && !cur.paused) cur.pause();
    if (activeFrame && activeFrame !== except) { var f = activeFrame; activeFrame = null; f.parentNode && f.parentNode.removeChild(f); }
  }
  document.addEventListener("play", function (e) { stopAll(e.target); }, true);
  document.addEventListener("click", function (e) {
    var fac = e.target.closest(".facade[data-embed]");
    if (fac) {
      stopAll(null);
      var i = document.createElement("iframe");
      i.src = fac.getAttribute("data-embed"); i.title = fac.getAttribute("aria-label") || "Video";
      i.allow = "autoplay; fullscreen"; i.allowFullscreen = true;
      fac.parentNode.appendChild(i); activeFrame = i; return;
    }
    var b = e.target.closest(".play[data-src]"); if (!b) return;
    if (curBtn === b && cur) { if (cur.paused) { stopAll(cur); cur.play(); } else cur.pause(); return; }
    if (cur) cur.pause();
    cur = new Audio(b.getAttribute("data-src")); curBtn = b;
    cur.addEventListener("play", function () { b.innerHTML = PAUSE; b.classList.add("on"); });
    cur.addEventListener("pause", function () { b.innerHTML = PLAY; b.classList.remove("on"); });
    cur.addEventListener("ended", function () { b.innerHTML = PLAY; b.classList.remove("on"); });
    stopAll(cur); cur.play().catch(function () { b.innerHTML = PLAY; });
  });
  function playBtn(url, title) { return '<button class="play" type="button" aria-label="Play ' + esc(title) + '"' + (url ? ' data-src="' + esc(url) + '"' : " disabled") + ">" + PLAY + "</button>"; }
  function video(x) {
    if (x.kind === "video") return '<div class="video"><video controls playsinline preload="none" poster="' + esc(x.poster || "") + '" src="' + esc(x.src) + '"></video></div>';
    return '<div class="video"><button class="facade" type="button" data-embed="' + esc(x.embed) + '" aria-label="Play ' + esc(x.title) + '" style="background-image:url(' + esc(x.thumb || "") + ')"><span class="play">' + PLAY + "</span></button></div>";
  }

  /* ---------- WORK ---------- */
  document.querySelectorAll("[data-work]").forEach(function (box) {
    json("data/portfolio.json").then(function (d) {
      var items = (d.items || []).filter(function (x) { return x.src || x.embed || x.audio; });
      var vids = items.filter(function (x) { return x.kind !== "audio"; }), auds = items.filter(function (x) { return x.kind === "audio"; });
      box.innerHTML = '<div class="grid">' + vids.map(function (x, i) {
        return '<article class="item rv">' + video(x) + '<div class="meta"><div><h3>' + esc(x.title) + "</h3><p>" + esc(x.service) + " · " + esc(x.languages) + '</p></div><span class="num">' + pad(i) + "</span></div></article>";
      }).join("") + "</div>" + (false ? '<div style="margin-top:96px"><p class="label">( Audio )</p>' + auds.map(function (x) {
        return '<div class="audio">' + playBtn(x.audio, x.title) + "<div><h3>" + esc(x.title) + "</h3><p>" + esc(x.service) + " · " + esc(x.languages) + "</p></div></div>";
      }).join("") + "</div>" : "");
      reveal(box);
    });
  });

  /* ---------- VOICES ---------- */
  var list = document.getElementById("voices");
  if (list) json("data/artists.json").then(function (d) {
    var all = (d.artists || []).filter(function (a) { return a.published && a.consentOnFile && !a.example; });
    var F = { language: "languages", style: "characteristics", category: "categories", gender: "gender" };
    var bar = document.querySelector(".filters"); if (bar && all.length < 3) bar.setAttribute("data-hide", "");
    var sel = {}; Object.keys(F).forEach(function (k) { sel[k] = document.getElementById("f-" + k); });
    function vals(k) { var s = {}; all.forEach(function (a) { [].concat(a[F[k]] || []).forEach(function (v) { if (v) s[v] = 1; }); }); return Object.keys(s).sort(); }
    Object.keys(sel).forEach(function (k) {
      var v = vals(k), el = sel[k]; if (!el) return;
      if (v.length < 2) { el.parentNode.setAttribute("data-hide", ""); return; }
      v.forEach(function (x) { var o = document.createElement("option"); o.value = o.textContent = x; el.appendChild(o); });
      el.addEventListener("change", draw);
    });
    function ok(a) { return Object.keys(sel).every(function (k) { var v = sel[k] && sel[k].value; return !v || [].concat(a[F[k]] || []).indexOf(v) >= 0; }); }
    function draw() {
      var l = all.filter(ok);
      list.innerHTML = l.length ? l.map(function (a) {
        var s = (a.samples || []).filter(function (x) { return x.type !== "video" && x.url; })[0];
        return '<article class="voice rv" id="' + esc(a.id) + '">' + playBtn(s && s.url, a.name) +
          "<div><h3>" + esc(a.name) + '</h3><p class="muted">' + esc((a.languages || []).join(" · ")) + ((a.categories || []).length ? " — " + esc(a.categories.slice(0, 3).join(", ")) : "") + "</p></div>" +
          '<button class="more u" type="button" data-open="' + esc(a.id) + '" style="background:none;border:0;color:inherit">Profile →</button></article>';
      }).join("") + '<div class="list-end"></div>' : '<p class="empty">No voices match. <a class="u" href="contact.html">Tell us what you need</a> and we\'ll cast it.</p>';
      reveal(list);
    }
    draw();
    var dlg = document.getElementById("voice-dialog");
    function open(id) {
      var a = all.filter(function (x) { return x.id === id; })[0]; if (!a || !dlg) return;
      var line = function (k, v) { return v && [].concat(v).length ? k + ": <span>" + esc([].concat(v).join(", ")) + "</span><br>" : ""; };
      dlg.querySelector(".dlg").innerHTML = "<h2>" + esc(a.name) + "</h2>" + (a.bio ? '<p class="muted">' + esc(a.bio) + "</p>" : "") +
        '<p class="facts">' + line("Languages", a.languages) + line("Accent", a.accents) + line("Voice", a.characteristics) + line("Age", a.ageRange) + line("Best for", a.categories) + "</p>" +
        (a.samples || []).map(function (s) { return s.type === "video" ? '<div style="margin-bottom:32px">' + video(s.url, s.title) + '<p class="muted" style="font-size:14px;letter-spacing:.15em;text-transform:uppercase">' + esc(s.title) + "</p></div>" : '<div class="audio">' + playBtn(s.url, s.title) + "<div><h3>" + esc(s.title) + "</h3></div></div>"; }).join("") +
        '<p style="margin-top:40px"><a class="btn" href="contact.html?voice=' + encodeURIComponent(a.name) + '">Enquire about this voice</a>' +
        (a.demoDownload && a.demoAuthorised ? ' <a class="btn" href="' + esc(a.demoDownload) + '" download>Download demo</a>' : "") + "</p>";
      dlg.showModal ? dlg.showModal() : dlg.setAttribute("open", "");
    }
    list.addEventListener("click", function (e) { var b = e.target.closest("[data-open]"); if (b) open(b.getAttribute("data-open")); });
    if (dlg) {
      dlg.querySelector(".close").addEventListener("click", function () { dlg.close(); });
      dlg.addEventListener("close", function () { dlg.querySelector(".dlg").innerHTML = ""; if (cur) cur.pause(); });
    }
    if (location.hash) open(location.hash.slice(1));
  });
})();
