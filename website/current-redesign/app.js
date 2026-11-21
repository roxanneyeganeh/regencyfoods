/* Regency Foods — site behaviour (no dependencies) */
(function () {
  "use strict";

  /* ---------- Product data ---------- */
  // Prices other than Pecans are placeholders — swap in real catalogue data.
  var PRODUCTS = [
    { id: "pecans",     name: "Pecan Nuts",   label: "Pecan nuts",  note: "Mildly roasted",   size: "1kg", price: 16.45, img: "assets/img/bag-pecan-blank.jpg", tags: ["baking", "snacking"], badge: "Bestseller" },
    { id: "almonds",    name: "Almonds",      label: "Almonds",     note: "Whole, natural",   size: "1kg", price: 12.95, img: "assets/img/bag-yellow.jpg",      tags: ["baking"] },
    { id: "pistachios", name: "Pistachios",   label: "Pistachios",  note: "Roasted & salted", size: "1kg", price: 19.50, was: 21.50, img: "assets/img/bag-green.jpg", tags: ["snacking", "offer"], badge: "On offer" },
    { id: "cashews",    name: "Cashew Nuts",  label: "Cashews",     note: "Whole, raw",       size: "1kg", price: 15.20, img: "assets/img/bag-salmon.jpg",      tags: ["snacking", "baking"] },
    { id: "walnuts",    name: "Walnut Halves",label: "Walnuts",     note: "Light halves",     size: "1kg", price: 13.75, was: 14.95, img: "assets/img/bag-forest.jpg", tags: ["baking", "offer"], dark: true, badge: "On offer" }
  ];
  var byId = {};
  PRODUCTS.forEach(function (p) { byId[p.id] = p; });

  var SUB_DISCOUNT = 0.10;
  var gbp = new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP" });
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }

  /* ---------- Storage (safe) ---------- */
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };

  /* ---------- Render product cards ---------- */
  var row = $("#productRow");
  row.innerHTML = PRODUCTS.map(function (p) {
    return (
      '<article class="card" data-tags="' + p.tags.join(" ") + '">' +
        '<div class="card-media">' +
          '<img src="' + p.img + '" alt="Regency Foods ' + esc(p.name) + ' ' + p.size + ' bag" loading="lazy">' +
          '<span class="bag-label' + (p.dark ? " on-dark" : "") + '" aria-hidden="true"><small>' + esc(p.note) + '</small><b>' + esc(p.label) + '</b></span>' +
          (p.badge ? '<span class="tag">' + esc(p.badge) + "</span>" : "") +
        "</div>" +
        '<div class="card-body">' +
          "<h3>" + esc(p.name) + "</h3>" +
          '<p class="card-meta">' + esc(p.note) + " · " + p.size + "</p>" +
          '<div class="card-foot">' +
            '<span class="price">' + gbp.format(p.price) + (p.was ? " <s>" + gbp.format(p.was) + "</s>" : "") + "</span>" +
            '<button class="add-btn" type="button" data-add="' + p.id + '" aria-label="Add ' + esc(p.name) + ' to basket">Add <span aria-hidden="true">+</span></button>' +
          "</div>" +
        "</div>" +
      "</article>"
    );
  }).join("");

  /* ---------- Filters ---------- */
  $$(".chip[data-filter]").forEach(function (chip) {
    chip.addEventListener("click", function () {
      var f = chip.getAttribute("data-filter");
      $$(".chip[data-filter]").forEach(function (c) { c.setAttribute("aria-pressed", c === chip ? "true" : "false"); });
      $$(".card", row).forEach(function (card) {
        card.hidden = !(f === "all" || card.getAttribute("data-tags").split(" ").indexOf(f) > -1);
      });
    });
  });

  /* ---------- Basket ---------- */
  var basket = store.get("rf-basket", {});
  var subscribe = store.get("rf-sub", false);
  Object.keys(basket).forEach(function (k) { if (!byId[k]) delete basket[k]; });

  var countEl = $("#basketCount");
  var drawer = $("#drawer");
  var scrim = $("#scrim");
  var body = $("#drawerBody");
  var foot = $("#drawerFoot");
  var totalsEl = $("#totals");
  var subBox = $("#drawerSub");
  var spotSub = $("#spotSub");
  subBox.checked = subscribe;
  spotSub.checked = subscribe;

  function itemCount() { return Object.keys(basket).reduce(function (n, k) { return n + basket[k]; }, 0); }

  function add(id, qty) {
    basket[id] = (basket[id] || 0) + (qty || 1);
    save(); render();
    countEl.classList.remove("bump"); void countEl.offsetWidth; countEl.classList.add("bump");
    toast(byId[id].name + " added to your basket");
  }
  function setQty(id, q) {
    if (q <= 0) delete basket[id]; else basket[id] = q;
    save(); render();
  }
  function setSub(v) {
    subscribe = v; subBox.checked = v; spotSub.checked = v;
    store.set("rf-sub", v); render();
  }
  function save() { store.set("rf-basket", basket); }

  function render() {
    var n = itemCount();
    countEl.textContent = n;
    countEl.classList.toggle("has-items", n > 0);
    $("#basketOpen").setAttribute("aria-label", "Basket, " + n + (n === 1 ? " item" : " items"));

    var ids = Object.keys(basket);
    if (!ids.length) {
      body.innerHTML =
        '<div class="empty"><h3>Your basket is empty</h3><p>Add something good. Order today and it arrives tomorrow.</p>' +
        '<a class="btn btn-dark" href="#bestsellers" data-close>Shop bestsellers</a></div>';
      foot.hidden = true;
      return;
    }
    foot.hidden = false;
    var sub = 0;
    body.innerHTML = ids.map(function (id) {
      var p = byId[id], q = basket[id], line = p.price * q;
      sub += line;
      return (
        '<div class="line-item">' +
          '<div class="thumb"><img src="' + p.img + '" alt=""></div>' +
          "<div><h3>" + esc(p.name) + '</h3><div class="meta">' + p.size + " · " + gbp.format(p.price) + " each</div>" +
            '<div class="qty" role="group" aria-label="Quantity for ' + esc(p.name) + '">' +
              '<button type="button" data-dec="' + id + '" aria-label="Decrease">–</button>' +
              "<output>" + q + "</output>" +
              '<button type="button" data-inc="' + id + '" aria-label="Increase">+</button>' +
            "</div>" +
          "</div>" +
          '<div class="lp"><span>' + gbp.format(line) + '</span><button class="remove" type="button" data-remove="' + id + '">Remove</button></div>' +
        "</div>"
      );
    }).join("");
    var disc = subscribe ? sub * SUB_DISCOUNT : 0;
    totalsEl.innerHTML =
      "<div><span>Subtotal</span><span>" + gbp.format(sub) + "</span></div>" +
      (subscribe ? '<div class="saving"><span>Subscribe &amp; save</span><span>−' + gbp.format(disc) + "</span></div>" : "") +
      "<div><span>Delivery</span><span>Next day</span></div>" +
      '<div class="grand"><span>Total</span><span>' + gbp.format(sub - disc) + "</span></div>";
  }

  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-add],[data-inc],[data-dec],[data-remove],[data-close]");
    if (!t) return;
    if (t.dataset.add) {
      add(t.dataset.add, 1);
      t.classList.add("added"); t.innerHTML = "Added ✓";
      setTimeout(function () { t.classList.remove("added"); t.innerHTML = 'Add <span aria-hidden="true">+</span>'; }, 1400);
    } else if (t.dataset.inc) setQty(t.dataset.inc, basket[t.dataset.inc] + 1);
    else if (t.dataset.dec) setQty(t.dataset.dec, basket[t.dataset.dec] - 1);
    else if (t.dataset.remove) setQty(t.dataset.remove, 0);
    else if (t.hasAttribute("data-close")) closeDrawer();
  });

  subBox.addEventListener("change", function () { setSub(subBox.checked); });
  spotSub.addEventListener("change", function () { setSub(spotSub.checked); });

  var lastFocus = null;
  function openDrawer() {
    lastFocus = document.activeElement;
    drawer.classList.add("open"); scrim.classList.add("open");
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    setTimeout(function () { $("#basketClose").focus(); }, 50);
  }
  function closeDrawer() {
    drawer.classList.remove("open"); scrim.classList.remove("open");
    drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }
  $("#basketOpen").addEventListener("click", openDrawer);
  $("#basketClose").addEventListener("click", closeDrawer);
  scrim.addEventListener("click", function () { closeDrawer(); closeSearch(); });
  $("#checkout").addEventListener("click", function () {
    toast("Checkout is not connected yet. Hook this button up to your payment provider.");
  });

  /* ---------- Spotlight qty ---------- */
  var spotQ = 1, spotOut = $("#spotQty");
  $("#spotMinus").addEventListener("click", function () { spotQ = Math.max(1, spotQ - 1); spotOut.textContent = spotQ; });
  $("#spotPlus").addEventListener("click", function () { spotQ = Math.min(99, spotQ + 1); spotOut.textContent = spotQ; });
  $("#spotAdd").addEventListener("click", function () { add("pecans", spotQ); spotQ = 1; spotOut.textContent = 1; });

  /* ---------- Toast ---------- */
  var toastEl = $("#toast"), toastT;
  function toast(msg) {
    toastEl.textContent = msg; toastEl.classList.add("show");
    clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove("show"); }, 2600);
  }

  /* ---------- Mobile menu ---------- */
  var menuBtn = $("#menuToggle"), mnav = $("#mobileNav");
  menuBtn.addEventListener("click", function () {
    var open = mnav.hidden;
    mnav.hidden = !open;
    menuBtn.setAttribute("aria-expanded", String(open));
    menuBtn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  });
  $$("a", mnav).forEach(function (a) { a.addEventListener("click", function () { mnav.hidden = true; menuBtn.setAttribute("aria-expanded", "false"); }); });

  /* ---------- Search ---------- */
  var sp = $("#searchPanel"), si = $("#searchInput"), sr = $("#searchResults"), sh = $("#searchHint");
  var CATS = ["Meat & Seafood", "Frozen Foods", "Soft Drinks", "Nuts & Seeds", "Alcohol & Spirits", "Snacks & Sweets", "Store Cupboard"];
  function openSearch() {
    sp.hidden = false;
    requestAnimationFrame(function () { sp.classList.add("open"); scrim.classList.add("open"); });
    setTimeout(function () { si.focus(); }, 60);
  }
  function closeSearch() {
    if (sp.hidden) return;
    sp.classList.remove("open");
    if (!drawer.classList.contains("open")) scrim.classList.remove("open");
    setTimeout(function () { sp.hidden = true; }, 400);
  }
  $("#searchOpen").addEventListener("click", openSearch);
  $("#searchClose").addEventListener("click", closeSearch);
  si.addEventListener("input", function () {
    var q = si.value.trim().toLowerCase();
    if (!q) { sr.innerHTML = ""; sh.textContent = "Popular: pecans, pistachios, almonds"; return; }
    var hits = PRODUCTS.filter(function (p) { return (p.name + " " + p.label + " " + p.note).toLowerCase().indexOf(q) > -1; });
    var cats = CATS.filter(function (c) { return c.toLowerCase().indexOf(q) > -1; });
    sh.textContent = hits.length + cats.length ? "Results for “" + si.value.trim() + "”" : "No matches for “" + si.value.trim() + "”. Try a category like frozen or drinks.";
    sr.innerHTML =
      hits.map(function (p) { return '<button class="chip" type="button" data-add="' + p.id + '">' + esc(p.name) + " · " + gbp.format(p.price) + " +</button>"; }).join("") +
      cats.map(function (c) { return '<a class="chip" href="#categories" data-cat>' + esc(c) + " →</a>"; }).join("");
  });
  sr.addEventListener("click", function (e) { if (e.target.closest("[data-cat]")) closeSearch(); });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { closeDrawer(); closeSearch(); }
  });

  /* ---------- Forms ---------- */
  var tf = $("#tradeForm");
  tf.addEventListener("submit", function (e) {
    e.preventDefault();
    var bad = $$("[required]", tf).filter(function (i) { return !i.value.trim() || (i.type === "email" && !/^\S+@\S+\.\S+$/.test(i.value)); });
    $$("[required]", tf).forEach(function (i) { i.style.borderColor = bad.indexOf(i) > -1 ? "var(--orange)" : ""; });
    if (bad.length) { $("#tradeNote").textContent = "Please fill in your name, business name and a valid work email."; bad[0].focus(); return; }
    var biz = esc($("#tfBiz").value.trim());
    tf.innerHTML = '<div class="form-done"><span class="tag">Request received</span><h3>Thanks, ' + biz + '.</h3><p>We have your details. A member of the Regency Foods team will be in touch to set up your trade account.</p></div>';
  });

  var nl = $("#nlForm"), nlMsg = $("#nlMsg");
  nl.addEventListener("submit", function (e) {
    e.preventDefault();
    var v = $("#nlEmail").value.trim();
    if (!/^\S+@\S+\.\S+$/.test(v)) { nlMsg.textContent = "Enter a valid email address to subscribe."; return; }
    nlMsg.textContent = "You are on the list. Look out for new arrivals and offers in your inbox.";
    nl.reset();
  });

  var y = $("#year"); if (y) y.textContent = new Date().getFullYear();

  render();
})();
