# brightplace — Property Page Structure Guide

**Audience:** engineers building and maintaining the property page template
**Scope:** the property detail page (`/property/{state}/{city}/{slug}/{listing-key}`) at marketplace scale — thousands of pages, growing
**Companion:** the visual version of this document is the *Property Page Content Layers* canvas
**Reference page used throughout:** `600 Washington Apartments`, `equity-b2662` (staging), measured 2026-09-09

---

## 0. Why this document exists

The property page is the product's main organic surface. It is fetched by three audiences with different capabilities:

| Audience | Executes JS? | What it needs |
|---|---|---|
| Human visitor | Yes | Fast first paint, working interactivity |
| Googlebot | No (for our purposes — assume no) | Complete content in the HTML response |
| GPTBot / ClaudeBot / PerplexityBot / OAI-SearchBot | **No** | Complete, self-dated, unambiguous facts in the HTML response |

Everything below follows from one consequence: **any fact that is not in the server-rendered HTML does not exist** for two of those three audiences.

The current implementation already gets this right — the staging page returns 1,668 words of real DOM content with JavaScript disabled. This guide exists to keep it that way as the page network scales and features are added.

---

## 1. Rendering model

### 1.1 Server Components are the SSR layer

Next.js App Router. Server Components by default. `'use client'` only at the leaves listed in §5.

Any data needed to render page content is fetched in a Server Component and passed down as props. Never re-fetch page content on the client, and never hand-maintain a parallel client state blob — the RSC payload is the hydration mechanism.

### 1.2 Generation tiers

At thousands of pages, full SSG at deploy time is not viable and per-request SSR is unnecessary. Use three tiers:

| Tier | Pages | Strategy |
|---|---|---|
| Warm | Top-traffic properties, all city / neighborhood / facet hubs | `generateStaticParams` — pre-rendered at deploy |
| Long tail | Everything else | ISR with **blocking** fallback — generated on first request, then cached |
| Slow sections | POIs, nearby listings, market data | Streaming SSR via `<Suspense>` — keeps TTFB low without pushing content client-side |

**Blocking fallback is mandatory.** A crawler must never receive a loading state.

### 1.3 Revalidation is event-driven, not time-driven

Do not put a time-based `revalidate` on property pages. Time-based ISR at this scale either serves stale pricing or burns compute on unchanged pages.

```
feed ingest detects change on listing L
  → revalidatePath('/property/.../L')
  → revalidatePath(parent neighborhood hub)
  → revalidatePath(parent city hub)
  → revalidateTag(any facet the listing belongs to)
```

Cache TTL by page type: property pages short, hub/facet pages longer, editorial pages longest.

### 1.4 Personalization must not touch cached HTML

Sign-in state, favorites and personalization hydrate **after** load, from the client. A logged-in view renders the same HTML as an anonymous view. Anything else poisons the shared cache.

---

## 2. The four layers

Every element on the page belongs to exactly one layer. The layer determines its owner, its permitted change frequency, and the failure mode when the rule is broken.

| Layer | Definition | Cadence | Owner |
|---|---|---|---|
| **LOCKED** | The ranking substrate. Set once at page creation. | Effectively never | Engineering + SEO sign-off |
| **STABLE** | Evergreen content. Changes when the world changes. | Quarterly or on material trigger | Content agents, diff-gated |
| **LIVE** | Feed-owned facts. Expected to move. | As often as the feed moves | Feed pipeline |
| **ISLAND** | Client-side interactivity. | On release | Engineering |

### LOCKED
URL and slug · title pattern · canonical · H1 · every H2 question heading · property name · street address and geo · manager name · breadcrumbs · schema `@id` and `@type` · nav and footer link graph

*Failure mode:* ranking history resets. The page re-enters the index as new and loses accumulated relevance. Any AI citation pointing at the old URL breaks. Recovery takes months.

### STABLE
Amenity list · building description · photos and alt text · neighborhood and POI narrative · walk/transit/bike scores · schools · review synthesis prose · agent-written context and comparisons

*Failure mode:* continuous rewriting churns the page's semantic fingerprint and resets accrued topical relevance. The page never settles on a ranking.

### LIVE
Rent range and per-unit prices · available unit count · availability dates · which floor plans have inventory · deposits, fees, move-in specials · review count and rating · the "as of" stamp itself

