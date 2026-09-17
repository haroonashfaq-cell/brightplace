# brightplace.ai — Webflow → Vercel Migration
## Developer Handover Guide

**Version 1 · 2026-09-17**

All facts below were verified by live probing of `www.brightplace.ai`,
`brightplace-ai.webflow.io`, `app.brightplace.ai` and the Webflow Data API on 2026-09-17.
Re-verify before cutover if significant time has passed.

---

## 1. What we are doing

The marketing site at `www.brightplace.ai` currently runs on Webflow. The product app runs on
Vercel at `app.brightplace.ai`. We are consolidating: **the Vercel app becomes the whole site at
`www.brightplace.ai`**, and Webflow is retired.

Concretely, after the migration:

| URL | Served by | Today |
|---|---|---|
| `www.brightplace.ai/` | **The Vercel app's homepage** | Webflow homepage (gets replaced) |
| `www.brightplace.ai/property/...` | Vercel app | `app.brightplace.ai/property/...` |
| `www.brightplace.ai/guides/...` | Vercel app (new routes) | Webflow |
| `www.brightplace.ai/resources/...` | Vercel app (new routes) | Webflow |
| `www.brightplace.ai/news/...`, `/communities/...`, `/operators/...`, `/stories/...`, `/category/...` | Vercel app (new routes) | Webflow |
| Legal + static pages | Vercel app (new routes) | Webflow |
| `app.brightplace.ai/*` | **301 → `www.brightplace.ai/*`** | Vercel app |

The Webflow homepage is **not** being ported. The app's existing homepage becomes the site
homepage.

---

## 2. This is two migrations, and they carry very different risk

Please internalise this before planning the work — it drives the whole sequencing.

| Migration | URLs | What changes | SEO risk |
|---|---|---|---|
| **A.** Webflow content → Vercel | 148 | Origin only. Paths stay **byte-identical** on `www.brightplace.ai` | **Low.** Google sees the same URLs, better markup |
| **B.** `app.brightplace.ai` → `www.brightplace.ai` | **22,774** | The hostname changes on every single URL | **High.** Google must re-attribute 22,774 URLs to a different host |

Migration B is 99% of the URLs and is the real traffic exposure. It is entirely doable — this is a
standard, well-understood subdomain-to-root consolidation, and it usually ends with *more* organic
traffic because authority consolidates onto one host. But it must be done with correct 301s and
Search Console handling, and there is normally a 4–12 week settling period with a visible dip
before recovery.

**Do not run A and B in the same change window.** If traffic moves, you need to know which
migration caused it.

---

## 3. Current state — verified facts

### 3.1 DNS

| Host | Record | Value | Notes |
|---|---|---|---|
| `www.brightplace.ai` | CNAME | `cdn.webflow.com` | Webflow CDN. The Cloudflare seen in response headers is Webflow's own, not a customer account in the path |
| `brightplace.ai` (apex) | A | `198.202.211.1` | 301s to `www`, **preserving the path** |
| `app.brightplace.ai` | CNAME | `…vercel-dns-017.com` | The Vercel app |
| `operator.brightplace.ai` | — | Vercel | Separate property, out of scope |

Registrar DNS is **Namecheap BasicDNS** (`dns1/dns2.registrar-servers.com`). There is **no ALIAS/
ANAME support at the apex**, so the apex must stay an A record (Vercel: `76.76.21.21`). MX is
Google — do not touch it.

### 3.2 URL conventions that must be preserved exactly

- **No trailing slashes.** `/guides/` → 301 → `/guides`. This matches Next.js default
  `trailingSlash: false`. Do not change it.
- **Apex → www 301, path preserved.**
- **Unknown paths return a real 404** (not a soft 200).
- `robots.txt` today is:
  ```
  User-agent: *
  Allow: /
  Disallow: /*?*_page=
  Sitemap: https://www.brightplace.ai/sitemap.xml
  ```
  (The `Sitemap:` line is duplicated in the live file — fix that.)

