/* Regency Foods — shared shop behaviour for all three directions.
   Pages provide: [data-add="id"] buttons, [data-count] badges, [data-open-basket]
   triggers, and style the .rf-drawer markup this script creates. */
(function () {
  "use strict";
  // Only Pecans (£16.45) is a real price; the rest are placeholders.
  var PRODUCTS = window.RF_PRODUCTS = [
    { id: "pecans",     name: "Pecan Nuts",    label: "Pecan nuts", note: "Mildly roasted",   size: "1kg", price: 16.45, img: "assets/img/cut-pecan.png",  colour: "#d54415", tint: "#f7d3c2", use: "Baking & snacking" },
    { id: "almonds",    name: "Almonds",       label: "Almonds",    note: "Whole, natural",   size: "1kg", price: 12.95, img: "assets/img/cut-yellow.png", colour: "#dcb357", tint: "#f5e7bf", use: "Baking" },
    { id: "pistachios", name: "Pistachios",    label: "Pistachios", note: "Roasted & salted", size: "1kg", price: 19.50, was: 21.50, img: "assets/img/cut-green.png", colour: "#45a94f", tint: "#d5eccf", use: "Bar & snacking" },
    { id: "cashews",    name: "Cashew Nuts",   label: "Cashews",    note: "Whole, raw",       size: "1kg", price: 15.20, img: "assets/img/cut-salmon.png", colour: "#f39684", tint: "#fbe0d9", use: "Curries & snacking" },
    { id: "walnuts",    name: "Walnut Halves", label: "Walnuts",    note: "Light halves",     size: "1kg", price: 13.75, was: 14.95, img: "assets/img/cut-forest.png", colour: "#1a3429", tint: "#d3ddd6", use: "Baking & salads", dark: true }
  ];
  var by = {}; PRODUCTS.forEach(function (p) { by[p.id] = p; });
  var gbp = window.RF_GBP = new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP" });
  var esc = window.RF_ESC = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var KEY = "rf-basket-" + (document.body.dataset.store || "v3");
  var basket = {}, sub = false;
  try { basket = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) {}
  Object.keys(basket).forEach(function (k) { if (!by[k]) delete basket[k]; });

  /* Drawer markup */
  var wrap = document.createElement("div");
  wrap.innerHTML =
    '<div class="rf-scrim" hidden></div>' +
    '<aside class="rf-drawer" aria-label="Basket" hidden>' +
      '<div class="rf-head"><h2>Basket</h2><button type="button" class="rf-close" aria-label="Close basket">Close</button></div>' +
      '<div class="rf-body"></div>' +
      '<div class="rf-foot"></div>' +
    '</aside>' +
    '<div class="rf-toast" role="status" aria-live="polite"></div>';
  while (wrap.firstChild) document.body.appendChild(wrap.firstChild);
  var drawer = document.querySelector(".rf-drawer"), scrim = document.querySelector(".rf-scrim");
  var body = drawer.querySelector(".rf-body"), foot = drawer.querySelector(".rf-foot"), toastEl = document.querySelector(".rf-toast");

  function save() { try { localStorage.setItem(KEY, JSON.stringify(basket)); } catch (e) {} }
  function tomorrow() { var d = new Date(); d.setDate(d.getDate() + 1); return d.toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long" }); }

  function render() {
    var ids = Object.keys(basket), n = 0, total = 0;
    ids.forEach(function (k) { n += basket[k]; total += basket[k] * by[k].price; });
    document.querySelectorAll("[data-count]").forEach(function (el) { el.textContent = n; el.classList.toggle("has", n > 0); });
    document.querySelectorAll("[data-open-basket]").forEach(function (el) { el.setAttribute("aria-label", "Basket, " + n + (n === 1 ? " item" : " items")); });
    if (!ids.length) {
      body.innerHTML = '<p class="rf-empty">Your basket is empty.</p>';
      foot.innerHTML = '';
      return;
    }
    body.innerHTML = ids.map(function (k) {
      var p = by[k];
      return '<div class="rf-line"><div class="rf-thumb" style="background:' + p.tint + '"><img src="' + p.img + '" alt=""></div>' +
        '<div class="rf-info"><span class="rf-name">' + esc(p.name) + '</span><span class="rf-meta">' + p.size + ' · ' + gbp.format(p.price) + '</span>' +
        '<span class="rf-qty"><button type="button" data-dec="' + k + '" aria-label="Remove one ' + esc(p.name) + '">−</button><output>' + basket[k] + '</output><button type="button" data-inc="' + k + '" aria-label="Add one ' + esc(p.name) + '">+</button></span></div>' +
        '<span class="rf-price">' + gbp.format(p.price * basket[k]) + '</span></div>';
    }).join("");
    var off = sub ? total * 0.1 : 0;
    foot.innerHTML =
      '<label class="rf-sub"><input type="checkbox" id="rfSub"' + (sub ? " checked" : "") + '> Subscribe &amp; save 10%</label>' +
      '<div class="rf-row"><span>Subtotal</span><span>' + gbp.format(total) + '</span></div>' +
      (sub ? '<div class="rf-row rf-save"><span>Subscribe &amp; save</span><span>−' + gbp.format(off) + '</span></div>' : '') +
      '<div class="rf-row"><span>Delivery</span><span>' + tomorrow() + '</span></div>' +
      '<div class="rf-row rf-total"><span>Total</span><span>' + gbp.format(total - off) + '</span></div>' +
      '<button type="button" class="rf-checkout">Checkout</button>';
  }

  var lastFocus = null;
  function open() { lastFocus = document.activeElement; scrim.hidden = false; drawer.hidden = false; requestAnimationFrame(function () { drawer.classList.add("open"); scrim.classList.add("open"); }); drawer.querySelector(".rf-close").focus(); }
  function close() { if (drawer.hidden) return; drawer.classList.remove("open"); scrim.classList.remove("open"); setTimeout(function () { drawer.hidden = true; scrim.hidden = true; }, 300); if (lastFocus) lastFocus.focus(); }
  var tt; function toast(m) { toastEl.textContent = m; toastEl.classList.add("show"); clearTimeout(tt); tt = setTimeout(function () { toastEl.classList.remove("show"); }, 2200); }
  window.RF_TOAST = toast;

  document.addEventListener("click", function (e) {
    var t;
    if ((t = e.target.closest("[data-add]"))) {
      var id = t.dataset.add, q = +(t.dataset.qty || 1);
      basket[id] = (basket[id] || 0) + q; save(); render();
      toast(by[id].name + " added to your basket");
    } else if ((t = e.target.closest("[data-inc]"))) { basket[t.dataset.inc]++; save(); render(); }
    else if ((t = e.target.closest("[data-dec]"))) { var k = t.dataset.dec; if (--basket[k] <= 0) delete basket[k]; save(); render(); }
    else if (e.target.closest("[data-open-basket]")) { e.preventDefault(); open(); }
    else if (e.target.closest(".rf-close") || e.target === scrim) close();
    else if (e.target.closest(".rf-checkout")) toast("Checkout isn't connected yet.");
  });
  drawer.addEventListener("change", function (e) { if (e.target.id === "rfSub") { sub = e.target.checked; render(); } });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });

  /* Forms: any form[data-form] validates email and shows its [data-msg] */
  document.querySelectorAll("form[data-form]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var req = Array.prototype.slice.call(f.querySelectorAll("[required]"));
      var bad = req.filter(function (i) { return !i.value.trim() || (i.type === "email" && !/^\S+@\S+\.\S+$/.test(i.value)); });
      var msg = f.querySelector("[data-msg]");
      req.forEach(function (i) { i.setAttribute("aria-invalid", bad.indexOf(i) > -1 ? "true" : "false"); });
      if (bad.length) { msg.textContent = f.dataset.form === "news" ? "Enter a valid email address." : "Please fill in every field with a valid email."; bad[0].focus(); return; }
      msg.textContent = f.dataset.form === "news" ? "You're subscribed. Look out for new arrivals and offers." : "Thanks. We'll be in touch to set up your trade account.";
      f.reset();
    });
  });

  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
  document.querySelectorAll("[data-years]").forEach(function (el) { el.textContent = new Date().getFullYear() - 1995; });
  render();
})();
