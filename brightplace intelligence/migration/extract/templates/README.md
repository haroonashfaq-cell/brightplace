# HTML Templates

Three templates for the Vercel rebuild. They match the structure already used by the AIR operator
Stage-10 articles (`AIR operator/*/…/10-*.html`), so this is the shape the team already works with.

| File | Use |
|---|---|
| `resource.page.template.html` | A single article at `/resources/<slug>` |
| `guide.page.template.html` | A single article at `/guides/<slug>` |
| `listing.template.html` | A collection index: `/resources`, `/guides`, `/news` |

The two article templates are **structurally identical**. They differ only in the BreadcrumbList
`name` / `item` values (`Resources` + `/resources` vs `Guides` + `/guides`). News uses the same
shape with `News` + `/news`.

Filled examples of all three are in the collection folders: `<slug>.page.html` (127 of them) and
`_listing.page.html` (3). Use those to see a template with real data in it.

## Placeholders

Everything in `{{DOUBLE_BRACES}}` is substituted. Source is the per-item record in
`reports/<collection>-metadata.json`.

### Article templates

| Placeholder | Source field | Notes |
|---|---|---|
| `{{SEO_TITLE}}` | `seo_title` | Must differ from the H1. Falls back to `title` if unset. Webflow's live API enforces ~59 chars |
| `{{ARTICLE_TITLE}}` | `title` | The H1 |
| `{{META_DESCRIPTION}}` | `meta_description` | ~154 chars enforced |
| `{{FOCUS_KEYWORD}}` | `focus_keyword` | |
| `{{AUTHOR_NAME}}` | `author` | Resolved from the `author-2` reference. 123 of 127 articles are Katie Mikles |
| `{{CANONICAL_URL}}` | `url` | Absolute, `https://www.brightplace.ai/...` |
| `{{FEATURED_IMAGE_URL}}` | `main_image` | **4 live items are null** — omit the `og:image` and `twitter:image` tags entirely rather than emitting `content=""` |
| `{{DATE_PUBLISHED}}` | `created_on` | `YYYY-MM-DD` |
| `{{DATE_MODIFIED}}` | `last_updated` | `YYYY-MM-DD` |
| `{{DATE_PUBLISHED_READABLE}}` / `{{DATE_MODIFIED_READABLE}}` | derived | e.g. `September 3, 2026` |
| `{{BODY_HTML}}` | `<slug>.html` | See the warning below |

### Listing template

| Placeholder | Notes |
|---|---|
| `{{COLLECTION_NAME}}` | `Renter Guides` · `Renter Resources` · `News` |
| `{{COLLECTION_DESCRIPTION}}` | One line; also used for the meta description |
| `{{COLLECTION_URL}}` | `https://www.brightplace.ai/guides` etc. |
| `{{ITEM_COUNT}}` | Live items only, drafts excluded |
| `{{CATEGORY_NAME}}` | Resolved from `category-2`. **May be null** — omit the badge |
| `{{ARTICLE_SUMMARY}}` | `post-summary` |

The card block repeats once per article, newest first. The template includes both variants: with
an image, and the placeholder used when `main-image` is null.

## Three things the templates encode deliberately

### 1. JSON-LD must be server-rendered

The live Webflow site injects structured data with JavaScript, so **crawlers currently see zero
`application/ld+json` blocks**. It also has no `rel="canonical"` and no real Open Graph tags —
only `og:type="website"`.

Each article template ships three blocks — `Article`, `BreadcrumbList`, `WebPage` (with
`speakable`) — and the listing ships `CollectionPage` + `ItemList` + `BreadcrumbList`. Rendering
these server-side is the single largest SEO gain available in this migration.

Add a `FAQPage` block only when the Q&A is actually visible on the page. Google requires the
markup to match the rendered content.

### 2. Webflow bodies are not clean HTML

Every body contains `<div data-rt-embed-type='true'>` wrappers holding raw HTML fragments — across
the Guides alone, 129 `<head>` tags, 17 `<style>` blocks, 7 `<table>`s and 4 `<body>` tags,
**embedded mid-article**. That is how the info-cards and comparison tables were built.

Before inserting `{{BODY_HTML}}`, strip the document-level tags — `html`, `head`, `body`, `title`,
`meta`, `link` — and **keep everything else, including `<style>`**. Leaving them in produces
invalid markup and leaks CSS across the page.

This is what the generated `.page.html` files do. Longer term these patterns are better expressed
as components (info-card, comparison-table) than as raw embedded HTML.

### 3. The canonical and og:image are filled here

The AIR Stage-10 template leaves `rel="canonical"`, `og:url` and `og:image` empty, with a TODO on
the image. These templates fill all three, because the CMS has the data. Do not ship a page with
an empty canonical.

## Styling

The inline `<style>` block is carried over unchanged from the AIR Stage-10 template. The listing
template adds a card-grid block in the same visual language (responsive `auto-fill` grid, 16:9
thumbnails, pill category badges, single column under 600px).

These are content-page styles, not the brightplace design system. Expect them to be replaced by
the app's own components — they exist so the pages render correctly standalone and so the
structure is legible.