### 3.3 Existing SEO debt the rebuild fixes for free

Verified on a live guide page (`/guides/dallas-families`):

- **Zero `application/ld+json` blocks in the server HTML.** All schema is JS-injected, so crawlers
  never see it.
- **No `<link rel="canonical">` anywhere.**
- **No `og:url`, no `og:title`, no `og:description`, no `og:image`.** Only `og:type="website"`.
- No `datePublished` / `dateModified`.
- Every page loads jQuery 3.5.1 plus four Webflow runtime chunks.

Server-rendered Next.js fixes all of this. Treat these as **requirements** for the new pages, not
nice-to-haves — they are a large part of why the migration is worth doing.

---

## 4. Part A — Getting the content out of Webflow

### 4.1 Do not scrape the live site, and do not use the files in this repo

There is a partial content export in `brightplace intelligence/Webflow CMS Data/` (57 `.json` +
71 `.html`). **It is incomplete** — a slug-by-slug diff against the live sitemap shows many live
URLs missing, and ~21 of the JSON files are metadata-only with the body in a sibling `.html`.
Do not use it as the migration payload.

Use the **Webflow Data API v2**. You will need a Site API token with read access.

```
Site ID:      69d6907887b739e09622100f
Workspace ID: 69d67b4d0c38f8dc963472f3
```

```
GET https://api.webflow.com/v2/sites/{site_id}/collections
GET https://api.webflow.com/v2/collections/{collection_id}
GET https://api.webflow.com/v2/collections/{collection_id}/items?limit=100&offset=…
GET https://api.webflow.com/v2/sites/{site_id}/assets
Authorization: Bearer <token>
```

Cache every raw API response to disk before transforming anything. That cache is the audit trail
and lets you re-run the transform without re-hitting the API.

### 4.2 The collections

10 collections, 158 staged items total.

| Collection | ID | Items | Item URL | Has index page? | In sitemap? |
|---|---|---|---|---|---|
| Guides | `69dccfeabed64ec697c4f7d2` | 31 | `/guides/<slug>` | yes | yes |
| Resources | `69fcfcef26d35b66ba874f9d` | 86 | `/resources/<slug>` | yes | yes (76 live) |
| News | `6a32f0722779d53e287b5cc5` | 10 | `/news/<slug>` | yes | yes (9 live) |
| Categories | `69df6e40b18552d426ddd816` | 7 | `/category/<slug>` *(singular)* | no | yes |
| Authors | `69dcd5b9150dec1c53e3e8de` | 3 | `/author/<slug>` *(singular)* | no | **no** |
| Operators | `6a86c25e5afcc88ca23b88b5` | 1 | `/operators/<slug>` | yes | yes |
| Communities | `6a86c25fa4cc0c8821ee0f1f` | 6 | `/communities/<slug>` | yes | yes |
| Stories | `6a86c25fa4cc0c8821ee0fe2` | 3 | `/stories/<slug>` | no | yes |
| Floor Plans | `6a872c94c6f57eb37e79d98a` | 7 | `/floor-plans/<slug>` | no | **no** |
| Nearby Places | `6a87460cc934a52e6d181864` | 4 | `/nearby-places/<slug>` | no | **no** |

Note `/category/` and `/author/` are **singular** in the URL while the collections are plural.
Easy thing to get wrong.

**Staged counts exceed live URLs** (Resources 86 vs 76 live, News 10 vs 9). The difference is
drafts and archived items. **Filter on `isDraft` and `isArchived`** — do not assume parity.

### 4.3 Field schemas

**Guides, Resources and News are field-identical** — same 13 field slugs, same types, same
required flags. Only the internal field IDs differ. One content type covers all three:

