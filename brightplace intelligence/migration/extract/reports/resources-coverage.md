# Resources Extraction — Coverage Report

**Completed 2026-09-17** · all 86 CMS items extracted

## Result

| Asset | Count |
|---|---|
| `.md` | **86 / 86** |
| `.html` | **86 / 86** |
| Image | **83 / 86** (3 have no `main-image` in the CMS) |

Total with guides: 71 MB.

## Status breakdown — the sitemap is not the full picture

| Status | Count | Meaning |
|---|---|---|
| Live + in sitemap | **76** | Indexed normally |
| **Live, NOT in sitemap** | **4** | Reachable (HTTP 200) but Webflow is not listing them |
| Draft (404) | 6 | `isDraft: true`, not reachable |

Per-item detail: `reports/resources-status-table.md`.

**The 4 live-but-unlisted resources:**
`apartment-with-terrace` · `apartments-with-gyms` · `apartments-with-pools` ·
`washer-dryer-in-unit-apartments`

All four return HTTP 200 and were published between 2026-09-15 and 2026-09-17, but the sitemap
still lists 148 URLs and does not include them. I re-fetched the sitemap to rule out a stale cache
— it had not changed. **These pages are invisible to search engines via the sitemap.** Worth
investigating in Webflow (the per-item "include in sitemap" setting) independently of the
migration.

`washer-dryer-in-unit-apartments` returned 404 at the start of extraction and 200 roughly ten
minutes later — it was published mid-run. Content is moving while this snapshot is being taken, so
re-verify counts close to cutover.

**The 6 drafts** (`find-apartment-1` … `find-apartment-5`, `what-credit-score-to-rent-apartment`)
are included as requested. They are 404 on the live site and their markdown carries a `status:`
line saying so, so nobody mistakes them for published pages.

## Resources with no featured image

`what-credit-score-to-rent-apartment` (draft) · `randolph-towers-ballston-arlington-va` ·
`las-brisas-apartments-california`

`main-image` is null in the CMS for these three. Not an extraction failure — the field is empty.

## Finding — local markdown is systematically out of date

74 resource `.md` files came from `brightplace intelligence/Complete Articles/`. Comparing each
against the published CMS body by word count:

- **median ratio 1.46** — the local markdown is consistently ~46% longer than what is published
- **69 of 74 fall outside the 0.8–1.25 band**, ranging from 1.26 to 1.57

This is the opposite pattern to the Guides, where 30 of 31 matched within 1.01–1.08.

The likely explanation is that these markdown files are the **full drafts**, and the published
Webflow versions were trimmed during editing. The consistency of the gap (a tight 1.4–1.55 cluster
rather than random scatter) points to a systematic editing step, not sporadic divergence.

**Implication for the developer: `.html` is authoritative, not `.md`.** The `.html` files are the
exact published bodies. The `.md` files are useful as source/reference but must not be treated as
what is live — migrating from them would republish ~46% more text than the site currently serves.

Full per-item ratios: `reports/resources-divergence.json`.

## Method

4 MCP batches of 22 against collection `69fcfcef26d35b66ba874f9d`. Responses (422 KB, 350 KB,
339 KB, 320 KB) auto-persisted to disk and parsed locally, so nothing was truncated.

Images taken from CMS `main-image` at original resolution — Webflow's `-p-500` / `-p-1080` /
`-p-1600` responsive variants were stripped to fetch the source file. Real extensions preserved
(71 png, 9 webp, 5 jpeg, 29 jpg across both collections).

Per-item metadata — SEO title, meta description, focus keyword, category, author, dates, Webflow
item ID, inline image URLs — is in `reports/resources-metadata.json`.
