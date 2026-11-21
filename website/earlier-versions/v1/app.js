/* Regency Foods — "The Docket". No dependencies. */
(function () {
  "use strict";

  /* ------------------------------------------------------------------
     The range. Pecan (£16.45) is the only confirmed price.
     TODO before launch: confirm Almond and Pistachio prices, their
     descriptions and ingredients, and every nutrition figure (the brand
     guidelines mark the pack nutrition values as placeholders too).
     ------------------------------------------------------------------ */
  var RANGE = [
    { id: "almond", name: "Almond", descriptor: "100% Raw Organic", price: 12.95, colour: "var(--yellow)", dot: "#F2C44B",
      pack: "assets/img/pack-almond.png",
      about: "Whole, raw organic almonds with a clean, sweet crunch. Perfect for baking, granola, salads and snacking.",
      ingredients: "<b>Almonds</b> (100%).",
      allergy: "For allergens, see ingredients in <b>bold</b>. Packed in a facility that also handles other tree nuts and peanuts.",
      nutrition: [["Energy", "2534 kJ / 612 kcal"], ["Fat", "55.8 g"], ["of which saturates", "4.3 g", 1], ["Carbohydrate", "6.9 g"], ["of which sugars", "4.2 g", 1], ["Fibre", "7.4 g"], ["Protein", "21.1 g"], ["Salt", "0.01 g"]] },
    { id: "pecan", name: "Pecan", descriptor: "Mildly Roasted", price: 16.45, colour: "var(--orange)", dot: "#E85A10",
      pack: "assets/img/pack-pecan.png",
      about: "Hand-selected pecan halves, mildly roasted for a rich, buttery crunch. Rich in healthy fats, vitamin E and minerals like manganese and copper. Perfect for baking, salads and snacking.",
      ingredients: "<b>Pecan nuts</b> (100%).",
      allergy: "For allergens, see ingredients in <b>bold</b>: <b>pecans</b>. Packed in a facility that also handles other tree nuts and peanuts.",
      nutrition: [["Energy", "2895 kJ / 702 kcal"], ["Fat", "70.1 g"], ["of which saturates", "5.7 g", 1], ["Carbohydrate", "5.8 g"], ["of which sugars", "4.3 g", 1], ["Fibre", "4.7 g"], ["Protein", "9.2 g"], ["Salt", "0.01 g"]] },
    { id: "pistachio", name: "Pistachio", descriptor: "Premium Roasted", price: 19.50, colour: "var(--bright)", dot: "#44AF5D",
      pack: "assets/img/pack-pistachio.png",
      about: "Premium pistachios, roasted in the shell for a rich, savoury crunch. Made for the snack bowl, salads, pastry and desserts.",
      ingredients: "<b>Pistachio nuts</b> (100%).",
      allergy: "For allergens, see ingredients in <b>bold</b>. Packed in a facility that also handles other tree nuts and peanuts.",
      nutrition: [["Energy", "2459 kJ / 594 kcal"], ["Fat", "48.5 g"], ["of which saturates", "5.9 g", 1], ["Carbohydrate", "17.6 g"], ["of which sugars", "7.7 g", 1], ["Fibre", "10.3 g"], ["Protein", "20.6 g"], ["Salt", "0.01 g"]] }
  ];
  var BY = {}; RANGE.forEach(function (p) { BY[p.id] = p; });
  var gbp = new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP" });
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var canHover = window.matchMedia && matchMedia("(hover: hover) and (pointer: fine)").matches;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };

  /* ---------- Small timer: counts down to local midnight ---------- */
  var timers = $$("[data-timer]");
  function tick() {
    var now = new Date(), mid = new Date(now); mid.setHours(24, 0, 0, 0);
    var s = Math.max(0, Math.floor((mid - now) / 1000));
    var str = String(Math.floor(s / 3600)).padStart(2, "0") + ":" + String(Math.floor(s / 60) % 60).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0");
    timers.forEach(function (t) { t.textContent = str; });
  }
  tick(); setInterval(tick, 1000);
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- The shelf ---------- */
  var shelf = $("#shelf");
  shelf.innerHTML = RANGE.map(function (p) {
    return '<div class="bay" data-bay="' + p.id + '" style="--c:' + p.colour + '">' +
      '<button class="facing" type="button" data-open-product="' + p.id + '" aria-label="Take ' + p.name + ' off the shelf: see ingredients and nutrition">' +
        '<span class="pouch"><img src="' + p.pack + '" alt="Regency Foods ' + p.name + ', ' + p.descriptor.toLowerCase() + ', 1 kg resealable pack" draggable="false"><span class="sheen"></span></span>' +
        '<span class="contact" aria-hidden="true"></span>' +
      '</button>' +
      '<div class="board" aria-hidden="true"></div>' +
      '<div class="sel">' +
        '<div class="top"><div><h3>' + p.name + '</h3><p class="desc">' + p.descriptor + '</p></div>' +
        '<div style="text-align:right"><p class="price">' + gbp.format(p.price) + '</p><p class="unit">' + gbp.format(p.price / 10) + ' / 100 g</p></div></div>' +
        '<div class="row"><span class="qty" role="group" aria-label="Quantity of ' + p.name + '"><button type="button" data-step="-1" aria-label="Decrease">−</button><output data-q>1</output><button type="button" data-step="1" aria-label="Increase">+</button></span>' +
        '<button class="btn btn--green add" type="button" data-add="' + p.id + '">Add to docket</button></div>' +
        '<button class="more" type="button" data-open-product="' + p.id + '" data-turned>Ingredients &amp; nutrition</button>' +
      '</div></div>';
  }).join("");

  /* Hover: the pack lifts off the shelf, tilts toward the cursor and catches the light */
  if (canHover && !reduce) {
    $$(".facing", shelf).forEach(function (f) {
      var pouch = $(".pouch", f), raf = 0, px = 0, py = 0;
      f.addEventListener("pointermove", function (e) {
        var r = pouch.getBoundingClientRect();
        px = (e.clientX - r.left) / r.width; py = (e.clientY - r.top) / r.height;
        if (!raf) raf = requestAnimationFrame(function () {
          raf = 0;
          pouch.style.setProperty("--rx", Math.max(-.6, Math.min(.6, px - .5)).toFixed(3));
          pouch.style.setProperty("--ry", Math.max(-.6, Math.min(.6, py - .5)).toFixed(3));
          pouch.style.setProperty("--mx", (px * 100).toFixed(1) + "%");
          pouch.style.setProperty("--my", (py * 100).toFixed(1) + "%");
        });
      });
      f.addEventListener("pointerleave", function () {
        pouch.style.setProperty("--rx", 0); pouch.style.setProperty("--ry", 0);
      });
    });
  }

  /* Quantity steppers */
  document.addEventListener("click", function (e) {
    var s = e.target.closest("[data-step]"); if (!s) return;
    var out = s.parentNode.querySelector("[data-q]");
    out.textContent = Math.max(1, Math.min(99, (+out.textContent || 1) + (+s.dataset.step)));
  });

  /* ---------- The docket (basket) ---------- */
  var basket = store.get("rf-docket", {}), sub = store.get("rf-sub", false), fresh = null;
  Object.keys(basket).forEach(function (k) { if (!BY[k]) delete basket[k]; });
  var paper = $("#paper"), tab = $("#docketTab"), autoClose = 0;

  function save() { store.set("rf-docket", basket); }
  function render() {
    var ids = Object.keys(basket), n = 0, total = 0;
    ids.forEach(function (k) { n += basket[k]; total += basket[k] * BY[k].price; });
    $$("[data-count]").forEach(function (el) { el.textContent = n; });
    $$("[data-open-docket]").forEach(function (el) { el.setAttribute("aria-label", "Your docket, " + n + (n === 1 ? " item" : " items")); });
    tab.classList.toggle("hidden-empty", n === 0 && paper.hidden);
    var time = new Date().toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" });
    var off = sub ? total * 0.1 : 0;
    paper.innerHTML =
      '<div class="ph"><span class="logo logo--h" role="img" aria-label="Regency Foods"></span><span class="when">' + time + '</span></div>' +
      (ids.length ? ids.map(function (k) {
        var p = BY[k];
        return '<div class="ln' + (k === fresh ? " new" : "") + '"><span class="q"><button type="button" data-dec="' + k + '" aria-label="Remove one ' + p.name + '">−</button>' + basket[k] + '×<button type="button" data-inc="' + k + '" aria-label="Add one ' + p.name + '">+</button></span>' +
          '<span class="nm">' + p.name + '<small>' + p.descriptor + '</small></span><span>' + gbp.format(p.price * basket[k]) + '</span></div>';
      }).join("") +
        '<label class="sub"><input type="checkbox" id="subBox"' + (sub ? " checked" : "") + '> Subscribe &amp; save 10% on every order</label>' +
        '<div class="tot"><div><span>Subtotal</span><span>' + gbp.format(total) + '</span></div>' +
        (sub ? '<div class="save"><span>Subscribe &amp; save</span><span>−' + gbp.format(off) + '</span></div>' : '') +
        '<div><span>Delivery</span><span>Next day</span></div>' +
        '<div class="g"><span>Total</span><span>' + gbp.format(total - off) + '</span></div></div>' +
        '<button class="btn btn--green send" type="button" id="send">Send order <span aria-hidden="true">→</span></button>' +
        '<p class="cut">Order today, delivered tomorrow.</p>'
      : '<p class="empty">Nothing on the docket yet. Take something off the shelf.</p>');
    fresh = null;
  }
  function openPaper(print) {
    paper.hidden = false; tab.classList.remove("hidden-empty"); tab.setAttribute("aria-expanded", "true");
    if (print && !reduce) { paper.classList.remove("printing"); void paper.offsetWidth; paper.classList.add("printing"); }
  }
  function closePaper() { paper.hidden = true; tab.setAttribute("aria-expanded", "false"); render(); }
  function scheduleClose() {
    clearTimeout(autoClose);
    autoClose = setTimeout(function () { if (!paper.matches(":hover") && !paper.contains(document.activeElement)) closePaper(); }, 4000);
  }
  function add(id, q) {
    basket[id] = (basket[id] || 0) + q; fresh = id; save(); render();
    openPaper(true); scheduleClose();
    $$("[data-count]").forEach(function (el) { el.classList.remove("bump"); void el.offsetWidth; el.classList.add("bump"); });
    var bay = $('[data-bay="' + id + '"]');
    if (bay && !reduce) { bay.classList.remove("picked"); void bay.offsetWidth; bay.classList.add("picked"); }
    toast(q + " × " + BY[id].name + " on the docket");
  }
  tab.addEventListener("click", function () { clearTimeout(autoClose); if (paper.hidden) { openPaper(true); } else { closePaper(); } });
  paper.addEventListener("pointerenter", function () { clearTimeout(autoClose); });
  paper.addEventListener("change", function (e) { if (e.target.id === "subBox") { sub = e.target.checked; store.set("rf-sub", sub); render(); } });

  document.addEventListener("click", function (e) {
    var t;
    if ((t = e.target.closest("[data-add]"))) {
      var q = t.parentNode.querySelector("[data-q]");
      add(t.dataset.add, q ? +q.textContent : 1);
      if (q) q.textContent = 1;
    } else if ((t = e.target.closest("[data-inc]"))) { clearTimeout(autoClose); basket[t.dataset.inc]++; save(); render(); }
    else if ((t = e.target.closest("[data-dec]"))) { clearTimeout(autoClose); var k = t.dataset.dec; if (--basket[k] <= 0) delete basket[k]; save(); render(); }
    else if (e.target.closest("[data-open-docket]")) { clearTimeout(autoClose); openPaper(true); var b = $("#send") || tab; b.focus(); }
    else if (e.target.closest("#send")) toast("Checkout isn't connected yet. Plug in your payment provider here.");
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !paper.hidden && !$("#pd").open) { closePaper(); tab.focus(); } });

  /* ---------- Product dialog: turn the pack over ---------- */
  var pd = $("#pd"), lastFocus = null;
  function back(p) {
    return '<div class="face back" style="--c:' + p.colour + '"><div class="panel">' +
      '<div class="ptop"><div><h3>' + p.name + '</h3><p class="label">' + p.descriptor + '</p></div><span class="logo logo--s" role="img" aria-label="Regency Foods"></span></div>' +
      '<p>' + esc(p.about.split(". ")[0]) + '.</p>' +
      '<div><span class="k">Ingredients</span>' + p.ingredients + '</div>' +
      '<div><span class="k">Allergy advice</span>' + p.allergy + '</div>' +
      '<div><span class="k">Storage</span>Store in a cool, dry place away from direct sunlight. Once opened, reseal and enjoy within 4 weeks.</div>' +
      '<table><thead><tr><th scope="col">Nutrition</th><th scope="col">Per 100 g</th></tr></thead><tbody>' +
      p.nutrition.map(function (r) { return '<tr' + (r[2] ? ' class="ind"' : '') + '><td>' + r[0] + '</td><td>' + r[1] + '</td></tr>'; }).join("") +
      '</tbody></table>' +
      '<div class="sign"><b>From Our Kitchen<br>to Yours</b><span>1 kg ℮</span></div>' +
    '</div></div>';
  }
  function openProduct(id, turned) {
    var p = BY[id];
    pd.innerHTML = '<div class="pd-in">' +
      '<button class="pd-close" type="button" data-close-pd aria-label="Close">✕</button>' +
      '<div class="pd-stage">' +
        '<div class="pack' + (turned ? " turned" : "") + '" id="pack"><div class="flip">' +
          '<div class="face front"><img src="' + p.pack + '" alt="Front of the Regency Foods ' + p.name + ' 1 kg pack"></div>' + back(p) +
        '</div></div>' +
        '<button class="btn turn" type="button" id="turnBtn" aria-pressed="' + !!turned + '" aria-controls="pack"><span class="ic" aria-hidden="true">↻</span> <span id="turnLbl">' + (turned ? "Show the front" : "Turn it over") + '</span></button>' +
      '</div>' +
      '<div class="pd-info">' +
        '<h2 id="pdName">' + p.name + '</h2>' +
        '<p class="descriptor">' + p.descriptor + ', 1 kg</p>' +
        '<p class="price">' + gbp.format(p.price) + '<small>' + gbp.format(p.price / 10) + ' per 100 g</small></p>' +
        '<p class="about">' + esc(p.about) + '</p>' +
        '<div class="buy"><span class="qty" role="group" aria-label="Quantity"><button type="button" data-step="-1" aria-label="Decrease">−</button><output data-q>1</output><button type="button" data-step="1" aria-label="Increase">+</button></span>' +
        '<button class="btn btn--green" type="button" data-add="' + p.id + '">Add to docket</button></div>' +
        
        '<div class="switch" role="group" aria-label="Other products">' + RANGE.map(function (q) {
          return '<button type="button" data-switch="' + q.id + '"' + (q.id === p.id ? ' aria-current="true"' : '') + '><i style="background:' + q.dot + '"></i>' + q.name + '</button>';
        }).join("") + '</div>' +
      '</div></div>';
    if (!pd.open) { lastFocus = document.activeElement; pd.showModal(); }
    pd.scrollTop = 0;
  }
  function turn() {
    var pack = $("#pack"), on = !pack.classList.contains("turned");
    pack.classList.toggle("turned", on);
    $("#turnBtn").setAttribute("aria-pressed", String(on));
    $("#turnLbl").textContent = on ? "Show the front" : "Turn it over";
  }
  pd.addEventListener("click", function (e) {
    if (e.target === pd || e.target.closest("[data-close-pd]")) { pd.close(); return; }
    var sw = e.target.closest("[data-switch]");
    if (sw) { openProduct(sw.dataset.switch, $("#pack").classList.contains("turned")); $('[data-switch="' + sw.dataset.switch + '"]', pd).focus(); return; }
    if (e.target.closest("#turnBtn") || e.target.closest(".face.front")) turn();
  });
  pd.addEventListener("close", function () { if (lastFocus && lastFocus.focus) lastFocus.focus(); });
  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-open-product]");
    if (!t || pd.contains(t)) return;
    e.preventDefault();
    openProduct(t.dataset.openProduct, t.hasAttribute("data-turned"));
  });

  /* ---------- Category tickets (aisle pages come next) ---------- */
  $$("[data-aisle]").forEach(function (a) {
    a.addEventListener("click", function (e) { e.preventDefault(); toast(a.dataset.aisle + ": aisle page coming soon"); });
  });

  /* ---------- Navigation ---------- */
  var mb = $("#menuBtn"), mn = $("#mnav");
  mb.addEventListener("click", function () { var open = mn.hidden; mn.hidden = !open; mb.setAttribute("aria-expanded", String(open)); mb.setAttribute("aria-label", open ? "Close menu" : "Open menu"); });
  $$("a", mn).forEach(function (a) { a.addEventListener("click", function () { mn.hidden = true; mb.setAttribute("aria-expanded", "false"); mb.setAttribute("aria-label", "Open menu"); }); });
  if ("IntersectionObserver" in window) {
    var links = $$(".nav a");
    var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) links.forEach(function (a) { a.setAttribute("aria-current", a.getAttribute("href") === "#" + en.target.id ? "true" : "false"); }); }); }, { rootMargin: "-45% 0px -50% 0px" });
    ["shop", "range", "delivery", "trade", "story"].forEach(function (id) { var el = document.getElementById(id); if (el) io.observe(el); });
  }

  /* ---------- Forms ---------- */
  var tf = $("#tradeForm");
  tf.addEventListener("submit", function (e) {
    e.preventDefault();
    var req = $$("[required]", tf);
    var bad = req.filter(function (i) { return !i.value.trim() || (i.type === "email" && !/^\S+@\S+\.\S+$/.test(i.value)); });
    req.forEach(function (i) { i.setAttribute("aria-invalid", bad.indexOf(i) > -1 ? "true" : "false"); });
    if (bad.length) { $("#tfErr").textContent = "Please add your name, business and a valid work email."; bad[0].focus(); return; }
    var biz = esc($("#tfBiz").value.trim());
    tf.innerHTML = '<div class="received"><span class="stamp">Received</span><h3>Thanks, ' + biz + '.</h3><p class="note">Your request is with us. An account manager will be in touch shortly with pricing.</p></div>';
  });
  $("#newsForm").addEventListener("submit", function (e) {
    e.preventDefault();
    var i = $("#newsEmail"), ok = /^\S+@\S+\.\S+$/.test(i.value);
    i.setAttribute("aria-invalid", ok ? "false" : "true");
    $("#newsMsg").textContent = ok ? "You're on the list. Look out for new arrivals and offers." : "Enter a valid email address to subscribe.";
    if (ok) this.reset();
  });

  var tt;
  function toast(m) { var t = $("#toast"); t.textContent = m; t.classList.add("show"); clearTimeout(tt); tt = setTimeout(function () { t.classList.remove("show"); }, 2200); }
  render();
})();