| Slug | Type | Required |
|---|---|---|
| `name` | PlainText (max 256) | **yes** |
| `slug` | PlainText (max 256) | **yes** |
| `post-body` | RichText | no |
| `post-summary` | PlainText (multiline) | no |
| `main-image` | Image | no |
| `thumbnail-image` | Image | no |
| `featured` | Switch | no |
| `color` | Color | no |
| `author-2` | Reference → Authors | no |
| `category-2` | Reference → Categories | no |
| `seo-title` | PlainText | no |
| `meta-description` | PlainText | no |
| `focus-keyword` | PlainText | no |

The other collections are **not** the same shape and need their own types:

- **Communities** — 27 fields. Includes `faq` (RichText, H3 per question, feeds FAQPage schema),
  `related-guides` (MultiReference → Guides), `photo-gallery` (MultiImage, 4–10),
  `last-verified` (DateTime), plus city/state/address/pricing/amenity fields.
- **Operators** — 15 fields. `partner-status` is an Option (Featured / Standard / Archived).
- **Stories** — 13 fields. `community` (Reference → Communities, required) and `story-type`
  (Option, 5 values).
- **Floor Plans** and **Nearby Places** are one-to-many **child records of Communities** — they
  render inside community pages. Model them as nested data, not as content types. Their
  standalone routes are Webflow auto-created and almost certainly unlinked (see §6.4).

**Three traps in the field mapping:**

1. In Authors, the field slug is `facebook-profile-link` but its **label is "Instagram Profile
   Link"**. Mapping by slug wires the wrong social network. Map by label, and eyeball the values.
2. The author reference slug is `author-2` in Guides/Resources/News but plain **`author` in
   Stories**. There is no shared convention — read the schema per collection.
3. **Required-field asymmetry.** Guides/Resources/News require only `name` + `slug`, so bulk
   import succeeds but data will be sparse. Stories/Communities/Operators require most of their
   fields — those imports fail without backfill.

### 4.4 Capture the dates — this is one-way

Per item, persist `createdOn`, `lastPublished` and `lastUpdated` from the API response, plus any
date field on the item.

```
datePublished = <item date field> ?? createdOn
dateModified  = lastUpdated ?? lastPublished ?? datePublished
```

**These values exist only inside Webflow.** If the export misses them, `datePublished` and
`dateModified` can never be reconstructed after Webflow is cancelled. This is an export
requirement, not a rendering one.

### 4.5 Import order

References must resolve, so import in dependency order:

```
Authors + Categories  (no dependencies)
  → Operators
  → Communities       (references Operators and Guides)
  → Guides / Resources / News
  → Stories           (requires Communities)
  → Floor Plans + Nearby Places  (nested into Communities)
```

### 4.6 Assets — must be rehosted

Images are served from `cdn.prod.website-files.com`. That CDN keeps working after the DNS switch
**and** after the custom domains are removed from Webflow. It stops at **account cancellation or
downgrade**.

So: rehosting does not block cutover, but it **absolutely blocks cancelling Webflow**. If you skip
it, every image on the site 404s the day the plan lapses.

1. Extract every `cdn.prod.website-files.com` / `cdn.webflow.com` / `uploads-ssl.webflow.com` URL
   from image fields **and from inside `post-body` HTML**.
2. Download, hash-name, store in your own asset pipeline (Vercel Blob, S3, or `public/`).
3. Rewrite the references in the body HTML.
4. Also sweep `GET /sites/{id}/assets` for anything not referenced in a body.
5. **Make it a build failure if any `webflow.com` or `website-files.com` string survives in the
   content directory.** A checklist will not catch this; a failing build will.

### 4.7 Body HTML — import verbatim, clean up later

The existing article bodies contain Webflow-specific workarounds. Most notably, lists were written
as `<p><strong>Label:</strong> …</p>` because **Webflow's rich text editor strips `<ul><li>`**.

**Import this verbatim. Do not "improve" it during migration.** A zero-diff content cutover keeps
the blast radius confined to rendering. Restoring real list markup is a separate, reviewed pass
after the migration is stable.

---

## 5. Part B — Rebuilding in the Vercel app

### 5.1 Routes to create

