/* Photo mix & match: pick a photo for every image spot on the page. */
(function () {
  "use strict";
  var PH = window.PH || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var SLOTS = Object.keys(PH);
  var KEY = "regency-photos-v1";
  var state = {};
  try { state = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { state = {}; }
  SLOTS.forEach(function (s) { if (!find(s, state[s])) state[s] = PH[s].opts[0][0]; });
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }
  function find(slot, code) { var o = PH[slot] && PH[slot].opts; if (!o) return null; for (var i = 0; i < o.length; i++) if (o[i][0] === code) return o[i]; return null; }

  function apply() {
    SLOTS.forEach(function (s) {
      var o = find(s, state[s]);
      $$('img[data-ph="' + s + '"]').forEach(function (img) {
        if (img.getAttribute("src") === o[1]) return;
        img.src = o[1]; img.alt = o[2];
      });
    });
    $$("[data-key]", groups).forEach(function (b) {
      var on = state[b.dataset.key] === b.dataset.val;
      b.setAttribute("aria-checked", String(on)); b.tabIndex = on ? 0 : -1;
    });
    SLOTS.forEach(function (s) { var c = $('[data-cur="' + s + '"]'); if (c) c.textContent = state[s]; });
  }

  /* ---------- panel ---------- */
  var panel = $("#mxPanel"), fab = $("#mxFab"), groups = $("#mxGroups");
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  groups.innerHTML = SLOTS.map(function (s) {
    var g = PH[s];
    return '<section class="mx-g"><div class="mx-gh"><h3>' + esc(g.title) + ' <span class="mx-cur" data-cur="' + s + '"></span></h3><a class="mx-jump" href="#" data-goto="' + s + '">Show me</a></div>' +
      '<div class="mx-thumbs" role="radiogroup" aria-label="' + esc(g.title) + '">' + g.opts.map(function (o) {
        return '<button type="button" class="mx-th" role="radio" data-key="' + s + '" data-val="' + o[0] + '" aria-label="' + esc(o[0] + ": " + o[2]) + '"><img src="' + o[1] + '" alt="" loading="lazy"><span>' + o[0] + "</span></button>";
      }).join("") + "</div></section>";
  }).join("");

  function target(slot) { return $('img[data-ph="' + slot + '"]'); }
  function reveal(slot, force) {
    var el = target(slot); if (!el) return;
    var r = el.getBoundingClientRect(), vh = window.innerHeight;
    if (force || r.top > vh * 0.75 || r.bottom < 100) el.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "center" });
  }
  function choose(slot, code) { state[slot] = code; save(); apply(); reveal(slot); }

  groups.addEventListener("click", function (e) {
    var b = e.target.closest("[data-key]");
    if (b) { choose(b.dataset.key, b.dataset.val); return; }
    var j = e.target.closest("[data-goto]");
    if (j) { e.preventDefault(); reveal(j.dataset.goto, true); if (narrow()) openPanel(false); }
  });
  groups.addEventListener("keydown", function (e) {
    var b = e.target.closest("[data-key]"); if (!b) return;
    var dir = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key]; if (!dir) return;
    e.preventDefault();
    var sib = $$("[data-key]", b.parentNode), n = sib[(sib.indexOf(b) + dir + sib.length) % sib.length];
    choose(n.dataset.key, n.dataset.val); n.focus();
  });

  function narrow() { return window.innerWidth < 1200; }
  function openPanel(on) {
    panel.hidden = !on; fab.setAttribute("aria-expanded", String(on));
    document.body.classList.toggle("mx-open", on);
    try { localStorage.setItem(KEY + "-open", on ? "1" : "0"); } catch (e) {}
  }
  fab.addEventListener("click", function () { openPanel(panel.hidden); if (!panel.hidden) $("#mxClose").focus(); });
  $("#mxClose").addEventListener("click", function () { openPanel(false); fab.focus(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden && narrow() && !document.querySelector("dialog[open]")) { openPanel(false); fab.focus(); } });

  /* ---------- copy, shuffle, reset ---------- */
  var msg = $("#mxMsg"), out = $("#mxOut"), mt;
  function say(t) { msg.textContent = t; clearTimeout(mt); mt = setTimeout(function () { msg.textContent = ""; }, 3200); }
  function summary() { return SLOTS.map(function (s) { return PH[s].title + ": " + state[s]; }).join("\n"); }
  $("#mxCopy").addEventListener("click", function () {
    var text = summary();
    function fallback() { out.hidden = false; out.value = text; out.focus(); out.select(); say("Select all and copy, then paste it into the chat."); }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function () { out.hidden = true; say("Copied. Paste it into the chat."); }, fallback);
    else fallback();
  });
  $("#mxShuffle").addEventListener("click", function () {
    SLOTS.forEach(function (s) { var o = PH[s].opts; state[s] = o[Math.floor(Math.random() * o.length)][0]; });
    save(); apply(); say("Shuffled. Scroll through to see the new mix.");
  });
  $("#mxReset").addEventListener("click", function () {
    SLOTS.forEach(function (s) { state[s] = PH[s].opts[0][0]; });
    save(); apply(); say("Back to the photos the site uses now.");
  });

  apply();
  var was = null; try { was = localStorage.getItem(KEY + "-open"); } catch (e) {}
  openPanel(was === null ? !narrow() : was === "1" && !narrow());
})();
