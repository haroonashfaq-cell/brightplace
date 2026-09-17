# Server-side JSON-LD for the Resources template (NOT YET APPLIED)

Blocked on 2026-09-17 by the Claude Code auto-mode permission classifier
("Modify Shared Resources") because it writes to a CMS template that renders
all ~76 /resources/ pages at once.

## What it fixes
Resource pages currently ship EMPTY JSON-LD tags:
`<script type="application/ld+json" id="bp-article"></script>`
filled client-side by an inline script. Google's renderer may pick it up late;
GPTBot, PerplexityBot and ClaudeBot never will. Four of five audited pages also
ship no datePublished/dateModified at all, because the Resources collection has
no date field (verified: post-body, post-summary, main-image, thumbnail-image,
featured, color, author-2, category-2, seo-title, meta-description,
focus-keyword, name, slug).

## How to apply
Webflow MCP, data_pages_tool:
  bulk_update_pages_schema_markup
    site_id: 69d6907887b739e09622100f
    pages: [{ id: "69fcfcef26d35b66ba874fa4", rawJsonLdSchema: <contents of resources-template-jsonld.json as a single string> }]
Then publish the site.

## Verify after applying
1. curl a resource page and confirm a NON-EMPTY <script type="application/ld+json">
   appears in the raw HTML (not just the bp-article/bp-bread/bp-faq stubs).
2. Check /resources/university-club-apartments specifically: its `name` field
   contains escaped double quotes ("University Club Apartments"), the only such
   item in the collection. If Webflow does not escape it, that page's JSON-LD
   will be malformed. Fix by removing the quotes from that item's name, or swap
   the `name` binding for `seo-title` (verified quote-free across all 86 items).
3. Confirm created-on / updated-on / main-image bindings actually resolve.
   If a binding renders literally, drop that property and re-publish.

## Known follow-up
This adds server-side Article + BreadcrumbList while the existing inline script
still injects its own Article + BreadcrumbList + FAQPage client-side, so Google
would see duplicate nodes. To finish cleanly, remove the Article and Breadcrumb
generation from the embed in the Resources template (keep the FAQ scraper, which
cannot be reproduced server-side). That edit needs the Webflow Designer, which
was not connected during this session.
