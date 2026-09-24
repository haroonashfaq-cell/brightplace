# Content Output Configuration

> Source of truth for where finished content goes and what shape it takes.
> Last updated: 2026-09-24. Replaces the Webflow CMS configuration.

## Publishing model

Webflow is retired. The site is Next.js on Vercel and builds from GitHub.
There is no CMS, no API push, and no MCP call in the publishing path.

```
Agent writes files → brightplace content/<collection>/ → git commit → GitHub → Vercel build → live
```

An article is published by landing in the output folder and being committed.
Commit only when the user explicitly asks.

## Output location

```
brightplace content/
├── guides/      → www.brightplace.ai/guides/<slug>
├── news/        → www.brightplace.ai/news/<slug>
└── resources/   → www.brightplace.ai/resources/<slug>
```

The folder name is the URL prefix. The file name is the URL segment.

**Routing:**
- `resources/` — all new resource, property, neighborhood and Renter's Corner articles.
  This is the default.
- `news/` — announcements only, and only on an explicit news task. Its presence is not
  permission to route ordinary articles there.
- `guides/` — **restricted.** Do not write here without explicit user instruction.

## File set per article

Three files, one slug. Format matches `migration/extract/`, the Webflow pull the
live site was built from, so new articles are shaped like the 127 already published.

| File | Contents |
|---|---|
| `<slug>.md` | Full article, markdown, with YAML frontmatter. The archival record. |
| `<slug>.html` | Body only — a fragment. No `<head>`, no nav, no footer. |
| `<slug>.<ext>` | Featured image, original resolution. `png`, `jpg`, `jpeg` or `webp`. |

## Frontmatter schema (`<slug>.md`)

```yaml
---
title: "..."                     # renders as the <h1>
seo_title: "... | brightplace"   # <title>. Must differ from title. Under 60 chars.
meta_description: "..."          # under 155 chars
slug: ...                        # matches the file name and the URL segment
primary_keyword: "..."
secondary_keywords: ["...", "..."]
schema_types: ["Article", "FAQPage", "WebPage"]
word_count_target: "1,100-1,300"
last_reviewed: "Month YYYY"
date_published: YYYY-MM-DD
date_modified: YYYY-MM-DD
author: Katie Mikles
---
```

**`author` is `Katie Mikles`, not `brightplace`.** The old drafts carried
`author: brightplace` (76 of 86 resource drafts) because Webflow overrode it with the
real author on publish. Nothing overrides it now — the frontmatter is the only source,
and the live site shows Katie Mikles on 123 of 127 articles. Writing `brightplace`
there would publish a wrong byline.

### Fields the page template also needs

The Vercel template builds the `<head>`, byline, breadcrumb and JSON-LD from the
article record. Three values it needs are not in the frontmatter above:

| Field | Value | Notes |
|---|---|---|
| `category` | category slug | One of the seven below |
| `summary` | first paragraph, plain text, under 300 chars | Intro and `og:description` fallback |
| `main_image_alt` | alt text for the featured image | Stage 5 already produces this |
| `main_image` | absolute URL, see below | Verified against the live site 2026-09-24 |

Add these to frontmatter. They were CMS fields under Webflow, so the pipeline already
produces every one of them; this is a relocation, not new work.

### Featured image URL (verified, not assumed)

The live site serves content images at:

```
https://www.brightplace.ai/content/<collection>/<slug>.<ext>
```

Note `/content/` in the path. It is **not** `/resources/<slug>.<ext>` — that returns 404.

Confirmed 2026-09-24 by reading `og:image` off live pages and fetching the files:
`.png` (200, image/png) and `.webp` (200, image/webp) both serve, so the Stage 5 WebP
output needs no conversion. Articles with no image fall back to `/brightplace-logo.png`.

Use this exact URL in `main_image` and in the Article schema `image` property.

### Category slugs

`property` · `lifestyle` · `neighborhood-guides` · `renter-advice` ·
`top-apartments` · `renter-corner` · `news`

⚠️ `renter-corner` is **singular** in the slug and plural in the display name
("Renters Corner"). The live URL is `/category/renter-corner`. Do not "fix" it.

## Body rules (`<slug>.html`)

- **No `<h1>`.** The template supplies it from `title`. A body with an `<h1>` puts two
  on the page. The old Webflow step stripped it; whatever converts markdown → html now
  must do the same.
- Opens with `<p><em>Last reviewed: Month YYYY</em></p>`, then the first `<h2>`.
- **FAQ questions are `<h3>`, not `<p><strong>`.** Measured across the live corpus:
  86 of 86 Resources bodies contain `<h3>`, and 82 of 86 use it for FAQ questions.
- **No `<script>`.** Schema is server-rendered by the template from frontmatter.
  Keep the JSON-LD blocks in the `.md`; never carry them into the body html.
- No `<head>`, `<body>`, `<style>` or `<base>` tags. No
  `<div data-rt-embed-type='true'>` wrappers — those were a Webflow rich-text artifact
  and the template now renders cards and tables as components.
- No frontmatter, no duplicate H1, no internal review notes.
- `<ul><li>` is now **allowed**. The ban existed because Webflow RichText stripped
  the tags. Vercel does not. Bold-label bullets remain the editorial preference for
  comparisons, but lists no longer break the page.
- `<table>` is allowed for the same reason.

## Image

1200 x 628, 16:9, under 200KB, no people visible (Fair Housing), no text or logos.
Named by slug. Same spec Stage 5 has always produced.

The user no longer needs to add the featured image separately — it ships in the commit.

## Draft handling

There is no draft flag in this file set. An article is live once committed and built.
Anything not ready to publish stays out of `brightplace content/` and lives in
`Complete Articles/` until it passes QA.

## Provenance

The Webflow site (`69d6907887b739e09622100f`), its collection, author and category IDs,
and the `post-body` / `post-summary` / `author-2` / `category-2` field mapping are
retired as of the 2026-09 migration. They are preserved in
`migration/migration planning/DEVELOPER-GUIDE-VERCEL-CMS.md` and
`migration/extract/reports/` for traceability. Do not use them to route new content.
