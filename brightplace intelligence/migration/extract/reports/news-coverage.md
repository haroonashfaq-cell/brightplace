# News Extraction — Coverage Report

**Completed 2026-09-17** · all 10 CMS items extracted

## Result

| Asset | Count |
|---|---|
| `.md` | **10 / 10** — all generated from CMS body |
| `.html` | **10 / 10** |
| Featured image | **10 / 10** |
| Inline body images | **4** (2 articles) |

## Status

| Status | Count |
|---|---|
| Live + in sitemap | 9 |
| Draft (404) | 1 |

The draft is `ten-questions-with-brightplace-founder-brian-lichtenberger-3` — a duplicate of the
published `ten-questions-brightplace-founder`. Included as requested, with a `status:` line in its
markdown marking it as a 404 draft.

## No local markdown existed for News

Unlike Guides (30 of 31 local) and Resources (74 of 79 local), **no News article had a matching
local markdown file**. `brightplace intelligence/News/` contains only
`how-brightplace-earned-30-ai-citations.md` — which does not match any live slug — and a PDF.

All 10 markdown files were therefore generated from the published CMS body, which makes them
**exactly faithful to what is live**. No divergence check is needed or possible here.

## News is the only collection with inline body images

| Collection | Inline `<img>` in body |
|---|---|
| Guides | 0 |
| Resources | 0 |
| **News** | **4** across 2 articles |

- `how-brightplace-became-ai-search-favorite` — 2
- `what-we-learned-about-mcp-building-brightplace-connect` — 2

Saved as `<slug>-inline-1.png`, `<slug>-inline-2.png`. These sit inside Webflow
`<figure class="w-richtext-figure-type-image">` wrappers — screenshots of AI Overview results
embedded in the article body.

**Implication:** Guides and Resources need only a featured-image pipeline. News additionally needs
in-body image handling, and the `<figure>` wrapper markup carries Webflow-specific classes
(`w-richtext-figure-type-image`, `w-richtext-align-fullwidth`) that will need replacement styling
in the rebuild.

## Method

One MCP batch of 20 against collection `6a32f0722779d53e287b5cc5` (52.5 KB, persisted to disk).

Note: this response came back in a different wrapper shape than the Guides and Resources batches —
an MCP content-block array rather than a bare result object. The extraction script handles both.

Per-item metadata: `reports/news-metadata.json`.
