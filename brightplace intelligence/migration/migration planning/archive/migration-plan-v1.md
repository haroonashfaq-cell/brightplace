# Migrate brightplace.ai from Webflow to Vercel

> ## ⚠️ SUPERSEDED BY `migration-plan-v2.md`
>
> This document was written under the assumption that the Webflow site would be rebuilt as a
> **separate new Next.js repo**, with the Webflow homepage ported across and `app.brightplace.ai`
> left untouched.
>
> **That is not the plan.** See `migration-plan-v2.md` for the current plan and
> `DEVELOPER-HANDOVER.md` for the dev-facing guide. The actual plan is that `app.brightplace.ai` *becomes*
> `www.brightplace.ai`: the app's homepage becomes the site homepage, the Webflow content is
> rebuilt inside the existing app, and all 22,774 `/property/*` URLs change hostname.
>
> **Still valid here:** every fact in "Verified current state", the Webflow collection inventory
> and field schemas, the export/import method, the rendering requirements, the two proxy traps,
> and the parity-harness approach.
>
> **No longer valid here:** the `brightplace-web` separate-repo decision, the "visual rebuild /
> BRIX port" section (the homepage is replaced, not ported), and the phasing — which omits the
> hostname migration entirely.

> **Version 1** — approved 2026-09-17. Revisions become `migration-plan-v2.md` etc. rather than
> overwriting this file, so the reasoning behind each version stays auditable.
>
> All facts in "Verified current state" were established by live probing of `www.brightplace.ai`,
> `brightplace-ai.webflow.io` and the Webflow Data API on 2026-09-17. Re-verify before Phase 3 if
> significant time has passed — the site had unpublished Designer changes at the time of writing.

## Context

`www.brightplace.ai` is a Webflow site (BRIX template) serving 148 indexed URLs — the marketing
homepage, the `/guides/` and `/resources/` content libraries, `/news/`, `/communities/`,
`/stories/`, `/operators/`, a `/category/` taxonomy, and ~12 static/legal pages. A separate
Vercel/Next.js deployment runs the renter product at `app.brightplace.ai` (22,774 `/property/...`
pages), and a third runs `operator.brightplace.ai`.

We are moving the Webflow site itself onto Vercel. The non-negotiable constraint is **traffic
preservation**: this is an origin swap, not a URL change. Every one of the 148 URLs keeps its
exact path on `www.brightplace.ai`. Google should see a faster, better-marked-up version of the
same site at the same addresses — not a move.

The second constraint is that the **agent content pipeline must keep publishing**. Content is
produced today by the workflow in `brightplace intelligence/Agents/WORKFLOW.md` and pushed into
the Webflow Resources collection via the Webflow MCP. That push step needs a replacement, and the
memory files that encode Webflow's quirks need rewriting.

**Rough shape of the effort.** The build (export + repo + templates + static pages) is the bulk of
it; the cutover itself is Phases 3–8 with a 7-day hold between each, so **~5–7 weeks of cutover
alone**, deliberately slow because the holds are what make each step reversible. Answering the
underlying question directly: yes, this is possible without losing traffic — the URLs never change,
and the verification below is what earns that claim.

The migration is also an opportunity to clear known SEO debt recorded in
`memory/brightplace-site-seo-constraints.md`: JSON-LD currently ships empty because Webflow
injects it with JavaScript, there are no canonical tags, and published/modified dates are missing.
Server-rendered Next.js fixes all three as a side effect.

---

## Verified current state

Established by live probing and repository inspection during planning. Treat as ground truth.

### DNS and routing

| Fact | Value |
|---|---|
| `www.brightplace.ai` | CNAME → `cdn.webflow.com` (Webflow's own CDN; the Cloudflare in response headers is Webflow's, not a customer account in the path) |
| `brightplace.ai` (apex) | A → `198.202.211.1`, 301s to `www` **preserving the path** |
| Trailing slashes | **None.** `/guides/` → 301 → `/guides`. Matches Next.js default `trailingSlash: false` |
| Unknown paths | Real `404` |
| `robots.txt` | `Allow: /`, `Disallow: /*?*_page=`, `Sitemap: https://www.brightplace.ai/sitemap.xml` (listed twice) |

### URL inventory — 148 sitemap URLs

| Section | Count | Webflow collection ID |
|---|---|---|
| `/resources/<slug>` | 77 | `69fcfcef26d35b66ba874f9d` — all new agent content goes here |
| `/guides/<slug>` | 32 | `69dccfeabed64ec697c4f7d2` — currently RESTRICTED from agent writes |
| `/news/<slug>` | 10 | `6a32f0722779d53e287b5cc5` |
| `/communities/<slug>` | 7 | — |
| `/category/<slug>` | 7 | lifestyle, neighborhood-guides, news, property, renter-advice, renter-corner, top-apartments |
| `/stories/<slug>` | 3 | — |
| `/operators/<slug>` | 2 | — |
| Static pages | ~12 | `/`, `/guides`, `/resources`, `/news`, `/communities`, `/operators`, `/search`, `/property-managers`, `/contact-us`, `/privacy`, `/terms`, `/fair-housing`, `/financial-disclosure`, `/llm-info`, `/community-voice-survey` |

