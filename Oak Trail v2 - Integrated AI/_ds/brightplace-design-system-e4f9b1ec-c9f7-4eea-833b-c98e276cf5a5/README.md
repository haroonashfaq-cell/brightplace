# brightplace Design System

> The apartment rental industry's first AI-native discovery platform.
> This folder is the source of truth for how brightplace looks, sounds, and feels.

---

## What is brightplace

brightplace (always lowercase, always one word) serves two audiences:

- **Renters** — personalized rental recommendations delivered by the **AI Rental Advisor**.
- **Operators** — real-time renter intent data delivered through **IntentOS**.

The content engine produces **Instagram carousels** (1080×1350, 4:5), **TikTok / Stories** (1080×1920, 9:16), **illustrated + precise neighborhood maps**, neighborhood guides, and operator-facing materials. The aesthetic target is **editorial, warm, intelligent** — premium city guide meets modern tech platform. Not cartoonish, not corporate, not cold.

## Products represented here

| Product | Audience | Surface |
|---|---|---|
| AI Rental Advisor | Renters | Web + social content |
| IntentOS | Operators | Web dashboards, decks, reports |
| Content system | Both | Instagram carousels, TikTok/Stories, map assets, neighborhood guides |

## Sources provided

This design system was built from brand materials supplied directly:

- **Logos (wordmark + symbol):** `brightplace.svg/.png/.pdf/.eps`, `Symbol-brightplace.svg/.png/.pdf/.eps`
- **Sketch treatment:** `brightplace - sketch.png` — key illustrative motif for editorial covers
- **Linked cover:** `brightplace-linked-cover-03.jpg` — orange gradient header band
- **Mascot (Penny):** `Penny 1.jpg`, `Penny 2.jpg` — internal character illustrations
- **App icons:** `favicon.png`, `apple-touch-icon.png`
- **Fonts:** Urbanist (complete variable + static family) — shipped locally in `fonts/`
- **Brand rules + copy tone:** captured from the engagement brief (included below)

> **Self-hosted:** Urbanist and Libre Baskerville ship locally in `fonts/`. **Lato still loads from Google Fonts** — upload the Lato zip to fully self-host. All `.eps` and `.pdf` logo variants were listed but not delivered; the `.svg` and `.png` variants we have are sufficient for digital work.

---

## Index

```
brightplace-design-system/
├── README.md                 ← you are here
├── SKILL.md                  ← agent skill manifest
├── colors_and_type.css       ← tokens + semantic classes (import this)
├── fonts/                    ← Urbanist ttf family + variable axis + OFL
├── assets/                   ← logos, symbol, mascot, cover imagery, icons
├── preview/                  ← design-system preview cards (Type, Colors, Spacing, Components, Brand)
├── ui_kits/
│   ├── carousel/             ← Instagram 1080×1350 templates (cover → bridge → map → detail → CTA)
│   ├── story/                ← TikTok / Stories 1080×1920 templates
│   └── maps/                 ← editorial + precise map samples
└── uploads/                  ← original uploaded source files (do not edit)
```

Quick links
- **Foundation CSS:** [`colors_and_type.css`](./colors_and_type.css)
- **Instagram carousel kit:** [`ui_kits/carousel/index.html`](./ui_kits/carousel/index.html)
- **Stories / TikTok kit:** [`ui_kits/story/index.html`](./ui_kits/story/index.html)
- **Maps kit:** [`ui_kits/maps/index.html`](./ui_kits/maps/index.html)
- **Skill manifest:** [`SKILL.md`](./SKILL.md)

---

## CONTENT FUNDAMENTALS

The voice is **confident, editorial, city-literate**. Every line should read like someone who has actually walked the neighborhood, not someone generating filler. Copy is where the brand earns trust.

### Casing & grammar
- **"brightplace" is always lowercase.** Even at the start of a sentence, in a headline, in a DM, in a chart title, everywhere. Treat it like "iPhone" with the opposite rule.
- **No em dashes, anywhere.** Use a period, a comma, or a line break. (Note: hyphens in compound words are fine; em-dashes as punctuation are not.)
- Sentence case for most headlines. Avoid ALL CAPS. **Maps specifically prohibit ALL CAPS labels.**
- Oxford comma, standard US English.

### Voice
- **Second person ("you") to renters**, first-person plural ("we") sparingly when speaking as the platform.
- **Third person to operators** ("renters who…", "your portfolio…").
- Concrete > abstract. "A 14-minute walk to the J" beats "great transit."
- One idea per sentence. Short > long.

