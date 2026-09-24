# brightplace content

Final, ready-to-push output. Everything in here is what goes to GitHub for the site build.

Webflow is retired. There is no CMS push step any more — an article is published by
landing here and being committed.

## Layout

```
brightplace content/
├── guides/      → www.brightplace.ai/guides/<slug>
├── news/        → www.brightplace.ai/news/<slug>
└── resources/   → www.brightplace.ai/resources/<slug>
```

The folder name is the URL prefix. The file name is the URL segment.

All paths below are relative to `brightplace intelligence/`, per `AGENTS.md`.

## File set per article

Three files, all named by the same slug. The format matches
`migration/extract/` — the Webflow pull the live site was built from — so new
articles are shaped exactly like the 127 already on the site.

| File | Contents |
|---|---|
| `<slug>.md` | Full article, markdown, with YAML frontmatter |
| `<slug>.html` | Body only — a fragment, no `<head>`, no nav, no footer |
| `<slug>.<ext>` | Featured image. Real extension: `png`, `jpg`, `jpeg` or `webp` |

The image is served at `https://www.brightplace.ai/content/<collection>/<slug>.<ext>`
(note `/content/` in the path). Verified live 2026-09-24; both `.png` and `.webp` serve
correctly. Use that absolute URL in `main_image` and in the Article schema.

### Frontmatter keys (`<slug>.md`)

```yaml
---
title: "..."                  # renders as the <h1>
seo_title: "... | brightplace"  # <title>; must differ from title
meta_description: "..."       # under 155 chars
slug: ...                     # matches the file name
primary_keyword: "..."
secondary_keywords: ["...", "..."]
schema_types: ["Article", "FAQPage", "WebPage"]
word_count_target: "1,100-1,300"
last_reviewed: "Month YYYY"
date_published: YYYY-MM-DD
date_modified: YYYY-MM-DD
author: ...
---
```

### Body rules (`<slug>.html`)

- **No `<h1>`.** The page template supplies it from `title`. A body that opens with
  an `<h1>` produces two on the page.
- Opens with the `<p><em>Last reviewed: Month YYYY</em></p>` line, then the first `<h2>`.
- **FAQ questions are `<h3>`.** Every one of the 86 live Resources bodies contains
  `<h3>` (corpus range 7 to 11), and 82 of 86 use it for FAQ questions. Write them as
  `###` in the markdown, never as bold paragraphs.
- Internal links site-relative (`/resources/<slug>`), never apex `https://brightplace.ai`
  — apex 301s to www, so an apex link costs a needless redirect hop.
- No `<head>`, `<body>`, `<style>` or `<base>` tags. The Webflow rich-text embed blocks
  (`<div data-rt-embed-type='true'>`) that caused this on the old site do not belong in
  new bodies.
- No `<script>`. Schema is server-rendered by the template from frontmatter.

### Image

1200 x 628, 16:9, under 200KB, no people visible (Fair Housing), no text or logos.
Same spec as Stage 5 has always produced.

## What does not change

Every earlier stage writes where it always did:

| Stage | Still writes to |
|---|---|
| 0 Brief | `Content Brief/` |
| 2 Brief Check | `Brief Check/` |
| 2.5 Reddit | `Reddit Research/` |
| 3 Writing | `Complete Articles/` |
| 4 QA | `QA Reports/` |
| 5 Image | `Images/` |

Same agents, same gates, same QA. Only the final step changed.