*Failure mode:* undated prices get cited months later as current. Sources that are repeatedly contradicted get cited less.

### ISLAND
Ask brightplace chat · map and POI toggles · photo lightbox · floor-plan filter tabs · "Show all amenities" and "Show more" expanders · tour scheduling and lead forms · favorites, sign-in, personalization

*Failure mode:* one component converted to lazy-fetch silently removes a whole section from every AI crawler across every property page at once. Nothing visibly breaks, so nobody notices.

---

## 3. The rules

> **Pin the frame. Slot the facts. Date the numbers. Islands show and hide — they never fetch.**

1. **Islands may show, hide, sort or filter content that is already in the HTML. They may never fetch it.** Code review rejects any island that introduces a content fetch.
2. **Heading text is pinned copy in a shared constant, never generated from data.** A heading whose wording changes when inventory changes is a bug.
3. **Every LIVE value sits in a pinned sentence frame and carries the date it was checked.** Slot the value; never regenerate the sentence.
4. **Bump `lastmod` only on material change** — new floor plan, availability state flip, evergreen regeneration. Not on a $5 price tick. Inflated `lastmod` across 100k URLs teaches Google to ignore it.
5. **Evergreen regeneration is diff-gated.** If an agent run changes more than ~20% of stable text without a matching change in source data, hold it for review. Version the evergreen layer so a bad run can be rolled back.
6. **Operator-supplied feed descriptions are duplicate content across the web.** They must never be the only prose on a page.
7. **Non-production hosts serve `Disallow: /` and `X-Robots-Tag: noindex`, env-gated.** A production canonical does *not* stop AI crawlers ingesting staging.

### 3.1 The hybrid pattern

The lead answer paragraph is the most-cited block on the page and the model for the whole design:

> As of **{as_of_date}**, *600 Washington Apartments at 600 Washington St, New York, NY, 10014* has **{unit_count} apartments** for rent, **{bed_range}** layouts, with rents from **{min_rent} to {max_rent}/mo**. Managed by *Equity Residential*, it has a gym, parking, and a concierge.

*Italic* = LOCKED. **Bold** = LIVE slots. The prose between them is authored once and pinned. Only the slots refresh.

---

## 4. Page structure specification

DOM order. Every section is server-rendered unless marked ISLAND.

### A. Document head

| Element | Layer | Contract |
|---|---|---|
| URL | LOCKED | `/property/{state}/{city}/{slug}/{listing-key}` — one canonical URL per property, for the life of the property. If the property renames, keep the URL and change the H1. |
| `<title>` | LOCKED | Pattern: `{Property} – {City}, {State} · brightplace`. **Never inject live data into the title.** |
| `<link rel="canonical">` | LOCKED | Self-referencing on production. |
| `<meta name="robots">` | LOCKED | `index, follow` on production only. |
| `<meta name="description">` | STABLE | May include a price range; regenerate on the stable cadence, not per feed tick. |
| JSON-LD × 3 | LOCKED + LIVE | See §6. |

### B. Above the fold

| Section | Layer | Notes |
|---|---|---|
| Header nav | LOCKED | Carries the internal link graph. Sign-in state is an island. |
| Ask brightplace panel | ISLAND | Lazy-load on click. Every question it can answer must already be answered in the HTML below. |
| Breadcrumb | LOCKED | Must mirror `BreadcrumbList` schema. |
| `<h1>` | LOCKED | Exactly one. Matches entity name in schema and internal links. |
| Address line | LOCKED | Byte-identical everywhere it appears — page, schema, hub pages. |
| Stat bar (rent / beds / baths / sq ft) | LIVE | All four derive from *currently available* units, so bed/bath/sq-ft ranges move with inventory. Not property attributes — a view of the feed. |
| Lead answer paragraph | STABLE frame + LIVE slots | See §3.1. |

### C. The FAQ spine

Twelve H2 sections, in this order. **The heading text is a locked constant.** The body layer varies.

