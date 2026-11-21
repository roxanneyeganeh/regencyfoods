/* Mix & match preview: switches section variants and photos. */
(function () {
  "use strict";
  var IMG = window.MX_IMG || {}, ALT = window.MX_ALT || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  var HERO_PHOTOS = ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "packs", "box", "pouch"];
  var STORY_PHOTOS = ["kitchen", "K1", "K2", "K3", "K4", "K5"];
  var CATIMG = {
    yours: { meat: "y-meat", frozen: "y-frozen", drinks: "y-drinks", alcohol: "y-alcohol", nuts: "pouch", snacks: "y-snacks" },
    "new": { meat: "n-meat", frozen: "n-frozen", drinks: "D4", alcohol: "n-alcohol", nuts: "packs", snacks: "P3" }
  };
  var CODE = { packs: "Packs", box: "Box", pouch: "Pouch", kitchen: "Yours" };

  /* group -> controls. kind: chips | thumbs */
  var GROUPS = [
    { title: "Hero", jump: "top", controls: [
      { key: "heroPhoto", label: "Photo", kind: "thumbs", opts: HERO_PHOTOS },
      { key: "heroSide", label: "Photo side", opts: [["right", "Right"], ["left", "Left"]] },
      { key: "heroTone", label: "Panel colour", opts: [["green", "Dark Green"], ["cream", "Cream"], ["blue", "Dark Blue"]] }
    ] },
    { title: "Shop by category", jump: "shop", controls: [
      { key: "cats", label: "Layout", opts: [["bento", "Big + small tiles"], ["ingredients", "Ingredients list"], ["tall", "Tall cards"], ["index", "Numbered list"]] },
      { key: "catPhotos", label: "Photos", opts: [["yours", "Your photos"], ["new", "New photos"]] }
    ] },
    { title: "Trusted-by strip", jump: "trust", controls: [
      { key: "trust", label: "", opts: [["on", "Show"], ["off", "Hide"]] }
    ] },
    { title: "Delivery & van", jump: "delivery", controls: [
      { key: "deliv", label: "", opts: [["salmon", "Salmon, van photo"], ["green", "Dark Green, van drives in"], ["blue", "Dark Blue, van centred"]] }
    ] },
    { title: "Our story", jump: "story", controls: [
      { key: "story", label: "Layout", opts: [["light", "Light, with note"], ["dark", "Dark Green"]] },
      { key: "storyPhoto", label: "Photo", kind: "thumbs", opts: STORY_PHOTOS }
    ] },
    { title: "Trade account", jump: "trade", controls: [
      { key: "trade", label: "", opts: [["table", "Book a table (orange)"], ["boxed", "Green, numbered, boxed form"], ["underline", "Green, lined form"], ["cards", "Two cards + subscribe"]] }
    ] },
    { title: "Small labels", jump: null, note: "The little capitals above some headings, like “Since 1995”.", controls: [
      { key: "labels", label: "", opts: [["off", "Off"], ["on", "On"]] }
    ] }
  ];
  var DEFAULTS = { heroPhoto: "H1", heroSide: "right", heroTone: "green", cats: "bento", catPhotos: "yours", trust: "on",
                   deliv: "green", story: "light", storyPhoto: "kitchen", trade: "table", labels: "off" };
  var KEY = "regency-mix-v1";
  var state = {};
  try { state = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { state = {}; }
  Object.keys(DEFAULTS).forEach(function (k) { if (!(k in state)) state[k] = DEFAULTS[k]; });
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }

  function setImg(el, k) { if (!IMG[k]) return; if (el.getAttribute("src") !== IMG[k]) el.src = IMG[k]; }

  /* static images */
  $$("[data-k]").forEach(function (el) { setImg(el, el.dataset.k); });

  function showSlot(name, v) {
    $$('.mx-v[data-slot="' + name + '"]').forEach(function (el) { el.hidden = el.dataset.v !== v; });
  }

  function apply() {
    showSlot("hero", "split");
    showSlot("cats", state.cats);
    showSlot("trust", state.trust);
    showSlot("deliv", state.deliv);
    showSlot("story", state.story);
    showSlot("trade", state.trade);
    var news = $("[data-news-wrap]"); if (news) news.hidden = state.trade === "cards";

    var hero = $(".mx-hero"), hi = $("[data-hero]");
    if (hi) { setImg(hi, state.heroPhoto); hi.alt = ALT[state.heroPhoto] || ""; }
    if (hero) {
      hero.classList.toggle("mx-hero--left", state.heroSide === "left");
      hero.classList.toggle("mx-hero--cream", state.heroTone === "cream");
      hero.classList.toggle("mx-hero--blue", state.heroTone === "blue");
    }
    var set = CATIMG[state.catPhotos] || CATIMG.yours;
    $$("img[data-cat]").forEach(function (el) { setImg(el, set[el.dataset.cat]); });
    $$("[data-story]").forEach(function (el) { setImg(el, state.storyPhoto); el.alt = ALT[state.storyPhoto] || ""; });
    document.body.classList.toggle("mx-labels", state.labels === "on");
    document.body.classList.toggle("mx-cat-new", state.catPhotos === "new");
    syncPanel();
  }

  /* ---------- panel ---------- */
  var panel = $("#mxPanel"), fab = $("#mxFab"), groups = $("#mxGroups");
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  groups.innerHTML = GROUPS.map(function (g, gi) {
    var head = '<div class="mx-gh"><h3>' + esc(g.title) + "</h3>" + (g.jump ? '<a class="mx-jump" href="#' + g.jump + '">Show me</a>' : "") + "</div>";
    if (g.note) head += '<p class="mx-note">' + esc(g.note) + "</p>";
    return '<section class="mx-g">' + head + g.controls.map(function (c) {
      var lid = "mxl" + gi + c.key;
      var lab = c.label ? '<p class="mx-cl" id="' + lid + '">' + esc(c.label) + "</p>" : "";
      var aria = c.label ? 'aria-labelledby="' + lid + '"' : 'aria-label="' + esc(g.title) + '"';
      if (c.kind === "thumbs") {
        return lab + '<div class="mx-thumbs" role="radiogroup" ' + aria + ">" + c.opts.map(function (o) {
          return '<button type="button" class="mx-th" role="radio" data-key="' + c.key + '" data-val="' + o + '" aria-label="' + esc((CODE[o] || o) + ": " + (ALT[o] || "")) + '"><img src="' + (IMG[o] || "") + '" alt="" loading="lazy"><span>' + esc(CODE[o] || o) + "</span></button>";
        }).join("") + "</div>";
      }
      return lab + '<div class="mx-chips" role="radiogroup" ' + aria + ">" + c.opts.map(function (o) {
        return '<button type="button" class="mx-chip" role="radio" data-key="' + c.key + '" data-val="' + o[0] + '">' + esc(o[1]) + "</button>";
      }).join("") + "</div>";
    }).join("") + "</section>";
  }).join("");

  function syncPanel() {
    $$("[data-key]", groups).forEach(function (b) {
      var on = state[b.dataset.key] === b.dataset.val;
      b.setAttribute("aria-checked", String(on));
      b.tabIndex = on ? 0 : -1;
    });
  }

  function jumpFor(key) {
    for (var i = 0; i < GROUPS.length; i++) for (var j = 0; j < GROUPS[i].controls.length; j++) if (GROUPS[i].controls[j].key === key) return GROUPS[i].jump;
    return null;
  }
  function reveal(id) {
    var el = id && document.getElementById(id);
    if (!el) return;
    var r = el.getBoundingClientRect(), vh = window.innerHeight;
    if (r.top > vh * 0.6 || r.bottom < 120) el.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
  }

  function choose(key, val, noJump) {
    state[key] = val; save(); apply(); afterSwitch();
    if (!noJump) reveal(key === "trade" && val === "cards" ? "trade" : jumpFor(key));
  }

  groups.addEventListener("click", function (e) {
    var b = e.target.closest("[data-key]");
    if (b) { choose(b.dataset.key, b.dataset.val); return; }
    var j = e.target.closest(".mx-jump");
    if (j) { e.preventDefault(); var t = document.getElementById(j.getAttribute("href").slice(1)); if (t) t.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" }); if (narrow()) openPanel(false); }
  });
  /* arrow keys inside each radio group */
  groups.addEventListener("keydown", function (e) {
    var b = e.target.closest("[data-key]"); if (!b) return;
    var dir = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key]; if (!dir) return;
    e.preventDefault();
    var sib = $$("[data-key]", b.parentNode), i = sib.indexOf(b), n = sib[(i + dir + sib.length) % sib.length];
    choose(n.dataset.key, n.dataset.val); n.focus();
  });

  function narrow() { return window.innerWidth < 1200; }
  function openPanel(on) {
    panel.hidden = !on;
    fab.setAttribute("aria-expanded", String(on));
    document.body.classList.toggle("mx-open", on);
    try { localStorage.setItem(KEY + "-open", on ? "1" : "0"); } catch (e) {}
  }
  fab.addEventListener("click", function () { openPanel(panel.hidden); if (!panel.hidden) $("#mxClose").focus(); });
  $("#mxClose").addEventListener("click", function () { openPanel(false); fab.focus(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden && narrow() && !document.querySelector("dialog[open]")) { openPanel(false); fab.focus(); } });

  /* ---------- copy, shuffle, reset ---------- */
  function label(key) {
    for (var i = 0; i < GROUPS.length; i++) for (var j = 0; j < GROUPS[i].controls.length; j++) {
      var c = GROUPS[i].controls[j];
      if (c.key !== key) continue;
      if (c.kind === "thumbs") return CODE[state[key]] ? (state[key] === "kitchen" ? "your kitchen photo" : "your " + CODE[state[key]].toLowerCase() + " photo") : state[key];
      for (var k = 0; k < c.opts.length; k++) if (c.opts[k][0] === state[key]) return c.opts[k][1];
    }
    return state[key];
  }
  function summary() {
    return [
      "Hero: photo " + label("heroPhoto") + ", photo on the " + label("heroSide").toLowerCase() + ", " + label("heroTone") + " panel",
      "Shop by category: " + label("cats") + ", " + label("catPhotos").toLowerCase(),
      "Trusted-by strip: " + label("trust"),
      "Delivery & van: " + label("deliv"),
      "Our story: " + label("story") + ", photo " + label("storyPhoto"),
      "Trade account: " + label("trade"),
      "Small labels: " + label("labels")
    ].join("\n");
  }
  var msg = $("#mxMsg"), out = $("#mxOut"), mt;
  function say(t) { msg.textContent = t; clearTimeout(mt); mt = setTimeout(function () { msg.textContent = ""; }, 3200); }
  $("#mxCopy").addEventListener("click", function () {
    var text = summary();
    function fallback() { out.hidden = false; out.value = text; out.focus(); out.select(); say("Select all and copy, then paste it into the chat."); }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { out.hidden = true; say("Copied. Paste it into the chat."); }, fallback);
    } else fallback();
  });
  $("#mxShuffle").addEventListener("click", function () {
    GROUPS.forEach(function (g) { g.controls.forEach(function (c) {
      if (c.key === "labels") return;
      var vals = c.opts.map(function (o) { return c.kind === "thumbs" ? o : o[0]; });
      state[c.key] = vals[Math.floor(Math.random() * vals.length)];
    }); });
    save(); apply(); afterSwitch(); say("Shuffled. Scroll through to see the new mix.");
    window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
  });
  $("#mxReset").addEventListener("click", function () {
    Object.keys(DEFAULTS).forEach(function (k) { state[k] = DEFAULTS[k]; });
    save(); apply(); afterSwitch(); say("Back to the starting mix.");
  });

  /* ---------- section behaviours ---------- */
  /* Numbered list: hovering a row swaps the big preview */
  var prev = $("#bPreview");
  if (prev) {
    var rows = $$(".b-row");
    var show = function (r) {
      rows.forEach(function (x) { x.classList.toggle("on", x === r); });
      prev.dataset.cat = r.dataset.pv;
      var k = (CATIMG[state.catPhotos] || CATIMG.yours)[r.dataset.pv];
      if (prev.getAttribute("src") === IMG[k]) return;
      prev.style.opacity = 0;
      setTimeout(function () { setImg(prev, k); prev.style.opacity = 1; }, reduce ? 0 : 150);
    };
    rows.forEach(function (r) {
      r.addEventListener("pointerenter", function () { show(r); });
      r.addEventListener("focus", function () { show(r); });
    });
    if (rows[0]) rows[0].classList.add("on");
  }

  /* Dark Green delivery: the van drives in each time the section appears */
  var vanIO = null;
  function afterSwitch() {
    var van = $('.mx-v:not([hidden]) .a-van[data-drive]');
    if (!van || reduce || !("IntersectionObserver" in window)) return;
    document.documentElement.classList.add("js-drive");
    van.classList.remove("in");
    if (vanIO) vanIO.disconnect();
    vanIO = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { van.classList.add("in"); vanIO.disconnect(); } });
    }, { threshold: 0.3 });
    vanIO.observe(van);
  }

  /* Extra forms in the variants (the main trade form and newsletter are handled by app.js) */
  $$("form[data-mx-form], form[data-mx-news]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var req = $$("[required]", f), err = $(".err", f);
      var bad = req.filter(function (i) { return !i.value.trim() || (i.type === "email" && !/^\S+@\S+\.\S+$/.test(i.value)); });
      req.forEach(function (i) { i.setAttribute("aria-invalid", bad.indexOf(i) > -1 ? "true" : "false"); });
      if (bad.length) { if (err) err.textContent = f.hasAttribute("data-mx-news") ? "Enter a valid email address to subscribe." : "Please add your name, business and a valid work email."; bad[0].focus(); return; }
      var biz = $("[data-biz]", f);
      var title = f.hasAttribute("data-mx-news") ? "You’re on the list." : "Thanks, " + esc(biz ? biz.value.trim() : "") + ".";
      var note = f.hasAttribute("data-mx-news") ? "Look out for new arrivals and offers." : "Your request is with us. An account manager will be in touch shortly with pricing.";
      f.innerHTML = '<div class="mx-done" tabindex="-1"><h3>' + title + "</h3><p>" + note + "</p></div>";
      $(".mx-done", f).focus();
    });
  });

  apply();
  afterSwitch();
  var wasOpen = null; try { wasOpen = localStorage.getItem(KEY + "-open"); } catch (e) {}
  openPanel(wasOpen === null ? !narrow() : wasOpen === "1" && !narrow());
})();