The app currently serves **only** `/property/*`. Everything below is new. Every one of these 404s
on `app.brightplace.ai` today — verified.

```
/                          ← the app's existing homepage (no work; it becomes the site homepage)
/guides                    listing
/guides/[slug]             31 items
/resources                 listing
/resources/[slug]          76 items
/news                      listing
/news/[slug]               9 items
/communities               listing
/communities/[slug]        6 items
/operators                 listing
/operators/[slug]          1 item
/stories/[slug]            3 items   (no listing page today)
/category/[slug]           7 items   (no listing page today)
/property-managers
/contact-us
/privacy
/terms
/fair-housing
/financial-disclosure
/llm-info
/community-voice-survey
/search                    ← see §8, needs a decision
```

### 5.2 Rendering requirements (non-negotiable)

These fix the debt in §3.3. All of it must be **server-rendered** — JS injection is exactly what
is broken today.

- **JSON-LD in the server HTML**: Article (with `datePublished`, `dateModified`, `author`,
  `publisher`), BreadcrumbList, FAQPage where FAQs exist, WebPage with `speakable`.
- **Self-referencing canonical on every route**, including listings and `/category/*`. Absolute
  `https://www.brightplace.ai/...`.
- **Real Open Graph tags** — `og:title`, `og:description`, `og:image`, `og:url`, and
  `article:published_time` / `article:modified_time` on articles.
- **Visible `<time dateTime>`** in the article header or footer.
- **`sitemap.ts` and `robots.ts` generated from the content source** — do not hand-maintain a file
  with 148+ URLs in it.
- Ship a real `llms.txt`. Webflow has none today (`/llm-info` is a human page, not a machine file).

Config notes:
- Keep `trailingSlash: false` (the default) — it matches Webflow's current behaviour exactly.
- **Do not** set `output: 'export'` — it would remove the ability to run the contact form handler.
- **Do not** copy `images: { unoptimized: true }` from the `operator-pages` project. That flag
  exists there for static export. On an image-heavy content site it throws away `next/image`
  optimisation, which is one of the main performance wins of leaving Webflow.

### 5.3 Design

The Webflow site is a **BRIX template**. The homepage is being replaced by the app's homepage, so
that design does not need porting. What **does** need building in the app's existing design system:

- listing/index pages (6)
- the article template
- the static/legal page template
- nav and footer that work across both the product surface and the content surface

Page weights today, as a rough guide to what is there: `/resources` **315KB** (renders all 77
items, no pagination), `/` 60KB, `/guides` 51KB, `/news` 33KB, `/property-managers` 31KB,
`/communities` 19KB, `/operators` 15KB.

Ship `/resources` **at parity first** — all items, no pagination. Adding pagination during the
migration would mint URLs that never existed. Optimise it afterwards.

### 5.4 Forms — this breaks silently, so handle it explicitly

- **`/contact-us` uses a native Webflow form** (`wf-form-BRIX---Contact-V2`). Submissions go to
  Webflow's backend. After cutover the page still renders and the form still *appears* to submit —
  the data simply goes nowhere, with no error. It needs a real endpoint: validation, honeypot,
  rate limiting, delivery to a monitored inbox, **and** persistence so nothing is fire-and-forget.
  Run the old and new forms in parallel for ~2 weeks and compare receipt counts before switching
  off.
- **`/community-voice-survey` posts to `formsubmit.co`** — external, unaffected. Port the markup
  unchanged, no backend work.

### 5.5 Content publishing after migration

brightplace publishes content through internal tooling that currently writes to Webflow via API.
After migration it needs an equivalent programmatic path into the new site. What the dev team
needs to provide is a **contract**, not the tooling:

- a documented, versioned content schema (the types in §4.3)
- a programmatic way to create/update a content item and get a preview URL before it goes live
- a draft state, so content can land without publishing
- deterministic slug → URL mapping, and **a redirect mechanism if a slug ever changes**

