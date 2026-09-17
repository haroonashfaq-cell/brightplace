# brightplace.ai → Vercel Consolidation — Migration Plan

**Version 2 · 2026-09-17** · supersedes `migration-plan-v1.md`

Companion document: **`DEVELOPER-HANDOVER.md`** — the dev-facing build guide.
This file is the internal plan: architecture, decisions, content-pipeline impact, sequencing.

> **What changed from v1.** v1 assumed the Webflow site would be rebuilt as a separate new Next.js
> repo, with the Webflow homepage ported and `app.brightplace.ai` untouched. The actual plan is
> that **`app.brightplace.ai` becomes `www.brightplace.ai`** — the app's homepage becomes the site
> homepage, Webflow content is rebuilt inside the existing app, and 22,774 `/property/*` URLs
> change hostname. All verified facts from v1 carry over; the architecture, phasing and
> content-store decision do not.

---

## 1. Goal and end state

Consolidate everything onto one Vercel application at one hostname, and retire Webflow.

| URL | After | Today |
|---|---|---|
| `www.brightplace.ai/` | Vercel app homepage | Webflow homepage — **replaced, not ported** |
| `www.brightplace.ai/property/...` | Vercel app | `app.brightplace.ai/property/...` |
| `www.brightplace.ai/guides/...`, `/resources/...`, `/news/...`, `/communities/...`, `/operators/...`, `/stories/...`, `/category/...` | Vercel app, new routes | Webflow |
| Legal + static pages | Vercel app, new routes | Webflow |
| `app.brightplace.ai/*` | **301 → `www.brightplace.ai/*`**, kept alive indefinitely | Vercel app |

Two constraints, in priority order:

1. **Do not lose organic traffic.**
2. **The content pipeline must keep publishing** without depending on an app deploy cycle.

---

## 2. This is two migrations with asymmetric risk

| | URLs | What changes | Risk | Google's view |
|---|---|---|---|---|
| **A.** Webflow content → Vercel | 148 | Origin only; paths byte-identical | **Low** | Same URLs, better markup |
| **B.** `app.` → `www.` | **22,774** | Hostname on every URL | **High** | A site move |

Migration B is 99% of the URL surface and carries essentially all the risk. It is a standard
subdomain→root consolidation and typically *nets positive* — authority stops being split across
two hosts — but it involves a 4–12 week settling period with a visible dip.

**Hard rule: A and B ship in separate change windows, at least 2–4 weeks apart.** Combined, a
traffic movement is undiagnosable and the rollback decision becomes guesswork.

Consequence worth stating plainly: the original question was "can we move Webflow without losing
traffic," and the answer is yes. But the larger traffic question in this project is B, which the
original framing did not include.

---

## 3. Verified current state

Established by live probing of `www.brightplace.ai`, `brightplace-ai.webflow.io`,
`app.brightplace.ai` and the Webflow Data API on 2026-09-17.

### 3.1 Hosts

| Host | Record | Value |
|---|---|---|
| `www.brightplace.ai` | CNAME | `cdn.webflow.com` (Webflow's CDN; the Cloudflare in headers is Webflow's own) |
| `brightplace.ai` | A | `198.202.211.1` → 301 to `www`, path preserved |
| `app.brightplace.ai` | CNAME | `…vercel-dns-017.com` |
| `operator.brightplace.ai` | — | Vercel, separate property, out of scope |

Registrar DNS is **Namecheap BasicDNS**, no ALIAS at apex → apex stays an A record
(Vercel `76.76.21.21`). MX is Google; untouched.

### 3.2 Conventions to preserve exactly

- No trailing slashes (`/guides/` → 301 → `/guides`) — matches Next.js `trailingSlash: false`.
- Apex → www 301, path preserved.
- Unknown paths → real 404.
- `robots.txt`: `Allow: /`, `Disallow: /*?*_page=`, plus the sitemap line (currently duplicated).

### 3.3 The app today

`app.brightplace.ai` serves **only** `/property/*` — 22,774 sitemap URLs. Verified 404 on
`/guides`, `/resources`, `/news`, `/communities`, `/operators`, `/stories`, `/property-managers`,
`/privacy`, `/terms`, `/search`. Every content route is net-new.

### 3.4 Webflow inventory

10 collections, 158 staged items, 26 pages. Site `69d6907887b739e09622100f`.
Full IDs, field schemas and the three mapping traps are in `DEVELOPER-HANDOVER.md` §4.2–4.3.

