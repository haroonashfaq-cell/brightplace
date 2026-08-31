/* @ds-bundle: {"format":4,"namespace":"BrightplaceDesignSystem_e4f9b1","components":[],"sourceHashes":{"export/src/deck-stage.js":"522102a1c71e","export/src/shared.jsx":"2253c8a0f664","export/src/slides.jsx":"9666106bef16","ui_kits/carousel/BridgeSlide.jsx":"759946755703","ui_kits/carousel/CoverSlide.jsx":"600edf228c5b","ui_kits/carousel/CtaSlide.jsx":"7e69064fe0e5","ui_kits/carousel/DetailSlide.jsx":"96ea0f46136f","ui_kits/carousel/MapSlide.jsx":"7c2f0f1b31f8","ui_kits/dallas_families/deck-stage.js":"522102a1c71e","ui_kits/dallas_families/shared.jsx":"2253c8a0f664","ui_kits/dallas_families/slides.jsx":"516ccf89c2e0","ui_kits/maps/EditorialMap.jsx":"d02e936cb0ec","ui_kits/maps/PreciseMap.jsx":"e089f765ad9d","ui_kits/story/StoryCta.jsx":"9a247b3399c2","ui_kits/story/StoryHero.jsx":"5f2055e9050b","ui_kits/story/StoryQuote.jsx":"06e5a7c1c052","ui_kits/story/StoryStat.jsx":"0de3d2faf3a4"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.BrightplaceDesignSystem_e4f9b1 = window.BrightplaceDesignSystem_e4f9b1 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// export/src/deck-stage.js
try { (() => {
/**
 * <deck-stage> — reusable web component for HTML decks.
 *
 * Handles:
 *  (a) speaker notes — reads <script type="application/json" id="speaker-notes">
 *      and posts {slideIndexChanged: N} to the parent window on nav.
 *  (b) keyboard navigation — ←/→, PgUp/PgDn, Space, Home/End, number keys.
 *  (c) press R to reset to slide 0 (with a tasteful keyboard hint).
 *  (d) bottom-center overlay showing slide count + hints, fades out on idle.
 *  (e) auto-scaling — inner canvas is a fixed design size (default 1920×1080)
 *      scaled with `transform: scale()` to fit the viewport, letterboxed.
 *      Set the `noscale` attribute to render at authored size (1:1) — the
 *      PPTX exporter sets this so its DOM capture sees unscaled geometry.
 *  (f) print — `@media print` lays every slide out as its own page at the
 *      design size, so the browser's Print → Save as PDF produces a clean
 *      one-page-per-slide PDF with no extra setup.
 *
 * Slides are HIDDEN, not unmounted. Non-active slides stay in the DOM with
 * `visibility: hidden` + `opacity: 0`, so their state (videos, iframes,
 * form inputs, React trees) is preserved across navigation.
 *
 * Lifecycle event — the component dispatches a `slidechange` CustomEvent on
 * itself whenever the active slide changes (including the initial mount).
 * The event bubbles and composes out of shadow DOM, so you can listen on
 * the <deck-stage> element or on document:
 *
 *   document.querySelector('deck-stage').addEventListener('slidechange', (e) => {
 *     e.detail.index         // new 0-based index
 *     e.detail.previousIndex // previous index, or -1 on init
 *     e.detail.total         // total slide count
 *     e.detail.slide         // the new active slide element
 *     e.detail.previousSlide // the prior slide element, or null on init
 *     e.detail.reason        // 'init' | 'keyboard' | 'click' | 'tap' | 'api'
 *   });
 *
 * Persistence: current slide index is saved to localStorage keyed by the
 * document path, so refresh returns you to the same place.
 *
 * Usage:
 *   <deck-stage width="1920" height="1080">
 *     <section data-label="Title">...</section>
 *     <section data-label="Agenda">...</section>
 *   </deck-stage>
 *
 * Slides are the direct element children of <deck-stage>. Each slide is
 * automatically tagged with:
 *   - data-screen-label="NN Label"   (1-indexed, for comment flow)
 *   - data-om-validate="no_overflowing_text,no_overlapping_text,slide_sized_text"
 */

(() => {
  const DESIGN_W_DEFAULT = 1920;
  const DESIGN_H_DEFAULT = 1080;
  const STORAGE_PREFIX = 'deck-stage:slide:';
  const OVERLAY_HIDE_MS = 1800;
  const VALIDATE_ATTR = 'no_overflowing_text,no_overlapping_text,slide_sized_text';
  const pad2 = n => String(n).padStart(2, '0');
  const stylesheet = `
    :host {
      position: fixed;
      inset: 0;
      display: block;
      background: #000;
      color: #fff;
      font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, Arial, sans-serif;
      overflow: hidden;
    }

    .stage {
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .canvas {
      position: relative;
      transform-origin: center center;
      flex-shrink: 0;
      background: #fff;
      will-change: transform;
    }

    /* Slides live in light DOM (via <slot>) so authored CSS still applies.
       We absolutely position each slotted child to stack them. */
    ::slotted(*) {
      position: absolute !important;
      inset: 0 !important;
      width: 100% !important;
      height: 100% !important;
      box-sizing: border-box !important;
      overflow: hidden;
      opacity: 0;
      pointer-events: none;
      visibility: hidden;
    }
    ::slotted([data-deck-active]) {
      opacity: 1;
      pointer-events: auto;
      visibility: visible;
    }

    /* Tap zones for mobile — back/forward thirds like Stories.
       Transparent, no visible UI, don't block the overlay. */
    .tapzones {
      position: fixed;
      inset: 0;
      display: flex;
      z-index: 2147482000;
      pointer-events: none;
    }
    .tapzone {
      flex: 1;
      pointer-events: auto;
      -webkit-tap-highlight-color: transparent;
    }
    /* Only activate tap zones on coarse pointers (touch devices). */
    @media (hover: hover) and (pointer: fine) {
      .tapzones { display: none; }
    }

    .overlay {
      position: fixed;
      left: 50%;
      bottom: 22px;
      transform: translate(-50%, 6px) scale(0.92);
      filter: blur(6px);
      display: flex;
      align-items: center;
      gap: 4px;
      padding: 4px;
      background: #000;
      color: #fff;
      border-radius: 999px;
      font-size: 12px;
      font-feature-settings: "tnum" 1;
      letter-spacing: 0.01em;
      opacity: 0;
      pointer-events: none;
      transition: opacity 260ms ease, transform 260ms cubic-bezier(.2,.8,.2,1), filter 260ms ease;
      transform-origin: center bottom;
      z-index: 2147483000;
      user-select: none;
    }
    .overlay[data-visible] {
      opacity: 1;
      pointer-events: auto;
      transform: translate(-50%, 0) scale(1);
      filter: blur(0);
    }

    .btn {
      appearance: none;
      -webkit-appearance: none;
      background: transparent;
      border: 0;
      margin: 0;
      padding: 0;
      color: inherit;
      font: inherit;
      cursor: default;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      height: 28px;
      min-width: 28px;
      border-radius: 999px;
      color: rgba(255,255,255,0.72);
      transition: background 140ms ease, color 140ms ease;
      -webkit-tap-highlight-color: transparent;
    }
    .btn:hover { background: rgba(255,255,255,0.12); color: #fff; }
    .btn:active { background: rgba(255,255,255,0.18); }
    .btn:focus { outline: none; }
    .btn:focus-visible { outline: none; }
    .btn::-moz-focus-inner { border: 0; }
    .btn svg { width: 14px; height: 14px; display: block; }
    .btn.reset {
      font-size: 11px;
      font-weight: 500;
      letter-spacing: 0.02em;
      padding: 0 10px 0 12px;
      gap: 6px;
      color: rgba(255,255,255,0.72);
    }
    .btn.reset .kbd {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 16px;
      height: 16px;
      padding: 0 4px;
      font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
      font-size: 10px;
      line-height: 1;
      color: rgba(255,255,255,0.88);
      background: rgba(255,255,255,0.12);
      border-radius: 4px;
    }

    .count {
      font-variant-numeric: tabular-nums;
      color: #fff;
      font-weight: 500;
      padding: 0 8px;
      min-width: 42px;
      text-align: center;
      font-size: 12px;
    }
    .count .sep { color: rgba(255,255,255,0.45); margin: 0 3px; font-weight: 400; }
    .count .total { color: rgba(255,255,255,0.55); }

    .divider {
      width: 1px;
      height: 14px;
      background: rgba(255,255,255,0.18);
      margin: 0 2px;
    }

    /* ── Print: one page per slide, no chrome ────────────────────────────
       The screen layout stacks every slide at inset:0 inside a scaled
       canvas; for print we want them in document flow at the authored
       design size so the browser paginates one slide per sheet. The
       @page size is set from the width/height attributes via the inline
       <style id="deck-stage-print-page"> that connectedCallback injects
       into <head> (the @page at-rule has no effect inside shadow DOM). */
    @media print {
      :host {
        position: static;
        inset: auto;
        background: none;
        overflow: visible;
        color: inherit;
      }
      .stage { position: static; display: block; }
      .canvas {
        transform: none !important;
        width: auto !important;
        height: auto !important;
        background: none;
        will-change: auto;
      }
      ::slotted(*) {
        position: relative !important;
        inset: auto !important;
        width: var(--deck-design-w) !important;
        height: var(--deck-design-h) !important;
        box-sizing: border-box !important;
        opacity: 1 !important;
        visibility: visible !important;
        pointer-events: auto;
        break-after: page;
        page-break-after: always;
        break-inside: avoid;
        overflow: hidden;
      }
      ::slotted(*:last-child) {
        break-after: auto;
        page-break-after: auto;
      }
      .overlay, .tapzones { display: none !important; }
    }
  `;
  class DeckStage extends HTMLElement {
    static get observedAttributes() {
      return ['width', 'height', 'noscale'];
    }
    constructor() {
      super();
      this._root = this.attachShadow({
        mode: 'open'
      });
      this._index = 0;
      this._slides = [];
      this._notes = [];
      this._hideTimer = null;
      this._mouseIdleTimer = null;
      this._storageKey = STORAGE_PREFIX + (location.pathname || '/');
      this._onKey = this._onKey.bind(this);
      this._onResize = this._onResize.bind(this);
      this._onSlotChange = this._onSlotChange.bind(this);
      this._onMouseMove = this._onMouseMove.bind(this);
      this._onTapBack = this._onTapBack.bind(this);
      this._onTapForward = this._onTapForward.bind(this);
    }
    get designWidth() {
      return parseInt(this.getAttribute('width'), 10) || DESIGN_W_DEFAULT;
    }
    get designHeight() {
      return parseInt(this.getAttribute('height'), 10) || DESIGN_H_DEFAULT;
    }
    connectedCallback() {
      this._render();
      this._loadNotes();
      this._syncPrintPageRule();
      window.addEventListener('keydown', this._onKey);
      window.addEventListener('resize', this._onResize);
      window.addEventListener('mousemove', this._onMouseMove, {
        passive: true
      });
      // Initial collection + layout happens via slotchange, which fires on mount.
    }
    disconnectedCallback() {
      window.removeEventListener('keydown', this._onKey);
      window.removeEventListener('resize', this._onResize);
      window.removeEventListener('mousemove', this._onMouseMove);
      if (this._hideTimer) clearTimeout(this._hideTimer);
      if (this._mouseIdleTimer) clearTimeout(this._mouseIdleTimer);
    }
    attributeChangedCallback() {
      if (this._canvas) {
        this._canvas.style.width = this.designWidth + 'px';
        this._canvas.style.height = this.designHeight + 'px';
        this._canvas.style.setProperty('--deck-design-w', this.designWidth + 'px');
        this._canvas.style.setProperty('--deck-design-h', this.designHeight + 'px');
        this._fit();
        this._syncPrintPageRule();
      }
    }
    _render() {
      const style = document.createElement('style');
      style.textContent = stylesheet;
      const stage = document.createElement('div');
      stage.className = 'stage';
      const canvas = document.createElement('div');
      canvas.className = 'canvas';
      canvas.style.width = this.designWidth + 'px';
      canvas.style.height = this.designHeight + 'px';
      canvas.style.setProperty('--deck-design-w', this.designWidth + 'px');
      canvas.style.setProperty('--deck-design-h', this.designHeight + 'px');
      const slot = document.createElement('slot');
      slot.addEventListener('slotchange', this._onSlotChange);
      canvas.appendChild(slot);
      stage.appendChild(canvas);

      // Tap zones (mobile): left third = back, right third = forward.
      const tapzones = document.createElement('div');
      tapzones.className = 'tapzones export-hidden';
      tapzones.setAttribute('aria-hidden', 'true');
      const tzBack = document.createElement('div');
      tzBack.className = 'tapzone tapzone--back';
      const tzMid = document.createElement('div');
      tzMid.className = 'tapzone tapzone--mid';
      tzMid.style.pointerEvents = 'none';
      const tzFwd = document.createElement('div');
      tzFwd.className = 'tapzone tapzone--fwd';
      tzBack.addEventListener('click', this._onTapBack);
      tzFwd.addEventListener('click', this._onTapForward);
      tapzones.append(tzBack, tzMid, tzFwd);

      // Overlay: compact, solid black, with clickable controls.
      const overlay = document.createElement('div');
      overlay.className = 'overlay export-hidden';
      overlay.setAttribute('role', 'toolbar');
      overlay.setAttribute('aria-label', 'Deck controls');
      overlay.innerHTML = `
        <button class="btn prev" type="button" aria-label="Previous slide" title="Previous (←)">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 3L5 8l5 5"/></svg>
        </button>
        <span class="count" aria-live="polite"><span class="current">1</span><span class="sep">/</span><span class="total">1</span></span>
        <button class="btn next" type="button" aria-label="Next slide" title="Next (→)">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3l5 5-5 5"/></svg>
        </button>
        <span class="divider"></span>
        <button class="btn reset" type="button" aria-label="Reset to first slide" title="Reset (R)">Reset<span class="kbd">R</span></button>
      `;
      overlay.querySelector('.prev').addEventListener('click', () => this._go(this._index - 1, 'click'));
      overlay.querySelector('.next').addEventListener('click', () => this._go(this._index + 1, 'click'));
      overlay.querySelector('.reset').addEventListener('click', () => this._go(0, 'click'));
      this._root.append(style, stage, tapzones, overlay);
      this._canvas = canvas;
      this._slot = slot;
      this._overlay = overlay;
      this._countEl = overlay.querySelector('.current');
      this._totalEl = overlay.querySelector('.total');
    }

    /** @page must live in the document stylesheet — it's a no-op inside
     *  shadow DOM. Inject/update a single <head> style tag so the print
     *  sheet matches the design size and Save-as-PDF yields one slide per
     *  page with no margins. */
    _syncPrintPageRule() {
      const id = 'deck-stage-print-page';
      let tag = document.getElementById(id);
      if (!tag) {
        tag = document.createElement('style');
        tag.id = id;
        document.head.appendChild(tag);
      }
      tag.textContent = '@page { size: ' + this.designWidth + 'px ' + this.designHeight + 'px; margin: 0; } ' + '@media print { html, body { margin: 0 !important; padding: 0 !important; background: none !important; overflow: visible !important; height: auto !important; } ' + '* { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }';
    }
    _onSlotChange() {
      this._collectSlides();
      this._restoreIndex();
      this._applyIndex({
        showOverlay: false,
        broadcast: true,
        reason: 'init'
      });
      this._fit();
    }
    _collectSlides() {
      const assigned = this._slot.assignedElements({
        flatten: true
      });
      this._slides = assigned.filter(el => {
        // Skip template/style/script nodes even if someone slots them.
        const tag = el.tagName;
        return tag !== 'TEMPLATE' && tag !== 'SCRIPT' && tag !== 'STYLE';
      });
      this._slides.forEach((slide, i) => {
        const n = i + 1;
        // Determine a label for comment flow: prefer explicit data-label,
        // then an existing data-screen-label, then first heading, else "Slide".
        let label = slide.getAttribute('data-label');
        if (!label) {
          const existing = slide.getAttribute('data-screen-label');
          if (existing) {
            // Strip any leading number the author may have included.
            label = existing.replace(/^\s*\d+\s*/, '').trim() || existing;
          }
        }
        if (!label) {
          const h = slide.querySelector('h1, h2, h3, [data-title]');
          if (h) label = (h.textContent || '').trim().slice(0, 40);
        }
        if (!label) label = 'Slide';
        slide.setAttribute('data-screen-label', `${pad2(n)} ${label}`);

        // Validation attribute for comment flow / auto-checks.
        if (!slide.hasAttribute('data-om-validate')) {
          slide.setAttribute('data-om-validate', VALIDATE_ATTR);
        }
        slide.setAttribute('data-deck-slide', String(i));
      });
      if (this._totalEl) this._totalEl.textContent = String(this._slides.length || 1);
      if (this._index >= this._slides.length) this._index = Math.max(0, this._slides.length - 1);
    }
    _loadNotes() {
      const tag = document.getElementById('speaker-notes');
      if (!tag) {
        this._notes = [];
        return;
      }
      try {
        const parsed = JSON.parse(tag.textContent || '[]');
        if (Array.isArray(parsed)) this._notes = parsed;
      } catch (e) {
        console.warn('[deck-stage] Failed to parse #speaker-notes JSON:', e);
        this._notes = [];
      }
    }
    _restoreIndex() {
      try {
        const raw = localStorage.getItem(this._storageKey);
        if (raw != null) {
          const n = parseInt(raw, 10);
          if (Number.isFinite(n) && n >= 0 && n < this._slides.length) {
            this._index = n;
          }
        }
      } catch (e) {/* ignore */}
    }
    _persistIndex() {
      try {
        localStorage.setItem(this._storageKey, String(this._index));
      } catch (e) {/* ignore */}
    }
    _applyIndex({
      showOverlay = true,
      broadcast = true,
      reason = 'init'
    } = {}) {
      if (!this._slides.length) return;
      const prev = this._prevIndex == null ? -1 : this._prevIndex;
      const curr = this._index;
      this._slides.forEach((s, i) => {
        if (i === curr) s.setAttribute('data-deck-active', '');else s.removeAttribute('data-deck-active');
      });
      if (this._countEl) this._countEl.textContent = String(curr + 1);
      this._persistIndex();
      if (broadcast) {
        // (1) Legacy: host-window postMessage for speaker-notes renderers.
        try {
          window.postMessage({
            slideIndexChanged: curr
          }, '*');
        } catch (e) {}

        // (2) In-page CustomEvent on the <deck-stage> element itself.
        //     Bubbles and composes out of shadow DOM so slide code can listen:
        //       document.querySelector('deck-stage').addEventListener('slidechange', e => {
        //         e.detail.index, e.detail.previousIndex, e.detail.total, e.detail.slide, e.detail.reason
        //       });
        const detail = {
          index: curr,
          previousIndex: prev,
          total: this._slides.length,
          slide: this._slides[curr] || null,
          previousSlide: prev >= 0 ? this._slides[prev] || null : null,
          reason: reason // 'init' | 'keyboard' | 'click' | 'tap' | 'api'
        };
        this.dispatchEvent(new CustomEvent('slidechange', {
          detail,
          bubbles: true,
          composed: true
        }));
      }
      this._prevIndex = curr;
      if (showOverlay) this._flashOverlay();
    }
    _flashOverlay() {
      if (!this._overlay) return;
      this._overlay.setAttribute('data-visible', '');
      if (this._hideTimer) clearTimeout(this._hideTimer);
      this._hideTimer = setTimeout(() => {
        this._overlay.removeAttribute('data-visible');
      }, OVERLAY_HIDE_MS);
    }
    _fit() {
      if (!this._canvas) return;
      // PPTX export sets noscale so the DOM capture sees authored-size
      // geometry — the scaled canvas is in shadow DOM, so the exporter's
      // resetTransformSelector can't reach .canvas.style.transform directly.
      if (this.hasAttribute('noscale')) {
        this._canvas.style.transform = 'none';
        return;
      }
      const vw = window.innerWidth;
      const vh = window.innerHeight;
      const s = Math.min(vw / this.designWidth, vh / this.designHeight);
      this._canvas.style.transform = `scale(${s})`;
    }
    _onResize() {
      this._fit();
    }
    _onMouseMove() {
      // Keep overlay visible while mouse moves; hide after idle.
      this._flashOverlay();
    }
    _onTapBack(e) {
      e.preventDefault();
      this._go(this._index - 1, 'tap');
    }
    _onTapForward(e) {
      e.preventDefault();
      this._go(this._index + 1, 'tap');
    }
    _onKey(e) {
      // Ignore when the user is typing.
      const t = e.target;
      if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const key = e.key;
      let handled = true;
      if (key === 'ArrowRight' || key === 'PageDown' || key === ' ' || key === 'Spacebar') {
        this._go(this._index + 1, 'keyboard');
      } else if (key === 'ArrowLeft' || key === 'PageUp') {
        this._go(this._index - 1, 'keyboard');
      } else if (key === 'Home') {
        this._go(0, 'keyboard');
      } else if (key === 'End') {
        this._go(this._slides.length - 1, 'keyboard');
      } else if (key === 'r' || key === 'R') {
        this._go(0, 'keyboard');
      } else if (/^[0-9]$/.test(key)) {
        // 1..9 jump to that slide; 0 jumps to 10.
        const n = key === '0' ? 9 : parseInt(key, 10) - 1;
        if (n < this._slides.length) this._go(n, 'keyboard');
      } else {
        handled = false;
      }
      if (handled) {
        e.preventDefault();
        this._flashOverlay();
      }
    }
    _go(i, reason = 'api') {
      if (!this._slides.length) return;
      const clamped = Math.max(0, Math.min(this._slides.length - 1, i));
      if (clamped === this._index) {
        this._flashOverlay();
        return;
      }
      this._index = clamped;
      this._applyIndex({
        showOverlay: true,
        broadcast: true,
        reason
      });
    }

    // Public API ------------------------------------------------------------

    /** Current slide index (0-based). */
    get index() {
      return this._index;
    }
    /** Total slide count. */
    get length() {
      return this._slides.length;
    }
    /** Programmatically navigate. */
    goTo(i) {
      this._go(i, 'api');
    }
    next() {
      this._go(this._index + 1, 'api');
    }
    prev() {
      this._go(this._index - 1, 'api');
    }
    reset() {
      this._go(0, 'api');
    }
  }
  if (!customElements.get('deck-stage')) {
    customElements.define('deck-stage', DeckStage);
  }
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "export/src/deck-stage.js", error: String((e && e.message) || e) }); }