That last point matters: content slugs must either be immutable, or slug changes must
automatically create a 301. A mutable slug with no redirect layer silently destroys a live URL.

---

## 6. Part C — URLs and redirects

This is the part that determines whether traffic survives. Three separate jobs.

### 6.1 Job 1 — The 148 Webflow URLs (paths do not change)

Nothing to redirect. These paths stay identical on `www.brightplace.ai`; only the origin changes.
The work is making sure the new routes answer on exactly the same paths, with the same status
codes and the same trailing-slash behaviour.

### 6.2 Job 2 — Extract Webflow's existing 301 table **before** cutover

Webflow site settings holds redirect rules accumulated over the life of the site. They carry real
link equity from historical URLs, and **they vanish the moment the domain moves.**

The Webflow Data API does **not** expose redirects. Extract them manually:

> Webflow → Site Settings → Publishing → 301 Redirects. Open browser devtools → Network → filter
> XHR → read the JSON response backing the table. **Copy the JSON.** Do not hand-transcribe a
> paginated UI — you will miss rows.

Cross-check the result against Search Console's "Page with redirect" report. Commit the extracted
rules to the repo and port every one of them into the new app's redirect config as `permanent`
(301).

### 6.3 Job 3 — The 22,774 `app.brightplace.ai` → `www.brightplace.ai` redirects

This is the high-risk migration. Requirements:

1. **301, not 302.** Permanent, or the equity does not transfer.
2. **One hop.** `app.brightplace.ai/property/x` → `www.brightplace.ai/property/x` directly. No
   chains through intermediate redirects, and no redirect to the homepage — **every URL must
   redirect to its own exact equivalent.** Bulk-redirecting to `/` is the single most common way
   this kind of migration destroys traffic.
3. **Path preserved byte-for-byte**, including the full
   `/property/<state>/<city>/<name>/<id>` structure.
4. `app.brightplace.ai` must keep answering — and keep 301ing — **indefinitely**, or at minimum
   for 12 months. Do not decommission the hostname.
5. Update `robots.txt` and the sitemap so `www` is the only host advertising these URLs. The
   `app.brightplace.ai` sitemap should stop listing them once the redirect is live.
6. Every internal link, canonical tag and structured-data URL in the app must be updated to `www`.
   Leaving canonicals pointing at `app` will actively fight the migration.

**Search Console:**
- `www.brightplace.ai` and `app.brightplace.ai` are separate properties. Both must stay verified.
- Use the **Change of Address** tool in the `app.brightplace.ai` property, pointing to
  `www.brightplace.ai`. This tool *does* apply here — it is a genuine host change.
  (It does **not** apply to the Webflow migration in §6.1, where the host is unchanged.)
- Submit the new `www` sitemap containing all 22,774 + 148 URLs.

### 6.4 Decide these deliberately, do not discover them later

- **`/knowledgebase/*` returns 404 today** — verified. Do **not** invent a
  `/knowledgebase/*` → `/resources/*` redirect. That would be new behaviour, not parity. Preserve
  the 404.
- **`/author/<slug>`** — 3 live routes, not in the sitemap. Reproduce or drop?
- **`/floor-plans/<slug>` and `/nearby-places/<slug>`** — 11 live routes, Webflow auto-created,
  almost certainly unlinked and with no inbound traffic. Reproduce, or return 410?
- The `Disallow: /*?*_page=` rule exists because Webflow paginates with a `_page` query param.
  Keep the rule until `/resources` is rendered by the new app with self-canonicals, then drop it.

---

## 7. Cutover sequence

### Phase 0 — Baseline and gates (blocking)

