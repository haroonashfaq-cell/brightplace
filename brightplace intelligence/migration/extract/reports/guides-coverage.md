# Guides Extraction — Coverage Report

**Completed 2026-09-17** · 31/31 live guides extracted

## Result

| Asset | Count | Source |
|---|---|---|
| `.md` | **31 / 31** | 30 copied from `Guide Articles/Complete Articles/`; 1 generated from CMS body |
| `.html` | **31 / 31** | Webflow CMS `post-body`, verbatim |
| Image | **31 / 31** | Webflow CMS `main-image`, original resolution |

Slug-for-slug match against the live sitemap: **no missing items, no extras.**
No drafts in the Guides collection. Total size 41 MB.

Image formats: 29 `.jpg`, 1 `.png`, 1 `.webp` — real extensions preserved, so files open correctly.
Webflow serves responsive variants (`-p-500`, `-p-1080`, `-p-1600`); the **original** was taken in
every case, not a downscaled variant.

## Finding 1 — every guide body contains Webflow embed blocks

All 31 bodies contain `<div data-rt-embed-type='true'>` wrappers — Webflow rich-text embed
components holding raw HTML fragments:

| Embedded element | Occurrences |
|---|---|
| `<head>` | 129 |
| `<div>` | 48 |
| `<style>` | 17 |
| `<table>` | 7 |
| `<body>` | 4 |

These are **mini-documents inside the article body**, complete with their own `<head>` and inline
`<style>` blocks. They are how the info-cards and comparison tables were built in Webflow.

**Why this matters for the rebuild:** the bodies are not clean semantic HTML. Rendering them
as-is in Next.js will inject stray `<head>`, `<body>` and `<style>` tags into the middle of the
page, which is invalid markup and will leak CSS across the page. The developer must decide per
pattern whether to sanitise into components (info-card, comparison-table) or preserve as scoped
raw HTML. **This is a build decision, not an extraction problem** — the content is captured
faithfully.

## Finding 2 — one guide's local markdown is stale

A word-count comparison of local `.md` against the published CMS body:

- **30 of 31 are in sync** (ratio 1.01–1.08; markdown runs slightly longer because HTML tags are
  stripped and link text is retained)
- **1 outlier: `dallas-families` at 0.65** — the local markdown is ~35% shorter than what is
  published. 3,145 words in the CMS vs 2,059 in the local file.

The published CMS version is authoritative. `dallas-families.html` is correct; its `.md` is an
older draft and should be regenerated from the body before the developer uses it. Flagged rather
than silently overwritten, since the difference may be deliberate.

## Method

Content was pulled via the Webflow MCP in 2 batches of 16 against collection
`69dccfeabed64ec697c4f7d2`. Responses (508 KB and 326 KB) auto-persisted to disk and were parsed
locally, so nothing was truncated.

Per-item metadata — SEO title, meta description, focus keyword, category, author, dates, Webflow
item ID, inline image URLs — is in `reports/guides-metadata.json`.

Reference IDs resolved via `reports/lookups.json` (7 categories, 3 authors).

## Known data quirks recorded during extraction

- Authors field slug `facebook-profile-link` is **labelled "Instagram Profile Link"**, and Katie
  Mikles' value is an `instagram.com` URL. Map by label, never by slug.
- Katie Mikles' `linkedin-profile` contains a typo in the live data: `www.linkedign.com`.