### Tone
- Warm but not cute. Intelligent but not jargony. Specific but not listy.
- Feels like a friend who is a planner, not a marketer.
- Emoji: **no**, unless a very specific UI affordance requires one. Not for decoration.

### Banned words (do not use)
`vibrant`, `bustling`, `hidden gem`, `best-kept secret`, `signal`, `dive into`, `navigate`, `unlock`.
Also avoid "nestled", "eclectic mix", "something for everyone" and related city-guide clichés.

### Hard rules
- **Fair Housing compliant, always.** Describe neighborhoods by lifestyle infrastructure — coffee, transit, parks, grocery, noise, daylight — never by demographic framing or safety language. No "safe / unsafe", no "good for families / singles", no racial or economic shorthand.
- **No ranking language without named evidence.** "Best" / "top" / "#1" require a cited, published brightplace guide. If you can't name the source on the same slide, don't make the claim.
- **Every video script claim traces to a published brightplace guide.** No general-knowledge filler. If it's not in a guide, it's not in the script.

### Carousel copy examples

✅ **Good cover:**
> brooklyn's 7 quietest coffee blocks
> (sub) a 4-minute read, by neighborhood

✅ **Good detail bullet:**
> 14-minute walk to the G at Classon. Two indie bakeries open by 7am. Street parking is permit-only after 6pm.

❌ **Avoid:**
> Discover the vibrant, bustling heart of Brooklyn — a hidden gem nestled between…

### CTA pattern
> get your match
> (sub) free, 90 seconds, no account

Keep CTAs action-first, promise-second, receipt-third.

---

## VISUAL FOUNDATIONS

### Color
- **Orange `#F5A623`** — pins, CTAs, primary accent. Used in small, high-intent moments. Never as a large background except the CTA slide's full-bleed cover.
- **Navy `#1A2744`** — primary text, map streets (editorial style), logo, chart strokes. The load-bearing color of the brand.
- **Teal `#00BCD4`** — UI accent (small buttons, notifications, data callouts). Not used in maps.
- **Peach `#FFC180`** — soft backgrounds, secondary cards, editorial blocks. Warms the page when paper feels too stark.
- **Paper `#FAF6EF`** — default carousel / slide background. Warm off-white, not grey, not pure white.
- **Street grey `#D0D0D0`** and **Highway grey `#AAAAAA`** — maps only. Street grey for surface streets in **precise** maps; highway grey for arterials.

The palette is **warm-biased**: paper instead of white, navy instead of black, peach as the soft surface. Cool greys only appear inside maps.

### Type
- **Urbanist 600** — display headlines. Tight tracking (-0.02em). Sentence case.
- **Urbanist 500** — subheads, section labels, small UI chrome.
- **Libre Baskerville 400** — editorial accents (pull quotes, intro lines, captions), and **all map labels**.
- **Libre Baskerville 700** — city anchor labels on maps.
- **Lato 400** — body copy.
- **Lato 700** — inline emphasis only (`<strong>`), not headlines.

Maps use **Libre Baskerville exclusively**. Zero sans-serif, zero all-caps on maps.

