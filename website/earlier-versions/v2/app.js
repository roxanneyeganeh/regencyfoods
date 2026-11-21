/* Regency Foods — site behaviour. No dependencies. */
(function () {
  "use strict";

  /* ------------------------------------------------------------------
     The range. Only Pecan's price (£16.45) is confirmed.
     TODO before launch: confirm Almond and Pistachio prices, descriptions,
     ingredients and every nutrition figure (the brand guidelines mark the
     pack nutrition values as placeholders too).
     ------------------------------------------------------------------ */
  var RANGE = [
    {
      id: "almond", name: "Almond", descriptor: "100% Raw Organic", price: 12.95,
      shot: "assets/img/plinth-almond.jpg", pack: "assets/img/pack-almond.png",
      line: "Whole raw organic almonds with a clean, sweet crunch.",
      about: "Whole, raw organic almonds with a clean, sweet crunch. Perfect for baking, granola, salads and snacking.",
      ingredients: "<b>Almonds</b> (100%).",
      allergy: "For allergens, see ingredients in <b>bold</b>. Packed in a facility that also handles other tree nuts and peanuts.",
      nutrition: [["Energy", "2534 kJ / 612 kcal"], ["Fat", "55.8 g"], ["of which saturates", "4.3 g", 1], ["Carbohydrate", "6.9 g"], ["of which sugars", "4.2 g", 1], ["Fibre", "7.4 g"], ["Protein", "21.1 g"], ["Salt", "0.01 g"]]
    },
    {
      id: "pecan", name: "Pecan", descriptor: "Mildly Roasted", price: 16.45,
      shot: "assets/img/plinth-pecan.jpg", pack: "assets/img/pack-pecan.png",
      line: "Hand-selected halves, mildly roasted for a rich, buttery crunch.",
      about: "Hand-selected pecan halves, mildly roasted for a rich, buttery crunch. Rich in healthy fats, vitamin E and minerals like manganese and copper. Perfect for baking, salads and snacking.",
      ingredients: "<b>Pecan nuts</b> (100%).",
      allergy: "For allergens, see ingredients in <b>bold</b>: <b>pecans</b>. Packed in a facility that also handles other tree nuts and peanuts.",
      nutrition: [["Energy", "2895 kJ / 702 kcal"], ["Fat", "70.1 g"], ["of which saturates", "5.7 g", 1], ["Carbohydrate", "5.8 g"], ["of which sugars", "4.3 g", 1], ["Fibre", "4.7 g"], ["Protein", "9.2 g"], ["Salt", "0.01 g"]]
    },
    {
      id: "pistachio", name: "Pistachio", descriptor: "Premium Roasted", price: 19.50,
      shot: "assets/img/plinth-pistachio.jpg", pack: "assets/img/pack-pistachio.png",
      line: "Premium pistachios, roasted in the shell for a rich, savoury crunch.",
      about: "Premium pistachios, roasted in the shell for a rich, savoury crunch. Made for the snack bowl, salads, pastry and desserts.",
      ingredients: "<b>Pistachio nuts</b> (100%).",
      allergy: "For allergens, see ingredients in <b>bold</b>. Packed in a facility that also handles other tree nuts and peanuts.",
      nutrition: [["Energy", "2459 kJ / 594 kcal"], ["Fat", "48.5 g"], ["of which saturates", "5.9 g", 1], ["Carbohydrate", "17.6 g"], ["of which sugars", "7.7 g", 1], ["Fibre", "10.3 g"], ["Protein", "20.6 g"], ["Salt", "0.01 g"]]
    }
  ];
  var BY = {}; RANGE.forEach(function (p) { BY[p.id] = p; });
  var SUB_OFF = 0.10;
  var gbp = new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP" });
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };

  /* ---------- Range cards ---------- */
  $("#rangeGrid").innerHTML = RANGE.map(function (p) {
    return '<article class="product product--' + p.id + '" aria-labelledby="n-' + p.id + '">' +
      '<button class="shot" type="button" data-open-product="' + p.id + '" aria-label="View ' + p.name + ' details">' +
        '<img src="' + p.shot + '" alt="Regency Foods ' + p.name + ' 1 kg pouch on a ' + p.id + '-coloured plinth" loading="lazy">' +
        '<span class="tab peek">Turn it over</span>' +
      '</button>' +
      '<div class="info">' +
        '<div><h3 class="dim dim--' + p.id + ' name" id="n-' + p.id + '">' + p.name + '</h3><p class="desc" style="margin-top:8px">' + p.descriptor + '</p></div>' +
        '<hr class="stitch">' +
        '<p class="pline">' + esc(p.line) + '</p>' +
        '<div class="row"><span class="price">' + gbp.format(p.price) + '<small>1 kg</small></span>' +
          '<button class="details-link" type="button" data-open-product="' + p.id + '">Ingredients &amp; nutrition</button></div>' +
        '<div class="buy">' +
          '<span class="qty" role="group" aria-label="Quantity of ' + p.name + '"><button type="button" data-step="-1" aria-label="Decrease">−</button><output data-q>1</output><button type="button" data-step="1" aria-label="Increase">+</button></span>' +
          '<button class="btn btn--ink" type="button" data-add="' + p.id + '">Add to basket</button>' +
        '</div>' +
      '</div></article>';
  }).join("");

  /* Quantity steppers (cards and dialog) */
  document.addEventListener("click", function (e) {
    var s = e.target.closest("[data-step]");
    if (!s) return;
    var out = s.parentNode.querySelector("[data-q]");
    var v = Math.max(1, Math.min(99, (+out.textContent || 1) + (+s.dataset.step)));
    out.textContent = v;
  });

  /* ---------- Basket ---------- */
  var basket = store.get("rf-basket", {});
  var subscribe = store.get("rf-subscribe", false);
  Object.keys(basket).forEach(function (k) { if (!BY[k]) delete basket[k]; });
  var drawer = $("#drawer"), scrim = $("#scrim"), body = $("#drawerBody"), foot = $("#drawerFoot");

  function save() { store.set("rf-basket", basket); }
  function render() {
    var ids = Object.keys(basket), n = 0, total = 0;
    ids.forEach(function (k) { n += basket[k]; total += basket[k] * BY[k].price; });
    $$("[data-count]").forEach(function (el) { el.textContent = n; });
    $$("[data-open-basket]").forEach(function (el) { el.setAttribute("aria-label", "Basket, " + n + (n === 1 ? " item" : " items")); });
    if (!ids.length) {
      body.innerHTML = '<div class="empty"><p>Your basket is empty. Order today and it arrives tomorrow.</p><a class="btn btn--green" href="#range" data-close-drawer>Shop the range</a></div>';
      foot.innerHTML = "";
      return;
    }
    body.innerHTML = ids.map(function (k) {
      var p = BY[k];
      return '<div class="line"><img src="' + p.pack + '" alt="">' +
        '<div><div class="nm">' + p.name + '</div><div class="meta">' + p.descriptor + ' · 1 kg · ' + gbp.format(p.price) + '</div>' +
        '<span class="qty" role="group" aria-label="Quantity of ' + p.name + '"><button type="button" data-dec="' + k + '" aria-label="Remove one ' + p.name + '">−</button><output>' + basket[k] + '</output><button type="button" data-inc="' + k + '" aria-label="Add one ' + p.name + '">+</button></span></div>' +
        '<div class="lp"><span>' + gbp.format(p.price * basket[k]) + '</span><button class="rm" type="button" data-rm="' + k + '">Remove</button></div></div>';
    }).join("");
    var off = subscribe ? total * SUB_OFF : 0;
    foot.innerHTML =
      '<label class="sub" for="subBox"><span><input type="checkbox" id="subBox"' + (subscribe ? " checked" : "") + '> Subscribe &amp; save</span><em>−10% every order</em></label>' +
      '<div class="tr"><span>Subtotal</span><span>' + gbp.format(total) + '</span></div>' +
      (subscribe ? '<div class="tr save"><span>Subscribe &amp; save</span><span>−' + gbp.format(off) + '</span></div>' : '') +
      '<div class="tr"><span>Delivery</span><span>Next day</span></div>' +
      '<div class="tr total"><span>Total</span><span>' + gbp.format(total - off) + '</span></div>' +
      '<button class="btn btn--green" type="button" id="checkout">Checkout <span class="arr" aria-hidden="true">→</span></button>';
  }
  function add(id, q) {
    basket[id] = (basket[id] || 0) + q; save(); render();
    $$("[data-count]").forEach(function (el) { el.classList.remove("bump"); void el.offsetWidth; el.classList.add("bump"); });
    toast(q + " × " + BY[id].name + " added to your basket");
  }

  var lastFocus = null;
  function openDrawer() {
    lastFocus = document.activeElement;
    drawer.hidden = false; scrim.hidden = false;
    requestAnimationFrame(function () { drawer.classList.add("open"); scrim.classList.add("open"); });
    document.body.style.overflow = "hidden";
    setTimeout(function () { $("#drawerClose").focus(); }, 60);
  }
  function closeDrawer() {
    if (drawer.hidden) return;
    drawer.classList.remove("open"); scrim.classList.remove("open");
    document.body.style.overflow = "";
    setTimeout(function () { drawer.hidden = true; scrim.hidden = true; }, reduce ? 0 : 350);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  $("#drawerClose").addEventListener("click", closeDrawer);
  scrim.addEventListener("click", closeDrawer);
  drawer.addEventListener("change", function (e) { if (e.target.id === "subBox") { subscribe = e.target.checked; store.set("rf-subscribe", subscribe); render(); } });

  document.addEventListener("click", function (e) {
    var t;
    if ((t = e.target.closest("[data-add]"))) {
      var q = t.parentNode.querySelector("[data-q]");
      add(t.dataset.add, q ? +q.textContent : 1);
      if (q) q.textContent = 1;
    } else if ((t = e.target.closest("[data-inc]"))) { basket[t.dataset.inc]++; save(); render(); }
    else if ((t = e.target.closest("[data-dec]"))) { var k = t.dataset.dec; if (--basket[k] <= 0) delete basket[k]; save(); render(); }
    else if ((t = e.target.closest("[data-rm]"))) { delete basket[t.dataset.rm]; save(); render(); }
    else if (e.target.closest("[data-open-basket]")) openDrawer();
    else if (e.target.closest("[data-close-drawer]")) closeDrawer();
    else if (e.target.closest("#checkout")) toast("Checkout isn't connected yet. Plug in your payment provider here.");
  });

  /* ---------- Product dialog with turn-over pack ---------- */
  var pd = $("#pd");
  function backOfPack(p) {
    return '<div class="face back ' + p.id + '"><div class="bh"></div><div class="panel">' +
      '<div class="ptop"><div><h3>' + p.name + '</h3><p class="desc">' + p.descriptor + '</p></div><span class="logo logo--s" role="img" aria-label="Regency Foods"></span></div>' +
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
  function openProduct(id, opts) {
    var p = BY[id];
    pd.innerHTML =
      '<div class="pd-in">' +
        '<button class="pd-close" type="button" data-close-pd aria-label="Close">✕</button>' +
        '<div class="pd-stage ' + p.id + '">' +
          '<div class="pack' + (opts && opts.turned ? ' turned' : '') + '" id="pack"><div class="flip">' +
            '<div class="face front"><img src="' + p.pack + '" alt="Front of the Regency Foods ' + p.name + ' 1 kg pack"></div>' +
            backOfPack(p) +
          '</div></div>' +
          '<button class="btn turn" type="button" id="turnBtn" aria-pressed="' + (opts && opts.turned ? "true" : "false") + '" aria-controls="pack"><span class="ic" aria-hidden="true">↻</span> <span id="turnLbl">' + (opts && opts.turned ? "Show the front" : "Turn it over") + '</span></button>' +
        '</div>' +
        '<div class="pd-info">' +
          '<div class="namewrap ' + p.id + '"><h2 class="dim dim--' + p.id + '" id="pdName">' + p.name + '</h2><p class="desc">' + p.descriptor + '</p></div>' +
          '<p class="price">' + gbp.format(p.price) + '<small>1 kg · ' + gbp.format(p.price / 10) + ' per 100 g</small></p>' +
          '<p class="about">' + esc(p.about) + '</p>' +
          '<div class="tabs"><span class="tab">Resealable pack</span><span class="tab">Net wt 1 kg / 2.2 lb</span><span class="tab">Next-day delivery</span></div>' +
          '<div class="buy"><span class="qty" role="group" aria-label="Quantity"><button type="button" data-step="-1" aria-label="Decrease">−</button><output data-q>1</output><button type="button" data-step="1" aria-label="Increase">+</button></span>' +
          '<button class="btn btn--green" type="button" data-add="' + p.id + '">Add to basket</button></div>' +
          '<div class="switch" role="group" aria-label="Other products">' + RANGE.map(function (q) {
            return '<button type="button" data-switch="' + q.id + '"' + (q.id === p.id ? ' aria-current="true"' : '') + '><i style="background:var(--' + (q.id === "almond" ? "yellow" : q.id === "pecan" ? "orange" : "bright") + ')"></i>' + q.name + '</button>';
          }).join("") + '</div>' +
        '</div>' +
      '</div>';
    if (!pd.open) { lastFocus = document.activeElement; pd.showModal(); }
    pd.scrollTop = 0;
  }
  pd.addEventListener("click", function (e) {
    if (e.target === pd || e.target.closest("[data-close-pd]")) { pd.close(); return; }
    var sw = e.target.closest("[data-switch]");
    if (sw) { var turned = $("#pack").classList.contains("turned"); openProduct(sw.dataset.switch, { turned: turned }); $('[data-switch="' + sw.dataset.switch + '"]', pd).focus(); return; }
    if (e.target.closest("#turnBtn") || e.target.closest(".face.front")) {
      var pack = $("#pack"), on = !pack.classList.contains("turned");
      pack.classList.toggle("turned", on);
      $("#turnBtn").setAttribute("aria-pressed", String(on));
      $("#turnLbl").textContent = on ? "Show the front" : "Turn it over";
    }
  });
  pd.addEventListener("close", function () { if (lastFocus && lastFocus.focus) lastFocus.focus(); });
  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-open-product]");
    if (!t || pd.contains(t)) return;
    e.preventDefault();
    openProduct(t.dataset.openProduct, { turned: t.classList.contains("details-link") });
  });

  /* ---------- Mobile menu ---------- */
  var mb = $("#menuBtn"), mn = $("#mnav");
  mb.addEventListener("click", function () {
    var open = mn.hidden; mn.hidden = !open;
    mb.setAttribute("aria-expanded", String(open)); mb.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  });
  $$("a", mn).forEach(function (a) { a.addEventListener("click", function () { mn.hidden = true; mb.setAttribute("aria-expanded", "false"); mb.setAttribute("aria-label", "Open menu"); }); });

  /* Current section in the nav */
  if ("IntersectionObserver" in window) {
    var links = $$(".nav a");
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting) links.forEach(function (a) { a.setAttribute("aria-current", a.getAttribute("href") === "#" + en.target.id ? "true" : "false"); });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    ["range", "supply", "trade", "story", "contact"].forEach(function (id) { var el = document.getElementById(id); if (el) io.observe(el); });
  }

  /* ---------- Posters prefill the trade form ---------- */
  $$(".poster[data-interest]").forEach(function (a) {
    a.addEventListener("click", function () {
      var what = a.dataset.interest; if (!what) return;
      var m = $("#tfMsg"); if (!m.value.trim()) m.value = "I'm interested in " + what.toLowerCase() + ".";
    });
  });

  /* ---------- Forms ---------- */
  var tf = $("#trade-form");
  tf.addEventListener("submit", function (e) {
    e.preventDefault();
    var req = $$("[required]", tf);
    var bad = req.filter(function (i) { return !i.value.trim() || (i.type === "email" && !/^\S+@\S+\.\S+$/.test(i.value)); });
    req.forEach(function (i) { i.setAttribute("aria-invalid", bad.indexOf(i) > -1 ? "true" : "false"); });
    if (bad.length) { $("#tfErr").textContent = "Please add your name, business name and a valid work email."; bad[0].focus(); return; }
    var biz = esc($("#tfBiz").value.trim());
    tf.innerHTML = '<div class="done"><span class="tab" style="background:var(--bright-tint)">Request received</span><h3>Thanks, ' + biz + '.</h3><p>An account manager will be in touch shortly to set up your trade account and pricing.</p></div>';
  });
  $("#newsForm").addEventListener("submit", function (e) {
    e.preventDefault();
    var i = $("#newsEmail"), ok = /^\S+@\S+\.\S+$/.test(i.value);
    i.setAttribute("aria-invalid", ok ? "false" : "true");
    $("#newsMsg").textContent = ok ? "You're on the list. Look out for new arrivals and offers." : "Enter a valid email address to subscribe.";
    if (ok) this.reset();
  });

  /* ---------- Toast + misc ---------- */
  var tt;
  function toast(m) { var t = $("#toast"); t.textContent = m; t.classList.add("show"); clearTimeout(tt); tt = setTimeout(function () { t.classList.remove("show"); }, 2600); }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeDrawer(); });
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
  render();
})();