Headline points that drive planning:

- **Guides, Resources and News are field-identical** (13 fields) → one content type covers 127 items.
- Communities (27 fields), Operators (15), Stories (13) need their own types.
- Floor Plans (7) and Nearby Places (4) are **child records of Communities**, not content types.
- **14 live routes are not in the sitemap**: `/author/<slug>` (3), `/floor-plans/<slug>` (7),
  `/nearby-places/<slug>` (4). Decide on them deliberately.
- Staged counts exceed live URLs (Resources 86 vs 76) — drafts and archived items.

### 3.5 SEO debt the rebuild clears

Verified on a live guide page:

- **Zero `application/ld+json` blocks in server HTML** — all schema is JS-injected and invisible.
- No `<link rel="canonical">` anywhere.
- No `og:url` / `og:title` / `og:description` / `og:image`; only `og:type="website"`.
- No `datePublished` / `dateModified`.
- jQuery 3.5.1 + four Webflow runtime chunks on every page.

These become **requirements** on the new routes. A meaningful share of the migration's value is here.

---

## 4. The decision v2 has to make: where content lives

v1 recommended git-based content in a new, content-team-owned repo. **The new architecture breaks
that**, because the site is now the dev team's application repo — and `CLAUDE.md` states the dev
team never gets access to the SUPER SEO Agents content system.

So the content store must satisfy four things at once:

1. The agent pipeline can publish programmatically, without an app code deploy.
2. Content is not lossy — Webflow bodies are **HTML**, and must stay HTML.
3. The dev team never needs access to the content-production system.
4. The content team never needs commit access to the product application repo.

### Options

| | Approach | Verdict |
|---|---|---|
| **(a)** | Content files committed into the **app repo** | **Rejected.** Content team needs write access to the product repo, and every article becomes an app deploy. Violates constraints 1 and 4. |
| **(b)** | Extend the **existing brightplace CMS** with a site-scoped tenant | **Viable, but blocked as-is.** That CMS stores `body_markdown` and **has no `body_html`** — importing 148 Webflow rich-text bodies means a lossy HTML→Markdown conversion of exactly the artifact we are migrating for fidelity. It is also community-scoped (`unique(community_id, slug)`), flat `/blog/[slug]`, with no categories and no multi-prefix routing. Redirect, canonical, sitemap and robots tooling are all documented as **requested but not built**. Choosing this means funding those gaps first. |
| **(c)** | A **separate content repository**, consumed by the app at build time | **Recommended.** |

### Recommended: (c) separate content repo

```
brightplace-content/          ← content team owns; agent pipeline writes here
  guides/<slug>/index.json + body.html
  resources/<slug>/…
  news/<slug>/…
  communities/<slug>/…
  categories/<slug>.json
  authors/<slug>.json
  schema/types.ts             ← the contract, versioned
```

The app consumes it at build time (git submodule, a published package, or a build-step fetch), and
a **Vercel Deploy Hook** rebuilds on content merge. Nothing else couples the two teams.

Why this fits:

- **Bodies stay HTML.** No lossy conversion. This is the single strongest argument against (b).
- **Clean boundary.** The dev team consumes a versioned data package and never sees the production
  system. The content team never commits to the product repo. Both `CLAUDE.md` constraints hold.
- **Publishing is independent of app releases.** Content merge → deploy hook → live, with no
  dev-team involvement in the loop.
- **Link validation becomes a build-time assertion.** The repo *is* the URL graph, so every
  internal link can be checked against known paths and CI fails on an unknown one — including a
  permanent deny-list for `/knowledgebase/`. Today `link-registry.md` asks agents to fetch the live
  sitemap and check by hand; that becomes impossible to get wrong.
- **Reversible.** If the CMS route is funded later, the content repo is a clean import source.

**Cost, stated honestly:** publishing changes shape. Today it is a single MCP call. Under (c) it is
write-files → validate → commit → deploy hook. Mitigation is a thin MCP/skill wrapper shaped like
the current publish tool that performs write + validate + commit + preview in one call, preserving
the current feel. **Build the wrapper** — without it this is a real ergonomic regression.

**Reuse from the existing CMS spec, without adopting its storage:** the 13 validation checks in
`AIR operator/PLANNING/CMS-Publishing-Workflow.md`, the enforced 59-char `seo_title` / 154-char
`meta_description` limits, and its generated schema set (Article, WebPage+speakable, FAQPage,
BreadcrumbList) become build-time validators and render-time components.

---