| # | Action | Why |
|---|---|---|
| 0.1 | **Export Search Console data for both properties, 16-month window, before anything changes.** Per-URL clicks/impressions/CTR/position; Queries; the Links report; "Page with redirect" and "Not indexed" | It is a rolling window. Once it passes you cannot get it back, and without it you cannot tell migration damage from seasonality |
| 0.2 | Export GA4 landing-page data, same period, monthly granularity | Seasonality control |
| 0.3 | Extract the Webflow 301 table (§6.2) | Vanishes at cutover |
| 0.4 | Add `www.brightplace.ai` + `brightplace.ai` to the Vercel project; complete domain verification and cert issuance **with no DNS change** | `app` sits in a Vercel scope already; if the domain is claimed by another team account this blocks and needs a transfer. Find out now, not during the window |
| 0.5 | Build the parity harness (§9) and run it against the current live site | This is the baseline every later check diffs against |
| 0.6 | Lower DNS TTLs to 60s on `www` and apex, **values unchanged**, and wait 48h | Makes rollback fast. Must be done ≥48h ahead |

### Phase 1 — Build and verify on a preview

Build the new routes, import the content, run the parity harness against a Vercel preview with a
host override. Nothing public changes. Gate: content parity is 148/148 before anything ships.

### Phase 2 — Migration A: Webflow content

Point `www.brightplace.ai` at the Vercel project. Paths do not change.

**Incremental option (recommended).** This was verified as safe:
`https://brightplace-ai.webflow.io` stays live after the custom domain moves, serves
**byte-identical HTML** (48,629 vs 48,622 bytes — the entire difference is one attribute value),
and its internal links are **relative**. So you can point `www` at Vercel on day one and proxy
not-yet-built sections back to Webflow via Next.js rewrites, then migrate section by section with
a ~60-second rollback at each step.

**Two traps if you do this — both verified, both will bite:**

1. **A catch-all rewrite will deindex the entire site.** `brightplace-ai.webflow.io/robots.txt` is
   `User-agent: * / Disallow: /`. A rewrite declared in `beforeFiles` proxies `/robots.txt` from
   the staging host and serves *that* from `www.brightplace.ai`. Use `rewrites().fallback`, which
   runs only after Next's own routes and static files miss — and ship `robots.ts`, `sitemap.ts`
   and `llms.txt` from day one so those paths can never fall through.

2. **Proxied pages render a "Made in Webflow" badge.** The Webflow runtime force-shows it when the
   serving host does not match the page's `data-wf-domain`. Fix before the flip: add
   `<style>.w-webflow-badge{display:none!important}</style>` in Webflow → Site Settings → Custom
   Code → Head, and publish to **both** the custom domains and the `.webflow.io` subdomain.

**One more, easy to miss:** Webflow emits **absolute** redirect `Location` headers. On the staging
origin those carry the staging hostname:

```
brightplace-ai.webflow.io/guides/  →  301  location: https://brightplace-ai.webflow.io/guides
```

So any 301 missed in the §6.2 extraction will fall through to the proxy and bounce a real user
onto the `Disallow: /` staging host. Add a harness assertion: **no response `Location` header may
ever contain `webflow.io`.**

**And a mechanical constraint:** `rewrites().fallback` runs only after Next's own routes miss. The
moment `app/guides/[slug]/page.tsx` exists it wins for *all* of `/guides/*`, so that prefix can no
longer fall through. If the collection is only partly imported, missing slugs return **404 instead
of falling back to Webflow**. **Migrate each collection atomically** — every non-draft item
present, verified, before its route ships.

Hold and monitor. Do not start Phase 3 until this is stable.

### Phase 3 — Migration B: the hostname swap

Separate change window, after Phase 2 has settled.

1. Deploy the 301s from `app.brightplace.ai/*` → `www.brightplace.ai/*` (§6.3).
2. Update all internal links, canonicals and structured-data URLs to `www`.
3. Submit Change of Address in Search Console.
4. Submit the combined sitemap.
5. Keep `app.brightplace.ai` alive and redirecting indefinitely.

### Phase 4 — Retire Webflow

Only when **all** of these are true: no path is still being proxied; a full crawl finds zero
`website-files.com` references; Search Console shows the URLs indexed on Vercel-served responses
for 30 consecutive days; the extracted 301s are live and verified; contact form submissions have
been landing in the new handler for 30 days; and a full Webflow site export is archived.