| # | H2 (pinned) | Body layer | Notes |
|---|---|---|---|
| 1 | What floor plans are available at {property}? | LIVE | Floor-plan cards + per-unit tables (unit, price, sq ft, availability). Filter tabs are an island over fully-rendered content. |
| 2 | What are the fees and lease terms at {property}? | LIVE | Deposit, lease term, move-in special, monthly fees, due-at-signing. High-value AEO surface — competitors rarely put this in HTML. |
| 3 | What amenities does {property} have? | STABLE | Building facts. Changes when the building changes. |
| 4 | What do the amenities at {property} look like? | STABLE + ISLAND | Photos, captions and alt text are server content. Lightbox is the island. |
| 5 | Where is {property}? | LOCKED + ISLAND | Address text and coordinates in HTML. Map tiles and POI toggles lazy-load on viewport entry. |
| 6 | What is the neighborhood around {property} like? | STABLE | Named POIs with walk times. Recompute on POI dataset refresh. |
| 7 | What do residents say about {property}? | LIVE counts + STABLE prose | Regenerate synthesis on a review-count **threshold** (e.g. +10 or +15%), never per crawl. |
| 8 | Is {property} walkable? | STABLE | Third-party scores; pin the frame, swap grades on vendor refresh. |
| 9 | What is {property} like? | STABLE | Operator feed copy — see §7 duplicate-content note. |
| 10 | How big is {property}? | STABLE | Unit count, floors, year built, building type. |
| 11 | What schools are near {property}? | STABLE | Refresh on annual ratings release. |
| 12 | How do I contact {property}? | LOCKED + ISLAND | Manager, phone, website in HTML. Tour scheduling and lead forms are islands. |

### D. Chrome

Footer link graph is LOCKED. Favourites, personalization and auth are islands that hydrate after load.

---

## 5. Island contract

Every island must satisfy all four:

1. All content it touches is already in the server-rendered HTML
2. It is code-split out of the initial bundle (`next/dynamic`)
3. It does not alter the cached HTML for other viewers
4. Removing it entirely leaves a complete, readable page

| Island | Load trigger | Content precondition |
|---|---|---|
| Ask brightplace chat | On click | Every answerable question answered in HTML |
| Map + POI toggles | Viewport entry | Address + coordinates in HTML and schema |
| Photo lightbox | On click | First image is a real `<img>` with width/height |
| Floor-plan filter tabs | Hydration | **All** units rendered server-side; JS filters only |
| "Show all" / "Show more" expanders | Hydration | Full content in DOM **once**, collapsed with CSS line-clamp — never emitted twice |
| Tour / lead forms | On click | Phone and contact info in HTML |
| Favourites / auth | Hydration | No effect on server HTML |

**First-load JS budget: ≤ 160 KB.** Verify the chat widget is a lazy chunk, not part of `main`.

---

## 6. Structured data contract

Three schemas, generated **in the same server render as the DOM, from the same values**.

| Schema | Locked fields | Live fields |
|---|---|---|
| `ApartmentComplex` | `@id`, `@type`, `name`, `address`, `geo` | `offers.price`, `offers.availability`, `numberOfAvailableAccommodation` |
| `BreadcrumbList` | all | — |
| `FAQPage` | `Question.name` (the pinned H2 text) | `Answer.text` follows the section's body layer |

Rules:
- Schema price must equal visible price. A mismatch is a structured-data error and a citation-trust hit.
- Add **`dateModified`** to `ApartmentComplex` — currently missing. The "Prices checked" stamp is visible text only; make it machine-readable.
- At zero inventory, emit `offers` with `availability: OutOfStock`. Do not drop the offer node.

---

## 7. Content sourcing

**The operator's feed description is duplicate content across the web.** The identical text sits on the operator's own site and every competing aggregator. It is the one block on the page that differentiates us negatively.

The differentiator is the agent-written layer, and it must be present on every page:
- neighborhood and commute context specific to the address
- computed comparisons (e.g. "$340/mo below the 2BR median in West Village")
- question-format answers with real specifics
- transit / school / POI synthesis in prose, not only tables

This layer is STABLE. It is regenerated on cadence or material trigger, versioned, and diff-gated.

---

## 8. Zero-inventory behaviour

**This is the most important test in this document.** The real risk at scale is not that content changes — it is that a page collapses when the feed empties. Pages oscillating between substantial and thin is a site-level quality signal, and it is invisible in every dashboard we currently have.

### What must survive

| Disappears (inventory-dependent LIVE) | Survives |
|---|---|
| Floor-plan cards and unit tables | All 12 question headings, unchanged |
| Rent range, per-unit prices, sq-ft range | Amenities, photos, building description |
| Availability dates | Neighborhood, POIs, walk/transit/bike grades |
| Deposit, fees, move-in special | Schools, manager, address, all three schemas |
| Live numbers in the answer paragraph | Reviews, ratings and synthesis — LIVE, but independent of inventory |