## 5. Content model

Three shapes, not one — Guides/Resources/News are genuinely identical, the rest are not.

```
// 1. Article — guides | resources | news   (127 items)
{ collection, slug, title, seoTitle, metaDescription, focusKeyword, summary,
  categorySlug, authorSlug, datePublished, dateModified,
  heroImage, thumbnailImage, featured, faqs[], webflowItemId, draft }

// 2. Community — 27 fields (6 items)
//    faq (→ FAQPage), relatedGuides[], photoGallery[4–10], lastVerified,
//    floorPlans[]   ← nested child records
//    nearbyPlaces[] ← nested child records

// 3. Operator (15 fields, 1) · Story (13 fields, 3; story.community → Community)

// Supporting: Category (7) · Author (3)
```

Body stored as a sibling `body.html` file so it stays diffable and unescaped. No MDX — it adds a
compile step and buys components-in-content we do not need.

---

## 6. Export and import

Method, API calls, collection IDs, field schemas and traps: **`DEVELOPER-HANDOVER.md` §4**.
The points that must not be lost:

1. **Do not use the partial export in `brightplace intelligence/Webflow CMS Data/`.** It is
   incomplete — a slug diff against the live sitemap shows missing URLs, and ~21 files are
   metadata-only. Re-export from the Data API.
2. **Capture `createdOn` / `lastPublished` / `lastUpdated` per item.** These exist only inside
   Webflow. Miss them and dates can never be reconstructed after cancellation. One-way.
3. **Filter `isDraft` / `isArchived`.**
4. **Import in reference order:** Authors + Categories → Operators → Communities → Guides /
   Resources / News → Stories → child records.
5. **Rehost assets.** `cdn.prod.website-files.com` survives the DNS move but dies at account
   cancellation. Make a surviving `webflow.com` string a **build failure**, not a checklist item.
6. **Import bodies verbatim.** They contain Webflow scar tissue — lists written as
   `<p><strong>Label:</strong> …</p>` because Webflow strips `<ul><li>`. A zero-diff content
   cutover keeps the blast radius at rendering. Clean up later, reviewed.

---

## 7. Publishing pipeline changes

The Webflow-only rules currently constraining writing quality get **deleted** — they were
workarounds for a CMS we are leaving.

| File | Change |
|---|---|
| `Agents/WORKFLOW.md` | Rewrite Stage 6: write `index.json` + `body.html` into `brightplace-content`, run validation, commit, report preview. **Delete** the `<ul><li>` bans (lines ~215, ~392). Retire Stage 5.5 standalone-HTML generation — the app owns `<head>`, canonical, OG and JSON-LD now; the agent supplies `faqs[]` as data. |
| `Agents/qa-agent.md` | **Delete** line 90 ("no markdown tables — Webflow can't render them") and the bold-label-only rule (91/146). Tables and real lists are now allowed and preferred. **Keep** `/knowledgebase/` rejection (183, 323, 356) and the breadcrumb rule (185). Replace "verify links against sitemap" with the build-time link validator. |
| `Agents/content-writing-guidelines.md` | **Delete** lines 78–79 and the §12 Webflow field-mapping table (354+); replace with the `Article` type. Line 212's bold-label mandate becomes a style option. |
| `Agents/SKILL.md` | Line 141: delete Webflow embed components, `<div data-rt-embed-type>`, `<p>‍</p>` spacers, the ~35K post-body limit. Line 135 ("stop at draft, Katie signs off") **survives** as `draft: true`. Resolve the `/knowledgebase/` contradiction at lines 38–40 against `WORKFLOW.md:461-463`. |
| `memory/semantic/cms-config.md` | Replace wholesale. Webflow IDs become an import-only historical appendix. New: the three types, path rules, 7 category slugs, `authorSlug`, `draft: true` default. **Guides write-restriction survives** as a path rule + CODEOWNERS on `brightplace-content/guides/`. H1-in-body and `<script>`-in-body stay banned — not Webflow quirks, they are correct. |
| `memory/semantic/link-registry.md` | Internal-URL section becomes **generated**: the validator walks every `href` in `**/body.html` and fails the build on an unknown internal path. `/knowledgebase/` stays a hard deny. The external broken-URL table stays hand-maintained. |

---

## 8. Cutover sequence

### Phase 0 — Baseline and gates (blocking)