Then remove the custom domains and downgrade. Keep the Webflow plan read-only for 30 more days
before cancelling — cancellation is the one step with no rollback.

---

## 8. Rollback

| Tier | Action | Time |
|---|---|---|
| 1 | Redeploy with the affected prefix returned to the Webflow fallback, or Vercel instant-rollback to the previous deployment | ~60s, no DNS propagation |
| 2 | Revert DNS: `www` CNAME → `cdn.webflow.com`, apex A → `198.202.211.1` | Bounded by the 60s TTL from Phase 0.6 |

**Leave both domains configured as custom domains inside Webflow** through the whole migration.
They cost nothing and they are what makes Tier 2 possible.

---

## 9. Verification

Build **one parity harness** and run it before the flip, after the flip, and after every phase.
It should cover the 148 sitemap URLs, the ~14 live-but-unlisted routes, and every redirect source
from §6.2, recording per URL:

- HTTP status
- final URL after following redirects
- redirect hop count
- `<title>` and `<h1>`
- canonical and `meta[robots]`
- a normalised text hash of the body

Every phase's acceptance criterion is then: **the diff against baseline is empty except for the
section intentionally migrated**, and within that section only the *text hash* may change —
status, final URL and hop count must be identical.

Explicit assertions to include:

- `trailingSlash: false` — `/guides/` → 301 → `/guides`
- apex → `www` 301 **preserving the path**
- unknown path → real 404, not a soft 200
- `/resources?x_page=2` → 200
- **no `Location` header anywhere contains `webflow.io`**
- after Phase 3: every `app.brightplace.ai` URL → exactly one 301 → the same path on `www`

Plus:

- **Schema:** Google Rich Results Test on one URL per collection. Article, FAQPage and
  BreadcrumbList must be detected in the **server** HTML. Today zero JSON-LD blocks ship, so this
  is a genuine regression check on the new work, not a formality.
- **Asset sweep:** zero `website-files.com` / `webflow.com` strings in the content directory,
  enforced as a build failure.
- **Forms:** parallel-run receipts match for ~2 weeks.

### Monitoring after each migration

Daily for 14 days, then weekly through day 90. Compare **month-over-month against the same month
last year** — never week-over-week.

**Roll back automatically on (deterministic, HTTP-level):**
- any 5xx on a migrated path
- any URL that returned 200 in the baseline now returning non-200
- a redirect chain where the baseline had none, or hop count increasing
- `/robots.txt` differing from the intended file by one byte

**Investigate, but do not auto-roll-back (ranking signals are noisy and lag):**
- clicks on a migrated section down >20% vs. the same period last year, sustained 14 days
- down >35% sustained 14 days → roll that section back while diagnosing
- average position drifting >3 places on head terms for 14 days
- "Crawled — currently not indexed" rising in Coverage

A 10–15% dip in weeks 1–3 that recovers is normal settling, especially for Migration B. Expect it,
and do not panic-roll-back on week 1 data.

---

## 10. Decisions needed before work starts

1. **`/search`** — Webflow-native site search, currently in the sitemap, no equivalent in the app.
   Rebuild, ship a 200 empty state, or drop from the sitemap and redirect?
2. **`/author/<slug>`** (3 routes) — reproduce or drop?
3. **`/floor-plans/<slug>` and `/nearby-places/<slug>`** (11 unlinked routes) — reproduce or 410?
4. **Contact form destination** — which inbox/CRM, and where do submissions persist?
5. **Content publishing contract** (§5.5) — who owns it, and what is the interface?
6. **Timing between Phase 2 and Phase 3** — recommend at least 2–4 weeks of stability before the
   hostname swap.
7. **Do the Webflow homepage's marketing sections need to survive** anywhere, or is the app
   homepage a complete replacement? This is currently assumed to be a complete replacement.
