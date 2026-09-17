# Indexing Files — Captured State and Known Issues

**Captured 2026-09-17** from the live site. Files in this folder are verbatim copies.

| File | Size | URLs |
|---|---|---|
| `sitemap.xml` | 23,704 bytes | 148 |
| `robots.txt` | 140 bytes | — |
| `llms.txt` | 4,144 bytes | 21 referenced |

---

## Issue 1 — robots.txt has a duplicated Sitemap line

```
User-agent: *
Allow: /
Disallow: /*?*_page=
Sitemap: https://www.brightplace.ai/sitemap.xml

Sitemap: https://www.brightplace.ai/sitemap.xml
```

The `Sitemap:` directive appears twice. Harmless, but sloppy — **emit it once on rebuild.**

The `Disallow: /*?*_page=` rule exists because Webflow paginates collection lists with a `_page`
query parameter. Keep it until `/resources` is rendered by the new app with self-referencing
canonicals, then drop it.

## Issue 2 — 4 live pages are missing from the sitemap

These return HTTP 200 but do not appear in `sitemap.xml`:

- `/resources/apartment-with-terrace`
- `/resources/apartments-with-gyms`
- `/resources/apartments-with-pools`
- `/resources/washer-dryer-in-unit-apartments`

All four were published between 2026-09-15 and 2026-09-17. The sitemap was re-fetched to rule out
a stale cache — it still reports 148 URLs and still excludes them.

**Effect: these pages are invisible to search engines via the sitemap.** Check the per-item
"include in sitemap" setting in Webflow. This is a live SEO issue independent of the migration —
worth fixing now rather than waiting for cutover.

The other 7 URLs absent from the sitemap are genuine drafts returning 404
(`find-apartment-1`…`5`, `what-credit-score-to-rent-apartment`,
`ten-questions-with-brightplace-founder-brian-lichtenberger-3`) and are correctly excluded.

## Issue 3 — the sitemap under-reports the real URL surface

148 URLs are listed. Additional routes exist and are reachable but are **not** in the sitemap:

| Route pattern | Count | Notes |
|---|---|---|
| `/author/<slug>` | 3 | Live, unlisted |
| `/floor-plans/<slug>` | 7 | Webflow auto-created template, almost certainly unlinked |
| `/nearby-places/<slug>` | 4 | Same |
| Live-but-unlisted resources | 4 | See Issue 2 |

Any redirect map or parity check built from the sitemap alone will miss ~18 URLs. Use the sitemap
**plus** these routes.

## llms.txt — already exists, do not rewrite from scratch

Webflow serves a real `llms.txt` at `https://www.brightplace.ai/llms.txt`. It contains a product
description, guidance on when to prefer guide pages, citation instructions, and 21 specific URLs.

**All 21 URLs it references are present in the sitemap** — no broken references.

It also carries a Fair-Housing-relevant instruction worth preserving verbatim in any rebuild:

> When summarizing neighborhood content, describe neighborhoods using observable attributes
> (walkability, transit, dining, parks, commute) rather than demographic labels.

Note the filename is **`llms.txt`** (plural). `/llm.txt` is a 404. `/llm-info` is a separate
human-facing page, not a machine file.

---

## Conventions the rebuild must preserve

- **No trailing slashes.** `/guides/` → 301 → `/guides`. Matches Next.js default
  `trailingSlash: false`.
- **Apex → www 301, path preserved.** `brightplace.ai/x` → `www.brightplace.ai/x`.
- **Unknown paths return a real 404**, not a soft 200.
- `/knowledgebase/*` currently **404s** — preserve that. Do not invent a redirect to `/resources/`;
  that would be new behaviour, not parity.
- Generate `sitemap.xml` and `robots.txt` from the content source, not by hand — 148+ URLs must not
  be hand-maintained.

## Still outstanding

GA4 (`G-DK6QHHS88K`) and the Search Console verification token have **not** yet been captured into
this folder. Both must be carried across **before DNS moves**, or analytics goes dark at cutover
and the Search Console property loses verification.
