# Migration Docs — Index and Reading Order

**Updated 2026-09-18.** Everything needed for the rebuild is in this folder. This index says which to read, in what
order, and records where they disagree.

## Reading order for the developer

| # | Doc | Covers |
|---|---|---|
| 1 | `DEVELOPER-GUIDE-VERCEL-CMS.md` | **Start here.** The system: two-repo split, content schema, routes, SEO files, redirects, validation, verification |
| 2 | `VERCEL-CONTENT-TEMPLATES.md` | Page rendering: templates, `<head>`, JSON-LD, and the body-HTML embed problem |
| 2a | `TEMPLATE-blog-page.html` | **Working article template.** Complete design, all five body components styled |
| 2b | `TEMPLATE-blog-listing-page.html` | **Working archive template.** Card grid, category chips, listing schema |
| 3 | `DEVELOPER-HANDOVER.md` | Extraction method, the 22,774-URL hostname migration, DNS, cutover sequencing, rollback |
| 4 | `extract/README.md` | The extracted content itself — what is in the folders |
| 5 | `extract/templates/README.md` | Placeholder → field mapping for the blank templates |

## 🔒 Internal only — do NOT send to the dev team

| Doc | Why |
|---|---|
| `migration-plan-v2.md` | §7 details edits to the content-agent pipeline (`Agents/WORKFLOW.md`, `qa-agent.md`, `SKILL.md`). Per `CLAUDE.md`, the dev team never gets access to that system |

These are planning and internal-process records. Everything the developer needs is in the five
documents above, none of which reference the content pipeline.

---

## Corrections and conflicts

### ✅ Corrected — `llms.txt` is curated, not generated

`DEVELOPER-HANDOVER.md` previously said *"Ship a real llms.txt. Webflow has none today."*
**That was wrong.** `/llms.txt` exists, is live, is 4,144 bytes, and is hand-curated with editorial
groupings and a Fair Housing instruction that must survive verbatim.

Fixed 2026-09-18. `DEVELOPER-GUIDE-VERCEL-CMS.md` §5 has the authoritative treatment.
**If anything still says to generate it, that text is stale.**

### Note — the rendered Webflow samples are not in the repo

`VERCEL-CONTENT-TEMPLATES.md` §2 cites `HTML sample.html` and `Resources-HTML template.html` as the
source for the article structure. They were supplied directly rather than committed, and are not in
this folder.

They are not needed to build: the design tokens sampled from them are already baked into
`TEMPLATE-blog-page.html` and `TEMPLATE-blog-listing-page.html`, and the structure they showed is
documented in `VERCEL-CONTENT-TEMPLATES.md` §2.

The committed equivalents, showing content in the **new** structure:
- `extract/templates/{guide,resource}.page.template.html` — blank templates
- `extract/{collection}/<slug>.page.html` — 127 filled examples
- `extract/{collection}/_listing.page.html` — 3 filled archives

### Note — the 23-key schema includes extraction artifacts

`DEVELOPER-GUIDE-VERCEL-CMS.md` §2 adopts the 23-key record from
`extract/reports/*-metadata.json` as the content contract. Verified: 23 keys, byte-identical
across guides, resources and news.

Three of those keys are **extraction byproducts, not content fields**:
`body_chars` (a length proxy), `inline_images` (populated on 2 news items), and `webflow_item_id`
(provenance). Useful during migration; decide deliberately whether they belong in the long-term
schema before freezing `schema/types.ts`.

---

## Claims verified against the extract

Every measurement in the two new docs was re-checked against the extracted corpus on 2026-09-18.
**All exact:**

| Claim | Verified |
|---|---|
| 223 embed blocks | ✅ 223 |
| 145 `<head>`, 149 `<body>`, 190 `<style>` | ✅ exact |
| 1 `<!DOCTYPE>`, 1 `<base target="_blank">` | ✅ exact |
| 33 `<table>`, all inside embeds | ✅ exact |
| 4 `<img>` across all bodies | ✅ exact |
| No body contains `<h1>` | ✅ 0 |
| Links: 473 www / 417 apex / 182 app / 3 docs / 10 relative | ✅ exact |
| `main_image_alt` null ~97% | ✅ 123/127 (96.9%) |
| `thumbnail_image` null 18/31, 10/86, 3/10 | ✅ exact |
| 23 keys, identical across collections | ✅ exact |

One trivial imprecision: guides carry **2–17** embeds each, not "1 to 17".

The embed distribution is the load-bearing finding for estimation — **31/31 guides, 1/86
resources, 0/10 news.** It is a guides problem, not a corpus-wide one.

---

## Open items across all docs

| Item | Owner | Deadline |
|---|---|---|
| **Search Console verification token** | — | **Before DNS moves** |
| GA4 `G-DK6QHHS88K` carried to new routes | Dev | **Before DNS moves** |
| Content consumption: submodule / package / build fetch | Dev | Before build |
| Asset hosting: Vercel Blob / S3 / `public/` | Dev | Before build |
| `/author/[slug]` — rebuild, redirect or 410 | Product | Before launch |
| `/search` — rebuild, empty state, or drop | Product | Before launch |
| Category page content (`property` 41 articles, no metadata) | Content | Before launch |
| `main_image_alt` backfill (~97% null) | Content | Post-launch acceptable |
| In-body image binaries beyond the 4 news inline | Dev | **Before Webflow cancellation** |

The two "before DNS moves" rows are the only ones with a hard external deadline: miss them and
analytics goes dark at cutover and the Search Console property loses verification.
