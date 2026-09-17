# Vercel Content Templates — brightplace.ai

**Version 1 · 2026-09-18**
**Audience:** Dennis
**Companion to:** `DEVELOPER-GUIDE-VERCEL-CMS.md` — that document covers scope, the content repo, routes, SEO files, redirects and verification. This one covers **how the pages render**: template structure, `<head>` generation, structured data, and the body-HTML problem.

Read the guide's §2 (content schema) and §3 (routes) first — everything here assumes them.

**Working references, all committed:**

| Path | What it gives you |
|---|---|
| `extract/templates/guide.page.template.html` | Blank article template with `{{PLACEHOLDER}}` slots |
| `extract/templates/resource.page.template.html` | Same shape, different breadcrumb |
| `extract/templates/listing.template.html` | Blank archive template |
| `extract/templates/README.md` | Placeholder → metadata field mapping |
| `extract/<collection>/<slug>.page.html` | 127 filled examples — the same templates with real data |
| `extract/<collection>/_listing.page.html` | 3 filled archive examples |

The two article templates are structurally identical, differing only in the BreadcrumbList `name` and `item` values. News reuses the same shape.

---

## 1. Two templates cover everything

Guides, resources and news are field-identical, so one article template serves all 120 live articles across three URL prefixes. A second template serves the archives.

| Template | Serves | Count |
|---|---|---|
| **Article** | `/guides/[slug]`, `/resources/[slug]`, `/news/[slug]` | 120 pages |
| **Archive** | `/guides`, `/resources`, `/news`, `/category/[slug]` | 10 pages |

---

## 2. Article template

### Structure

Taken from the supplied rendered samples (`HTML sample.html`, `Resources-HTML template.html`):

```
header
  breadcrumb
  h1                ← from index.json `title`
  author block      ← from `author`, links to /author/<slug>
body                ← body.html renders here
CTA section
footer
```

### Implementation