| # | Action | Why |
|---|---|---|
| 0.1 | **Export Search Console, both properties, 16-month window, before anything changes.** Per-URL clicks/impressions/CTR/position; Queries; Links; "Page with redirect"; "Not indexed" | Rolling window — one-shot. Without it, migration damage and seasonality are indistinguishable |
| 0.2 | GA4 landing-page export, same period, monthly granularity | Seasonality control |
| 0.3 | **Extract Webflow's 301 table.** Not exposed by the API — Site Settings → Publishing → 301 Redirects, devtools → Network → XHR → copy the JSON. Do not hand-transcribe | Vanishes at cutover; carries real equity |
| 0.4 | Add `www.brightplace.ai` + `brightplace.ai` to the Vercel project; verify domains and issue certs **with no DNS change** | If the domain is claimed by another Vercel team account this blocks. Find out now, not mid-window |
| 0.5 | Build the parity harness (§9) and capture the baseline against the live site | Every later check diffs against this |
| 0.6 | Lower `www` + apex DNS TTL to 60s, **values unchanged**; wait 48h | Makes Tier-2 rollback fast. Must precede the flip by ≥48h |
| 0.7 | Stand up `brightplace-content` + the publish wrapper; prove one article end-to-end **while Webflow is still live** | Never let a cutover be the first test of the publishing loop |

**Rankings baseline is Search Console average position.** The Semrush MCP returned a plan-access
error, so it is unavailable — record this so nobody later compares a GSC figure to a Semrush one.

### Phase 1 — Build and verify on preview

New routes, content import, harness run against a Vercel preview with host override. Nothing
public changes. **Gate: content parity 148/148 plus a decision on the 14 unlisted routes.**

### Phase 2 — Migration A: Webflow content (low risk)

Point `www.brightplace.ai` at the Vercel project. Paths unchanged.

**Incremental option, verified safe.** `brightplace-ai.webflow.io` stays live after the custom
domain moves, serves **byte-identical HTML** (48,629 vs 48,622 bytes — the whole difference is one
attribute value), and its internal links are **relative**. So `www` can point at Vercel on day one
while un-built sections proxy back to Webflow via `rewrites().fallback`, migrating section by
section with ~60-second rollback at each step.

Three things that will bite, all verified:

1. **A catch-all rewrite in `beforeFiles` would deindex the entire site.**
   `brightplace-ai.webflow.io/robots.txt` is `Disallow: /`, and `beforeFiles` would serve it from
   `www`. Use `rewrites().fallback`, and ship `robots.ts` / `sitemap.ts` / `llms.txt` from day one.
2. **Proxied pages render a "Made in Webflow" badge** — the runtime force-shows it when the serving
   host ≠ `data-wf-domain`. Pre-flip fix: `<style>.w-webflow-badge{display:none!important}</style>`
   in Webflow Custom Code → Head, published to **both** the custom domains and the `.webflow.io`
   subdomain.
3. **Webflow emits absolute redirect `Location` headers**, carrying the staging host on the staging
   origin. Any 301 missed in 0.3 bounces a real user onto the `Disallow: /` host. Harness
   assertion: **no `Location` header may ever contain `webflow.io`**.

**Atomicity rule.** `rewrites().fallback` runs only after Next's own routes miss, so the moment
`app/guides/[slug]/page.tsx` exists it wins for all of `/guides/*` and that prefix can no longer
fall through. A partially-imported collection therefore returns **404 on missing slugs instead of
falling back**. Ship each collection only when every non-draft item is present and verified.

Suggested order — lowest equity first, largest last:
`/news` (11) → static/legal (8) → `/guides` (33) → `/resources` + `/category` (85, same phase —
an index and its facets cannot straddle two origins) → `/communities`, `/operators`, `/stories`.

Hold 7 days between sections. **Do not migrate `/` in this phase** — the homepage swap belongs
with Phase 3, since it is the app's homepage that replaces it.

### Phase 3 — Migration B: the hostname swap (high risk)

Separate window, ≥2–4 weeks after Phase 2 has settled.

1. Deploy one-hop 301s: `app.brightplace.ai/*` → `www.brightplace.ai/*`, **same path, byte for
   byte**, including the full `/property/<state>/<city>/<name>/<id>` structure. No chains. **Never
   bulk-redirect to `/`** — that is the single most common way this migration destroys traffic.
2. `www.brightplace.ai/` starts serving the app homepage.
3. Update every internal link, canonical and structured-data URL to `www`. Canonicals left pointing
   at `app` actively fight the migration.