// export/src/shared.jsx
try { (() => {
// Shared washi tape element — cream textured torn-edge rectangle.
function Washi({
  width = 260,
  rotate = -2,
  top = -22,
  left = "50%"
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      top,
      left,
      transform: `translateX(-50%) rotate(${rotate}deg)`,
      width,
      height: 64,
      zIndex: 2,
      pointerEvents: "none"
    }
  }, /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 260 64",
    width: "100%",
    height: "100%",
    preserveAspectRatio: "none"
  }, /*#__PURE__*/React.createElement("defs", null, /*#__PURE__*/React.createElement("linearGradient", {
    id: "washiG",
    x1: "0",
    x2: "0",
    y1: "0",
    y2: "1"
  }, /*#__PURE__*/React.createElement("stop", {
    offset: "0",
    stopColor: "#F1E7D2"
  }), /*#__PURE__*/React.createElement("stop", {
    offset: ".5",
    stopColor: "#E8DCC3"
  }), /*#__PURE__*/React.createElement("stop", {
    offset: "1",
    stopColor: "#EFE4CE"
  })), /*#__PURE__*/React.createElement("filter", {
    id: "washiN",
    x: "0",
    y: "0"
  }, /*#__PURE__*/React.createElement("feTurbulence", {
    type: "fractalNoise",
    baseFrequency: "0.9",
    numOctaves: "2",
    seed: "3"
  }), /*#__PURE__*/React.createElement("feColorMatrix", {
    values: "0 0 0 0 0.2  0 0 0 0 0.15  0 0 0 0 0.1  0 0 0 .22 0"
  }), /*#__PURE__*/React.createElement("feComposite", {
    in2: "SourceGraphic",
    operator: "in"
  }))), /*#__PURE__*/React.createElement("path", {
    d: "M 4 10 L 14 6 L 28 10 L 42 5 L 60 9 L 80 6 L 100 10 L 124 7 L 150 10 L 172 6 L 196 9 L 222 7 L 244 10 L 256 8 L 256 54 L 246 58 L 228 54 L 208 57 L 184 54 L 160 58 L 140 54 L 116 57 L 92 54 L 70 58 L 48 54 L 28 57 L 10 55 L 4 58 Z",
    fill: "url(#washiG)"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 4 10 L 14 6 L 28 10 L 42 5 L 60 9 L 80 6 L 100 10 L 124 7 L 150 10 L 172 6 L 196 9 L 222 7 L 244 10 L 256 8 L 256 54 L 246 58 L 228 54 L 208 57 L 184 54 L 160 58 L 140 54 L 116 57 L 92 54 L 70 58 L 48 54 L 28 57 L 10 55 L 4 58 Z",
    filter: "url(#washiN)",
    opacity: ".5"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 90 18 L 130 46",
    stroke: "rgba(0,0,0,.08)",
    strokeWidth: "1"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 170 20 L 200 48",
    stroke: "rgba(0,0,0,.06)",
    strokeWidth: "1"
  })));
}
window.Washi = Washi;

// Orange asterisk/star bullet — 6-point stylized asterisk
function StarBullet({
  size = 28,
  color = "#F5A623"
}) {
  return /*#__PURE__*/React.createElement("svg", {
    width: size,
    height: size,
    viewBox: "0 0 32 32",
    style: {
      flex: `0 0 ${size}px`
    }
  }, /*#__PURE__*/React.createElement("g", {
    stroke: color,
    strokeWidth: "4",
    strokeLinecap: "round",
    fill: "none"
  }, /*#__PURE__*/React.createElement("line", {
    x1: "16",
    y1: "5",
    x2: "16",
    y2: "27"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "6",
    y1: "10",
    x2: "26",
    y2: "22"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "6",
    y1: "22",
    x2: "26",
    y2: "10"
  })));
}
window.StarBullet = StarBullet;

// Warm photo placeholder with SWAP tag
function PhotoPlaceholder({
  gradient = ["#BFD9C7", "#9EC5B8"],
  label = "SWAP PHOTO"
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      background: `linear-gradient(155deg, ${gradient[0]} 0%, ${gradient[1]} 100%)`,
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      backgroundImage: "radial-gradient(circle at 25% 30%, rgba(255,255,255,.35) 0%, transparent 45%), radial-gradient(circle at 75% 75%, rgba(255,255,255,.2) 0%, transparent 40%)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      top: 28,
      right: 28,
      fontFamily: "var(--ff-body)",
      fontSize: 14,
      fontWeight: 700,
      letterSpacing: ".12em",
      color: "rgba(255,255,255,.92)",
      background: "rgba(0,0,0,.28)",
      padding: "6px 12px",
      borderRadius: 4,
      backdropFilter: "blur(4px)"
    }
  }, label));
}
window.PhotoPlaceholder = PhotoPlaceholder;

// Detail card — white panel with washi tape, title, star bullets
function DetailCard({
  title,
  bullets
}) {
  // bullets are strings. First char can be a special marker to style tradeoff/best-for labels
  return /*#__PURE__*/React.createElement("div", {
    style: dcS.card
  }, /*#__PURE__*/React.createElement(Washi, {
    width: 260,
    rotate: -2,
    top: -22,
    left: "50%"
  }), /*#__PURE__*/React.createElement("h2", {
    style: dcS.title
  }, title), /*#__PURE__*/React.createElement("ul", {
    style: dcS.list
  }, bullets.map((b, i) => {
    // Detect "Tradeoff:" or "Best for:" prefix; split on first colon if present
    const tradeoffMatch = /^Tradeoff:\s*/i.test(b);
    const bestforMatch = /^Best for:\s*/i.test(b);
    let labelEl = null,
      rest = b;
    if (tradeoffMatch) {
      rest = b.replace(/^Tradeoff:\s*/i, "");
      labelEl = /*#__PURE__*/React.createElement("span", {
        style: {
          ...dcS.inlineLabel,
          color: "#F5A623"
        }
      }, "Tradeoff: ");
    } else if (bestforMatch) {
      rest = b.replace(/^Best for:\s*/i, "");
      labelEl = /*#__PURE__*/React.createElement("span", {
        style: {
          ...dcS.inlineLabel,
          color: "#00BCD4"
        }
      }, "Best for: ");
    }
    return /*#__PURE__*/React.createElement("li", {
      key: i,
      style: dcS.item
    }, /*#__PURE__*/React.createElement(StarBullet, {
      size: 28
    }), /*#__PURE__*/React.createElement("span", {
      style: dcS.text
    }, labelEl, rest));
  })));
}
const dcS = {
  card: {
    position: "absolute",
    left: 80,
    right: 80,
    top: 300,
    bottom: 140,
    background: "#FFFFFF",
    padding: "60px 56px 52px",
    boxShadow: "0 30px 60px rgba(26,39,68,.2), 0 4px 12px rgba(26,39,68,.12)",
    boxSizing: "border-box"
  },
  title: {
    fontFamily: "'Libre Baskerville', serif",
    fontWeight: 700,
    fontSize: 64,
    lineHeight: 1.05,
    color: "#F5A623",
    textAlign: "center",
    margin: "0 0 36px",
    letterSpacing: "-0.005em"
  },
  list: {
    listStyle: "none",
    padding: 0,
    margin: 0,
    display: "flex",
    flexDirection: "column",
    gap: 22
  },
  item: {
    display: "flex",
    gap: 18,
    alignItems: "flex-start",
    listStyle: "none"
  },
  text: {
    fontFamily: "'Lato', sans-serif",
    fontWeight: 400,
    fontSize: 26,
    lineHeight: 1.4,
    color: "#1A2744",
    paddingTop: 2,
    flex: "1 1 auto",
    display: "block"
  },
  inlineLabel: {
    fontFamily: "'Lato', sans-serif",
    fontWeight: 700
  }
};
window.DetailCard = DetailCard;
})(); } catch (e) { __ds_ns.__errors.push({ path: "export/src/shared.jsx", error: String((e && e.message) || e) }); }