Webflow site ID `69d6907887b739e09622100f`. Author item "Katie Mikles" = `69dcd70089c4135f7a4158bc`.
Full field map and category item IDs: `brightplace intelligence/memory/semantic/cms-config.md`.

### Page weights (rendered HTML)

`/resources` **315KB** — renders all 77 items with no pagination; `/` 60KB, `/guides` 51KB,
`/news` 33KB, `/property-managers` 31KB, `/communities` 19KB, `/operators` 15KB, `/search` 7KB.

### Full Webflow collection inventory (read from the Data API)

10 collections, 26 pages (10 collection templates + 16 static). Workspace `69d67b4d0c38f8dc963472f3`.
Last published 2026-09-14T22:11:41Z, last updated 2026-09-15T14:55:29Z — **unpublished Designer
changes exist**, so a live scrape will not match the CMS exactly.

| Collection | ID | Items | Item URL | Index page? | In sitemap? |
|---|---|---|---|---|---|
| Guides | `69dccfeabed64ec697c4f7d2` | 31 | `/guides/<slug>` | yes | yes (31) |
| Resources | `69fcfcef26d35b66ba874f9d` | 86 | `/resources/<slug>` | yes | yes (76) |
| News | `6a32f0722779d53e287b5cc5` | 10 | `/news/<slug>` | yes | yes (9) |
| Categories | `69df6e40b18552d426ddd816` | 7 | `/category/<slug>` *(singular)* | **no** | yes (7) |
| Authors | `69dcd5b9150dec1c53e3e8de` | 3 | `/author/<slug>` *(singular)* | **no** | **no** |
| Operators | `6a86c25e5afcc88ca23b88b5` | 1 | `/operators/<slug>` | yes | yes |
| Communities | `6a86c25fa4cc0c8821ee0f1f` | 6 | `/communities/<slug>` | yes | yes |
| Stories | `6a86c25fa4cc0c8821ee0fe2` | 3 | `/stories/<slug>` | **no** | yes |
| Floor Plans | `6a872c94c6f57eb37e79d98a` | 7 | `/floor-plans/<slug>` | **no** | **no** |
| Nearby Places | `6a87460cc934a52e6d181864` | 4 | `/nearby-places/<slug>` | **no** | **no** |

**The real URL count is higher than 148.** Authors (3), Floor Plans (7) and Nearby Places (4) have
live Webflow template routes that never made the sitemap — 14 addressable URLs the sitemap-derived
inventory misses. Floor Plans and Nearby Places are one-to-many child records that render *inside*
community pages; their standalone routes are Webflow auto-created and almost certainly unlinked.
Decide deliberately whether to reproduce them or 410 them — do not discover them post-cutover.

The gap between staged items and sitemap URLs (Resources 86 vs 76, News 10 vs 9) is drafts and
archived items. Export must filter on `isDraft`/`isArchived` rather than assuming parity. The
static page `Home Copy 2` (`6a2b048f9a2faff297611042`, `/home-copy-2`) is `draft:true` — exclude.

**Schema shape.** Guides, Resources and News are **field-identical** — same 13 slugs, same types,
same required flags (only internal field IDs differ). One shared content type covers all three:

```
post-body (RichText) · post-summary · main-image · thumbnail-image · featured (Switch)
color · author-2 (→Authors) · category-2 (→Categories) · seo-title · meta-description
focus-keyword · name* · slug*                                    (* = required)
```

Communities is the heavy one (27 fields incl. `faq` RichText that feeds FAQPage schema,
`related-guides` MultiReference, `photo-gallery` MultiImage 4–10, `last-verified` DateTime).
Operators has 15, Stories 13.

**Two mapping traps to encode in the importer:**
1. In Authors, the field slug is `facebook-profile-link` but its label is **"Instagram Profile
   Link"**. Mapping by slug wires the wrong social network. Map by label and verify against content.
2. The author reference slug is `author-2` in Guides/Resources/News but plain `author` in Stories.
   Use per-collection field slugs; there is no shared convention.

**Required-field asymmetry.** Guides/Resources/News require only `name` + `slug`, so bulk import is
easy but data will be sparse. Stories/Communities/Operators require most of their fields — imports
fail without backfill. Sequence the import accordingly.

### Verified: incremental cutover via proxy is safe

The approach below depends on being able to serve some paths from Vercel and the rest from Webflow
during the transition. This was tested against the live site, not assumed:

- `https://brightplace-ai.webflow.io` is **live and serves the complete site** (200 on `/` and on
  `/guides/dallas-families`). It survives the custom domain moving away, so it works as a proxy
  origin.
- Its `robots.txt` is `User-agent: * / Disallow: /` — it is already protected from being indexed
  as a duplicate.
