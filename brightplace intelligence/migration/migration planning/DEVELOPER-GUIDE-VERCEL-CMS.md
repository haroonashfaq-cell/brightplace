# Developer Guide — brightplace.ai Content on Vercel

**Version 1 · 2026-09-18**
**Audience:** Dennis
**Companion to:** `DEVELOPER-HANDOVER.md` (Webflow extraction, redirects, cutover sequencing) and `migration-plan-v2.md` (architecture rationale, phasing). This guide covers what those two leave out: the content repo, routes, SEO files, redirects and verification. Page rendering — templates, `<head>`, structured data and body HTML — is in `VERCEL-CONTENT-TEMPLATES.md`.

---

## 0. Scope — read this first

This document governs **brightplace.ai only** — the guides, resources and news content currently on Webflow.

It does **not** cover AIR community sites or brightplace Direct. Those are separate products with their own specs, and `brightplace direct/Planning/13-cms-endpoint-spec.md` proposes a different architecture (Supabase + ISR). **Do not build against that document for this work.**

**What's moving:** 120 live articles — 31 guides, 80 resources, 9 news. Paths stay byte-identical; only the origin changes. Because the URLs don't change, Google doesn't have to relearn anything, and the SEO risk is execution error rather than migration mechanics.

---

## 1. What you're building

Two repositories, two owners, one automatic link between them.

```
brightplace-content/          ← content team owns. Articles live here.
        │
        │  read at build time
        ▼
brightplace app (your repo)   ← you own. Turns articles into pages.
        │
        │  Vercel Deploy Hook on content merge
        ▼
   www.brightplace.ai
```

**You never need access to the content pipeline. The content team never needs commit access to your application repo.** That separation is the point of the design.

### The publish loop

1. Content engine writes `index.json` + `body.html` into `brightplace-content` and opens a PR
2. Vercel builds a preview deployment; the PR gets a preview URL
3. Content team reviews on that URL and merges
4. Merge fires a Deploy Hook; the site rebuilds; the article is live

Content is published without an application deploy. That constraint is why content lives in its own repo rather than in yours.

---

## 2. The content repo

### Layout

```
brightplace-content/
├── guides/
│   └── <slug>/
│       ├── index.json
│       └── body.html
├── resources/<slug>/…
├── news/<slug>/…
├── categories/<slug>.json
├── authors/<slug>.json
├── redirects.json
├── llms.txt
└── schema/types.ts          ← the versioned contract
```

One folder per article, named by slug. The folder name **is** the URL segment.

### Why two files

`body.html` is the article body only — no `<head>`, no nav, no footer. It goes in the middle of your template.

`index.json` is everything else. Your template reads it to build the `<head>`, the byline, the breadcrumb, the sitemap entry and the structured data.

Bodies stay HTML rather than Markdown because the source is Webflow rich text, and converting it would lose fidelity on exactly the content we're migrating to preserve.

### Article schema — 23 keys

This is not a proposal. It is the schema already extracted and sitting in `extract/reports/{guides,resources,news}-metadata.json`, **identical across all three collections with zero key variance.**

| Key | Type | Notes |
|---|---|---|
| `slug` | string | Matches the folder name. URL segment. |
| `title` | string | Renders as `<h1>` |
| `url` | string | Full absolute URL, e.g. `https://www.brightplace.ai/guides/dallas-families` |
| `collection` | string | `guides` \| `resources` \| `news` |
| `seo_title` | string | `<title>`. Distinct from `title`. |
| `meta_description` | string \| null | `<meta name="description">` |
| `focus_keyword` | string \| null | Editorial metadata; not rendered |
| `summary` | string \| null | Intro paragraph and `og:description` fallback |
| `category` | string \| null | Category **slug**, e.g. `neighborhood-guides` |
| `category_name` | string \| null | Display name, e.g. `Neighborhood Guides` |
| `author` | string \| null | Display name, e.g. `Katie Mikles` |
| `featured` | boolean | Archive sort/promotion |
| `main_image` | string \| null | Hero image |
| `main_image_alt` | string \| null | **Null on ~97% of items — see §10** |
| `thumbnail_image` | string \| null | Archive card image |
| `draft` | boolean | **Excluded from the build entirely** |
| `archived` | boolean | Excluded from the build |
| `created_on` | ISO-8601 | |
| `last_updated` | ISO-8601 | Feeds `dateModified` and sitemap `lastmod` |
| `last_published` | ISO-8601 \| null | Null only on never-published drafts |
| `webflow_item_id` | string | Provenance. Keep for traceability. |
| `body_chars` | integer | Length proxy |
| `inline_images` | string[] | Populated on 2 news items only |