// export/src/slides.jsx
try { (() => {
// Dallas Families carousel — 8 slides, 1080x1350
// Uses window.Washi, window.StarBullet, window.PhotoPlaceholder, window.DetailCard

function CoverSlide() {
  return /*#__PURE__*/React.createElement("div", {
    style: sS.slide,
    "data-screen-label": "01 Cover"
  }, /*#__PURE__*/React.createElement("img", {
    src: window.__resources.photo_cover,
    alt: "",
    style: sS.bg
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      background: "linear-gradient(180deg, rgba(0,0,0,.15) 0%, rgba(0,0,0,.05) 40%, rgba(0,0,0,.25) 100%)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      padding: "0 80px",
      textAlign: "center",
      color: "#fff"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "'Lato',sans-serif",
      fontWeight: 400,
      fontSize: 30,
      letterSpacing: ".02em",
      marginBottom: 28,
      textShadow: "0 2px 12px rgba(0,0,0,.3)"
    }
  }, "where to find a family home in"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontFamily: "'Libre Baskerville',serif",
      fontWeight: 700,
      fontSize: 132,
      lineHeight: 1,
      margin: 0,
      letterSpacing: "-0.01em",
      textShadow: "0 2px 20px rgba(0,0,0,.35)"
    }
  }, "dallas, texas"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "'Lato',sans-serif",
      fontWeight: 400,
      fontSize: 30,
      lineHeight: 1.45,
      marginTop: 52,
      maxWidth: 820,
      textShadow: "0 2px 12px rgba(0,0,0,.3)"
    }
  }, "School district lines don't follow city limits here. Here's where to look before you sign.")));
}
function MapSlide() {
  return /*#__PURE__*/React.createElement("div", {
    style: sS.slide,
    "data-screen-label": "02 Map"
  }, /*#__PURE__*/React.createElement("img", {
    src: window.__resources.photo_cover,
    alt: "",
    style: sS.bg
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      background: "linear-gradient(180deg, rgba(0,0,0,.1) 0%, transparent 40%, rgba(0,0,0,.25) 100%)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      left: 80,
      right: 80,
      top: 130,
      bottom: 180,
      background: "#F5EFE2"
    }
  }, /*#__PURE__*/React.createElement(Washi, {
    width: 300,
    rotate: -3,
    top: -26,
    left: "50%"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: "40px 40px 40px 40px",
      background: "repeating-linear-gradient(90deg, transparent 0 60px, rgba(26,39,68,.08) 60px 61px), repeating-linear-gradient(0deg, transparent 0 60px, rgba(26,39,68,.08) 60px 61px), #FDF9EE"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      top: 20,
      left: 20,
      fontFamily: "'Libre Baskerville',serif",
      fontSize: 14,
      color: "#1A2744",
      background: "rgba(255,255,255,.8)",
      padding: "4px 10px",
      letterSpacing: ".1em",
      fontWeight: 700
    }
  }, "SWAP MAP"), [{
    top: "22%",
    left: "68%",
    name: "Lake Highlands",
    price: "1BRs from $1,100 to $1,600",
    anchor: "left"
  }, {
    top: "16%",
    left: "28%",
    name: "Richardson",
    price: "1BRs from $1,100 to $2,100",
    anchor: "right"
  }, {
    top: "58%",
    left: "20%",
    name: "Plano",
    price: "1BRs from $1,400 to $2,400",
    anchor: "right"
  }, {
    top: "72%",
    left: "72%",
    name: "Irving / Las Colinas",
    price: "1BRs from $1,100 to $2,000",
    anchor: "left"
  }].map((p, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      position: "absolute",
      top: p.top,
      left: p.left,
      transform: "translate(-50%,-50%)"
    }
  }, /*#__PURE__*/React.createElement(Pin, null), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      top: "100%",
      [p.anchor]: "50%",
      transform: p.anchor === "left" ? "translateX(-50%)" : "translateX(50%)",
      marginTop: 4,
      whiteSpace: "nowrap",
      textAlign: "center"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "'Libre Baskerville',serif",
      fontWeight: 700,
      fontSize: 18,
      color: "#1A2744"
    }
  }, p.name), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "'Libre Baskerville',serif",
      fontWeight: 400,
      fontSize: 13,
      color: "#1A2744",
      opacity: .75,
      marginTop: 2
    }
  }, p.price)))))), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      bottom: 60,
      left: 0,
      right: 0,
      textAlign: "center",
      fontFamily: "'Libre Baskerville',serif",
      fontStyle: "italic",
      fontSize: 26,
      color: "#fff",
      textShadow: "0 2px 10px rgba(0,0,0,.4)"
    }
  }, "The Neighborhoods"));
}
function Pin() {
  return /*#__PURE__*/React.createElement("svg", {
    width: "28",
    height: "36",
    viewBox: "0 0 28 36",
    style: {
      filter: "drop-shadow(0 2px 3px rgba(0,0,0,.25))"
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "M14 0 C6 0 0 6 0 14 C0 24 14 36 14 36 C14 36 28 24 28 14 C28 6 22 0 14 0 Z",
    fill: "#F5A623"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "14",
    cy: "14",
    r: "5",
    fill: "#fff"
  }));
}
function BridgeSlide() {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      ...sS.slide,
      background: "#FFC180"
    },
    "data-screen-label": "03 Bridge"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      padding: "0 100px",
      textAlign: "center"
    }
  }, /*#__PURE__*/React.createElement("h2", {
    style: {
      fontFamily: "'Libre Baskerville',serif",
      fontWeight: 700,
      fontSize: 68,
      lineHeight: 1.15,
      color: "#1A2744",
      margin: 0,
      letterSpacing: "-0.005em"
    }
  }, "Most families find this out after they've already signed."), /*#__PURE__*/React.createElement("div", {
    style: {
      width: 80,
      height: 3,
      background: "#F5A623",
      margin: "48px 0 44px"
    }
  }), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: "'Lato',sans-serif",
      fontWeight: 400,
      fontSize: 30,
      lineHeight: 1.5,
      color: "#1A2744",
      margin: 0,
      maxWidth: 820
    }
  }, "School district boundaries in Dallas don't match city limits. A Plano address doesn't guarantee you're in the Plano school district. Here are the four neighborhoods where the math actually works.")));
}
function LakeHighlands() {
  return /*#__PURE__*/React.createElement("div", {
    style: sS.slide,
    "data-screen-label": "04 Lake Highlands"
  }, /*#__PURE__*/React.createElement("img", {
    src: window.__resources.photo_lake_highlands,
    alt: "",
    style: sS.bg
  }), /*#__PURE__*/React.createElement(DetailCard, {
    title: "Lake Highlands",
    bullets: ["Intown Dallas with White Rock Lake on its doorstep", "1,015-acre park, 9-mile loop trail, sailing club, dog park", "Under 20 minutes to downtown", "One of the stronger intown options within Dallas's school district, though quality varies across the city", "Tradeoff: Families needing school district consistency tend to find the suburbs more reliable", "Best for: Families who want to stay intown with serious park access on their doorstep"]
  }));
}
function Richardson() {
  return /*#__PURE__*/React.createElement("div", {
    style: sS.slide,
    "data-screen-label": "05 Richardson"
  }, /*#__PURE__*/React.createElement("img", {
    src: window.__resources.photo_richardson,
    alt: "",
    style: sS.bg
  }), /*#__PURE__*/React.createElement(DetailCard, {
    title: "Richardson",
    bullets: ["Established suburb with one of the most well-regarded school districts in the metro", "Breckinridge Park: 418 acres of trails, athletic fields, disc golf, and a dog park", "DART rail to downtown in about 30 minutes", "CityLine adds walkable grocery, restaurants, and retail nearby", "Tradeoff: Rents run higher than Lake Highlands. Canyon Creek has the strongest family inventory", "Best for: Families where school quality is a priority and want an established community feel"]
  }));
}
function Plano() {
  return /*#__PURE__*/React.createElement("div", {
    style: sS.slide,
    "data-screen-label": "06 Plano"
  }, /*#__PURE__*/React.createElement("img", {
    src: window.__resources.photo_plano,
    alt: "",
    style: sS.bg
  }), /*#__PURE__*/React.createElement(DetailCard, {
    title: "Plano",
    bullets: ["The go-to answer if school quality is the single biggest factor", "Bluebonnet Trail connects neighborhoods and parks for biking and jogging", "30 to 45 minutes to downtown along the tollway", "Shops at Willow Bend and Legacy West nearby for retail and restaurants", "Tradeoff: Runs 10 to 20 percent higher on rent than comparable Richardson buildings", "Best for: Families where school district is the top priority and budget allows for it"]
  }));
}
function Irving() {
  return /*#__PURE__*/React.createElement("div", {
    style: sS.slide,
    "data-screen-label": "07 Irving / Las Colinas"
  }, /*#__PURE__*/React.createElement("img", {
    src: window.__resources.photo_irving,
    alt: "",
    style: sS.bg
  }), /*#__PURE__*/React.createElement(DetailCard, {
    title: "Irving / Las Colinas",
    bullets: ["The value option for families near DFW airport or the mid-cities corridor", "Lake Carolyn waterfront with restaurants and a lakefront path", "DFW airport 10 minutes away. DART rail to downtown in about 25 minutes", "More urban feel than most Dallas suburbs at a lower price point", "Tradeoff: School quality varies by campus. Research specific zoning before signing", "Best for: Families prioritizing budget flexibility or proximity to the airport"]
  }));
}
function CTASlide() {
  return /*#__PURE__*/React.createElement("div", {
    style: sS.slide,
    "data-screen-label": "08 CTA"
  }, /*#__PURE__*/React.createElement("img", {
    src: window.__resources.photo_cover,
    alt: "",
    style: sS.bg
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      background: "linear-gradient(180deg, rgba(0,0,0,.15) 0%, rgba(0,0,0,.1) 50%, rgba(0,0,0,.35) 100%)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      padding: "0 80px",
      textAlign: "center",
      color: "#fff"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "'Lato',sans-serif",
      fontWeight: 400,
      fontSize: 32,
      letterSpacing: ".05em",
      marginBottom: 16,
      textShadow: "0 2px 12px rgba(0,0,0,.3)"
    }
  }, "Comment"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontFamily: "'Libre Baskerville',serif",
      fontWeight: 700,
      fontSize: 164,
      lineHeight: 1,
      margin: 0,
      letterSpacing: "-0.01em",
      textShadow: "0 2px 24px rgba(0,0,0,.4)"
    }
  }, "\"DALLAS\""), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "'Lato',sans-serif",
      fontWeight: 400,
      fontSize: 30,
      lineHeight: 1.5,
      marginTop: 44,
      maxWidth: 720,
      textShadow: "0 2px 12px rgba(0,0,0,.3)"
    }
  }, "to get the full guide before you sign your lease.")), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      bottom: 70,
      left: 0,
      right: 0,
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      gap: 14
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: window.__resources.logo_symbol,
    alt: "",
    style: {
      height: 44,
      filter: "brightness(0) invert(1)"
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "'Urbanist',sans-serif",
      fontWeight: 600,
      fontSize: 32,
      color: "#fff",
      letterSpacing: "-0.01em"
    }
  }, "brightplace")));
}
const sS = {
  slide: {
    position: "relative",
    width: 1080,
    height: 1350,
    overflow: "hidden",
    background: "#fff"
  },
  bg: {
    position: "absolute",
    inset: 0,
    width: "100%",
    height: "100%",
    objectFit: "cover",
    objectPosition: "center"
  }
};
Object.assign(window, {
  CoverSlide,
  MapSlide,
  BridgeSlide,
  LakeHighlands,
  Richardson,
  Plano,
  Irving,
  CTASlide
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "export/src/slides.jsx", error: String((e && e.message) || e) }); }