4. **Search Console Change of Address** in the `app.brightplace.ai` property → `www.brightplace.ai`.
   This tool *does* apply here (genuine host change) and did **not** apply to Phase 2.
5. Submit the combined sitemap (22,774 + 148) on `www`; stop `app` advertising those URLs.
6. **Keep `app.brightplace.ai` alive and redirecting indefinitely** — 12 months minimum.

### Phase 4 — Retire Webflow

All must hold: zero proxied paths; a full crawl finds no `website-files.com` references; Search
Console shows the URLs indexed on Vercel-served responses for 30 consecutive days; extracted 301s
live and verified; contact-form submissions landing in the new handler for 30 days; full Webflow
site export archived.

Then remove the custom domains and downgrade. **Keep the plan read-only for 30 further days before
cancelling** — cancellation is the only step with no rollback.

---

## 9. Verification

One parity harness, run before the flip, after the flip and after every phase. Covers the 148
sitemap URLs, the 14 unlisted routes, and every redirect source from 0.3 — recording status, final
URL, hop count, `<title>`, `<h1>`, canonical, `meta[robots]`, and a normalised body-text hash.

Acceptance per phase: **diff vs. baseline empty except the intended section**, and within it only
the *text hash* may change — status, final URL and hop count identical.

Explicit assertions:
- `trailingSlash: false`; apex → www 301 preserving path; unknown path → real 404
- `/resources?x_page=2` → 200
- **no `Location` header contains `webflow.io`**
- post-Phase-3: every `app` URL → exactly one 301 → the same path on `www`

Plus:
- **Schema:** Rich Results Test per collection — Article, FAQPage, BreadcrumbList detected in the
  **server** HTML. Today zero JSON-LD ships, so this is a real check on new work.
- **Assets:** zero `website-files.com` / `webflow.com` in content, enforced as a build failure.
- **Links:** validator fails CI on unknown internal paths and on any `/knowledgebase/` reference.
- **Forms:** `/contact-us` parallel-run receipts match for ~2 weeks before the Webflow form is
  switched off. It fails **silently** otherwise — the page renders, the form submits, the data
  goes nowhere.
- **Pipeline:** one article published end-to-end through the new path before cutover depends on it.

### Monitoring

Daily for 14 days, then weekly to day 90. Compare **month-over-month against the same month last
year**, never week-over-week. Expect a larger, longer dip on Phase 3 than Phase 2.

**Auto-rollback (deterministic):** any 5xx on a migrated path; any baseline-200 URL returning
non-200; a redirect chain appearing or hop count rising; `robots.txt` differing by one byte.

**Investigate, do not auto-rollback (noisy, lagging):** clicks on a migrated section down >20% vs.
same period last year sustained 14 days → investigate; >35% sustained 14 days → roll that section
back while diagnosing; average position drifting >3 places on head terms for 14 days; "Crawled —
currently not indexed" rising. A 10–15% dip in weeks 1–3 that recovers is normal settling.

---

## 10. Open decisions

| # | Decision | Recommendation |
|---|---|---|
| 1 | **Content store** — separate content repo (c), or fund the CMS gaps (b)? | **(c)**, per §4. Highest-impact decision in this plan |
| 2 | Build the publish MCP wrapper, or accept commit-based publishing? | **Build it.** Without it this is a real ergonomic regression |
| 3 | Does anything from the Webflow homepage need to survive? | Currently assumed **no** — app homepage is a complete replacement. Needs confirmation |
| 4 | `/search` — rebuild, 200 empty state, or drop + redirect? | Open |
| 5 | `/author/<slug>` (3 live, unlisted) | Open |
| 6 | `/floor-plans/<slug>` + `/nearby-places/<slug>` (11 live, unlisted, likely zero traffic) | Lean **410** |
| 7 | Gap between Phase 2 and Phase 3 | **2–4 weeks minimum** |
| 8 | Contact form destination and persistence | Open |
| 9 | Legacy pseudo-list cleanup — during migration or after? | **After**, reviewed. Keep the cutover zero-diff |
| 10 | Does Guides stay write-restricted, enforced by whom? | Path rule + CODEOWNERS |

---

## 11. Files

| File | Purpose |
|---|---|
| `migration-plan-v2.md` | **This file.** Internal plan: architecture, decisions, pipeline impact, sequencing |
| `DEVELOPER-HANDOVER.md` | Dev-facing build guide: extraction, rebuild, redirects, verification |
| `migration-plan-v1.md` | Superseded. Retained for the reasoning trail; verified facts still valid |