```tsx
// app/guides/[slug]/page.tsx
// resources and news are identical bar the collection string

export async function generateStaticParams() {
  return getSlugs('guides')          // reads brightplace-content/guides/
}

export async function generateMetadata({ params }): Promise<Metadata> {
  const item = getItem('guides', params.slug)
  const url = `https://www.brightplace.ai/guides/${item.slug}`

  return {
    title: item.seo_title,
    description: item.meta_description,
    alternates: { canonical: url },
    openGraph: {
      title: item.seo_title,
      description: item.meta_description ?? item.summary,
      images: item.main_image ? [item.main_image] : [],
      url,
      type: 'article',
      publishedTime: item.last_published,
      modifiedTime: item.last_updated,
    },
  }
}
```

**Items with `draft` or `archived` set to true are excluded from `generateStaticParams`**, so they never build a page. That is the entire draft mechanism — no separate preview system is needed, because pull requests already produce preview deployments.

---

## 3. Archive template

Card listing. No breadcrumb. Related posts section.

Cards use `thumbnail_image`, falling back to `main_image`.

⚠️ **The fallback is load-bearing, not defensive** — `thumbnail_image` is null on 18 of 31 guides, 10 of 86 resources and 3 of 10 news.

### Pagination — you probably don't need it

`robots.txt` carries `Disallow: /*?*_page=` and the migration docs reference an `x_page` parameter. Both appear vestigial: the live `/resources` page renders all 80 items with no pagination UI at all.

Build the archive as a single page. Drop the robots rule once the new archive ships with a self-referencing canonical.

---

## 4. Generating the `<head>`

**The content team owns the values. You own the rendering.** Nobody hand-writes a meta tag.

| `index.json` field | Output |
|---|---|
| `title` | `<h1>` |
| `seo_title` | `<title>` |
| `meta_description` | `<meta name="description">`, `og:description` |
| `summary` | Intro paragraph, `og:description` fallback |
| `main_image` | Hero `<img>`, `og:image` |
| `main_image_alt` | Hero `alt` |
| `author` | Byline, link to `/author/<slug>`, Person schema |
| `category` / `category_name` | Breadcrumb, category link |
| `last_published` | `article:published_time`, `datePublished`, visible `<time>` |
| `last_updated` | `article:modified_time`, `dateModified`, sitemap `lastmod` |
| *derived* | **Self-referencing canonical** — built from prefix + slug, never authored |

### What is net-new versus carried over

Measured across the three supplied rendered samples:

| | Guide | Resource | Archive | After migration |
|---|---|---|---|---|
| Canonical | ✗ | ✗ | ✗ | **Required** |
| Meta description | ✗ | ✗ | ✗ | **Required** |
| JSON-LD | 0 | 0 | 0 | **Required** |
| OG tags | partial, no image | only `og:image` | partial | **Complete set** |
| Visible `<time>` | ✗ | ✗ | ✗ | **Required** |
| Breadcrumb | ✓ | ✓ | ✗ | Keep |
| GA4 `G-DK6QHHS88K` | ✓ | ✓ | ✓ | **Carry across** |

Every page on the current site ships without a canonical, without a meta description and without structured data. Closing that gap is a large share of this migration's value — so treat the first five rows as acceptance criteria, not nice-to-haves.

**GA4 already exists on Webflow.** Carry the existing measurement ID across; do not create a new property. It must be live on the new routes before DNS moves, or analytics goes dark at cutover.

---

## 5. Structured data

All JSON-LD must appear in the **server-rendered HTML**. JS injection is precisely what is broken today — the current pages inject schema client-side, where crawlers do not reliably see it.

| Route | Schemas |
|---|---|
| `/guides/[slug]`, `/resources/[slug]`, `/news/[slug]` | `Article`, `BreadcrumbList`, `WebPage` (with `speakable`), `FAQPage` where FAQs exist |
| `/guides`, `/resources`, `/news` | `CollectionPage`, `BreadcrumbList` |
| `/category/[slug]` | `CollectionPage`, `BreadcrumbList` |
| `/author/[slug]` | `Person`, `BreadcrumbList` |

`Article` must carry `headline`, `datePublished`, `dateModified`, `author` (as `Person`), `publisher`, `image` and `mainEntityOfPage`.

Verify with Google's Rich Results Test on one URL per collection. Since zero JSON-LD ships today, this is a genuine check on new work rather than a formality.

---

## 6. Rendering `body.html` — the hard part

Read this section carefully. It is the only part of the build that is not mechanical.

### What's in the bodies

Bodies are **fragments**, not documents. They start at `<h2>` — **no article body contains an `<h1>`**, because the template supplies it.

⚠️ **Author bios are the exception.** All three open with their own `<h1>` ("About Katie", etc.). The author template must not add a second one.

But bodies also contain **223 Webflow rich-text embed blocks** wrapped in `<div data-rt-embed-type='true'>`, holding malformed mini-documents:

- 145 `<head>` tags
- 149 `<body>` tags
- 190 `<style>` blocks
- 1 `<!DOCTYPE html>` and `<html lang="en">`
- 1 `<base target="_blank">`

All nested **mid-article**. This is how the info cards and comparison tables were built in Webflow.

**Distribution is lopsided — all 31 guides have embeds (1 to 17 each), only 1 of 86 resources does, and news has none.** This is effectively a guides problem.

### Why you cannot inject this raw

`dangerouslySetInnerHTML` on these bodies produces invalid markup and leaking CSS. The `<style>` blocks use **bare element selectors**:

```css
table { width: 100%; border-collapse: collapse; }
tr:nth-child(even) { background-color: #f2f2f2; }
body { font-family: Arial, sans-serif; background: #f5f5f5; }
```

That restyles every table on the page, and the page body itself.

And `guides/fort-collins-outdoor-renters.html` contains `<base target="_blank">`. If that escapes its wrapper, **every link on the page opens in a new tab.**

### The five patterns

223 blocks, but only five recurring patterns:

| Pattern | Count | Suggested component |
|---|---|---|
| Property card — "WORTH LOOKING AT" + name + address/operator/price + bullets + CTA button | 74 | `<PropertyCard>` |
| Callout box — titled tinted box | 39 | `<Callout>` |
| Comparison table | 33 | `<ComparisonTable>` |
| Info-card row — Market / Lifestyle / Price Range / Last Reviewed | 31 | `<StatCardRow>` |
| CTA box — centred italic pitch + link | 25 | `<CTABox>` |
| Unclassified residue | 21 | variants of the above |

All 33 `<table>` elements in the corpus are inside embeds. There are no bare rich-text tables.

### Real examples

**Info-card row** — `guides/dallas-families.html`, abbreviated:

```html
<div data-rt-embed-type='true'><style>
  .info-container { display: flex; gap: 20px; flex-wrap: wrap; }
  .info-card { background: #f3f4f6; border-radius: 16px; padding: 20px 24px;
               width: 230px; border-top: 4px solid #f7931e; }
  .info-title { color: #00a8cc; font-size: 14px; font-weight: 500; }
</style>
<div class="info-container">
  <div class="info-card"><p class="info-title">Market</p><p class="info-value">Dallas, TX</p></div>
  <div class="info-card"><p class="info-title">Price Range</p><p class="info-value">$1,100 - $2,400/mo</p></div>
</div></div>
```

**Comparison table** — `guides/brooklyn-neighborhood-guide.html`, abbreviated. Note the nested `<head>` and the bare element selectors:

```html
<div data-rt-embed-type="true"><head><style>
table { width: 100%; border-collapse: collapse; }
th { background-color: #00bcd4; color: white; }
tr:nth-child(even) { background-color: #f2f2f2; }
</style></head>
<body><table>
<thead><tr><th>Neighborhood</th><th>Median 1BR</th><th>Vibe</th></tr></thead>
<tbody><tr><td>Park Slope</td><td>$3,200-$3,950</td><td>Brownstones, Prospect Park</td></tr></tbody>
</table></body></div>
```

### The catch — three syntaxes, two vocabularies

The same visual pattern is implemented three different ways:

| Style | Count |
|---|---|
| `<head><style>…</style></head><body>` + classes | 145 |
| Bare `<style>` + classes | 45 |
| Pure inline `style="…"`, **no classes at all** | 33 |

Class names also vary for the same component — `property-card` / `bp-prop-card` / none; `info-card` / `card` / `bp-card`. Attribute quoting varies too (`class='x'` vs `class="x"`), so any parser must be quote-agnostic.

**Recommended approach:** write a one-time normalising extractor that runs at import and keys off stable **content strings** rather than class names. The literal `WORTH LOOKING AT` identifies a property card regardless of which of the three syntaxes it uses. Map each block to a component, discard the embedded `<style>`, and render with your own styling.

One-time cost, clean semantic markup for all 120 articles.

### Links inside bodies

Normalise these at import. Current state across the corpus:

| Host in `href` | Count |
|---|---|
| `https://www.brightplace.ai` | 473 |
| `https://brightplace.ai` (apex) | **417** |
| `https://app.brightplace.ai` | 182 |
| `https://docs.brightplace.ai` | 3 |
| relative `/guides/…` | 10 |

Because apex 301s to www, **those 417 apex links each cost a needless redirect hop today.** Convert all internal links to site-relative paths (`/guides/dallas-families`). Leave external links absolute.

### Images inside bodies

Only 4 `<img>` tags exist across all 120 bodies, both in news articles, wrapped in Webflow figure markup with absolute `cdn.prod.website-files.com` sources. Hero images are separate files and are not in the body.

### Heading structure

`news/brightplace-connect-launch.html` has **no `<h2>` at all** — it uses `<p><strong>` as pseudo-headings, and `how-brightplace-became-ai-search-favorite.html` mixes both. Any auto-generated table of contents will silently skip those sections.

---

## 7. Template acceptance

`curl` a built page and confirm all of this is in the **raw HTML**, not injected by JavaScript:

- Full body text
- Exactly one `<h1>`
- Self-referencing canonical, absolute
- `<title>` and `<meta name="description">`
- Complete OG tags including `og:image`
- JSON-LD blocks
- Visible `<time>`
- GA4 tag
- No `webflow.com` or `website-files.com` strings
- No stray `<head>`, `<body>` or `<base>` tags from embeds
- No `<style>` block using a bare element selector

The last three exist because of the embed problem in §6. They are the checks that catch a regression there.