// ui_kits/carousel/BridgeSlide.jsx
try { (() => {
// BridgeSlide — 1080x1350. Sets the thesis. Warm paper, big serif pull-quote feel.
function BridgeSlide({
  intro = "five specifics.",
  body = "zero clichés.",
  tail = "every claim sourced to a published brightplace guide."
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: bridgeStyles.slide
  }, /*#__PURE__*/React.createElement("div", {
    style: bridgeStyles.rule
  }), /*#__PURE__*/React.createElement("div", {
    style: bridgeStyles.content
  }, /*#__PURE__*/React.createElement("div", {
    style: bridgeStyles.kicker
  }, "the promise"), /*#__PURE__*/React.createElement("div", {
    style: bridgeStyles.lineA
  }, intro), /*#__PURE__*/React.createElement("div", {
    style: bridgeStyles.lineB
  }, body), /*#__PURE__*/React.createElement("div", {
    style: bridgeStyles.tail
  }, tail)), /*#__PURE__*/React.createElement("div", {
    style: bridgeStyles.footmark
  }, /*#__PURE__*/React.createElement("span", {
    style: bridgeStyles.n
  }, "01"), /*#__PURE__*/React.createElement("span", {
    style: bridgeStyles.of
  }, "of 7")));
}
const bridgeStyles = {
  slide: {
    position: "relative",
    width: "100%",
    height: "100%",
    background: "var(--bp-paper)",
    padding: "96px 72px 112px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    fontFamily: "var(--ff-display)"
  },
  rule: {
    position: "absolute",
    top: 96,
    left: 72,
    width: 96,
    height: 3,
    background: "var(--bp-orange)"
  },
  content: {
    marginTop: 48,
    display: "flex",
    flexDirection: "column",
    gap: 18
  },
  kicker: {
    fontFamily: "'Libre Baskerville', serif",
    fontStyle: "italic",
    fontSize: 22,
    color: "var(--bp-ink-muted)"
  },
  lineA: {
    fontFamily: "var(--ff-display)",
    fontWeight: 600,
    fontSize: 96,
    lineHeight: 1.0,
    letterSpacing: "-0.02em",
    color: "var(--bp-navy)"
  },
  lineB: {
    fontFamily: "var(--ff-display)",
    fontWeight: 600,
    fontSize: 96,
    lineHeight: 1.0,
    letterSpacing: "-0.02em",
    color: "var(--bp-orange)"
  },
  tail: {
    marginTop: 24,
    fontFamily: "'Libre Baskerville', serif",
    fontSize: 26,
    lineHeight: 1.45,
    color: "var(--bp-ink-soft)",
    maxWidth: 760
  },
  footmark: {
    display: "flex",
    alignItems: "baseline",
    gap: 12
  },
  n: {
    fontFamily: "var(--ff-display)",
    fontWeight: 600,
    fontSize: 36,
    color: "var(--bp-navy)"
  },
  of: {
    fontFamily: "'Libre Baskerville', serif",
    fontSize: 20,
    color: "var(--bp-ink-muted)"
  }
};
window.BridgeSlide = BridgeSlide;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/carousel/BridgeSlide.jsx", error: String((e && e.message) || e) }); }

// ui_kits/carousel/CoverSlide.jsx
try { (() => {
// CoverSlide — 1080x1350. Full-bleed editorial sketch background, navy headline.
// brightplace is always lowercase. Logo does NOT appear on cover (CTA only).
function CoverSlide({
  eyebrow = "brooklyn",
  headline = "7 quietest\ncoffee blocks",
  meta = "a 4-minute read, by neighborhood"
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: coverStyles.slide
  }, /*#__PURE__*/React.createElement("div", {
    style: coverStyles.bgWrap
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/brightplace-sketch.png",
    style: coverStyles.bg,
    alt: ""
  }), /*#__PURE__*/React.createElement("div", {
    style: coverStyles.scrim
  })), /*#__PURE__*/React.createElement("div", {
    style: coverStyles.content
  }, /*#__PURE__*/React.createElement("div", {
    style: coverStyles.eyebrow
  }, eyebrow), /*#__PURE__*/React.createElement("h1", {
    style: coverStyles.headline
  }, headline.split("\n").map((l, i) => /*#__PURE__*/React.createElement("span", {
    key: i,
    style: {
      display: "block"
    }
  }, l))), /*#__PURE__*/React.createElement("div", {
    style: coverStyles.meta
  }, meta)), /*#__PURE__*/React.createElement("div", {
    style: coverStyles.swipe
  }, "swipe \u2192"));
}
const coverStyles = {
  slide: {
    position: "relative",
    width: "100%",
    height: "100%",
    background: "var(--bp-paper)",
    overflow: "hidden",
    fontFamily: "var(--ff-display)"
  },
  bgWrap: {
    position: "absolute",
    inset: 0
  },
  bg: {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    opacity: 0.92
  },
  scrim: {
    position: "absolute",
    inset: 0,
    background: "linear-gradient(180deg, rgba(250,246,239,0) 0%, rgba(250,246,239,0) 40%, rgba(250,246,239,.85) 80%, rgba(250,246,239,.98) 100%)"
  },
  content: {
    position: "absolute",
    left: 72,
    right: 72,
    bottom: 112,
    display: "flex",
    flexDirection: "column",
    gap: 18
  },
  eyebrow: {
    fontFamily: "'Libre Baskerville', serif",
    fontStyle: "italic",
    fontSize: 28,
    color: "var(--bp-navy)",
    letterSpacing: 0
  },
  headline: {
    fontFamily: "var(--ff-display)",
    fontWeight: 600,
    fontSize: 112,
    lineHeight: 1.02,
    letterSpacing: "-0.02em",
    color: "var(--bp-navy)",
    margin: 0
  },
  meta: {
    fontFamily: "'Libre Baskerville', serif",
    fontStyle: "italic",
    fontSize: 22,
    color: "var(--bp-ink-soft)"
  },
  swipe: {
    position: "absolute",
    right: 72,
    bottom: 52,
    fontFamily: "var(--ff-display)",
    fontWeight: 500,
    fontSize: 20,
    color: "var(--bp-navy)",
    opacity: 0.6
  }
};
window.CoverSlide = CoverSlide;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/carousel/CoverSlide.jsx", error: String((e && e.message) || e) }); }

// ui_kits/carousel/CtaSlide.jsx
try { (() => {
// CtaSlide — 1080x1350. Same bg as cover. ONLY slide with the brightplace logo.
function CtaSlide({
  action = "get your match",
  sub = "free · 90 seconds · no account",
  receipt = "built from 400+ on-foot neighborhood guides"
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: ctaStyles.slide
  }, /*#__PURE__*/React.createElement("div", {
    style: ctaStyles.bgWrap
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/brightplace-sketch.png",
    style: ctaStyles.bg,
    alt: ""
  }), /*#__PURE__*/React.createElement("div", {
    style: ctaStyles.scrim
  })), /*#__PURE__*/React.createElement("img", {
    src: "../../assets/brightplace-logo.svg",
    style: ctaStyles.logo,
    alt: "brightplace"
  }), /*#__PURE__*/React.createElement("div", {
    style: ctaStyles.content
  }, /*#__PURE__*/React.createElement("div", {
    style: ctaStyles.receipt
  }, receipt), /*#__PURE__*/React.createElement("button", {
    style: ctaStyles.cta
  }, action, " ", /*#__PURE__*/React.createElement("span", {
    style: {
      marginLeft: 8
    }
  }, "\u2192")), /*#__PURE__*/React.createElement("div", {
    style: ctaStyles.sub
  }, sub)));
}
const ctaStyles = {
  slide: {
    position: "relative",
    width: "100%",
    height: "100%",
    background: "var(--bp-paper)",
    overflow: "hidden",
    fontFamily: "var(--ff-display)"
  },
  bgWrap: {
    position: "absolute",
    inset: 0
  },
  bg: {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    opacity: 0.92
  },
  scrim: {
    position: "absolute",
    inset: 0,
    background: "linear-gradient(180deg, rgba(250,246,239,.2) 0%, rgba(250,246,239,.5) 50%, rgba(250,246,239,.98) 100%)"
  },
  logo: {
    position: "absolute",
    top: 72,
    left: 72,
    height: 56,
    zIndex: 2
  },
  content: {
    position: "absolute",
    left: 72,
    right: 72,
    bottom: 112,
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
    gap: 22,
    zIndex: 2
  },
  receipt: {
    fontFamily: "'Libre Baskerville', serif",
    fontStyle: "italic",
    fontSize: 22,
    color: "var(--bp-ink-soft)",
    maxWidth: 720
  },
  cta: {
    fontFamily: "var(--ff-display)",
    fontWeight: 600,
    fontSize: 44,
    padding: "26px 44px",
    border: 0,
    borderRadius: 999,
    background: "var(--bp-orange)",
    color: "var(--bp-navy)",
    letterSpacing: "-0.01em",
    cursor: "pointer",
    boxShadow: "0 8px 24px rgba(26,39,68,.12)"
  },
  sub: {
    fontFamily: "var(--ff-body)",
    fontSize: 18,
    color: "var(--bp-ink-muted)",
    letterSpacing: ".02em"
  }
};
window.CtaSlide = CtaSlide;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/carousel/CtaSlide.jsx", error: String((e && e.message) || e) }); }

// ui_kits/carousel/DetailSlide.jsx
try { (() => {
// DetailSlide — 1080x1350. Exactly 5 bullets. Last bullet is the tradeoff.
function DetailSlide({
  neighborhood = "Clinton Hill",
  index = 3,
  total = 7,
  bullets = ["14-minute walk to the G at Classon.", "Two indie bakeries open by 7am: Mia's, Parlor.", "Pratt's quad is a public-hours reading spot.", "Sunday farmers market at Underhill through October.", "Tradeoff: street parking is permit-only after 6pm."]
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: detailStyles.slide
  }, /*#__PURE__*/React.createElement("header", {
    style: detailStyles.header
  }, /*#__PURE__*/React.createElement("div", {
    style: detailStyles.num
  }, String(index).padStart(2, "0")), /*#__PURE__*/React.createElement("div", {
    style: detailStyles.head
  }, /*#__PURE__*/React.createElement("div", {
    style: detailStyles.kicker
  }, "neighborhood"), /*#__PURE__*/React.createElement("h2", {
    style: detailStyles.title
  }, neighborhood))), /*#__PURE__*/React.createElement("ol", {
    style: detailStyles.list
  }, bullets.map((b, i) => {
    const isTradeoff = i === bullets.length - 1;
    return /*#__PURE__*/React.createElement("li", {
      key: i,
      style: detailStyles.item
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        ...detailStyles.mark,
        background: isTradeoff ? "var(--bp-navy)" : "var(--bp-orange)"
      }
    }, isTradeoff ? "!" : i + 1), /*#__PURE__*/React.createElement("span", {
      style: {
        ...detailStyles.text,
        fontFamily: isTradeoff ? "'Libre Baskerville', serif" : "var(--ff-body)",
        fontStyle: isTradeoff ? "italic" : "normal"
      }
    }, b));
  })), /*#__PURE__*/React.createElement("footer", {
    style: detailStyles.footer
  }, /*#__PURE__*/React.createElement("span", null, "brooklyn \xB7 coffee blocks"), /*#__PURE__*/React.createElement("span", null, index, " / ", total)));
}
const detailStyles = {
  slide: {
    position: "relative",
    width: "100%",
    height: "100%",
    background: "var(--bp-paper)",
    padding: "88px 72px 72px",
    display: "flex",
    flexDirection: "column",
    gap: 36,
    fontFamily: "var(--ff-body)"
  },
  header: {
    display: "flex",
    gap: 24,
    alignItems: "flex-end"
  },
  num: {
    fontFamily: "var(--ff-display)",
    fontWeight: 600,
    fontSize: 96,
    lineHeight: 1,
    color: "var(--bp-peach)",
    letterSpacing: "-0.04em"
  },
  head: {
    display: "flex",
    flexDirection: "column",
    gap: 6,
    paddingBottom: 14
  },
  kicker: {
    fontFamily: "'Libre Baskerville', serif",
    fontStyle: "italic",
    fontSize: 22,
    color: "var(--bp-ink-muted)"
  },
  title: {
    fontFamily: "var(--ff-display)",
    fontWeight: 600,
    fontSize: 72,
    lineHeight: 1,
    letterSpacing: "-0.02em",
    color: "var(--bp-navy)",
    margin: 0
  },
  list: {
    listStyle: "none",
    padding: 0,
    margin: 0,
    display: "flex",
    flexDirection: "column",
    gap: 22
  },
  item: {
    display: "flex",
    gap: 20,
    alignItems: "flex-start"
  },
  mark: {
    flex: "0 0 40px",
    width: 40,
    height: 40,
    borderRadius: 999,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontFamily: "var(--ff-display)",
    fontWeight: 700,
    fontSize: 18,
    color: "var(--bp-navy)"
  },
  text: {
    fontSize: 26,
    lineHeight: 1.4,
    color: "var(--bp-navy)",
    paddingTop: 4
  },
  footer: {
    marginTop: "auto",
    display: "flex",
    justifyContent: "space-between",
    fontFamily: "'Libre Baskerville', serif",
    fontStyle: "italic",
    fontSize: 18,
    color: "var(--bp-ink-muted)",
    borderTop: "1px solid var(--border-hair)",
    paddingTop: 20
  }
};
window.DetailSlide = DetailSlide;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/carousel/DetailSlide.jsx", error: String((e && e.message) || e) }); }

// ui_kits/carousel/MapSlide.jsx
try { (() => {
// MapSlide — 1080x1350. Illustrated editorial map with orange pins + serif labels.
// NO sans-serif. NO all-caps. Libre Baskerville 400 labels, 700 city anchor.
function MapSlide({
  city = "Brooklyn",
  neighborhoods = [{
    name: "Clinton Hill",
    x: 48,
    y: 32
  }, {
    name: "Fort Greene",
    x: 30,
    y: 48
  }, {
    name: "Bed-Stuy",
    x: 66,
    y: 44
  }, {
    name: "Prospect Heights",
    x: 42,
    y: 62
  }, {
    name: "Crown Heights",
    x: 58,
    y: 70
  }, {
    name: "Boerum Hill",
    x: 22,
    y: 64
  }, {
    name: "Park Slope",
    x: 34,
    y: 78
  }]
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: mapStyles.slide
  }, /*#__PURE__*/React.createElement("div", {
    style: mapStyles.paper
  }, /*#__PURE__*/React.createElement("div", {
    style: mapStyles.anchor
  }, city), /*#__PURE__*/React.createElement("svg", {
    style: mapStyles.streets,
    viewBox: "0 0 1000 1000",
    preserveAspectRatio: "none"
  }, /*#__PURE__*/React.createElement("g", {
    stroke: "#1A2744",
    strokeWidth: "2.5",
    fill: "none",
    strokeLinecap: "round",
    opacity: ".85"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M 80 200 Q 350 180 620 220 T 950 210"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 60 360 Q 280 400 540 370 T 960 400"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 100 520 Q 420 500 680 540 T 940 520"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 80 680 Q 360 700 620 670 T 960 700"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 120 840 Q 380 820 640 850 T 940 840"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 220 120 Q 240 420 220 700 T 260 960"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 480 100 Q 460 380 500 640 T 480 960"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 740 140 Q 760 420 720 700 T 760 960"
  })), /*#__PURE__*/React.createElement("g", {
    stroke: "#1A2744",
    strokeWidth: "4",
    fill: "none",
    opacity: ".95"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M 40 580 Q 300 560 600 600 T 980 580"
  }))), neighborhoods.map((n, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      ...mapStyles.pinWrap,
      left: `${n.x}%`,
      top: `${n.y}%`
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: mapStyles.pin
  }, /*#__PURE__*/React.createElement("div", {
    style: mapStyles.pinDot
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      ...mapStyles.label,
      fontWeight: i === 0 ? 700 : 400,
      fontStyle: i % 3 === 1 ? "italic" : "normal"
    }
  }, n.name)))), /*#__PURE__*/React.createElement("div", {
    style: mapStyles.caption
  }, "seven neighborhoods, one commute radius"));
}
const mapStyles = {
  slide: {
    position: "relative",
    width: "100%",
    height: "100%",
    background: "var(--bp-paper)",
    padding: "72px 64px 96px",
    display: "flex",
    flexDirection: "column",
    gap: 24,
    fontFamily: "'Libre Baskerville', serif"
  },
  paper: {
    position: "relative",
    flex: 1,
    background: "#FDFAF3",
    border: "1px solid var(--border-hair)",
    borderRadius: 16,
    overflow: "hidden"
  },
  anchor: {
    position: "absolute",
    top: 28,
    left: 32,
    fontFamily: "'Libre Baskerville', serif",
    fontWeight: 700,
    fontSize: 44,
    color: "var(--bp-navy)",
    zIndex: 3
  },
  streets: {
    position: "absolute",
    inset: 0,
    width: "100%",
    height: "100%"
  },
  pinWrap: {
    position: "absolute",
    transform: "translate(-50%, -50%)",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 6,
    zIndex: 2
  },
  pin: {
    width: 28,
    height: 28,
    borderRadius: 999,
    background: "var(--bp-orange)",
    border: "3px solid #FAF6EF",
    boxShadow: "0 2px 6px rgba(26,39,68,.3)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  },
  pinDot: {
    width: 8,
    height: 8,
    borderRadius: 999,
    background: "var(--bp-navy)"
  },
  label: {
    fontFamily: "'Libre Baskerville', serif",
    fontSize: 20,
    color: "var(--bp-navy)",
    background: "rgba(253,250,243,.9)",
    padding: "2px 8px",
    borderRadius: 4,
    whiteSpace: "nowrap"
  },
  caption: {
    fontFamily: "'Libre Baskerville', serif",
    fontStyle: "italic",
    fontSize: 22,
    color: "var(--bp-ink-soft)",
    textAlign: "center"
  }
};
window.MapSlide = MapSlide;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/carousel/MapSlide.jsx", error: String((e && e.message) || e) }); }

// ui_kits/dallas_families/deck-stage.js
try { (() => {
/**
 * <deck-stage> — reusable web component for HTML decks.
 *
 * Handles:
 *  (a) speaker notes — reads <script type="application/json" id="speaker-notes">
 *      and posts {slideIndexChanged: N} to the parent window on nav.
 *  (b) keyboard navigation — ←/→, PgUp/PgDn, Space, Home/End, number keys.
 *  (c) press R to reset to slide 0 (with a tasteful keyboard hint).
 *  (d) bottom-center overlay showing slide count + hints, fades out on idle.
 *  (e) auto-scaling — inner canvas is a fixed design size (default 1920×1080)
 *      scaled with `transform: scale()` to fit the viewport, letterboxed.
 *      Set the `noscale` attribute to render at authored size (1:1) — the
 *      PPTX exporter sets this so its DOM capture sees unscaled geometry.
 *  (f) print — `@media print` lays every slide out as its own page at the
 *      design size, so the browser's Print → Save as PDF produces a clean
 *      one-page-per-slide PDF with no extra setup.
 *
 * Slides are HIDDEN, not unmounted. Non-active slides stay in the DOM with
 * `visibility: hidden` + `opacity: 0`, so their state (videos, iframes,
 * form inputs, React trees) is preserved across navigation.
 *
 * Lifecycle event — the component dispatches a `slidechange` CustomEvent on
 * itself whenever the active slide changes (including the initial mount).
 * The event bubbles and composes out of shadow DOM, so you can listen on
 * the <deck-stage> element or on document:
 *
 *   document.querySelector('deck-stage').addEventListener('slidechange', (e) => {
 *     e.detail.index         // new 0-based index
 *     e.detail.previousIndex // previous index, or -1 on init
 *     e.detail.total         // total slide count
 *     e.detail.slide         // the new active slide element
 *     e.detail.previousSlide // the prior slide element, or null on init
 *     e.detail.reason        // 'init' | 'keyboard' | 'click' | 'tap' | 'api'
 *   });
 *
 * Persistence: current slide index is saved to localStorage keyed by the
 * document path, so refresh returns you to the same place.
 *
 * Usage:
 *   <deck-stage width="1920" height="1080">
 *     <section data-label="Title">...</section>
 *     <section data-label="Agenda">...</section>
 *   </deck-stage>
 *
 * Slides are the direct element children of <deck-stage>. Each slide is
 * automatically tagged with:
 *   - data-screen-label="NN Label"   (1-indexed, for comment flow)
 *   - data-om-validate="no_overflowing_text,no_overlapping_text,slide_sized_text"
 */

(() => {
  const DESIGN_W_DEFAULT = 1920;
  const DESIGN_H_DEFAULT = 1080;
  const STORAGE_PREFIX = 'deck-stage:slide:';
  const OVERLAY_HIDE_MS = 1800;
  const VALIDATE_ATTR = 'no_overflowing_text,no_overlapping_text,slide_sized_text';
  const pad2 = n => String(n).padStart(2, '0');
  const stylesheet = `
    :host {
      position: fixed;
      inset: 0;
      display: block;
      background: #000;
      color: #fff;
      font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, Arial, sans-serif;
      overflow: hidden;
    }

    .stage {
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .canvas {
      position: relative;
      transform-origin: center center;
      flex-shrink: 0;
      background: #fff;
      will-change: transform;
    }

    /* Slides live in light DOM (via <slot>) so authored CSS still applies.
       We absolutely position each slotted child to stack them. */
    ::slotted(*) {
      position: absolute !important;
      inset: 0 !important;
      width: 100% !important;
      height: 100% !important;
      box-sizing: border-box !important;
      overflow: hidden;
      opacity: 0;
      pointer-events: none;
      visibility: hidden;
    }
    ::slotted([data-deck-active]) {
      opacity: 1;
      pointer-events: auto;
      visibility: visible;
    }

    /* Tap zones for mobile — back/forward thirds like Stories.
       Transparent, no visible UI, don't block the overlay. */
    .tapzones {
      position: fixed;
      inset: 0;
      display: flex;
      z-index: 2147482000;
      pointer-events: none;
    }
    .tapzone {
      flex: 1;
      pointer-events: auto;
      -webkit-tap-highlight-color: transparent;
    }
    /* Only activate tap zones on coarse pointers (touch devices). */
    @media (hover: hover) and (pointer: fine) {
      .tapzones { display: none; }
    }

    .overlay {
      position: fixed;
      left: 50%;
      bottom: 22px;
      transform: translate(-50%, 6px) scale(0.92);
      filter: blur(6px);
      display: flex;
      align-items: center;
      gap: 4px;
      padding: 4px;
      background: #000;
      color: #fff;
      border-radius: 999px;
      font-size: 12px;
      font-feature-settings: "tnum" 1;
      letter-spacing: 0.01em;
      opacity: 0;
      pointer-events: none;
      transition: opacity 260ms ease, transform 260ms cubic-bezier(.2,.8,.2,1), filter 260ms ease;
      transform-origin: center bottom;
      z-index: 2147483000;
      user-select: none;
    }
    .overlay[data-visible] {
      opacity: 1;
      pointer-events: auto;
      transform: translate(-50%, 0) scale(1);
      filter: blur(0);
    }

    .btn {
      appearance: none;
      -webkit-appearance: none;
      background: transparent;
      border: 0;
      margin: 0;
      padding: 0;
      color: inherit;
      font: inherit;
      cursor: default;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      height: 28px;
      min-width: 28px;
      border-radius: 999px;
      color: rgba(255,255,255,0.72);
      transition: background 140ms ease, color 140ms ease;
      -webkit-tap-highlight-color: transparent;
    }
    .btn:hover { background: rgba(255,255,255,0.12); color: #fff; }
    .btn:active { background: rgba(255,255,255,0.18); }
    .btn:focus { outline: none; }
    .btn:focus-visible { outline: none; }
    .btn::-moz-focus-inner { border: 0; }
    .btn svg { width: 14px; height: 14px; display: block; }
    .btn.reset {
      font-size: 11px;
      font-weight: 500;
      letter-spacing: 0.02em;
      padding: 0 10px 0 12px;
      gap: 6px;
      color: rgba(255,255,255,0.72);
    }
    .btn.reset .kbd {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 16px;
      height: 16px;
      padding: 0 4px;
      font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
      font-size: 10px;
      line-height: 1;
      color: rgba(255,255,255,0.88);
      background: rgba(255,255,255,0.12);
      border-radius: 4px;
    }

    .count {
      font-variant-numeric: tabular-nums;
      color: #fff;
      font-weight: 500;
      padding: 0 8px;
      min-width: 42px;
      text-align: center;
      font-size: 12px;
    }
    .count .sep { color: rgba(255,255,255,0.45); margin: 0 3px; font-weight: 400; }
    .count .total { color: rgba(255,255,255,0.55); }

    .divider {
      width: 1px;
      height: 14px;
      background: rgba(255,255,255,0.18);
      margin: 0 2px;
    }

    /* ── Print: one page per slide, no chrome ────────────────────────────
       The screen layout stacks every slide at inset:0 inside a scaled
       canvas; for print we want them in document flow at the authored
       design size so the browser paginates one slide per sheet. The
       @page size is set from the width/height attributes via the inline
       <style id="deck-stage-print-page"> that connectedCallback injects
       into <head> (the @page at-rule has no effect inside shadow DOM). */
    @media print {
      :host {
        position: static;
        inset: auto;
        background: none;
        overflow: visible;
        color: inherit;
      }
      .stage { position: static; display: block; }
      .canvas {
        transform: none !important;
        width: auto !important;
        height: auto !important;
        background: none;
        will-change: auto;
      }
      ::slotted(*) {
        position: relative !important;
        inset: auto !important;
        width: var(--deck-design-w) !important;
        height: var(--deck-design-h) !important;
        box-sizing: border-box !important;
        opacity: 1 !important;
        visibility: visible !important;
        pointer-events: auto;
        break-after: page;
        page-break-after: always;
        break-inside: avoid;
        overflow: hidden;
      }
      ::slotted(*:last-child) {
        break-after: auto;
        page-break-after: auto;
      }
      .overlay, .tapzones { display: none !important; }
    }
  `;
  class DeckStage extends HTMLElement {
    static get observedAttributes() {
      return ['width', 'height', 'noscale'];
    }
    constructor() {
      super();
      this._root = this.attachShadow({
        mode: 'open'
      });
      this._index = 0;
      this._slides = [];
      this._notes = [];
      this._hideTimer = null;
      this._mouseIdleTimer = null;
      this._storageKey = STORAGE_PREFIX + (location.pathname || '/');
      this._onKey = this._onKey.bind(this);
      this._onResize = this._onResize.bind(this);
      this._onSlotChange = this._onSlotChange.bind(this);
      this._onMouseMove = this._onMouseMove.bind(this);
      this._onTapBack = this._onTapBack.bind(this);
      this._onTapForward = this._onTapForward.bind(this);
    }
    get designWidth() {
      return parseInt(this.getAttribute('width'), 10) || DESIGN_W_DEFAULT;
    }
    get designHeight() {
      return parseInt(this.getAttribute('height'), 10) || DESIGN_H_DEFAULT;
    }
    connectedCallback() {
      this._render();
      this._loadNotes();
      this._syncPrintPageRule();
      window.addEventListener('keydown', this._onKey);
      window.addEventListener('resize', this._onResize);
      window.addEventListener('mousemove', this._onMouseMove, {
        passive: true
      });
      // Initial collection + layout happens via slotchange, which fires on mount.
    }
    disconnectedCallback() {
      window.removeEventListener('keydown', this._onKey);
      window.removeEventListener('resize', this._onResize);
      window.removeEventListener('mousemove', this._onMouseMove);
      if (this._hideTimer) clearTimeout(this._hideTimer);
      if (this._mouseIdleTimer) clearTimeout(this._mouseIdleTimer);
    }
    attributeChangedCallback() {
      if (this._canvas) {
        this._canvas.style.width = this.designWidth + 'px';
        this._canvas.style.height = this.designHeight + 'px';
        this._canvas.style.setProperty('--deck-design-w', this.designWidth + 'px');
        this._canvas.style.setProperty('--deck-design-h', this.designHeight + 'px');
        this._fit();
        this._syncPrintPageRule();
      }
    }
    _render() {
      const style = document.createElement('style');
      style.textContent = stylesheet;
      const stage = document.createElement('div');
      stage.className = 'stage';
      const canvas = document.createElement('div');
      canvas.className = 'canvas';
      canvas.style.width = this.designWidth + 'px';
      canvas.style.height = this.designHeight + 'px';
      canvas.style.setProperty('--deck-design-w', this.designWidth + 'px');
      canvas.style.setProperty('--deck-design-h', this.designHeight + 'px');
      const slot = document.createElement('slot');
      slot.addEventListener('slotchange', this._onSlotChange);
      canvas.appendChild(slot);
      stage.appendChild(canvas);

      // Tap zones (mobile): left third = back, right third = forward.
      const tapzones = document.createElement('div');
      tapzones.className = 'tapzones export-hidden';
      tapzones.setAttribute('aria-hidden', 'true');
      const tzBack = document.createElement('div');
      tzBack.className = 'tapzone tapzone--back';
      const tzMid = document.createElement('div');
      tzMid.className = 'tapzone tapzone--mid';
      tzMid.style.pointerEvents = 'none';
      const tzFwd = document.createElement('div');
      tzFwd.className = 'tapzone tapzone--fwd';
      tzBack.addEventListener('click', this._onTapBack);
      tzFwd.addEventListener('click', this._onTapForward);
      tapzones.append(tzBack, tzMid, tzFwd);

      // Overlay: compact, solid black, with clickable controls.
      const overlay = document.createElement('div');
      overlay.className = 'overlay export-hidden';
      overlay.setAttribute('role', 'toolbar');
      overlay.setAttribute('aria-label', 'Deck controls');
      overlay.innerHTML = `
        <button class="btn prev" type="button" aria-label="Previous slide" title="Previous (←)">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 3L5 8l5 5"/></svg>
        </button>
        <span class="count" aria-live="polite"><span class="current">1</span><span class="sep">/</span><span class="total">1</span></span>
        <button class="btn next" type="button" aria-label="Next slide" title="Next (→)">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3l5 5-5 5"/></svg>
        </button>
        <span class="divider"></span>
        <button class="btn reset" type="button" aria-label="Reset to first slide" title="Reset (R)">Reset<span class="kbd">R</span></button>
      `;
      overlay.querySelector('.prev').addEventListener('click', () => this._go(this._index - 1, 'click'));
      overlay.querySelector('.next').addEventListener('click', () => this._go(this._index + 1, 'click'));
      overlay.querySelector('.reset').addEventListener('click', () => this._go(0, 'click'));
      this._root.append(style, stage, tapzones, overlay);
      this._canvas = canvas;
      this._slot = slot;
      this._overlay = overlay;
      this._countEl = overlay.querySelector('.current');
      this._totalEl = overlay.querySelector('.total');
    }

    /** @page must live in the document stylesheet — it's a no-op inside
     *  shadow DOM. Inject/update a single <head> style tag so the print
     *  sheet matches the design size and Save-as-PDF yields one slide per
     *  page with no margins. */
    _syncPrintPageRule() {
      const id = 'deck-stage-print-page';
      let tag = document.getElementById(id);
      if (!tag) {
        tag = document.createElement('style');
        tag.id = id;
        document.head.appendChild(tag);
      }
      tag.textContent = '@page { size: ' + this.designWidth + 'px ' + this.designHeight + 'px; margin: 0; } ' + '@media print { html, body { margin: 0 !important; padding: 0 !important; background: none !important; overflow: visible !important; height: auto !important; } ' + '* { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }';
    }
    _onSlotChange() {
      this._collectSlides();
      this._restoreIndex();
      this._applyIndex({
        showOverlay: false,
        broadcast: true,
        reason: 'init'
      });
      this._fit();
    }
    _collectSlides() {
      const assigned = this._slot.assignedElements({
        flatten: true
      });
      this._slides = assigned.filter(el => {
        // Skip template/style/script nodes even if someone slots them.
        const tag = el.tagName;
        return tag !== 'TEMPLATE' && tag !== 'SCRIPT' && tag !== 'STYLE';
      });
      this._slides.forEach((slide, i) => {
        const n = i + 1;
        // Determine a label for comment flow: prefer explicit data-label,
        // then an existing data-screen-label, then first heading, else "Slide".
        let label = slide.getAttribute('data-label');
        if (!label) {
          const existing = slide.getAttribute('data-screen-label');
          if (existing) {
            // Strip any leading number the author may have included.
            label = existing.replace(/^\s*\d+\s*/, '').trim() || existing;
          }
        }
        if (!label) {
          const h = slide.querySelector('h1, h2, h3, [data-title]');
          if (h) label = (h.textContent || '').trim().slice(0, 40);
        }
        if (!label) label = 'Slide';
        slide.setAttribute('data-screen-label', `${pad2(n)} ${label}`);

        // Validation attribute for comment flow / auto-checks.
        if (!slide.hasAttribute('data-om-validate')) {
          slide.setAttribute('data-om-validate', VALIDATE_ATTR);
        }
        slide.setAttribute('data-deck-slide', String(i));
      });
      if (this._totalEl) this._totalEl.textContent = String(this._slides.length || 1);
      if (this._index >= this._slides.length) this._index = Math.max(0, this._slides.length - 1);
    }
    _loadNotes() {
      const tag = document.getElementById('speaker-notes');
      if (!tag) {
        this._notes = [];
        return;
      }
      try {
        const parsed = JSON.parse(tag.textContent || '[]');
        if (Array.isArray(parsed)) this._notes = parsed;
      } catch (e) {
        console.warn('[deck-stage] Failed to parse #speaker-notes JSON:', e);
        this._notes = [];
      }
    }
    _restoreIndex() {
      try {
        const raw = localStorage.getItem(this._storageKey);
        if (raw != null) {
          const n = parseInt(raw, 10);
          if (Number.isFinite(n) && n >= 0 && n < this._slides.length) {
            this._index = n;
          }
        }
      } catch (e) {/* ignore */}
    }
    _persistIndex() {
      try {
        localStorage.setItem(this._storageKey, String(this._index));
      } catch (e) {/* ignore */}
    }
    _applyIndex({
      showOverlay = true,
      broadcast = true,
      reason = 'init'
    } = {}) {
      if (!this._slides.length) return;
      const prev = this._prevIndex == null ? -1 : this._prevIndex;
      const curr = this._index;
      this._slides.forEach((s, i) => {
        if (i === curr) s.setAttribute('data-deck-active', '');else s.removeAttribute('data-deck-active');
      });
      if (this._countEl) this._countEl.textContent = String(curr + 1);
      this._persistIndex();
      if (broadcast) {
        // (1) Legacy: host-window postMessage for speaker-notes renderers.
        try {
          window.postMessage({
            slideIndexChanged: curr
          }, '*');
        } catch (e) {}

        // (2) In-page CustomEvent on the <deck-stage> element itself.
        //     Bubbles and composes out of shadow DOM so slide code can listen:
        //       document.querySelector('deck-stage').addEventListener('slidechange', e => {
        //         e.detail.index, e.detail.previousIndex, e.detail.total, e.detail.slide, e.detail.reason
        //       });
        const detail = {
          index: curr,
          previousIndex: prev,
          total: this._slides.length,
          slide: this._slides[curr] || null,
          previousSlide: prev >= 0 ? this._slides[prev] || null : null,
          reason: reason // 'init' | 'keyboard' | 'click' | 'tap' | 'api'
        };
        this.dispatchEvent(new CustomEvent('slidechange', {
          detail,
          bubbles: true,
          composed: true
        }));
      }
      this._prevIndex = curr;
      if (showOverlay) this._flashOverlay();
    }
    _flashOverlay() {
      if (!this._overlay) return;
      this._overlay.setAttribute('data-visible', '');
      if (this._hideTimer) clearTimeout(this._hideTimer);
      this._hideTimer = setTimeout(() => {
        this._overlay.removeAttribute('data-visible');
      }, OVERLAY_HIDE_MS);
    }
    _fit() {
      if (!this._canvas) return;
      // PPTX export sets noscale so the DOM capture sees authored-size
      // geometry — the scaled canvas is in shadow DOM, so the exporter's
      // resetTransformSelector can't reach .canvas.style.transform directly.
      if (this.hasAttribute('noscale')) {
        this._canvas.style.transform = 'none';
        return;
      }
      const vw = window.innerWidth;
      const vh = window.innerHeight;
      const s = Math.min(vw / this.designWidth, vh / this.designHeight);
      this._canvas.style.transform = `scale(${s})`;
    }
    _onResize() {
      this._fit();
    }
    _onMouseMove() {
      // Keep overlay visible while mouse moves; hide after idle.
      this._flashOverlay();
    }
    _onTapBack(e) {
      e.preventDefault();
      this._go(this._index - 1, 'tap');
    }
    _onTapForward(e) {
      e.preventDefault();
      this._go(this._index + 1, 'tap');
    }
    _onKey(e) {
      // Ignore when the user is typing.
      const t = e.target;
      if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const key = e.key;
      let handled = true;
      if (key === 'ArrowRight' || key === 'PageDown' || key === ' ' || key === 'Spacebar') {
        this._go(this._index + 1, 'keyboard');
      } else if (key === 'ArrowLeft' || key === 'PageUp') {
        this._go(this._index - 1, 'keyboard');
      } else if (key === 'Home') {
        this._go(0, 'keyboard');
      } else if (key === 'End') {
        this._go(this._slides.length - 1, 'keyboard');
      } else if (key === 'r' || key === 'R') {
        this._go(0, 'keyboard');
      } else if (/^[0-9]$/.test(key)) {
        // 1..9 jump to that slide; 0 jumps to 10.
        const n = key === '0' ? 9 : parseInt(key, 10) - 1;
        if (n < this._slides.length) this._go(n, 'keyboard');
      } else {
        handled = false;
      }
      if (handled) {
        e.preventDefault();
        this._flashOverlay();
      }
    }
    _go(i, reason = 'api') {
      if (!this._slides.length) return;
      const clamped = Math.max(0, Math.min(this._slides.length - 1, i));
      if (clamped === this._index) {
        this._flashOverlay();
        return;
      }
      this._index = clamped;
      this._applyIndex({
        showOverlay: true,
        broadcast: true,
        reason
      });
    }

    // Public API ------------------------------------------------------------

    /** Current slide index (0-based). */
    get index() {
      return this._index;
    }
    /** Total slide count. */
    get length() {
      return this._slides.length;
    }
    /** Programmatically navigate. */
    goTo(i) {
      this._go(i, 'api');
    }
    next() {
      this._go(this._index + 1, 'api');
    }
    prev() {
      this._go(this._index - 1, 'api');
    }
    reset() {
      this._go(0, 'api');
    }
  }
  if (!customElements.get('deck-stage')) {
    customElements.define('deck-stage', DeckStage);
  }
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dallas_families/deck-stage.js", error: String((e && e.message) || e) }); }

// ui_kits/dallas_families/shared.jsx
try { (() => {
// Shared washi tape element — cream textured torn-edge rectangle.
function Washi({
  width = 260,
  rotate = -2,
  top = -22,
  left = "50%"
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      top,
      left,
      transform: `translateX(-50%) rotate(${rotate}deg)`,
      width,
      height: 64,
      zIndex: 2,
      pointerEvents: "none"
    }
  }, /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 260 64",
    width: "100%",
    height: "100%",
    preserveAspectRatio: "none"
  }, /*#__PURE__*/React.createElement("defs", null, /*#__PURE__*/React.createElement("linearGradient", {
    id: "washiG",
    x1: "0",
    x2: "0",
    y1: "0",
    y2: "1"
  }, /*#__PURE__*/React.createElement("stop", {
    offset: "0",
    stopColor: "#F1E7D2"
  }), /*#__PURE__*/React.createElement("stop", {
    offset: ".5",
    stopColor: "#E8DCC3"
  }), /*#__PURE__*/React.createElement("stop", {
    offset: "1",
    stopColor: "#EFE4CE"
  })), /*#__PURE__*/React.createElement("filter", {
    id: "washiN",
    x: "0",
    y: "0"
  }, /*#__PURE__*/React.createElement("feTurbulence", {
    type: "fractalNoise",
    baseFrequency: "0.9",
    numOctaves: "2",
    seed: "3"
  }), /*#__PURE__*/React.createElement("feColorMatrix", {
    values: "0 0 0 0 0.2  0 0 0 0 0.15  0 0 0 0 0.1  0 0 0 .22 0"
  }), /*#__PURE__*/React.createElement("feComposite", {
    in2: "SourceGraphic",
    operator: "in"
  }))), /*#__PURE__*/React.createElement("path", {
    d: "M 4 10 L 14 6 L 28 10 L 42 5 L 60 9 L 80 6 L 100 10 L 124 7 L 150 10 L 172 6 L 196 9 L 222 7 L 244 10 L 256 8 L 256 54 L 246 58 L 228 54 L 208 57 L 184 54 L 160 58 L 140 54 L 116 57 L 92 54 L 70 58 L 48 54 L 28 57 L 10 55 L 4 58 Z",
    fill: "url(#washiG)"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 4 10 L 14 6 L 28 10 L 42 5 L 60 9 L 80 6 L 100 10 L 124 7 L 150 10 L 172 6 L 196 9 L 222 7 L 244 10 L 256 8 L 256 54 L 246 58 L 228 54 L 208 57 L 184 54 L 160 58 L 140 54 L 116 57 L 92 54 L 70 58 L 48 54 L 28 57 L 10 55 L 4 58 Z",
    filter: "url(#washiN)",
    opacity: ".5"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 90 18 L 130 46",
    stroke: "rgba(0,0,0,.08)",
    strokeWidth: "1"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 170 20 L 200 48",
    stroke: "rgba(0,0,0,.06)",
    strokeWidth: "1"
  })));
}
window.Washi = Washi;

// Orange asterisk/star bullet — 6-point stylized asterisk
function StarBullet({
  size = 28,
  color = "#F5A623"
}) {
  return /*#__PURE__*/React.createElement("svg", {
    width: size,
    height: size,
    viewBox: "0 0 32 32",
    style: {
      flex: `0 0 ${size}px`
    }
  }, /*#__PURE__*/React.createElement("g", {
    stroke: color,
    strokeWidth: "4",
    strokeLinecap: "round",
    fill: "none"
  }, /*#__PURE__*/React.createElement("line", {
    x1: "16",
    y1: "5",
    x2: "16",
    y2: "27"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "6",
    y1: "10",
    x2: "26",
    y2: "22"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "6",
    y1: "22",
    x2: "26",
    y2: "10"
  })));
}
window.StarBullet = StarBullet;

// Warm photo placeholder with SWAP tag
function PhotoPlaceholder({
  gradient = ["#BFD9C7", "#9EC5B8"],
  label = "SWAP PHOTO"
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      background: `linear-gradient(155deg, ${gradient[0]} 0%, ${gradient[1]} 100%)`,
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      backgroundImage: "radial-gradient(circle at 25% 30%, rgba(255,255,255,.35) 0%, transparent 45%), radial-gradient(circle at 75% 75%, rgba(255,255,255,.2) 0%, transparent 40%)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      top: 28,
      right: 28,
      fontFamily: "var(--ff-body)",
      fontSize: 14,
      fontWeight: 700,
      letterSpacing: ".12em",
      color: "rgba(255,255,255,.92)",
      background: "rgba(0,0,0,.28)",
      padding: "6px 12px",
      borderRadius: 4,
      backdropFilter: "blur(4px)"
    }
  }, label));
}
window.PhotoPlaceholder = PhotoPlaceholder;

// Detail card — white panel with washi tape, title, star bullets
function DetailCard({
  title,
  bullets
}) {
  // bullets are strings. First char can be a special marker to style tradeoff/best-for labels
  return /*#__PURE__*/React.createElement("div", {
    style: dcS.card
  }, /*#__PURE__*/React.createElement(Washi, {
    width: 260,
    rotate: -2,
    top: -22,
    left: "50%"
  }), /*#__PURE__*/React.createElement("h2", {
    style: dcS.title
  }, title), /*#__PURE__*/React.createElement("ul", {
    style: dcS.list
  }, bullets.map((b, i) => {
    // Detect "Tradeoff:" or "Best for:" prefix; split on first colon if present
    const tradeoffMatch = /^Tradeoff:\s*/i.test(b);
    const bestforMatch = /^Best for:\s*/i.test(b);
    let labelEl = null,
      rest = b;
    if (tradeoffMatch) {
      rest = b.replace(/^Tradeoff:\s*/i, "");
      labelEl = /*#__PURE__*/React.createElement("span", {
        style: {
          ...dcS.inlineLabel,
          color: "#F5A623"
        }
      }, "Tradeoff: ");
    } else if (bestforMatch) {
      rest = b.replace(/^Best for:\s*/i, "");
      labelEl = /*#__PURE__*/React.createElement("span", {
        style: {
          ...dcS.inlineLabel,
          color: "#00BCD4"
        }
      }, "Best for: ");
    }
    return /*#__PURE__*/React.createElement("li", {
      key: i,
      style: dcS.item
    }, /*#__PURE__*/React.createElement(StarBullet, {
      size: 28
    }), /*#__PURE__*/React.createElement("span", {
      style: dcS.text
    }, labelEl, rest));
  })));
}
const dcS = {
  card: {
    position: "absolute",
    left: 80,
    right: 80,
    top: 300,
    bottom: 140,
    background: "#FFFFFF",
    padding: "60px 56px 52px",
    boxShadow: "0 30px 60px rgba(26,39,68,.2), 0 4px 12px rgba(26,39,68,.12)",
    boxSizing: "border-box"
  },
  title: {
    fontFamily: "'Libre Baskerville', serif",
    fontWeight: 700,
    fontSize: 64,
    lineHeight: 1.05,
    color: "#F5A623",
    textAlign: "center",
    margin: "0 0 36px",
    letterSpacing: "-0.005em"
  },
  list: {
    listStyle: "none",
    padding: 0,
    margin: 0,
    display: "flex",
    flexDirection: "column",
    gap: 22
  },
  item: {
    display: "flex",
    gap: 18,
    alignItems: "flex-start",
    listStyle: "none"
  },
  text: {
    fontFamily: "'Lato', sans-serif",
    fontWeight: 400,
    fontSize: 26,
    lineHeight: 1.4,
    color: "#1A2744",
    paddingTop: 2,
    flex: "1 1 auto",
    display: "block"
  },
  inlineLabel: {
    fontFamily: "'Lato', sans-serif",
    fontWeight: 700
  }
};
window.DetailCard = DetailCard;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dallas_families/shared.jsx", error: String((e && e.message) || e) }); }

// ui_kits/dallas_families/slides.jsx
try { (() => {
// Dallas Families carousel — 8 slides, 1080x1350
// Uses window.Washi, window.StarBullet, window.PhotoPlaceholder, window.DetailCard

function CoverSlide() {
  return /*#__PURE__*/React.createElement("div", {
    style: sS.slide,
    "data-screen-label": "01 Cover"
  }, /*#__PURE__*/React.createElement("img", {
    src: "photos/cover.jpg",
    alt: "",
    style: sS.bg
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      background: "linear-gradient(180deg, rgba(0,0,0,.15) 0%, rgba(0,0,0,.05) 40%, rgba(0,0,0,.25) 100%)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      padding: "0 80px",
      textAlign: "center",
      color: "#fff"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "'Lato',sans-serif",
      fontWeight: 400,
      fontSize: 30,
      letterSpacing: ".02em",
      marginBottom: 28,
      textShadow: "0 2px 12px rgba(0,0,0,.3)"
    }
  }, "where to find a family home in"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontFamily: "'Libre Baskerville',serif",
      fontWeight: 700,
      fontSize: 132,
      lineHeight: 1,
      margin: 0,
      letterSpacing: "-0.01em",
      textShadow: "0 2px 20px rgba(0,0,0,.35)"
    }
  }, "dallas, texas"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "'Lato',sans-serif",
      fontWeight: 400,
      fontSize: 30,
      lineHeight: 1.45,
      marginTop: 52,
      maxWidth: 820,
      textShadow: "0 2px 12px rgba(0,0,0,.3)"
    }
  }, "School district lines don't follow city limits here. Here's where to look before you sign.")));
}
function MapSlide() {
  return /*#__PURE__*/React.createElement("div", {
    style: sS.slide,
    "data-screen-label": "02 Map"
  }, /*#__PURE__*/React.createElement("img", {
    src: "photos/cover.jpg",
    alt: "",
    style: sS.bg
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      background: "linear-gradient(180deg, rgba(0,0,0,.1) 0%, transparent 40%, rgba(0,0,0,.25) 100%)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      left: 80,
      right: 80,
      top: 130,
      bottom: 180,
      background: "#F5EFE2"
    }
  }, /*#__PURE__*/React.createElement(Washi, {
    width: 300,
    rotate: -3,
    top: -26,
    left: "50%"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: "40px 40px 40px 40px",
      background: "repeating-linear-gradient(90deg, transparent 0 60px, rgba(26,39,68,.08) 60px 61px), repeating-linear-gradient(0deg, transparent 0 60px, rgba(26,39,68,.08) 60px 61px), #FDF9EE"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      top: 20,
      left: 20,
      fontFamily: "'Libre Baskerville',serif",
      fontSize: 14,
      color: "#1A2744",
      background: "rgba(255,255,255,.8)",
      padding: "4px 10px",
      letterSpacing: ".1em",
      fontWeight: 700
    }
  }, "SWAP MAP"), [{
    top: "22%",
    left: "68%",
    name: "Lake Highlands",
    price: "1BRs from $1,100 to $1,600",
    anchor: "left"
  }, {
    top: "16%",
    left: "28%",
    name: "Richardson",
    price: "1BRs from $1,100 to $2,100",
    anchor: "right"
  }, {
    top: "58%",
    left: "20%",
    name: "Plano",
    price: "1BRs from $1,400 to $2,400",
    anchor: "right"
  }, {
    top: "72%",
    left: "72%",
    name: "Irving / Las Colinas",
    price: "1BRs from $1,100 to $2,000",
    anchor: "left"
  }].map((p, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      position: "absolute",
      top: p.top,
      left: p.left,
      transform: "translate(-50%,-50%)"
    }
  }, /*#__PURE__*/React.createElement(Pin, null), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      top: "100%",
      [p.anchor]: "50%",
      transform: p.anchor === "left" ? "translateX(-50%)" : "translateX(50%)",
      marginTop: 4,
      whiteSpace: "nowrap",
      textAlign: "center"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "'Libre Baskerville',serif",
      fontWeight: 700,
      fontSize: 18,
      color: "#1A2744"
    }
  }, p.name), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "'Libre Baskerville',serif",
      fontWeight: 400,
      fontSize: 13,
      color: "#1A2744",
      opacity: .75,
      marginTop: 2
    }
  }, p.price)))))), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      bottom: 60,
      left: 0,
      right: 0,
      textAlign: "center",
      fontFamily: "'Libre Baskerville',serif",
      fontStyle: "italic",
      fontSize: 26,
      color: "#fff",
      textShadow: "0 2px 10px rgba(0,0,0,.4)"
    }
  }, "The Neighborhoods"));
}
function Pin() {
  return /*#__PURE__*/React.createElement("svg", {
    width: "28",
    height: "36",
    viewBox: "0 0 28 36",
    style: {
      filter: "drop-shadow(0 2px 3px rgba(0,0,0,.25))"
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "M14 0 C6 0 0 6 0 14 C0 24 14 36 14 36 C14 36 28 24 28 14 C28 6 22 0 14 0 Z",
    fill: "#F5A623"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "14",
    cy: "14",
    r: "5",
    fill: "#fff"
  }));
}
function BridgeSlide() {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      ...sS.slide,
      background: "#FFC180"
    },
    "data-screen-label": "03 Bridge"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      padding: "0 100px",
      textAlign: "center"
    }
  }, /*#__PURE__*/React.createElement("h2", {
    style: {
      fontFamily: "'Libre Baskerville',serif",
      fontWeight: 700,
      fontSize: 68,
      lineHeight: 1.15,
      color: "#1A2744",
      margin: 0,
      letterSpacing: "-0.005em"
    }
  }, "Most families find this out after they've already signed."), /*#__PURE__*/React.createElement("div", {
    style: {
      width: 80,
      height: 3,
      background: "#F5A623",
      margin: "48px 0 44px"
    }
  }), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: "'Lato',sans-serif",
      fontWeight: 400,
      fontSize: 30,
      lineHeight: 1.5,
      color: "#1A2744",
      margin: 0,
      maxWidth: 820
    }
  }, "School district boundaries in Dallas don't match city limits. A Plano address doesn't guarantee you're in the Plano school district. Here are the four neighborhoods where the math actually works.")));
}
function LakeHighlands() {
  return /*#__PURE__*/React.createElement("div", {
    style: sS.slide,
    "data-screen-label": "04 Lake Highlands"
  }, /*#__PURE__*/React.createElement("img", {
    src: "photos/lake-highlands.jpg",
    alt: "",
    style: sS.bg
  }), /*#__PURE__*/React.createElement(DetailCard, {
    title: "Lake Highlands",
    bullets: ["Intown Dallas with White Rock Lake on its doorstep", "1,015-acre park, 9-mile loop trail, sailing club, dog park", "Under 20 minutes to downtown", "One of the stronger intown options within Dallas's school district, though quality varies across the city", "Tradeoff: Families needing school district consistency tend to find the suburbs more reliable", "Best for: Families who want to stay intown with serious park access on their doorstep"]
  }));
}
function Richardson() {
  return /*#__PURE__*/React.createElement("div", {
    style: sS.slide,
    "data-screen-label": "05 Richardson"
  }, /*#__PURE__*/React.createElement("img", {
    src: "photos/richardson.jpg",
    alt: "",
    style: sS.bg
  }), /*#__PURE__*/React.createElement(DetailCard, {
    title: "Richardson",
    bullets: ["Established suburb with one of the most well-regarded school districts in the metro", "Breckinridge Park: 418 acres of trails, athletic fields, disc golf, and a dog park", "DART rail to downtown in about 30 minutes", "CityLine adds walkable grocery, restaurants, and retail nearby", "Tradeoff: Rents run higher than Lake Highlands. Canyon Creek has the strongest family inventory", "Best for: Families where school quality is a priority and want an established community feel"]
  }));
}
function Plano() {
  return /*#__PURE__*/React.createElement("div", {
    style: sS.slide,
    "data-screen-label": "06 Plano"
  }, /*#__PURE__*/React.createElement("img", {
    src: "photos/plano.jpg",
    alt: "",
    style: sS.bg
  }), /*#__PURE__*/React.createElement(DetailCard, {
    title: "Plano",
    bullets: ["The go-to answer if school quality is the single biggest factor", "Bluebonnet Trail connects neighborhoods and parks for biking and jogging", "30 to 45 minutes to downtown along the tollway", "Shops at Willow Bend and Legacy West nearby for retail and restaurants", "Tradeoff: Runs 10 to 20 percent higher on rent than comparable Richardson buildings", "Best for: Families where school district is the top priority and budget allows for it"]
  }));
}
function Irving() {
  return /*#__PURE__*/React.createElement("div", {
    style: sS.slide,
    "data-screen-label": "07 Irving / Las Colinas"
  }, /*#__PURE__*/React.createElement("img", {
    src: "photos/irving.jpg",
    alt: "",
    style: sS.bg
  }), /*#__PURE__*/React.createElement(DetailCard, {
    title: "Irving / Las Colinas",
    bullets: ["The value option for families near DFW airport or the mid-cities corridor", "Lake Carolyn waterfront with restaurants and a lakefront path", "DFW airport 10 minutes away. DART rail to downtown in about 25 minutes", "More urban feel than most Dallas suburbs at a lower price point", "Tradeoff: School quality varies by campus. Research specific zoning before signing", "Best for: Families prioritizing budget flexibility or proximity to the airport"]
  }));
}
function CTASlide() {
  return /*#__PURE__*/React.createElement("div", {
    style: sS.slide,
    "data-screen-label": "08 CTA"
  }, /*#__PURE__*/React.createElement("img", {
    src: "photos/cover.jpg",
    alt: "",
    style: sS.bg
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      background: "linear-gradient(180deg, rgba(0,0,0,.15) 0%, rgba(0,0,0,.1) 50%, rgba(0,0,0,.35) 100%)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      padding: "0 80px",
      textAlign: "center",
      color: "#fff"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "'Lato',sans-serif",
      fontWeight: 400,
      fontSize: 32,
      letterSpacing: ".05em",
      marginBottom: 16,
      textShadow: "0 2px 12px rgba(0,0,0,.3)"
    }
  }, "Comment"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontFamily: "'Libre Baskerville',serif",
      fontWeight: 700,
      fontSize: 164,
      lineHeight: 1,
      margin: 0,
      letterSpacing: "-0.01em",
      textShadow: "0 2px 24px rgba(0,0,0,.4)"
    }
  }, "\"DALLAS\""), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "'Lato',sans-serif",
      fontWeight: 400,
      fontSize: 30,
      lineHeight: 1.5,
      marginTop: 44,
      maxWidth: 720,
      textShadow: "0 2px 12px rgba(0,0,0,.3)"
    }
  }, "to get the full guide before you sign your lease.")), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      bottom: 70,
      left: 0,
      right: 0,
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      gap: 14
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/brightplace-symbol.svg",
    alt: "",
    style: {
      height: 44,
      filter: "brightness(0) invert(1)"
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "'Urbanist',sans-serif",
      fontWeight: 600,
      fontSize: 32,
      color: "#fff",
      letterSpacing: "-0.01em"
    }
  }, "brightplace")));
}
const sS = {
  slide: {
    position: "relative",
    width: 1080,
    height: 1350,
    overflow: "hidden",
    background: "#fff"
  },
  bg: {
    position: "absolute",
    inset: 0,
    width: "100%",
    height: "100%",
    objectFit: "cover",
    objectPosition: "center"
  }
};
Object.assign(window, {
  CoverSlide,
  MapSlide,
  BridgeSlide,
  LakeHighlands,
  Richardson,
  Plano,
  Irving,
  CTASlide
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dallas_families/slides.jsx", error: String((e && e.message) || e) }); }

// ui_kits/maps/EditorialMap.jsx
try { (() => {
function EditorialMap({
  title = "Brooklyn",
  pins = [{
    name: "Clinton Hill",
    x: 50,
    y: 30,
    anchor: true
  }, {
    name: "Bed-Stuy",
    x: 72,
    y: 42
  }, {
    name: "Fort Greene",
    x: 32,
    y: 48
  }, {
    name: "Prospect Heights",
    x: 44,
    y: 64
  }, {
    name: "Crown Heights",
    x: 60,
    y: 72
  }]
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: eS.frame
  }, /*#__PURE__*/React.createElement("div", {
    style: eS.anchor
  }, title), /*#__PURE__*/React.createElement("svg", {
    style: eS.streets,
    viewBox: "0 0 1000 1000",
    preserveAspectRatio: "none"
  }, /*#__PURE__*/React.createElement("g", {
    stroke: "#1A2744",
    strokeWidth: "2.5",
    fill: "none",
    strokeLinecap: "round",
    opacity: ".85"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M 60 200 Q 340 180 600 220 T 950 210"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 50 360 Q 270 400 520 370 T 960 400"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 90 520 Q 400 500 660 540 T 940 520"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 70 680 Q 340 700 600 670 T 960 700"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 220 100 Q 240 420 220 700 T 260 960"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 480 80 Q 460 380 500 640 T 480 960"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 740 120 Q 760 420 720 700 T 760 960"
  })), /*#__PURE__*/React.createElement("g", {
    stroke: "#1A2744",
    strokeWidth: "4.5",
    fill: "none",
    opacity: ".95"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M 20 560 Q 300 540 600 580 T 980 560"
  }))), pins.map((p, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      ...eS.pinWrap,
      left: `${p.x}%`,
      top: `${p.y}%`
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: eS.pin
  }, /*#__PURE__*/React.createElement("div", {
    style: eS.dot
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      ...eS.label,
      fontWeight: p.anchor ? 700 : 400,
      fontStyle: i % 3 === 1 ? "italic" : "normal"
    }
  }, p.name))));
}
const eS = {
  frame: {
    position: "relative",
    width: "100%",
    height: "100%",
    background: "#FDFAF3",
    overflow: "hidden",
    fontFamily: "'Libre Baskerville',serif"
  },
  anchor: {
    position: "absolute",
    top: 28,
    left: 36,
    fontFamily: "'Libre Baskerville',serif",
    fontWeight: 700,
    fontSize: 40,
    color: "var(--bp-navy)",
    zIndex: 3
  },
  streets: {
    position: "absolute",
    inset: 0,
    width: "100%",
    height: "100%"
  },
  pinWrap: {
    position: "absolute",
    transform: "translate(-50%,-50%)",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 6,
    zIndex: 2
  },
  pin: {
    width: 26,
    height: 26,
    borderRadius: 999,
    background: "var(--bp-orange)",
    border: "3px solid #FDFAF3",
    boxShadow: "0 2px 6px rgba(26,39,68,.3)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 999,
    background: "var(--bp-navy)"
  },
  label: {
    fontFamily: "'Libre Baskerville',serif",
    fontSize: 18,
    color: "var(--bp-navy)",
    background: "rgba(253,250,243,.9)",
    padding: "2px 8px",
    borderRadius: 4,
    whiteSpace: "nowrap"
  }
};
window.EditorialMap = EditorialMap;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/maps/EditorialMap.jsx", error: String((e && e.message) || e) }); }

