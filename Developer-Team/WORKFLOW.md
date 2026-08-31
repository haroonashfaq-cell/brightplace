# Operator Pages — Production Workflow

**Version:** 1.0
**Last Updated:** August 2026
**Purpose:** Defines the exact process for building and shipping operator property pages. Every page passes through all agents in order.

---

## Overview

```
1. Design Agent → 2. Developer Agent → 3. QA Agent → 4. Mobile QA Agent → 5. Deploy
```

---

## Stage 1: Design Agent

**Trigger:** New operator property page requested, or design revision needed.

**Agent file:** `agents/design-agent.md`

**What it does:**
- Audits the brightplace design system tokens (colors, type, spacing, radii, shadows)
- Creates the component hierarchy and layout structure
- Defines motion/animation patterns for each section
- Ensures visual consistency with brand guidelines
- Reviews typography hierarchy (Urbanist display, Lato body, Libre Baskerville editorial)
- Validates color contrast ratios (WCAG AA minimum)
- Produces a design spec the Developer Agent can build from

**Output:** Design spec with component list, layout grid, animation notes, and any new tokens needed.

---

## Stage 2: Developer Agent

**Trigger:** Design spec approved or design complete.

**Agent file:** `agents/developer-agent.md`

**What it does:**
- Builds Next.js components from the design spec
- Implements Framer Motion animations
- Adds SEO infrastructure (meta tags, JSON-LD, Open Graph)
- Ensures static export compatibility (`output: 'export'`)
- Wires up operator data from `src/data/operators.ts`
- Validates all content is server-rendered in HTML (not hidden behind JS)
- Runs `npm run build` to verify clean compilation

**Output:** Working page that builds successfully with `npm run build`.

---

## Stage 3: QA Agent

**Trigger:** Developer Agent reports clean build.

**Agent file:** `agents/qa-agent.md`

**What it does:**
- Runs ALL 6 QA sections (Brand, SEO, Performance, Accessibility, Content, Infrastructure)
- Verifies JSON-LD structured data in static HTML output
- Checks robots.txt and sitemap.xml
- Validates all images have alt text
- Confirms AI crawler compatibility (GPTBot, ClaudeBot, PerplexityBot)
- Checks for hardcoded URLs, broken links, missing meta tags
- Validates semantic HTML structure

**Output:** Structured PASS/FAIL report. All sections must PASS before proceeding.

---

## Stage 4: Mobile QA Agent

**Trigger:** QA Agent reports all sections PASS.

**Agent file:** `agents/mobile-qa-agent.md`

**What it does:**
- Audits every component at 375px, 390px, 428px, and 768px viewports
- Checks touch targets (minimum 44x44px)
- Validates text readability (minimum 12px)
- Tests grid collapse behavior at each breakpoint
- Checks for horizontal overflow
- Validates fixed/absolute positioning on small screens
- Tests interactive elements (menus, accordions, modals, lightboxes)
- Verifies AI chat panel usability on mobile

**Output:** Structured report with issues by viewport size. All MUST PASS.

---

## Stage 5: Deploy

**Trigger:** Mobile QA Agent reports all PASS.

**Actions:**
1. Final `npm run build` to generate static export
2. Verify `out/` directory contains all expected HTML files
3. Push to GitHub
4. Vercel auto-deploys from GitHub
5. Verify live URL loads correctly
6. Test structured data with Google Rich Results Test

---

## Rules

- **Never skip an agent.** Even for "small changes," run QA and Mobile QA.
- **Agents learn from failures.** When an agent catches an issue, update the agent's checklist so it catches the same class of issue automatically next time.
- **Design system is law.** Never introduce colors, fonts, or spacing outside the brightplace design system without updating the tokens.
- **Every page must build statically.** If `npm run build` fails, the page doesn't ship.
- **Content in HTML, motion in JS.** All text, data, and structured content must be in the static HTML. Animations are progressive enhancement only.
