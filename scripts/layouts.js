/* Layout-specific touches. */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* A: the van drives in once when its section scrolls into view */
  var van = document.querySelector(".a-van[data-drive]");
  if (van && !reduce && "IntersectionObserver" in window) {
    document.documentElement.classList.add("js-drive");
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { van.classList.add("in"); io.disconnect(); } });
    }, { threshold: 0.35 });
    io.observe(van);
  }

  /* B: hovering a category row swaps the large preview photo */
  var prev = document.getElementById("bPreview");
  if (prev) {
    var rows = Array.prototype.slice.call(document.querySelectorAll(".b-row"));
    function show(r) {
      rows.forEach(function (x) { x.classList.toggle("on", x === r); });
      if (prev.getAttribute("src") !== r.dataset.preview) {
        prev.style.opacity = 0;
        setTimeout(function () { prev.src = r.dataset.preview; prev.style.opacity = 1; }, reduce ? 0 : 150);
      }
    }
    rows.forEach(function (r) {
      r.addEventListener("pointerenter", function () { show(r); });
      r.addEventListener("focus", function () { show(r); });
    });
    if (rows[0]) rows[0].classList.add("on");
  }
})();