### The test

1. Render with the feed mocked to **zero available units**
2. Strip `<script>` tags and count rendered text — must clear **800 words**
3. Assert **all 12 H2 headings still render**, word for word — none suppressed for an empty answer
4. Assert **all three schemas still emit**, with offers marked out of stock rather than dropped
5. Run across a **random sample of production properties** — thin-state collapse shows up on small properties first

> Measured with inventory: **1,668 words**. Evergreen remainder at zero inventory: **not yet measured — run the test.**

### Lifecycle policy

| Situation | Policy |
|---|---|
| **Property page, zero inventory** | Stay indexed. Keep every evergreen section. State plainly that no units are available, offer a waitlist, surface nearby properties. **Never noindex** — you would discard accumulated equity on a page that relists in weeks. |
| **Facet page, below threshold** | Opposite rule. Below ~10 listings, `noindex, follow`. A facet is a result set, not an entity. |
| **Entity permanently gone** | `410` only when the entity itself is gone — demolished, converted, permanently off market. Delisting is not the same as ceasing to exist. |

---

## 9. Validation gates

At thousands of pages nobody reviews a page. The layer model only holds if it is a build gate plus a scheduled crawl.

Run against a rendered property page with `<script>` stripped — what a non-JS crawler sees. Run again with inventory mocked to zero.

| # | Gate | Severity |
|---|---|---|
| 1 | No-JS rendered text ≥ 800 words — with and without inventory | **Block** |
| 2 | Exactly one `<h1>`, no heading-level skips | **Block** |
| 3 | All three schemas emit | **Block** |
| 4 | Price and availability in the DOM, not only in the hydration payload | **Block** |
| 5 | Schema price equals visible price, same render | **Block** |
| 6 | Every H2 in the pinned heading set present, word for word | **Block** |
| 7 | Freshness stamp present and within 7 days; `dateModified` in schema | Warn |
| 8 | No question heading with an empty or placeholder answer | **Block** |
| 9 | Images carry `width`/`height`; first-load JS under budget | Warn |

Blocking gates run in CI on every deploy against a fixed sample, and on a scheduled crawl across a random production sample.

---

## 10. Open defects on the current page

Found while auditing the staging render of `equity-b2662` on 2026-09-09.

| # | Defect | Fix |
|---|---|---|
| 1 | **Staging is indexable.** `app-staging.brightplace.ai/robots.txt` is byte-identical to production (`Allow: /` for `*`, GPTBot, OAI-SearchBot). The page serves `index, follow` with a production canonical. Canonical does not stop AI crawlers ingesting staging, and staging pricing will drift from production. | Env-gate `Disallow: /` on non-production hosts; add `X-Robots-Tag: noindex` at the edge for those hostnames. |
| 2 | **Section 10 renders an unanswered question.** Output is `"600 Washington Apartments is a apartment. Building: Apartment"` — no content plus a grammar break. A question heading with an empty answer is a thin-content signal on an otherwise authoritative page. | Populate with unit count, floors, year built, building type. **The heading stays either way — it is LOCKED (rule 2, gate 6).** Fix the answer; never delete the question. |
| 3 | **The property description is emitted twice** in the DOM — collapsed preview plus the full "Show more" copy. Doubles duplicate feed text for crawlers. | Render once; collapse with CSS line-clamp. |
| 4 | **`dateModified` missing** from `ApartmentComplex`. Freshness is visible text only. | Add it, sourced from the same value as the "Prices checked" stamp. |

---

## 11. Definition of done — new property page template

- [ ] Renders complete content with JS disabled (`curl` + strip scripts)
- [ ] All 12 H2 headings from the pinned constant, in order
- [ ] Three schemas, generated in the same render as the DOM
- [ ] Every LIVE value carries a visible date stamp and a schema `dateModified`
- [ ] Zero-inventory render clears 800 words and keeps all headings and schemas
- [ ] Every island lazy-loaded, and removable without losing content
- [ ] First-load JS ≤ 160 KB
- [ ] Revalidation wired to feed events, not a timer
- [ ] `lastmod` bumps only on material change
- [ ] Non-production hosts noindexed
- [ ] Gates 1–6 wired into CI