### Backgrounds
- Default: warm paper (`#FAF6EF`). Full-bleed photography used sparingly, only for cover + CTA slides (and the cover image matches the CTA image — they're a pair).
- No gradients as decoration. The orange linked-cover band is the one sanctioned gradient; reuse that asset, don't invent new ones.
- Hand-drawn editorial maps are a hero motif for illustrated carousels. Clean flat maps for precise geography.
- Grain / noise texture at ~4% opacity on paper backgrounds is permitted, never required.

### Imagery character
- Warm-biased photography. Golden hour, morning sun, interior window light.
- Avoid: cold blue overcast, heavy saturation, HDR, stock-tropes (aerial skyline at night, neon rain, drone over bridge).
- If we show people, they're incidental to architecture or street life, not the subject.

### Borders, corners, elevation
- **Radii:** cards `12px`, buttons/pills `999px`, photos `8px`, map markers `999px` (circles).
- **Borders:** 1px hairline `#E3DDCF` on paper, 1.5px navy where a card needs to assert itself. No dashed, no dotted.
- **Shadows:** extremely light. Editorial prefers flatness. When used: `0 8px 24px rgba(26,39,68,.08)`. Map pins get a small drop: `0 2px 4px rgba(26,39,68,.25)`.
- **Inner shadows, neumorphism, glassmorphism: no.**

### Motion
- **Easing** `cubic-bezier(.2,.7,.2,1)` (`--ease-out`) for entrances.
- **Durations** 120 / 220 / 420 ms. Keep it crisp; no bounces, no overshoots.
- Carousels and stories: page-to-page transitions are instant or a 180ms cross-fade. No slide-in from the side.
- Hover: opacity 0.85 or a one-step darker color. Never scale.
- Press: translateY(1px). No color flash.

### Layout
- **Carousels (1080×1350):** 72px outer margin on sides, 96px top, 112px bottom. Safe zone pulls in another 24px on stories (1080×1920) because of system overlays.
- **12-column grid** for editorial layouts; 4-column for mobile previews. Gutter 24px.
- Fixed elements: the **brightplace logo appears on the CTA slide only**. Not on covers, not on detail slides. This is a hard rule.
- Slide-numbering dots / progress bars: no, unless a deck client specifically requires them.

### Transparency & blur
- Used only to fade an image behind text for contrast (black-to-transparent gradient, 0–60%).
- Backdrop-blur: never in carousels, occasionally in product UI (floating toolbars).

### Card pattern
```
background: var(--bg-surface);
border: 1px solid var(--border-hair);
border-radius: var(--r-md);           /* 12px */
padding: var(--sp-5);                  /* 24px */
box-shadow: var(--shadow-card);        /* very light */
```

### Button pattern
- **Primary:** orange fill, navy text (`--fg-on-accent`), pill radius, Urbanist 600, 16px vertical / 28px horizontal padding.
- **Secondary:** navy outline (1.5px), navy text, transparent fill.
- **Tertiary:** text button, navy, underline on hover.

---

## ICONOGRAPHY

brightplace does not ship a bespoke icon set. Our approach:

- **Primary source: Lucide icons via CDN** (`https://unpkg.com/lucide@latest`). Lucide's stroke weight (1.5–2px, rounded) matches our editorial warmth. Use `stroke="currentColor"`, inherit from navy by default.
- **Map pins are a brand element, not an icon.** A solid orange circle (`#F5A623`) with a small inner navy dot. Always flat, no shadow on the flat variant; subtle shadow (`--shadow-pin`) on illustrative maps.
- **Emoji: no.** Except in product UI where an explicit emoji affordance exists (reactions, tags) — never in marketing.
- **Unicode characters as icons:** avoid. Exceptions: `→` arrow in CTAs is permitted, always Urbanist 600.
- **brightplace symbol:** the skyline-under-sun glyph. Never recolored, never used below 24px (falls apart). Files live at `assets/brightplace-symbol.{svg,png}`.

### Icon substitution flag
We link Lucide from CDN rather than shipping our own icon set — this is a substitution decision. If brightplace adopts a custom icon system later, drop the SVG files in `assets/icons/` and update the CDN reference.

### Key brand assets (in `assets/`)
- `brightplace-logo.svg` / `.png` — full wordmark + symbol, black. Use on light backgrounds.
- `brightplace-symbol.svg` / `.png` — just the skyline-under-sun. Square-ish, works as avatar.
- `brightplace-sketch.png` — hand-drawn color treatment (teal buildings + orange sun). **Editorial hero motif** for illustrated carousels.
- `brightplace-linked-cover.jpg` — orange gradient band with wordmark top-right. Use as a section header on operator materials.
- `penny-1.jpg`, `penny-2.jpg` — "Penny," an internal mascot character. **Use sparingly, internal contexts only.** Not for external renter-facing content until brand confirms usage.
- `favicon.png`, `apple-touch-icon.png` — web/app icons.

---

## How to use this system

1. In any HTML: `<link rel="stylesheet" href="/colors_and_type.css">`.
2. Use CSS custom properties (`var(--bp-orange)`) — never hardcode hex values.
3. Use semantic classes (`.bp-h1`, `.bp-body`, `.bp-map-label`) over inventing new styles.
4. Pull assets from `assets/` — do not re-render the logo as HTML/SVG from memory.
5. When in doubt, re-read CONTENT FUNDAMENTALS. The words matter more than the pixels.

---

*Last updated by the design-system build. For questions or to flag missing assets, see the caveats at the bottom of the build handoff.*