- The staging HTML is **byte-equivalent to production**: 48,629 vs 48,622 bytes. The entire 7-byte
  difference is the `data-wf-domain` attribute value.
- **Internal links are relative** (`/guides`, `/category/neighborhood-guides`, `/privacy`). Exactly
  one absolute staging URL appears in the document, and it is that same `data-wf-domain` attribute.

So a Next.js `rewrite` from `www.brightplace.ai/*` to `brightplace-ai.webflow.io/*` serves visually
and structurally identical pages whose links all resolve back to `www`. There is no link-rewriting
workstream and no duplicate-content exposure. Migration can proceed one section at a time with a
config-change rollback at every step.

Assets are served from `cdn.prod.website-files.com` (Webflow's asset CDN) — confirming the
rehosting workstream below.

### Known traps found during planning

1. **The local export is not a usable payload.** `brightplace intelligence/Webflow CMS Data/`
   holds 57 `.json` + 71 `.html`, but a slug-by-slug diff against the live sitemap shows many
   live URLs missing, and ~21 JSON files are metadata-only with the body in a sibling `.html`.
   Content must be re-exported fresh from the Webflow Data API.
2. **`/contact-us` will silently break.** It uses a native Webflow form
   (`wf-form-BRIX---Contact-V2`) whose submissions go to Webflow's backend. After cutover the page
   still renders and the form still appears to submit — the data just goes nowhere. Needs a
   replacement endpoint. (`/community-voice-survey` posts to `formsubmit.co` and is unaffected.)
3. **Webflow's accumulated 301 table vanishes at cutover.** Those rules carry real link equity from
   historical URLs. The Webflow Data API does not expose them — they need a manual export from
   Webflow site settings *before* the switch.
4. **Images live on Webflow's CDN.** Port the HTML without rehosting assets and every image dies
   the day the Webflow subscription lapses. Same for `og:image`.
5. **`/knowledgebase/*` 404s today — keep it that way.** It was probed live: `/knowledgebase/prorated-rent`,
   `/blog` and `/resources/studio-apartments` all return 404. Do **not** invent a
   `/knowledgebase/*` → `/resources/*` redirect during the migration; that would be new behavior,
   not parity, and parity is the whole point. The agent-side rule stays as-is: never *emit* a
   `/knowledgebase/` link. (Note `Agents/SKILL.md:38-40` still uses it as a content-type label while
   `WORKFLOW.md:461-463` confirms those render at `/resources/` — resolve that contradiction.)
6. **Semrush MCP is unavailable on the current plan.** Traffic baselining must come from Google
   Search Console and GA4.

### Out of scope

`app.brightplace.ai` (dev-team-owned repo, not in this workspace) and `operator.brightplace.ai`
stay exactly where they are. Per `CLAUDE.md`, the dev team never gets access to the SUPER SEO
Agents system, so any shared publishing API needs an explicit owner.

---

## Where content lives: git-based content in a new Next.js repo

New repo `brightplace-web/`, sibling to `operator-pages/` (which already proves this exact stack
ships to Vercel: Next 15 App Router, React 19, `images:{unoptimized:true}`).

**Rejected: extending the existing brightplace CMS.** Two hard blockers, not preferences.
`AIR operator/PLANNING/MCP-Content-Specs.md:37` states `body_html` *does not exist — server renders
markdown*. Importing 148 Webflow rich-text bodies would mean a lossy HTML→Markdown conversion of
exactly the artifact we are migrating for fidelity. And that CMS is AIR-operator, dev-team-adjacent
infrastructure; per `CLAUDE.md` the dev team never touches the SUPER SEO Agents content system, so
putting brightplace.ai's content model inside it creates the coupling that rule exists to prevent.
Everything else — no brightplace tenant, `unique(community_id, slug)`, flat `/blog/[slug]`, no
canonical override, the live Anthropic `oneOf/allOf` schema blocker in
`CMS-Staging-Claude-Schema-Fix.md` — is confirmation, not the argument.

**Rejected: a new headless CMS.** Net-new vendor, auth, migration and a second API surface, buying
only a web editor. The primary author here is an agent.

**Why git wins beyond cost:** internal-link validation stops being an HTTP honor system. Today
`link-registry.md` says "fetch the live sitemap before each batch." Post-migration the repo *is* the
URL graph, so every internal link becomes a build-time assertion that fails CI on an unknown path —
including a permanent deny-list for `/knowledgebase/`. Stage 6 of `WORKFLOW.md` already emits
`[slug].json` + `[slug].html`; the on-disk model is a rename away.

**Port the CMS's specs, not its storage.** The 13 validation checks in
`AIR operator/PLANNING/CMS-Publishing-Workflow.md`, the 59-char `seo_title` / 154-char
`meta_description` limits its API actually enforces, and its generated schema set (Article,
WebPage+speakable, FAQPage, BreadcrumbList) become build-time validators and render-time components.
Reuse without coupling.

### Content model — three shapes, not one

Guides, Resources and News are field-identical (verified against the Data API), so they share one
type. Communities, Operators and Stories are not, and forcing them into a shared shape would lose
data. Types in `brightplace-web/src/content/types.ts`:

```
// 1. Article — covers guides | resources | news  (127 items)
{ collection, slug, title, seoTitle, metaDescription, focusKeyword, summary,
  categorySlug, authorSlug, datePublished, dateModified, heroImage, thumbnailImage,
  featured, faqs[], webflowItemId, draft }

// 2. Community — 27 fields (6 items). Includes faq (RichText → FAQPage),
//    relatedGuides[] (MultiReference → Guides), photoGallery[] (4–10), lastVerified,
//    plus nested child records:
//      floorPlans[]   ← Webflow "Floor Plans"   (7 items)
//      nearbyPlaces[] ← Webflow "Nearby Places" (4 items)

// 3. Operator (15 fields, 1 item) · Story (13 fields, 3 items)
//    Story.community → Community; Story.storyType is an enum of 5 values

// Supporting: Category (7) · Author (3)
```

Floor Plans and Nearby Places are **child records nested inside Community**, not standalone content
types — Webflow auto-created their `/floor-plans/<slug>` and `/nearby-places/<slug>` routes and they
are almost certainly unlinked. Do not reproduce those routes; see the decision in Open Questions.

**On-disk layout** — per-item directory, so body HTML stays diffable and unescaped:

```
brightplace-web/src/content/<collection>/<slug>/index.json   # typed fields
brightplace-web/src/content/<collection>/<slug>/body.html    # body, diffable
brightplace-web/src/content/categories/<slug>.json
brightplace-web/src/content/authors/katie-mikles.json
```

No MDX — it buys components-in-content we don't need and adds a compile step. Loader
`src/content/index.ts` exports `getPost`, `getCollection`, `getByCategory`, `getAllPaths`,
`getAllInternalPaths` (the last feeds the link validator). Routes mirror the live URL space exactly.

### Export and import

`scripts/export-webflow.ts` against site `69d6907887b739e09622100f`:

1. Read all 10 collection schemas from the API — do not assume `cms-config.md`'s field map holds
   beyond Resources; it doesn't.
2. Paginate every collection to completion, caching raw responses under `scripts/.cache/webflow/`
   as the audit trail. **Filter `isDraft`/`isArchived`** — staged counts exceed live URLs
   (Resources 86 vs 76, News 10 vs 9).
3. **Capture dates explicitly** — `createdOn`, `lastPublished`, `lastUpdated`. These exist only in
   Webflow. Miss them at export and `datePublished`/`dateModified` can never be correct afterwards.
   Map `datePublished = published-on ?? createdOn`, `dateModified = lastUpdated ?? lastPublished`.
4. Resolve references **by per-collection field slug**: `author-2` in Guides/Resources/News but
   plain `author` in Stories. And map the Authors social field **by label** — slug
   `facebook-profile-link` is labelled "Instagram Profile Link".
5. `scripts/rehost-assets.ts` — pull every `cdn.prod.website-files.com` / `cdn.webflow.com` /
   `uploads-ssl.webflow.com` URL out of image fields and body HTML, download, hash-name into
   `public/media/<collection>/<slug>/`, rewrite the reference. Sweep `GET /sites/{id}/assets` for
   anything not body-referenced. **Build fails if any Webflow URL survives in `src/content/**`.**
6. `scripts/verify-parity.ts` — diff the live sitemap plus the 14 non-sitemap routes against
   `getAllPaths()`; exit non-zero on any miss. This is the gate the local export failed.
7. **Import in reference-graph order**, or imports fail on unresolved references:
   `Authors + Categories` (no dependencies) → `Operators` → `Communities` (references Operators and
   Guides) → `Guides / Resources / News` → `Stories` (requires Communities) → `Floor Plans` and
   `Nearby Places` folded in as child records of Communities. Total staged items across all 10
   collections: 158.
8. **Import legacy bodies verbatim.** The existing articles carry Webflow scar tissue — pseudo-lists
   written as `<p><strong>Label:</strong> …</p>` because Webflow strips `<ul><li>`. Do not rewrite
   during import; a zero-diff cutover keeps the blast radius at rendering only. Restoring real list
   markup is a separate post-cutover pass with human review.

### Rendering — this is where the SEO debt gets paid

In `src/components/seo/` + `src/lib/schema.ts`, consumed by each route's `generateMetadata` and
server component. Nothing JS-injected — that is precisely what broke JSON-LD on Webflow.

- `JsonLd.tsx` renders `<script type="application/ld+json">` **server-side**: Article (with
  `datePublished`/`dateModified`/`author`/`publisher`), WebPage + `speakable`, FAQPage when
  `faqs.length > 0`, BreadcrumbList.
- Canonical via `metadata.alternates.canonical` on every route including indexes and `/category/*`.
- `<time dateTime>` in article header/footer, plus OG `article:published_time` /
  `article:modified_time` and real `og:title`/`og:description`/`og:image` (today only
  `og:type="website"` ships).
- `Breadcrumbs.tsx` — position-2 label matches the collection ("Resources", never "Knowledgebase",
  per `qa-agent.md:185`).
- `src/app/sitemap.ts` and `robots.ts` **generated from the content loader** — 148+ URLs must not be
  hand-maintained the way `operator-pages` does it. `public/llms.txt` generated by
  `scripts/build-llms-txt.ts`, seeded from `Agents/llms-txt-update.md`.
- `next.config.ts`: **do not set `output:'export'`** (it would delete the contact route handler) and
  **do not copy `images:{unoptimized:true}` from `operator-pages`**. That flag exists there for
  static export; on a 148-page image-heavy content site it throws away `next/image` optimization,
  which is one of the main performance wins of leaving Webflow.

### The visual rebuild — the largest workstream, and it shapes the phasing

This is not a bullet point. The site is a BRIX Webflow template, and porting it means rebuilding:
the homepage (60KB), `/property-managers` (31KB), six listing pages, the article template, the
global nav and footer, and every responsive breakpoint. It is almost certainly the biggest single
piece of work here and the most likely thing to slip.

It also has a consequence the incremental cutover makes unavoidable: **during Phases 4–8 the site
runs two designs at once.** `/news` and `/guides` render in the new templates while `/resources` and
the homepage still render Webflow's, for weeks. Two choices, and this needs an explicit answer
before Phase 4:

- **Accept the seam** (defensible — it trades weeks of visual inconsistency for a reversible,
  low-risk migration), or
- **Match BRIX closely** in the new templates so the seam is invisible, at the cost of more
  front-end work up front and carrying design debt you presumably want to shed anyway.

My recommendation is to match BRIX closely enough for nav, footer and article layout — those are
what a visitor crossing the seam actually notices — and treat a real redesign as a separate project
after Phase 9. Do not bundle a redesign into this migration; it would destroy the one property that
makes the whole plan safe, which is that every page is supposed to look the same before and after.

### Forms

`/contact-us` gets `app/contact-us/page.tsx` + client `ContactForm.tsx` posting to
`app/api/contact/route.ts` — validate, honeypot, rate-limit, send to a monitored inbox and append to
a store so nothing is fire-and-forget. **Run both forms in parallel for ~2 weeks and compare
receipts before killing the Webflow one.** `/community-voice-survey` posts to `formsubmit.co`; port
the markup unchanged, no backend work.

### Publishing pipeline rewrite

Stage 6 changes from "Webflow MCP push" to "write content files, validate, commit, report preview
URL." The Webflow-only rules that have been constraining writing quality get **deleted**:

| File | Change |
|---|---|
| `Agents/WORKFLOW.md` | Rewrite Stage 6 (~lines 407–425) to write `index.json` + `body.html`, run `npm run validate`, commit on a branch, report the Vercel preview. **Delete** line 215 and line 392's `<ul><li>` bans. Retire Stage 5.5's standalone-HTML generation — the app now owns `<head>`, canonical, OG and JSON-LD; the agent supplies `faqs[]` as data. |
| `Agents/qa-agent.md` | **Delete** line 90 ("no markdown tables — Webflow can't render them") and the bold-label-only rule at 91/146. Tables and real lists are now allowed and preferred. **Keep** `/knowledgebase/` rejection (183, 323, 356) and the breadcrumb rule (185). Replace "verify links against sitemap" with `npm run validate:links`. |
| `Agents/content-writing-guidelines.md` | **Delete** lines 78–79 and the §12 Webflow field-mapping table (354+); replace with the `Article` type. Line 212's bold-label mandate becomes a style option. |
| `Agents/SKILL.md` | Line 141: delete Webflow embed components, `<div data-rt-embed-type>`, `<p>‍</p>` spacers and the ~35K post-body limit. Line 135's "stop at draft, Katie signs off" **survives** as `draft: true`. Also resolve the `/knowledgebase/` contradiction at lines 38–40. |
| `memory/semantic/cms-config.md` | Replace wholesale; Webflow IDs become an import-only historical appendix. New content: the three types, path rules, the 7 category slugs, `authorSlug: katie-mikles`, `draft: true` default. **Guides restriction survives** as a path rule plus CODEOWNERS on `src/content/guides/`. H1-in-body and `<script>`-in-body stay banned — those aren't Webflow quirks, they're correct. |
| `memory/semantic/link-registry.md` | Internal-URL section becomes generated: `validate:links` walks every `href` in `src/content/**/body.html` and fails the build on an unknown internal path. `/knowledgebase/` stays a hard deny. The external broken-URL table stays hand-maintained. |

---

## Two traps that would cause real damage

**1. A catch-all rewrite would deindex the entire site.** `brightplace-ai.webflow.io/robots.txt` is
`User-agent: * / Disallow: /`. A rewrite declared in `beforeFiles` proxies `/robots.txt` to Webflow
and serves that file from `www.brightplace.ai`. Use `rewrites().fallback`, which runs only *after*
Next routes and static files miss — and ship `app/robots.ts`, `app/sitemap.ts` and `/llms.txt` on
day one so those paths can never fall through.

**2. Proxied pages will render a "Made in Webflow" badge.** The Webflow runtime
(`webflow.schunk.47e904a3f31ea8ba.js`) force-shows it when the serving host doesn't match
`data-wf-domain`: `/\.webflow\.io$/i.test(h) && s.hostname !== h && (f = !0)`. Fix before the flip by
adding `<style>.w-webflow-badge{display:none!important}</style>` to Webflow Site Settings → Custom
Code → Head and publishing to **both** the custom domains and the webflow.io subdomain.

The related risk we *don't* have: the same bundle contains no redirect-to-canonical-host logic, so
the proxy cannot loop. And since the site emits no `<link rel=canonical>` and no `og:url` at all
today, the usual "proxied pages emit the wrong canonical" problem is moot. Do not backfill
canonicals into Webflow.

## Cutover runbook

### Phase 0 — Gates (blocking)

| # | Action | Verify |
|---|---|---|
| 0.1 | **GSC export first, before anything.** Performance → Pages, full 16-month range: per-URL clicks/impressions/CTR/position, plus Queries, plus Pages filtered to "Page with redirect" and "Not indexed", plus the Links report. It's a rolling window — this is one-shot | 148+ rows committed under `brightplace intelligence/memory/episodic/migration-baseline/` |
| 0.2 | GA4 export: landing page × sessions × conversions, same 16 months, monthly granularity | CSV committed alongside |
| 0.3 | **Rankings baseline is GSC average position** — Semrush MCP is unavailable on the current plan. Record this so nobody later compares a GSC number to a Semrush one | Documented in the baseline README |
| 0.4 | **GATE — Vercel domain scope.** Add both domains to the new project and complete TXT verification + cert issuance **with no DNS change**. `app` sits on `vercel-dns-017` (dev-team scope); if `brightplace.ai` is already claimed at another team account, this blocks and needs a transfer | Vercel shows "Valid Configuration — pending DNS" + issued cert |
| 0.5 | **GATE — Webflow form on staging.** Submit a test through `brightplace-ai.webflow.io/contact-us` and confirm it lands in Webflow Forms | If it does **not** land, `/contact-us` cannot sit behind the proxy and moves to migration batch 1 |
| 0.6 | **Extract the Webflow 301 table.** The Data API does not expose it. Open Site Settings → Publishing → 301 Redirects with devtools Network open, filter XHR, copy the JSON backing the table — do not hand-transcribe a paginated UI. Cross-check against GSC "Page with redirect" | `redirects.json` committed; row count matches the UI |
| 0.7 | Decide `/search` (Webflow-native site search, in the sitemap, no Next equivalent) and confirm the 7 `/category/<slug>` routes are a hard parity constraint | Decisions recorded |

### Phase 1 — Parity harness

One script over **148 sitemap URLs + the 14 non-sitemap routes + every redirect source from 0.6 +
the known-nonexistent URLs from `link-registry.md`**, recording per URL: status, final URL after
redirects, hop count, `<title>`, `<h1>`, canonical, `meta[robots]`, and a normalized-text hash.
Run it against Webflow now to capture the baseline.

Every later phase's verification is then literally *"harness diff vs. baseline is empty except the
intended section."* Assert explicitly: `trailingSlash:false`, apex→www 301 preserving path, unknown
path → real 404 (not a soft 200), and `/resources?x_page=2` → 200 matching `/resources`.

**Plus one assertion that catches a leak nothing else would: no response `Location` header may ever
contain `webflow.io`.** Webflow emits *absolute* redirect Locations, and on the staging origin they
carry the staging host — verified live:

```
brightplace-ai.webflow.io/guides/  →  301  location: https://brightplace-ai.webflow.io/guides
www.brightplace.ai/guides/         →  301  location: https://www.brightplace.ai/guides
```

Next's `trailingSlash` handles the slash case before the fallback. But **any 301 that Phase 0.6's
extraction misses** falls through to the proxy and bounces a real user onto the `Disallow: /`
staging host. This assertion is how you find those misses.

### Phase 2 — DNS preparation (≥48h before the flip)

DNS is **Namecheap BasicDNS** (`dns1/dns2.registrar-servers.com`) with no ALIAS support at the apex,
so the apex stays an A record. Change **TTL only**, no values:

| Host | Type | Value (unchanged) | TTL |
|---|---|---|---|
| `www` | CNAME | `cdn.webflow.com` | Automatic (1800) → **60** |
| `@` | A | `198.202.211.1` | Automatic → **60** |

Wait a full 48h so old 1800s records expire everywhere. Do not touch MX (Google), `app`, or
`operator`. Do **not** use GSC's Change of Address tool — same domain, it does not apply.

### Phase 3 — Flip as a content no-op

Ship the Next project with a catch-all fallback so the DNS flip changes zero bytes of content:

```js
// next.config.ts — Phase 3 shape
const WF = 'https://brightplace-ai.webflow.io'
// MIGRATED shrinks the fallback each phase; anything not yet built falls through to Webflow.
export default {
  trailingSlash: false,
  async redirects() {
    return [
      { source: '/:path*', has: [{ type: 'host', value: 'brightplace.ai' }],
        destination: 'https://www.brightplace.ai/:path*', permanent: true },
      ...require('./redirects.json'),   // Phase 0.6 extraction, permanent: true
    ]
  },
  async rewrites() {
    // `fallback` runs only AFTER Next routes, static files and /_next/* miss.
    // This is what keeps /robots.txt, /sitemap.xml and /llms.txt on Vercel.
    return { fallback: [{ source: '/:path*', destination: `${WF}/:path*` }] }
  },
}
```

Then flip DNS in a single ~15-minute window: `www` CNAME → the project-specific
`*.vercel-dns-0xx.com` target Vercel gives you; `@` A → `76.76.21.21`.

**Leave both domains configured as custom domains inside Webflow.** They cost nothing and they are
the tier-2 rollback.

Verify: harness diff empty across all 148; `curl -sI` shows Vercel headers; `/robots.txt` still
reads `Allow: /`; no Webflow badge; `/contact-us` submits.

**Rollback tiers, applying to every phase:**
- **Tier 1 (the one you'll actually use):** redeploy with the prefix returned to the fallback, or
  Vercel instant-rollback to the prior deployment. ~60s, no DNS propagation.
- **Tier 2:** revert `www` → `cdn.webflow.com`, apex → `198.202.211.1`. Bounded by the 60s TTL.

### The atomicity rule — read before phasing

`rewrites().fallback` runs **only after Next's own routes miss**. So the moment
`app/guides/[slug]/page.tsx` exists, it wins for every `/guides/*` request — there is nothing to
"remove," and that prefix can no longer fall through to Webflow. The dangerous consequence: if a
collection is only partially imported, the route returns **404 for the missing slugs instead of
falling through**. A 31-item Guides import that lands 28 items silently 404s three live URLs.

**Rule: a collection migrates atomically.** Shipping its route requires `verify-parity.ts` to pass
for that entire prefix — every non-draft item present — as a deploy gate. The Phase 7 note that
`/category/*` cannot straddle two origins is the same rule; this is its general form.

### Phases 4–8 — Migrate one collection at a time, atomically

| Phase | Section | URLs | Why here |
|---|---|---|---|
| 4 | `/news` + `/news/*` | 11 | Lowest traffic and equity; exercises the full CMS → route → sitemap path on a section nobody will miss. ~7% blast radius |
| 5 | Static/legal: `/privacy`, `/terms`, `/fair-housing`, `/financial-disclosure`, `/llm-info`, `/community-voice-survey`, `/property-managers`, `/contact-us`¹ | 8 | Hand-authored, no CMS dependency, low query volume |
| 6 | `/guides` + `/guides/*` | 33 | The strategic content. Before `/resources` because it's a third the size with richer inbound links — validates JSON-LD, canonicals and dates on a set small enough to hand-check |
| 7 | `/resources` + `/resources/*` + `/category/*` | 85 | Largest and riskiest. `/category/*` must land in the **same** phase — an index and its facets cannot straddle two origins. Ship at parity first (all 77 items, 315KB, no pagination); paginating now would mint URLs that never existed |
| 8 | `/`, `/communities/*`, `/operators/*`, `/stories/*`, `/search` | 21 | Homepage last: most visible, least urgent, and by now every component is proven |

¹ If gate 0.5 failed, `/contact-us` jumps to Phase 4.

**Per-phase checklist, identical every time:**
1. Deploy to a Vercel preview; run the harness against it with a host override.
2. **Gate: `verify-parity.ts` passes for the whole prefix** (every non-draft item present). Then
   ship the route — which takes the prefix off the fallback automatically. Do not ship a partial
   collection.
3. Harness diff — only the intended section's *text hash* may change. Status, final URL and hop
   count must be **identical**.
4. Confirm the new pages add what Webflow lacked: self-referencing canonical, server-rendered
   JSON-LD, `datePublished`/`dateModified`.
5. GSC → URL Inspection → Live Test on 3 URLs from the batch; rendered HTML must contain the
   JSON-LD and canonical.
6. **Hold 7 days** before starting the next phase.

### Sitemap / robots / llms.txt during the split

Serve all three from Vercel from flip-minute-one. The sitemap is **one file listing all 148 URLs
regardless of which origin serves them** — Google doesn't care which backend answered, and splitting
it would drop 100+ URLs from discovery mid-migration.

```
User-agent: *
Allow: /
Disallow: /*?*_page=
Sitemap: https://www.brightplace.ai/sitemap.xml
```

Fix the duplicated `Sitemap:` line. Keep the `_page=` rule through Phase 7, then drop it once
`/resources` is Vercel-rendered with self-canonicals. Generate `lastmod` from real timestamps only
for migrated sections and keep Webflow's values for proxied ones — a global `lastmod` bump invites a
crawl of pages that didn't change. Ship a real `llms.txt` at Phase 3 (Webflow has none; `/llm-info`
is a page, not a machine file) seeded from `Agents/llms-txt-update.md`.

### Assets

`cdn.prod.website-files.com` keeps serving after the DNS flip **and** after the custom domains are
removed from Webflow. It stops at **account cancellation or downgrade** — so rehosting gates Phase 9,
not the cutover. Rehost during Phases 6–7 as each section migrates. Audit with a full-site crawl
grepping for `website-files.com`; it must return zero before Phase 9.

### Post-cutover monitoring

Daily for 14 days, then weekly through day 90. Compare against the Phase 0 baseline
**month-over-month against the same month last year**, never week-over-week.

**Automatic Tier-1 rollback (HTTP-level, deterministic):**
- any 5xx on a migrated path
- any URL that was 200 in the baseline returning non-200
- a redirect chain appearing where the baseline had none, or hop count increasing
- `/robots.txt` differing from the file above by one byte

**Investigate, never auto-rollback (ranking-level, noisy and lagging):**
- GSC Coverage "Crawled — currently not indexed" rising on a migrated prefix
- clicks on a migrated prefix down **>20% vs. the same period last year, sustained 14 days** →
  investigate; **>35% sustained 14 days** → roll that phase back to the proxy while diagnosing.
  A 10–15% dip in weeks 1–3 that recovers is normal settling.
- average position drifting >3 places on head terms for 14 days

Also watch Core Web Vitals on `/resources` — at 315KB it will look worse on Vercel before
optimization if shipped unchanged, which is the correct trade.

### Phase 9 — Cancel Webflow

All of these must be true: fallback rewrite removed entirely (zero proxied paths); a full crawl finds
zero `website-files.com` references; GSC shows all 148 URLs indexed on Vercel-served responses for 30
consecutive days; `redirects.json` is in the repo with sources verified live; `/contact-us`
submissions confirmed landing in the new handler for 30 days; a full Webflow site export archived.
Then remove the custom domains and downgrade — and keep the plan read-only for 30 more days before
cancelling, because cancellation is the one step with no rollback.

---

## Verification

- **Parity harness** (Phase 1) is the primary gate — run before the flip, after the flip, and after
  every phase. Empty diff except the intended section.
- **Export parity:** `scripts/verify-parity.ts` must reach 148/148 sitemap URLs plus the 14
  non-sitemap routes before any rendering work is trusted.
- **Asset sweep:** zero `website-files.com` / `webflow.com` strings in `src/content/**` — enforced as
  a build failure, not a checklist item.
- **Link validation:** `npm run validate:links` resolves every internal `href` in
  `src/content/**/body.html` against `getAllInternalPaths()`; unknown path or any `/knowledgebase/`
  reference fails CI.
- **Schema:** Google Rich Results Test on one URL per collection — Article, FAQPage and
  BreadcrumbList must be detected in the *server* HTML (today: zero `ld+json` blocks ship).
- **Pipeline proof:** publish one new article end-to-end through the new path **while Webflow is
  still live** (Phase P4), before any cutover depends on it.
- **Forms:** run the Webflow and Vercel contact forms in parallel ~2 weeks and compare receipt counts.

## Open decisions

1. **Publishing UX changes, and this is the real cost of the recommendation.** Today you publish by
   MCP call. Under git-based content it's write-files → commit → Vercel preview. Either accept that,
   or build a thin local MCP/skill wrapper shaped like `blog_save_post` that does write + commit +
   preview in one call to preserve today's feel. My recommendation is the wrapper.
2. **Visual approach during the split** — accept the two-design seam through Phases 4–8, or match
   BRIX closely so it's invisible? (Recommendation above.) And confirm a redesign is explicitly
   *out* of this project.
3. `/search` — rebuild client-side, ship a 200 empty state, or drop from the sitemap and redirect?
4. `/floor-plans/<slug>` and `/nearby-places/<slug>` (11 unlinked auto-created routes, not in the
   sitemap) — reproduce, or let them 410?
5. `/author/<slug>` (3 routes, live but not in the sitemap) — reproduce or drop?
6. Legacy pseudo-list rewrite: verbatim import now with a reviewed cleanup pass later
   (my recommendation), or rewrite all 148 bodies during migration?
7. Contact form destination — a monitored inbox via Resend, or HubSpot (a connector exists in this
   session)?
8. Does Guides stay write-restricted after migration, and enforced by whom?
9. `brightplace-web` as a nested repo alongside `operator-pages`, or a separate top-level repo?
