# Migration Docs — Index and Reading Order

**Updated 2026-09-18.** Six documents by two authors. This index says which to read, in what
order, and records where they disagree.

## Reading order for the developer

| # | Doc | Covers |
|---|---|---|
| 1 | `DEVELOPER-GUIDE-VERCEL-CMS.md` | **Start here.** The system: two-repo split, content schema, routes, SEO files, redirects, validation, verification |
| 2 | `VERCEL-CONTENT-TEMPLATES.md` | Page rendering: templates, `<head>`, JSON-LD, and the body-HTML embed problem |
| 3 | `DEVELOPER-HANDOVER.md` | Extraction method, the 22,774-URL hostname migration, DNS, cutover sequencing, rollback |
| 4 | `extract/README.md` | The extracted content itself — what is in the folders |
| 5 | `extract/templates/README.md` | Placeholder → field mapping for the blank templates |

## Planning docs (context, not build instructions)

| Doc | Status |
|---|---|
| `migration-plan-v2.md` | Current architecture and phasing rationale |
| `migration-plan-v1.md` | **Superseded.** Retained for the reasoning trail |
| `EXTRACTION-PLAN.md` | How the extraction was executed. Complete |

---

## Corrections and conflicts

### ✅ Corrected — `llms.txt` is curated, not generated

`DEVELOPER-HANDOVER.md` previously said *"Ship a real llms.txt. Webflow has none today."*
**That was wrong.** `/llms.txt` exists, is live, is 4,144 bytes, and is hand-curated with editorial
groupings and a Fair Housing instruction that must survive verbatim.

Fixed 2026-09-18. `DEVELOPER-GUIDE-VERCEL-CMS.md` §5 has the authoritative treatment.
**If anything still says to generate it, that text is stale.**

### ⚠️ Dangling references in `VERCEL-CONTENT-TEMPLATES.md` §2

It cites `HTML sample.html` and `Resources-HTML template.html` as the source for the article
structure. **Neither file is in this repository.** They appear to have been supplied directly
rather than committed.

The equivalents that *are* committed:
- `extract/templates/{guide,resource}.page.template.html` — blank templates
- `extract/{collection}/<slug>.page.html` — 127 filled examples
- `extract/{collection}/_listing.page.html` — 3 filled archives

Either commit the two originals or re-point those references, or Dennis will look for files that
do not exist.

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