// ui_kits/maps/PreciseMap.jsx
try { (() => {
function PreciseMap({
  title = "Brooklyn",
  pins = [{
    name: "Clinton Hill",
    x: 50,
    y: 28,
    anchor: true
  }, {
    name: "Bed-Stuy",
    x: 72,
    y: 44
  }, {
    name: "Fort Greene",
    x: 30,
    y: 50
  }, {
    name: "Prospect Heights",
    x: 44,
    y: 68
  }]
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: pS.frame
  }, /*#__PURE__*/React.createElement("div", {
    style: pS.water
  }), /*#__PURE__*/React.createElement("svg", {
    style: pS.streets,
    viewBox: "0 0 1000 1000",
    preserveAspectRatio: "none"
  }, /*#__PURE__*/React.createElement("g", {
    stroke: "#D0D0D0",
    strokeWidth: "3",
    fill: "none"
  }, Array.from({
    length: 10
  }).map((_, i) => /*#__PURE__*/React.createElement("line", {
    key: `h${i}`,
    x1: "0",
    y1: 100 + i * 100,
    x2: "1000",
    y2: 110 + i * 100
  })), Array.from({
    length: 9
  }).map((_, i) => /*#__PURE__*/React.createElement("line", {
    key: `v${i}`,
    x1: 120 + i * 100,
    y1: "0",
    x2: 140 + i * 100,
    y2: "1000"
  }))), /*#__PURE__*/React.createElement("g", {
    stroke: "#AAAAAA",
    strokeWidth: "6",
    fill: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M 0 520 Q 300 500 600 540 T 1000 520"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M 480 0 Q 460 380 500 640 T 480 1000"
  }))), /*#__PURE__*/React.createElement("div", {
    style: pS.anchor
  }, title), pins.map((p, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      ...pS.pinWrap,
      left: `${p.x}%`,
      top: `${p.y}%`
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: pS.pin
  }, /*#__PURE__*/React.createElement("div", {
    style: pS.dot
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      ...pS.label,
      fontWeight: p.anchor ? 700 : 400
    }
  }, p.name))));
}
const pS = {
  frame: {
    position: "relative",
    width: "100%",
    height: "100%",
    background: "#FFFFFF",
    overflow: "hidden",
    fontFamily: "'Libre Baskerville',serif"
  },
  water: {
    position: "absolute",
    left: "-10%",
    top: "78%",
    right: "-10%",
    bottom: "-10%",
    background: "#CDE7EC",
    transform: "rotate(-4deg)"
  },
  streets: {
    position: "absolute",
    inset: 0,
    width: "100%",
    height: "100%"
  },
  anchor: {
    position: "absolute",
    top: 26,
    left: 32,
    fontFamily: "'Libre Baskerville',serif",
    fontWeight: 700,
    fontSize: 36,
    color: "var(--bp-navy)",
    zIndex: 3,
    background: "rgba(255,255,255,.85)",
    padding: "4px 10px",
    borderRadius: 4
  },
  pinWrap: {
    position: "absolute",
    transform: "translate(-50%,-50%)",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 6,
    zIndex: 2
  },
  pin: {
    width: 24,
    height: 24,
    borderRadius: 999,
    background: "var(--bp-orange)",
    border: "3px solid #fff",
    boxShadow: "0 2px 4px rgba(26,39,68,.25)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  },
  dot: {
    width: 7,
    height: 7,
    borderRadius: 999,
    background: "var(--bp-navy)"
  },
  label: {
    fontFamily: "'Libre Baskerville',serif",
    fontSize: 17,
    color: "var(--bp-navy)",
    background: "rgba(255,255,255,.9)",
    padding: "2px 8px",
    borderRadius: 4,
    whiteSpace: "nowrap"
  }
};
window.PreciseMap = PreciseMap;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/maps/PreciseMap.jsx", error: String((e && e.message) || e) }); }

// ui_kits/story/StoryCta.jsx
try { (() => {
function StoryCta({
  headline = "find your block.",
  sub = "tell us what matters. we walk the rest.",
  action = "get your match"
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: ctaS.slide
  }, /*#__PURE__*/React.createElement("div", {
    style: ctaS.bgWrap
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/brightplace-sketch.png",
    style: ctaS.bg,
    alt: ""
  }), /*#__PURE__*/React.createElement("div", {
    style: ctaS.scrim
  })), /*#__PURE__*/React.createElement("img", {
    src: "../../assets/brightplace-logo.svg",
    alt: "brightplace",
    style: ctaS.logo
  }), /*#__PURE__*/React.createElement("div", {
    style: ctaS.mid
  }, /*#__PURE__*/React.createElement("div", {
    style: ctaS.headline
  }, headline), /*#__PURE__*/React.createElement("div", {
    style: ctaS.sub
  }, sub), /*#__PURE__*/React.createElement("button", {
    style: ctaS.btn
  }, action, " \u2192"), /*#__PURE__*/React.createElement("div", {
    style: ctaS.receipt
  }, "free \xB7 90 seconds \xB7 no account")));
}
const ctaS = {
  slide: {
    position: "relative",
    width: "100%",
    height: "100%",
    background: "var(--bp-paper)",
    overflow: "hidden",
    fontFamily: "var(--ff-display)"
  },
  bgWrap: {
    position: "absolute",
    inset: 0
  },
  bg: {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    opacity: .92
  },
  scrim: {
    position: "absolute",
    inset: 0,
    background: "linear-gradient(180deg,rgba(250,246,239,.15) 0%,rgba(250,246,239,.75) 55%,rgba(250,246,239,.98) 100%)"
  },
  logo: {
    position: "absolute",
    top: 120,
    left: 80,
    height: 72,
    zIndex: 2
  },
  mid: {
    position: "absolute",
    left: 80,
    right: 80,
    bottom: 220,
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
    gap: 28,
    zIndex: 2
  },
  headline: {
    fontFamily: "var(--ff-display)",
    fontWeight: 600,
    fontSize: 110,
    lineHeight: 1,
    letterSpacing: "-0.02em",
    color: "var(--bp-navy)"
  },
  sub: {
    fontFamily: "'Libre Baskerville',serif",
    fontStyle: "italic",
    fontSize: 32,
    lineHeight: 1.35,
    color: "var(--bp-ink-soft)",
    maxWidth: 800
  },
  btn: {
    fontFamily: "var(--ff-display)",
    fontWeight: 600,
    fontSize: 44,
    padding: "28px 56px",
    border: 0,
    borderRadius: 999,
    background: "var(--bp-orange)",
    color: "var(--bp-navy)",
    letterSpacing: "-0.01em",
    boxShadow: "0 10px 30px rgba(26,39,68,.15)",
    marginTop: 12
  },
  receipt: {
    fontFamily: "var(--ff-body)",
    fontSize: 22,
    color: "var(--bp-ink-muted)",
    letterSpacing: ".02em"
  }
};
window.StoryCta = StoryCta;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/story/StoryCta.jsx", error: String((e && e.message) || e) }); }

// ui_kits/story/StoryHero.jsx
try { (() => {
function StoryHero({
  eyebrow = "brooklyn, tonight",
  headline = "the 7pm\ncoffee block\nmap",
  meta = "a 4-minute read"
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: heroS.slide
  }, /*#__PURE__*/React.createElement("div", {
    style: heroS.bgWrap
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/brightplace-sketch.png",
    style: heroS.bg,
    alt: ""
  }), /*#__PURE__*/React.createElement("div", {
    style: heroS.scrim
  })), /*#__PURE__*/React.createElement("div", {
    style: heroS.top
  }, /*#__PURE__*/React.createElement("div", {
    style: heroS.eyebrow
  }, eyebrow)), /*#__PURE__*/React.createElement("div", {
    style: heroS.mid
  }, /*#__PURE__*/React.createElement("h1", {
    style: heroS.h1
  }, headline.split("\n").map((l, i) => /*#__PURE__*/React.createElement("span", {
    key: i,
    style: {
      display: "block"
    }
  }, l))), /*#__PURE__*/React.createElement("div", {
    style: heroS.meta
  }, meta)), /*#__PURE__*/React.createElement("div", {
    style: heroS.bot
  }, "swipe up \u2192"));
}
const heroS = {
  slide: {
    position: "relative",
    width: "100%",
    height: "100%",
    background: "var(--bp-paper)",
    overflow: "hidden",
    fontFamily: "var(--ff-display)"
  },
  bgWrap: {
    position: "absolute",
    inset: 0
  },
  bg: {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    opacity: .95
  },
  scrim: {
    position: "absolute",
    inset: 0,
    background: "linear-gradient(180deg,rgba(250,246,239,0) 30%,rgba(250,246,239,.95) 85%)"
  },
  top: {
    position: "absolute",
    top: 120,
    left: 72,
    right: 72
  },
  eyebrow: {
    fontFamily: "'Libre Baskerville',serif",
    fontStyle: "italic",
    fontSize: 34,
    color: "var(--bp-navy)"
  },
  mid: {
    position: "absolute",
    left: 72,
    right: 72,
    bottom: 240,
    display: "flex",
    flexDirection: "column",
    gap: 28
  },
  h1: {
    fontFamily: "var(--ff-display)",
    fontWeight: 600,
    fontSize: 150,
    lineHeight: .98,
    letterSpacing: "-0.025em",
    color: "var(--bp-navy)",
    margin: 0
  },
  meta: {
    fontFamily: "'Libre Baskerville',serif",
    fontStyle: "italic",
    fontSize: 30,
    color: "var(--bp-ink-soft)"
  },
  bot: {
    position: "absolute",
    left: 0,
    right: 0,
    bottom: 140,
    textAlign: "center",
    fontFamily: "var(--ff-display)",
    fontWeight: 500,
    fontSize: 24,
    color: "var(--bp-navy)",
    opacity: .55
  }
};
window.StoryHero = StoryHero;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/story/StoryHero.jsx", error: String((e && e.message) || e) }); }

// ui_kits/story/StoryQuote.jsx
try { (() => {
function StoryQuote({
  quote = "it feels like someone who actually walked the block wrote this.",
  attribution = "renter, clinton hill, 2025"
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: qS.slide
  }, /*#__PURE__*/React.createElement("div", {
    style: qS.mark
  }, "\""), /*#__PURE__*/React.createElement("div", {
    style: qS.mid
  }, /*#__PURE__*/React.createElement("div", {
    style: qS.quote
  }, quote), /*#__PURE__*/React.createElement("div", {
    style: qS.attr
  }, "\u2014 ", attribution)), /*#__PURE__*/React.createElement("div", {
    style: qS.rule
  }), /*#__PURE__*/React.createElement("div", {
    style: qS.footer
  }, "brightplace guides \xB7 400+ on-foot reports"));
}
const qS = {
  slide: {
    position: "relative",
    width: "100%",
    height: "100%",
    background: "var(--bp-paper)",
    padding: "140px 80px 160px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    gap: 40,
    boxSizing: "border-box",
    fontFamily: "var(--ff-display)"
  },
  mark: {
    position: "absolute",
    top: 180,
    left: 80,
    fontFamily: "'Libre Baskerville',serif",
    fontSize: 280,
    lineHeight: .7,
    color: "var(--bp-orange)",
    fontWeight: 700
  },
  mid: {
    marginTop: 120,
    display: "flex",
    flexDirection: "column",
    gap: 40
  },
  quote: {
    fontFamily: "'Libre Baskerville',serif",
    fontStyle: "italic",
    fontWeight: 400,
    fontSize: 70,
    lineHeight: 1.2,
    color: "var(--bp-navy)"
  },
  attr: {
    fontFamily: "var(--ff-display)",
    fontWeight: 500,
    fontSize: 28,
    color: "var(--bp-ink-muted)",
    letterSpacing: ".01em"
  },
  rule: {
    width: 96,
    height: 3,
    background: "var(--bp-orange)",
    marginTop: 60
  },
  footer: {
    fontFamily: "'Libre Baskerville',serif",
    fontStyle: "italic",
    fontSize: 22,
    color: "var(--bp-ink-muted)"
  }
};
window.StoryQuote = StoryQuote;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/story/StoryQuote.jsx", error: String((e && e.message) || e) }); }

// ui_kits/story/StoryStat.jsx
try { (() => {
function StoryStat({
  stat = "7",
  unit = "blocks",
  desc = "that cleared the bar. quiet after 8pm, two cafes open by 7am, 15-minute walk to express service.",
  footer = "brooklyn · coffee blocks"
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: statS.slide
  }, /*#__PURE__*/React.createElement("div", {
    style: statS.top
  }, /*#__PURE__*/React.createElement("div", {
    style: statS.kicker
  }, "our count")), /*#__PURE__*/React.createElement("div", {
    style: statS.mid
  }, /*#__PURE__*/React.createElement("div", {
    style: statS.stat
  }, stat), /*#__PURE__*/React.createElement("div", {
    style: statS.unit
  }, unit), /*#__PURE__*/React.createElement("div", {
    style: statS.desc
  }, desc)), /*#__PURE__*/React.createElement("div", {
    style: statS.foot
  }, footer));
}
const statS = {
  slide: {
    position: "relative",
    width: "100%",
    height: "100%",
    background: "var(--bp-peach)",
    overflow: "hidden",
    padding: "140px 80px 160px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    boxSizing: "border-box",
    fontFamily: "var(--ff-display)"
  },
  top: {},
  kicker: {
    fontFamily: "'Libre Baskerville',serif",
    fontStyle: "italic",
    fontSize: 30,
    color: "var(--bp-ink-soft)"
  },
  mid: {
    display: "flex",
    flexDirection: "column",
    gap: 16
  },
  stat: {
    fontFamily: "var(--ff-display)",
    fontWeight: 600,
    fontSize: 520,
    lineHeight: .82,
    letterSpacing: "-0.04em",
    color: "var(--bp-navy)"
  },
  unit: {
    fontFamily: "var(--ff-display)",
    fontWeight: 500,
    fontSize: 80,
    color: "var(--bp-navy)",
    letterSpacing: "-0.02em"
  },
  desc: {
    marginTop: 24,
    fontFamily: "'Libre Baskerville',serif",
    fontSize: 28,
    lineHeight: 1.45,
    color: "var(--bp-ink-soft)",
    maxWidth: 720
  },
  foot: {
    fontFamily: "'Libre Baskerville',serif",
    fontStyle: "italic",
    fontSize: 22,
    color: "var(--bp-ink-muted)",
    borderTop: "1px solid rgba(26,39,68,.25)",
    paddingTop: 18
  }
};
window.StoryStat = StoryStat;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/story/StoryStat.jsx", error: String((e && e.message) || e) }); }

})();
