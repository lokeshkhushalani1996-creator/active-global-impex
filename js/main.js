/* =========================================================
   ACTIVE GLOBAL IMPEX — main.js
   Vanilla-JS re-implementation of the original React behaviours:
   Header.tsx (scroll state + mobile drawer), HeroSection.tsx (ticker),
   ProductsSection/ProductsPageContent (category tabs),
   WhatsAppFloat.tsx (delayed tooltip + dismiss), scroll reveals.
   No external libraries.
   ========================================================= */

(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    initHeaderScroll();
    initMobileDrawer();
    initTicker();
    initReveal();
    initCategoryTabs();
    initWhatsAppFloat();
    initFooterYear();
    initActiveNav();
  });

  /* ---- Header background state on scroll (Header.tsx: scrolled > 24) ---- */
  function initHeaderScroll() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    var onScroll = function () {
      header.classList.toggle("scrolled", window.scrollY > 24);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---- Mobile drawer (Header.tsx mobile nav) ---- */
  function initMobileDrawer() {
    var toggle = document.querySelector(".mobile-toggle");
    var drawer = document.querySelector(".mobile-drawer");
    var scrim = document.querySelector(".mobile-scrim");
    var closeBtn = document.querySelector(".mobile-drawer-close");
    if (!toggle || !drawer) return;

    function open() {
      drawer.classList.add("open");
      if (scrim) scrim.classList.add("open");
      toggle.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
    }
    function close() {
      drawer.classList.remove("open");
      if (scrim) scrim.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    }

    toggle.addEventListener("click", function () {
      drawer.classList.contains("open") ? close() : open();
    });
    if (closeBtn) closeBtn.addEventListener("click", close);
    if (scrim) scrim.addEventListener("click", close);
    drawer.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", close);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
  }

  /* ---- Commodity ticker: triple the item list for seamless -50% loop ---- */
  function initTicker() {
    var track = document.querySelector(".ticker-track");
    if (!track) return;
    var original = Array.prototype.slice.call(track.children);
    if (!original.length) return;
    // Duplicate twice more (3x total) so the -50% keyframe loops seamlessly
    for (var r = 0; r < 2; r++) {
      original.forEach(function (node) {
        track.appendChild(node.cloneNode(true));
      });
    }
  }

  /* ---- Scroll-reveal via IntersectionObserver (replaces Framer Motion whileInView) ---- */
  function initReveal() {
    var targets = document.querySelectorAll("[data-animate]");
    if (!targets.length) return;

    document.querySelectorAll("[data-animate-group]").forEach(function (group) {
      var children = group.querySelectorAll("[data-animate]");
      children.forEach(function (child, i) {
        child.style.setProperty("--stagger", i);
      });
    });

    if (!("IntersectionObserver" in window)) {
      targets.forEach(function (el) { el.classList.add("in-view"); });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -10% 0px" }
    );
    targets.forEach(function (el) { observer.observe(el); });
  }

  /* ---- Product category tabs (ProductsSection / ProductsPageContent) ---- */
  function initCategoryTabs() {
    var tabs = document.querySelectorAll(".tabs [role='tab']");
    if (!tabs.length) return;
    var panels = document.querySelectorAll(".tab-panel");

    function activate(tab) {
      tabs.forEach(function (t) { t.setAttribute("aria-selected", "false"); });
      tab.setAttribute("aria-selected", "true");
      var target = tab.getAttribute("data-target");
      panels.forEach(function (p) {
        var match = p.getAttribute("data-panel") === target;
        p.classList.toggle("active", match);
        p.hidden = !match;
      });
    }

    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () { activate(tab); });
    });

    var hash = window.location.hash.replace("#", "");
    var preselect = null;
    if (hash) {
      // Individual product anchors (e.g. #sesame-seeds) belong to a category;
      // find the panel containing that anchor and select its tab.
      var target = document.getElementById(hash);
      if (target) {
        var panel = target.closest(".tab-panel");
        if (panel) {
          var panelKey = panel.getAttribute("data-panel");
          preselect = Array.prototype.find.call(tabs, function (t) {
            return t.getAttribute("data-target") === panelKey;
          });
        }
      }
    }
    activate(preselect || tabs[0]);
    if (hash) {
      window.setTimeout(function () {
        var el = document.getElementById(hash);
        if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
      }, 60);
    }
  }

  /* ---- WhatsApp float: tooltip auto-shows after 3.5s, dismissible (WhatsAppFloat.tsx) ---- */
  function initWhatsAppFloat() {
    var tooltip = document.querySelector(".wa-tooltip");
    var fab = document.querySelector(".wa-fab");
    var dismissBtn = document.querySelector(".wa-tooltip-dismiss");
    if (!tooltip) return;
    var dismissed = false;

    var timer = window.setTimeout(function () {
      if (!dismissed) tooltip.classList.add("show");
    }, 3500);

    if (dismissBtn) {
      dismissBtn.addEventListener("click", function () {
        dismissed = true;
        window.clearTimeout(timer);
        tooltip.classList.remove("show");
      });
    }
    if (fab) {
      fab.addEventListener("click", function () {
        tooltip.classList.remove("show");
      });
    }
  }

  /* ---- Footer year ---- */
  function initFooterYear() {
    document.querySelectorAll("[data-current-year]").forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  }

  /* ---- aria-current on nav links matching current path ---- */
  function initActiveNav() {
    var path = window.location.pathname.replace(/\/index\.html$/, "/").replace(/\/+$/, "/");
    document.querySelectorAll(".main-nav a[href], .mobile-nav-list a[href]").forEach(function (link) {
      var href = new URL(link.getAttribute("href"), window.location.href).pathname.replace(/\/+$/, "/");
      if (href === path) link.setAttribute("aria-current", "page");
    });
  }
})();