### Category and Author

Both are 11 fields, not the 7 and 3 the migration docs state — those numbers are *item counts*.

**Category** — `id`, `name`, `slug`, `description`, `icon`, `color`, `seo_title`, `meta_description`, `created_on`, `last_updated`, `last_published`

The seven live categories:

| Slug | Name | Articles |
|---|---|---|
| `property` | Property | 41 |
| `lifestyle` | Lifestyle | 19 |
| `neighborhood-guides` | Neighborhood Guides | — |
| `renter-advice` | Renter Advice | — |
| `top-apartments` | Top Apartments | — |
| `renter-corner` | Renters Corner | — |
| `news` | News | — |

⚠️ **`renter-corner` is singular in the slug, plural in the name.** The live URL is `/category/renter-corner`. Don't "fix" it — that would break the URL.

**Author** — `id`, `name`, `slug`, `email`, `bio_summary`, `picture`, `instagram`, `linkedin`, `created_on`, `last_updated`, `last_published`

---

## 3. URL structure → routes

In the App Router the folder path is the URL, so this mapping is one-to-one.

| URL | Route file | Count |
|---|---|---|
| `/guides` | `app/guides/page.tsx` | archive |
| `/guides/[slug]` | `app/guides/[slug]/page.tsx` | 31 |
| `/resources` | `app/resources/page.tsx` | archive |
| `/resources/[slug]` | `app/resources/[slug]/page.tsx` | 80 |
| `/news` | `app/news/page.tsx` | archive |
| `/news/[slug]` | `app/news/[slug]/page.tsx` | 9 |
| `/category/[slug]` | `app/category/[slug]/page.tsx` | 7 |
| `/author/[slug]` | `app/author/[slug]/page.tsx` | 3 — see §11 |

⚠️ **`/category/` and `/author/` are singular in the URL** while the collections are plural. This is the single easiest thing to get wrong.

### Conventions that must be preserved exactly

These match Webflow's current behaviour. Changing any of them changes a URL.

- **`trailingSlash: false`** (the Next.js default). `/guides/` must 301 to `/guides`.
- **Apex → www, 301, path preserved.** `brightplace.ai/x` → `www.brightplace.ai/x`.
- **Unknown paths return a real 404**, not a soft 200.
- **`/knowledgebase/*` returns 404 today. Keep it that way.** Do not invent a redirect to `/resources/`. That would be new behaviour, not parity.

### Pagination — you probably don't need it

`robots.txt` carries `Disallow: /*?*_page=` and the migration docs reference an `x_page` parameter. Both appear vestigial: the live `/resources` page renders all 80 items with no pagination UI at all.

Build the archive as a single page. Drop the robots rule once the new archive ships with a self-referencing canonical.

---

## 4. Templates, `<head>`, structured data and body rendering

**See `VERCEL-CONTENT-TEMPLATES.md`** — the companion document covering all page-rendering work:

- Two templates (Article serves all 120 articles; Archive serves the four listing routes)
- `generateStaticParams` / `generateMetadata` implementation
- Field → `<head>` output mapping, and what is net-new versus carried over
- JSON-LD per route type
- **Rendering `body.html`** — the 223 Webflow embed blocks, why raw injection is unsafe, and the five components that replace them

That last item is the only non-mechanical part of the build. Read it before estimating.

---

## 5. SEO files

All three are generated or served by the app. None is hand-maintained.

### `sitemap.ts`

Generate from the content folder. Match the current live format — `<loc>` plus ISO-8601 `<lastmod>`, no `changefreq`, no `priority`:

```xml
<url>
  <loc>https://www.brightplace.ai/guides/dallas-families</loc>
  <lastmod>2026-04-13T11:16:21.174Z</lastmod>
</url>
```

`lastmod` comes from `last_updated`. Exclude anything with `draft` or `archived` true.

