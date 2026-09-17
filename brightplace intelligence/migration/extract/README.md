# brightplace.ai — Webflow Content Extract

**Extracted 2026-09-17** from the live Webflow CMS via the Webflow Data API.
407 files, 75 MB.

## What this is

Every piece of CMS content on `www.brightplace.ai`, pulled straight from Webflow, as flat files
named by slug. Three files per item:

```
<slug>.md          text with YAML frontmatter (title, URL, SEO fields, category, author, dates)
<slug>.html        the published body, verbatim from the Webflow CMS
<slug>.page.html   standalone rendered page — full SEO head, OG, JSON-LD, inline styles
<slug>.<ext>       the featured image, original resolution
```

### `.page.html` — the full-page render

Built to match the AIR operator Stage-10 article template
(`AIR operator/*/…/10-*.html`), so it is the same shape the team already works with.
127 pages, one per Guide, Resource and News item. Each carries:

- SEO `<title>`, meta description, keywords, author, robots
- **Filled** `rel="canonical"` and `og:url` — the AIR template leaves these empty
- **Filled** `og:image` from the CMS featured image — the AIR template has a TODO here
- Open Graph + Twitter Card, `article:published_time` / `article:modified_time`
- **3 JSON-LD blocks server-rendered**: Article, BreadcrumbList, WebPage (with `speakable`)
- schema.org microdata on `<article>`, `<time>`, `articleBody`
- The AIR template's inline stylesheet, unchanged

All 381 JSON-LD blocks parse as valid JSON. 3 pages have an empty `og:image` — those are the
3 items with no `main-image` in the CMS.

**This is what the live site does not have.** Today's Webflow pages ship **zero** JSON-LD in the
server HTML, no canonical, and no real OG tags. These files show the target state.

## Contents

| Folder | Items | `.md` | `.html` | images |
|---|---|---|---|---|
| `guides/` | 31 | 31 | 31 | 31 |
| `resources/` | 86 | 86 | 86 | 83 |
| `news/` | 10 | 10 | 10 | 14 |
| `categories/` | 7 | 7 | 7 | 4 |
| `authors/` | 3 | 3 | 3 | 1 |
| `indexing/` | — | sitemap.xml · robots.txt · llms.txt · notes.md | | |
| `reports/` | — | coverage, metadata, status tables | | |

## Read these first

1. **`reports/resources-coverage.md`** — contains the most important finding (below)
2. **`indexing/notes.md`** — live SEO issues found during extraction
3. `reports/guides-coverage.md` · `reports/news-coverage.md` ·
   `reports/categories-authors-coverage.md`

## Three things that will bite if missed

### 1. `.html` is authoritative. `.md` is not.

For **Resources**, the local markdown is systematically **~46% longer** than what is published
(median ratio 1.46; 69 of 74 outside the 0.8–1.25 band). Those `.md` files are full drafts; the
Webflow versions were trimmed during editing.

**Migrating from `.md` would republish roughly 46% more text than the site currently serves.**

Guides are the opposite — 30 of 31 match within 1.01–1.08. News markdown was generated from the
CMS body directly, so it matches exactly.

### 2. Every body contains Webflow embed blocks

All bodies carry `<div data-rt-embed-type='true'>` wrappers holding raw HTML — across the Guides
alone that is 129 `<head>` tags, 17 `<style>` blocks, 7 `<table>`s and 4 `<body>` tags **embedded
mid-article**. They are how the info-cards and comparison tables were built.

Rendering them as-is in Next.js injects stray `<head>`/`<style>` into the page — invalid markup,
and the CSS leaks. Decide per pattern: sanitise into components, or preserve as scoped raw HTML.
The content is captured faithfully; this is a build decision, not an extraction gap.

The `.page.html` files show one workable answer: document-level tags (`<html>`, `<head>`,
`<body>`, `<title>`, `<meta>`, `<link>`) are stripped while **everything else is kept, including
`<style>`**, so the page renders and validates. `<slug>.html` remains the untouched payload.

### 3. The sitemap is not a complete URL inventory

148 URLs are listed, but ~18 more are live and unlisted: 4 published resources, 3 `/author/`
pages, 7 `/floor-plans/`, 4 `/nearby-places/`. Any redirect map built from the sitemap alone will
miss them. Detail in `indexing/notes.md`.

## Other notes

- **Images** were taken from the CMS `main-image` field at **original resolution** — Webflow's
  `-p-500` / `-p-1080` / `-p-1600` responsive variants were stripped. Real file extensions are
  preserved (png / jpg / jpeg / webp), so files open correctly.
- **News is the only collection with inline body images** (4 across 2 articles, saved as
  `<slug>-inline-N.png`). Guides and Resources need only a featured-image pipeline.
- **Drafts are included** and marked with a `status:` line in their frontmatter. 6 resource drafts
  and 1 news draft return 404 on the live site.
- **Categories have no rich-text body field** — `/category/` pages have no editorial content at
  all. `property` (41 articles) and `lifestyle` (19) have no SEO title or meta description either.
- **Katie Mikles authors 123 of 127 articles.**
- Two live-data quirks preserved verbatim rather than silently fixed: the Authors field slug
  `facebook-profile-link` is labelled *"Instagram Profile Link"* and holds an instagram.com URL;
  and Katie's LinkedIn URL is typo'd as `linkedign.com`.

## Not included yet

- HTML design templates (how the Guides/Resources *listing* pages are laid out)
- GA4 (`G-DK6QHHS88K`) and the Search Console verification token — **must be carried across before
  DNS moves**
- In-body image binaries beyond the News inline images

## How it was extracted

Webflow MCP, batched, against site `69d6907887b739e09622100f`. Responses (320–508 KB each) were
persisted to disk and parsed locally, so nothing was truncated. Category and author reference IDs
were resolved to names via `reports/lookups.json`.
