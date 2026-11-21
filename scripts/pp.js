  /* ---------- Product pages: #/product/<id>  (and #/product/<id>/nutrition) ---------- */
  var home = $("#main"), pp = $("#productPage"), baseTitle = document.title, homeY = 0;
  var STORAGE = "Store in a cool, dry place away from direct sunlight. Once opened, reseal the pack and enjoy within 4 weeks.";
  function back(p) {
    return '<div class="face back" style="--c:' + p.colour + '"><div class="panel">' +
      '<div class="ptop"><div><h3>' + p.name + '</h3><p class="label">' + p.descriptor + '</p></div><span class="logo logo--s" role="img" aria-label="Regency Foods"></span></div>' +
      '<p>' + esc(p.about.split(". ")[0]) + '.</p>' +
      '<div><span class="k">Ingredients</span>' + p.ingredients + '</div>' +
      '<div><span class="k">Allergy advice</span>' + p.allergy + '</div>' +
      '<div><span class="k">Storage</span>' + STORAGE + '</div>' +
      '<table><thead><tr><th scope="col">Nutrition</th><th scope="col">Per 100 g</th></tr></thead><tbody>' +
      p.nutrition.map(function (r) { return '<tr' + (r[2] ? ' class="ind"' : '') + '><td>' + r[0] + '</td><td>' + r[1] + '</td></tr>'; }).join("") +
      '</tbody></table>' +
      '<div class="sign"><b>From Our Kitchen<br>to Yours</b><span>1 kg ℮</span></div>' +
    '</div></div>';
  }
  function nutritionTable(p) {
    return '<table class="pp-table"><thead><tr><th scope="col">Typical values</th><th scope="col">Per 100 g</th><th scope="col">Per 30 g handful</th></tr></thead><tbody>' +
      p.nutrition.map(function (r) {
        var per30 = r[1].replace(/([\d.]+)/g, function (n) { var v = +n * .3; return v >= 100 ? Math.round(v) : v >= 10 ? v.toFixed(1) : v.toFixed(2).replace(/0$/, ""); });
        return '<tr' + (r[2] ? ' class="ind"' : '') + '><th scope="row">' + r[0] + '</th><td>' + r[1] + '</td><td>' + per30 + '</td></tr>';
      }).join("") + '</tbody></table>';
  }
  function card(q) {
    return '<a class="pp-card" href="#/product/' + q.id + '" style="--tint:' + q.tint + '">' +
      '<span class="pp-card-img"><img src="' + q.pack + '" alt="" loading="lazy"></span>' +
      '<span class="pp-card-txt"><b>' + q.name + '</b><span>' + q.descriptor + ', 1 kg</span><span class="pp-card-price">' + gbp.format(q.price) + '</span></span>' +
      '<span class="pp-card-go" aria-hidden="true">→</span></a>';
  }
  function productHTML(p) {
    var subPrice = gbp.format(p.price * .9);
    return '<nav class="wrap pp-crumbs" aria-label="Breadcrumb"><a href="#top">Home</a><span aria-hidden="true">/</span><a href="#range">Nuts &amp; Seeds</a><span aria-hidden="true">/</span><span aria-current="page">' + p.name + '</span></nav>' +
      '<section class="wrap pp-top" aria-labelledby="ppName">' +
        '<div class="pp-stage" style="--tint:' + p.tint + '">' +
          '<div class="pack" id="pack"><div class="flip">' +
            '<button class="face front" type="button" data-turn aria-label="Turn the pack over"><img src="' + p.pack + '" alt="Front of the Regency Foods ' + p.name + ' 1 kg pack"></button>' + back(p) +
          '</div></div>' +
          '<div class="pp-views" role="group" aria-label="Pack view">' +
            '<button type="button" data-view="front" aria-pressed="true">Front of pack</button><button type="button" data-view="back" aria-pressed="false">Back of pack</button>' +
          '</div>' +
        '</div>' +
        '<div class="pp-info" data-plan-scope>' +
          '<h1 id="ppName">' + p.name + '</h1>' +
          '<p class="pp-desc">' + p.descriptor + ' · 1 kg resealable pack</p>' +
          '<p class="pp-price">' + gbp.format(p.price) + '<small>' + gbp.format(p.price / 10) + ' per 100 g</small></p>' +
          '<p class="pp-about">' + esc(p.about) + '</p>' +
          '<fieldset class="pp-plan"><legend class="sr">How would you like to buy?</legend>' +
            '<label><input type="radio" name="plan" value="once"' + (sub ? '' : ' checked') + '><span><b>One-off purchase</b><em>' + gbp.format(p.price) + '</em></span></label>' +
            '<label><input type="radio" name="plan" value="sub"' + (sub ? ' checked' : '') + '><span><b>Subscribe &amp; save 10%</b><em>' + subPrice + '</em><small>Added to every order. Skip or cancel any time.</small></span></label>' +
          '</fieldset>' +
          '<div class="buy"><span class="qty" role="group" aria-label="Quantity"><button type="button" data-step="-1" aria-label="Decrease">−</button><output data-q>1</output><button type="button" data-step="1" aria-label="Increase">+</button></span>' +
          '<button class="btn btn--green" type="button" data-add="' + p.id + '">Add to basket</button></div>' +
          '<p class="pp-ship"><span class="dot" aria-hidden="true"></span>Order in <b data-timer>00:00:00</b> for delivery tomorrow</p>' +
          '<ul class="pp-facts"><li>1 kg resealable pouch</li><li>Next-day UK delivery</li><li>Trade pricing available</li></ul>' +
        '</div>' +
      '</section>' +
      '<section class="wrap pp-details" aria-label="Product details">' +
        '<details open><summary>Description</summary><div><p>' + esc(p.about) + '</p><p>Packed in our 1 kg resealable pouch, so it stays fresh from the first handful to the last, in a busy kitchen or at home.</p></div></details>' +
        '<details id="ppIngredients"><summary>Ingredients &amp; allergens</summary><div><p><b class="k">Ingredients</b> ' + p.ingredients + '</p><p><b class="k">Allergy advice</b> ' + p.allergy + '</p></div></details>' +
        '<details id="ppNutrition"><summary>Nutrition</summary><div>' + nutritionTable(p) + '</div></details>' +
        '<details><summary>Storage</summary><div><p>' + STORAGE + '</p></div></details>' +
        '<details><summary>Delivery</summary><div><p>Order before midnight and it arrives the next day, nationwide, from our North London hub. Trade customers can set up a standing order with their account manager.</p></div></details>' +
      '</section>' +
      '<section class="pp-more" aria-labelledby="ppMore"><div class="wrap">' +
        '<h2 id="ppMore">More from our own range</h2>' +
        '<div class="pp-cards">' + RANGE.filter(function (q) { return q.id !== p.id; }).map(card).join("") + '</div>' +
      '</div></section>' +
      '<section class="wrap pp-trade"><div><h2>Buying for a kitchen?</h2><p>Open a trade account for wholesale pricing, standing orders and an account manager who knows your menu.</p></div>' +
        '<a class="btn btn--cream" href="#trade">Open a trade account <span aria-hidden="true">→</span></a></section>';
  }
  function setView(back) {
    var pack = $("#pack"); if (!pack) return;
    pack.classList.toggle("turned", back);
    $$("[data-view]", pp).forEach(function (b) { b.setAttribute("aria-pressed", String((b.dataset.view === "back") === back)); });
  }
  function showProduct(id, part) {
    var p = BY[id];
    if (pp.hidden) homeY = window.scrollY;
    pp.innerHTML = productHTML(p);
    home.hidden = true; pp.hidden = false;
    document.title = p.name + " | Regency Foods";
    tick();
    if (part === "nutrition") {
      var d = $("#ppNutrition"); d.open = true; $("#ppIngredients").open = true;
      requestAnimationFrame(function () { d.scrollIntoView({ block: "start" }); });
    } else window.scrollTo(0, 0);
    pp.focus({ preventScroll: true });
  }
  function route() {
    var m = location.hash.match(/^#\/product\/(\w+)(?:\/(\w+))?/);
    if (m && BY[m[1]]) { showProduct(m[1], m[2]); return; }
    if (!pp.hidden) {
      pp.hidden = true; home.hidden = false; pp.innerHTML = ""; document.title = baseTitle;
      var el = location.hash.length > 1 && document.getElementById(location.hash.slice(1));
      if (el) el.scrollIntoView(); else window.scrollTo(0, homeY);
    }
  }
  pp.addEventListener("click", function (e) {
    var v = e.target.closest("[data-view]");
    if (v) { setView(v.dataset.view === "back"); return; }
    if (e.target.closest("[data-turn]") || e.target.closest(".face.back")) setView(!$("#pack").classList.contains("turned"));
  });
  window.addEventListener("hashchange", route);
  route();