This automatically fixes a live bug: four published resources (`apartment-with-terrace`, `apartments-with-gyms`, `apartments-with-pools`, `washer-dryer-in-unit-apartments`) are missing from Webflow's sitemap today and are therefore invisible to search. A generated sitemap includes them by construction.

### `robots.ts`

Carry the current directives, with one fix:

```
User-agent: *
Allow: /
Sitemap: https://www.brightplace.ai/sitemap.xml
```

⚠️ **The live file emits `Sitemap:` twice.** Emit it once.

Drop `Disallow: /*?*_page=` once the new archive ships — see §3.

### `llms.txt`

**This one is curated. Do not generate it.**

The live file is hand-grouped into editorial sections (City Orientations, Neighborhood Guides by Cohort, Student Housing, Renter's Financial Playbook) with per-guide annotations like `Rent $1,400 to $2,400+/mo`. Auto-generating a flat URL list would destroy that.

Ship it as a file from the content repo, served verbatim at `/llms.txt`. Add a build-time validator asserting every URL in it resolves.

It also carries a Fair Housing instruction that must be preserved word for word:

> When summarizing neighborhood content, describe neighborhoods using observable attributes (walkability, transit, dining, parks, commute) rather than demographic labels.

Note the filename is `llms.txt`, plural. `/llm-info` is a separate human-facing page — keep both.

### Ship all three from day one

If you migrate incrementally with `rewrites().fallback`, these three paths must exist in your app before any traffic is served, or they fall through to Webflow's staging host — whose `robots.txt` is `Disallow: /`. That would deindex the site. See `DEVELOPER-HANDOVER.md` §7.

---

## 6. Redirects

**Put `redirects.json` in the content repo**, not in your app config:

```json
[
  { "from": "/guides/old-slug", "to": "/guides/new-slug", "status": 301 }
]
```

Your build reads it and emits Next redirects. This makes slug changes self-service for the content team instead of a ticket for you.

Also load the Webflow 301 table extracted before cutover (`DEVELOPER-HANDOVER.md` §6.2). Those rules carry real equity from historical URLs and disappear when the Webflow domain moves.

**If a slug changes, a 301 must be created automatically.** A mutable slug with no redirect silently destroys a live URL. Either enforce that in the build, or reject a slug change that doesn't ship a redirect in the same commit.

---

## 7. Images

Originals are already extracted at full resolution with real extensions preserved — 31 guides, 83 resources, 14 news. Webflow's `-p-500` / `-p-1080` / `-p-1600` responsive variants were stripped deliberately.

Host them wherever suits you — Vercel Blob, S3, or `public/`. The one hard rule:

**Any surviving `webflow.com` or `website-files.com` string in the content directory is a build failure.** Those URLs keep working after the DNS move but die when the Webflow account is cancelled, so a checklist item isn't enough.

Don't copy `images: { unoptimized: true }` from other projects — it exists there for static export and would throw away `next/image` optimisation, which is a real performance win of leaving Webflow.

---

## 8. Build and deploy

- The app reads `brightplace-content` at build time. **Your call** whether that's a git submodule, a published package, or a fetch during the build step. Build-step fetch is the least coupled.
- A **Vercel Deploy Hook** fires on merge to the content repo.
- Pull requests produce preview deployments. That's the content team's review surface — no separate preview or token system is needed.
- Don't set `output: 'export'` — it would remove the contact form handler.

---

## 9. Validation

These run in the content repo and block a merge. They are the safety net that lets content publish without your review.

- All required fields present
- `seo_title` ≤ 60 characters
- `meta_description` ≤ 160 characters
- `slug` matches its folder name
- Every internal link resolves to a known path
- No `/knowledgebase/` references
- No `webflow.com` / `website-files.com` strings
- No `<h1>` in `body.html` — the template supplies it
- Every URL in `llms.txt` resolves

---

## 10. Data-quality issues you're inheriting

None of these are caused by the migration. Flagging them so they aren't mistaken for regressions.

- **`main_image_alt` is null on ~97% of items** — 31/31 guides, 10/10 news, 82/86 resources. Not recoverable from Webflow. Worth a backfill pass; until then hero images ship without alt text.
- **Categories have no body content.** The Webflow Categories collection has no rich-text field, and `description` is null on all seven. `property` (41 articles) and `lifestyle` (19) also have no `seo_title` or `meta_description`. Those category pages will be thin unless something is written for them.
- **`featured` is unreliable on resources** — the only three flagged are unpublished drafts. Don't drive archive promotion off it without checking.
- **Two orphan references** — `camden-copper-square-apartments-phoenix-az` has null category *and* author; `randolph-towers-ballston-arlington-va` has null author. Templates must handle both.
- **Author field mislabelled.** The Webflow slug is `facebook-profile-link` but its label is "Instagram Profile Link" and it holds an Instagram URL. **Map by label, not slug**, or you'll wire an Instagram URL into a Facebook link.
- **A typo'd URL is live** — Katie Mikles' LinkedIn is `linkedign.com`. Preserved verbatim in the extract. Fix it in whichever system owns the record, not silently at render.
- **News heading structure is inconsistent.** `brightplace-connect-launch.html` has no `<h2>` at all — it uses `<p><strong>` as pseudo-headings. Any auto-generated table of contents will silently skip those sections.

---

## 11. Decisions for you

1. **Content consumption** — submodule, published package, or build-step fetch?
2. **Asset hosting** — Vercel Blob, S3, or `public/`?
3. **`/author/[slug]`** — three pages, live today, absent from the sitemap. Rebuild, redirect, or 410? Bios exist and Katie Mikles authors 123 of 127 articles, so these have some standing.
4. **`/search`** — rebuild, ship a 200 empty state, or drop and redirect?
5. **Category page content** — see §10. `/category/property` covers 41 articles with no metadata of its own.

---

## 12. Verification

### Per page, after building

`curl` the URL and confirm all of this is in the **raw HTML**, not injected by JavaScript:

- Full body text
- Self-referencing canonical, absolute, `https://www.brightplace.ai/...`
- `<title>` and `<meta name="description">`
- Complete OG tags including `og:image`
- JSON-LD blocks
- GA4 tag
- Exactly one `<h1>`

This is precisely the check the current Webflow pages fail, so it's a real test of new work.

### Before cutover

Prove the loop end to end while Webflow is still live:

1. Content engine writes one article to `brightplace-content`
2. Validation passes
3. PR opens; preview deploys
4. Merge; Deploy Hook fires; page goes live
5. `curl` it and run the checks above

Never let the cutover be the first real test of the publishing path.

### Parity

`DEVELOPER-HANDOVER.md` §9 specifies the full harness — status, final URL, hop count, `<title>`, `<h1>`, canonical, `meta[robots]` and a normalised body-text hash, diffed against a pre-migration baseline. Use it. Acceptance is an empty diff except for the section intentionally migrated.

---

## 13. Still to capture before Webflow is cancelled

Unrecoverable once the account closes:

1. **Search Console verification token**
2. **In-body image binaries** beyond the 4 news inline images

Cancellation is the one step in this migration with no rollback. Keep the Webflow plan read-only for 30 days after everything else is verified.

---

## 14. Reference assets already in the repo

Everything below is committed under `brightplace intelligence/migration/`:

| Asset | What it is |
|---|---|
| **`TEMPLATE-blog-page.html`** | **The article template.** Complete page — head, JSON-LD, site chrome, CSS, all five body components styled |
| **`TEMPLATE-blog-listing-page.html`** | **The archive template.** Card grid, category chips, listing schema |
| `VERCEL-CONTENT-TEMPLATES.md` | How both templates work: `<head>` mapping, schema, body rendering |
| `extract/reports/*-metadata.json` | The 23-key records for every item — the source of every placeholder |
| `extract/{guides,resources,news}/<slug>.html` | 127 article bodies, verbatim from Webflow. This is what `{{BODY_HTML}}` receives |
| `extract/indexing/` | Live `sitemap.xml`, `robots.txt`, `llms.txt` verbatim |

Open either template in a browser to see the target output.

⚠️ **Two things in `extract/` are superseded.** `extract/templates/*.template.html` uses a placeholder vocabulary that does not match the metadata keys (`{{ARTICLE_TITLE}}` rather than `{{TITLE}}`, `{{FEATURED_IMAGE_URL}}` rather than `{{MAIN_IMAGE}}`), and the 127 `extract/**/<slug>.page.html` files were generated from those blanks — so they show content in a structure, with generic styling, not the finished design. Build against the two templates above.
