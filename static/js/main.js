/* ==========================================================================
   ALUPAN — motion layer
   GSAP + ScrollTrigger. Everything degrades: if the CDN is blocked (a real
   risk for visitors inside Iran) the page still renders fully, just static.
   ========================================================================== */
(function () {
  "use strict";

  var root = document.documentElement;
  var body = document.body;
  var RTL  = root.getAttribute("dir") === "rtl";
  var DIR  = RTL ? -1 : 1;                       // sign for horizontal motion

  /* --- 0. Graceful degradation ------------------------------------------ */
  function releasePage() {
    body.classList.remove("is-loading");
    document.querySelectorAll("[data-reveal], [data-reveal-line]")
      .forEach(function (el) { el.classList.add("is-revealed"); });
    var mask = document.querySelector("[data-hero-mask]");
    if (mask) mask.classList.add("is-open");
  }

  if (!window.gsap || !window.ScrollTrigger) {
    console.warn("[alupan] GSAP unavailable — rendering without motion.");
    releasePage();
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced) { releasePage(); }

  /* --- 1. Persian numerals ---------------------------------------------- */
  var FA_DIGITS = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"];

  function toPersian(value) {
    return String(value).replace(/\d/g, function (d) { return FA_DIGITS[+d]; });
  }

  function groupThousands(n) {
    // U+066C ARABIC THOUSANDS SEPARATOR — the correct mark in Persian text.
    return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, "٬");
  }

  /* --- 2. Word splitter -------------------------------------------------
     Wraps every word in an overflow-hidden mask so it can slide up from
     behind its own baseline. Skipped when the node contains markup, so a
     headline with a <span class="ltr"> inside is never destroyed.
     -------------------------------------------------------------------- */
  function splitWords(el) {
    if (el.children.length) return Array.prototype.slice.call(el.querySelectorAll(".word"));
    var words = el.textContent.trim().split(/\s+/);
    el.textContent = "";
    return words.map(function (w) {
      var mask = document.createElement("span");
      mask.className = "word-mask";
      var inner = document.createElement("span");
      inner.className = "word";
      inner.textContent = w;
      mask.appendChild(inner);
      el.appendChild(mask);
      return inner;
    });
  }

  var splitTargets = document.querySelectorAll("[data-split-words]");
  var splitMap = new Map();
  splitTargets.forEach(function (el) { splitMap.set(el, splitWords(el)); });

  if (!reduced) {
    splitMap.forEach(function (words) { gsap.set(words, { yPercent: 115, opacity: 0 }); });
  }

  /* ======================================================================
     3. CINEMATIC HERO LOAD
     The mask opens upward (clip-path inset from the bottom) while the
     artwork inside counter-moves downward — reads as a camera tilt, not a
     wipe. The headline words then stagger up out of their masks.
     ====================================================================== */
  function playHero() {
    var hero    = document.querySelector("#hero");
    var mask    = document.querySelector("[data-hero-mask]");
    var art     = document.querySelector("[data-hero-art]");
    var title   = hero && hero.querySelector("[data-split-words]");
    var items   = hero ? hero.querySelectorAll("[data-hero-item]") : [];
    var cue     = document.querySelector(".scroll-cue");

    if (!hero || reduced) { body.classList.remove("is-loading"); return; }

    gsap.set(items, { y: 26, opacity: 0 });
    gsap.set(cue,   { opacity: 0 });

    var tl = gsap.timeline({
      defaults: { ease: "expo.out" },
      onComplete: function () { body.classList.remove("is-loading"); }
    });

    tl.fromTo(mask,
        { clipPath: "inset(100% 0% 0% 0%)" },
        { clipPath: "inset(0% 0% 0% 0%)", duration: 1.5 })
      .fromTo(art,
        { yPercent: 14, scale: 1.12 },
        { yPercent: 0, scale: 1, duration: 1.8 }, 0)
      .to(splitMap.get(title) || [], {
        yPercent: 0,
        opacity: 1,
        duration: 1.15,
        stagger: 0.075
      }, 0.55)
      .to(items, { y: 0, opacity: 1, duration: 1, stagger: 0.11 }, 0.95)
      .to(cue,   { opacity: 1, duration: .8 }, 1.3);

    return tl;
  }

  /* ======================================================================
     4. Header state
     ====================================================================== */
  function initHeader() {
    var header = document.querySelector("[data-header]");
    if (!header) return;
    ScrollTrigger.create({
      start: "top -90",
      end: 99999,
      onToggle: function (self) { header.classList.toggle("is-stuck", self.isActive); }
    });
  }

  /* ======================================================================
     5. Credential marquee
     ====================================================================== */
  function initMarquee() {
    var track = document.querySelector("[data-marquee]");
    if (!track || reduced) return;
    // The track content is duplicated in the template, so travelling 50%
    // of its own width loops seamlessly.
    gsap.to(track, {
      xPercent: RTL ? 50 : -50,
      duration: 34,
      ease: "none",
      repeat: -1
    });
  }

  /* ======================================================================
     6. Generic scroll reveals
     ====================================================================== */
  function initReveals() {
    if (reduced) return;
    gsap.utils.toArray("[data-reveal]").forEach(function (el) {
      gsap.fromTo(el,
        { y: 34, opacity: 0 },
        {
          y: 0, opacity: 1, duration: 1.05, ease: "power3.out",
          scrollTrigger: { trigger: el, start: "top 88%", once: true }
        });
    });

    // Headlines outside the hero split and reveal on scroll.
    splitMap.forEach(function (words, el) {
      if (el.closest("#hero")) return;
      gsap.to(words, {
        yPercent: 0, opacity: 1, duration: 1.15, ease: "expo.out", stagger: 0.06,
        scrollTrigger: { trigger: el, start: "top 85%", once: true }
      });
    });
  }

  /* ======================================================================
     7. Counters — animate to the value, print Persian digits
     ====================================================================== */
  function initCounters() {
    gsap.utils.toArray("[data-count]").forEach(function (el) {
      var target = parseFloat(el.getAttribute("data-count")) || 0;
      var proxy  = { v: 0 };

      function paint() {
        el.textContent = toPersian(groupThousands(Math.round(proxy.v)));
      }

      if (reduced) { proxy.v = target; paint(); return; }

      gsap.to(proxy, {
        v: target,
        duration: 2.1,
        ease: "power2.out",
        onUpdate: paint,
        scrollTrigger: { trigger: el, start: "top 90%", once: true }
      });
    });
  }

  /* ======================================================================
     8. Scrollytelling — sticky visual, stepped copy
     Each step owns a scroll range; entering it activates the matching
     layer and updates the 01/03 index.
     ====================================================================== */
  function initStory() {
    var story = document.querySelector("[data-story]");
    if (!story) return;

    var layers = story.querySelectorAll("[data-story-layer]");
    var steps  = story.querySelectorAll("[data-story-step]");
    var index  = story.querySelector("[data-story-index]");
    if (!layers.length || !steps.length) return;

    function activate(i) {
      layers.forEach(function (layer, n) { layer.classList.toggle("is-active", n === i); });
      if (index) index.textContent = toPersian(String(i + 1).padStart(2, "0"));
    }

    steps.forEach(function (step, i) {
      ScrollTrigger.create({
        trigger: step,
        start: "top 62%",
        end: "bottom 38%",
        onEnter:     function () { activate(i); },
        onEnterBack: function () { activate(i); }
      });
    });
  }

  /* ======================================================================
     9. Parallax — background drifts slower than the page
     ====================================================================== */
  function initParallax() {
    if (reduced) return;
    gsap.utils.toArray("[data-parallax]").forEach(function (el) {
      var depth = parseFloat(el.getAttribute("data-parallax-depth")) || 12;
      gsap.fromTo(el,
        { yPercent: -depth },
        {
          yPercent: depth,
          ease: "none",
          scrollTrigger: {
            trigger: el.parentElement,
            start: "top bottom",
            end: "bottom top",
            scrub: true
          }
        });
    });
  }

  /* ======================================================================
     10. Mobile menu (progressive — the nav is CSS-hidden under 768px)
     ====================================================================== */
  function initBurger() {
    var burger = document.querySelector(".burger");
    var nav    = document.querySelector(".nav");
    if (!burger || !nav) return;
    burger.addEventListener("click", function () {
      var open = burger.getAttribute("aria-expanded") === "true";
      burger.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("is-open", !open);
    });
  }

  /* ======================================================================
     Boot
     ====================================================================== */
  function init() {
    playHero();
    initHeader();
    initMarquee();
    initReveals();
    initCounters();
    initStory();
    initParallax();
    initBurger();

    // Fonts change metrics; recalculate trigger positions once they land.
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(function () { ScrollTrigger.refresh(); });
    }
    window.addEventListener("load", function () { ScrollTrigger.refresh(); });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
