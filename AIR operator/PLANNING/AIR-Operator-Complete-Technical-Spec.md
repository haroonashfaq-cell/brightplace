# AIR Operator: Complete Technical Specification

**Version:** 1.0
**Date:** September 2026
**For:** Development team
**From:** brightplace Content/SEO team

---

# PART 1: Rendering & AI Crawler Requirements

How to build these sites so Google AND every AI search engine can read them.

---

## The Problem We're Solving

AI search engines (ChatGPT, Claude, Perplexity, Google AI Overviews) are now the primary way renters discover apartments. These AI crawlers do NOT execute JavaScript. They fetch raw HTML and read it — exactly like running `curl` on a URL.

If the site uses client-side rendering (React SPA, Angular SPA, or even Next.js with `'use client'` everywhere), the AI crawlers see an empty page. The content is invisible. We lose 100% of AI search traffic.

Our architecture must guarantee that every piece of content is in the raw HTML source — no JavaScript execution required.

---

## How Every Major AI Crawler Works (2026)

| Crawler | Who Operates It | Executes JavaScript? | What It Reads |
|---------|----------------|---------------------|---------------|
| **GPTBot** | OpenAI (ChatGPT, SearchGPT) | No | Raw HTML + JSON-LD schemas |
| **ClaudeBot** | Anthropic (Claude) | No | Raw HTML + JSON-LD schemas |
| **PerplexityBot** | Perplexity AI | No | Raw HTML + JSON-LD schemas |
| **Google-Extended** | Google (AI Overviews) | No | Raw HTML + JSON-LD schemas |
| **Googlebot** | Google (traditional search) | Yes (limited, delayed) | HTML first, JS second — prefers HTML |
| **Bingbot** | Microsoft (Copilot) | Limited | Raw HTML preferred |
| **AppleBot** | Apple (Siri, Spotlight) | No | Raw HTML + meta tags |

**Key insight:** Every AI crawler behaves like `curl`. If `curl https://your-site.com/page` doesn't show the content, no AI engine will ever surface it.

---

## Recommended Architecture

```
Framework:     Next.js 15+ with App Router
Language:      TypeScript (strict mode)
Rendering:     Static Site Generation (SSG) for property pages
               Incremental Static Regeneration (ISR) for blog pages
Styling:       CSS custom properties (no Tailwind, no CSS modules)
Animation:     Framer Motion 11+ (progressive enhancement only)
Deployment:    Vercel (CDN edge serving)
```

### Why SSG (Static Site Generation)

| Approach | AI Crawlers See Content? | Speed | Hosting Cost | Complexity |
|----------|------------------------|-------|-------------|------------|
| **SSG (our choice)** | Yes — pre-built HTML files | Fastest (CDN edge) | Near zero | Low |
| SSR (Server-Side Rendering) | Yes — rendered per request | Fast | Medium (server required) | Medium |
| ISR (for blog) | Yes — static + auto-regeneration | Fast | Low | Medium |
| CSR (Client-Side Rendering) | **No — empty page** | Slow (JS must load + execute) | Low | Low |
| SPA (Single Page App) | **No — empty page** | Slow | Low | Medium |

SSG builds every page into a plain `.html` file at deploy time. Vercel serves these from its global CDN. No server runtime. No JavaScript required to see content. Fastest possible Time to First Byte.

---

## The Two-Layer Rendering Model

### Layer 1: Static HTML (Server Components — DEFAULT)

Everything the user and AI crawlers need to READ is in plain HTML:

- Property names, addresses, phone numbers
- Floor plan names, pricing, square footage
- Amenity lists and descriptions
- FAQ questions and answers
- Neighborhood information and distances
- Blog article text
- All meta tags (title, description, canonical, Open Graph, Twitter Card)
- All JSON-LD structured data schemas

**Rule:** Server Components are the default. Never add `'use client'` unless the component absolutely needs `useState`, `useEffect`, or Framer Motion.

### Layer 2: Progressive Enhancement (Client Components — OPT-IN ONLY)

Interactive features that enhance the human experience but are NOT required to consume content:

- Scroll-triggered fade-in animations (Framer Motion)
- FAQ accordion expand/collapse
- Image gallery lightbox
- Rent calculator (interactive pricing tool)
- AI chat assistant widget
- Parallax scrolling effects
- Mobile menu toggle

**Rule:** If you disable JavaScript in the browser, the page must still display 100% of the content. Interactions stop working, animations disappear, but all text, pricing, images, and data remain visible.

### How to Verify

```bash
# This must show all content — if it doesn't, something is client-rendered
curl https://foxchaseofalexandriaapts.com/blog/foxchase-apartments | grep "88 wooded acres"

# Count JSON-LD schemas — must return 3 for property pages
curl -s https://site.com/page | grep -c "application/ld+json"

# Check that robots.txt allows AI crawlers
curl https://foxchaseofalexandriaapts.com/robots.txt
```

---

## AI Crawler Access Configuration

### robots.txt (MUST be at site root)

```
# AI Search Engines — ALLOW ALL
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

# Traditional Search Engines
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: AppleBot
Allow: /

# Sitemap
Sitemap: https://[domain]/sitemap.xml
```

**Why this matters:** 90%+ of apartment community websites block AI crawlers. By explicitly allowing them, our content gets indexed and cited in AI search results while competitors are invisible.

### llms.txt (MUST be at site root)

A plain-text file that gives AI models a structured summary of the site without requiring them to crawl every page. Format:

```
# [Community Name] Apartments
> [One-line description with key differentiators]

## Property Pages
- [Page Name](/url): [Key details — location, floor plans, price range, top amenities]

## Blog
- [Article Title](/blog/slug): [One-line summary]

## About
[Brief description of what the site offers]

## Contact
Website: [url]
Phone: [number]
```

AI models check for `llms.txt` before deep-crawling. This file gives them everything they need in one request.

### X-Robots-Tag Header (Vercel config)

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Robots-Tag", "value": "index, follow" },
        { "key": "X-Content-Type-Options", "value": "nosniff" }
      ]
    }
  ]
}
```

---

## JSON-LD Structured Data Requirements

Every page must inject schemas into the `<head>` via `<script type="application/ld+json">`. AI crawlers and Google parse these directly.

### Property Pages (3 schemas)

**1. ApartmentComplex**
```json
{
  "@context": "https://schema.org",
  "@type": "ApartmentComplex",
  "name": "Foxchase Apartments",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "766 N Howard Street",
    "addressLocality": "Alexandria",
    "addressRegion": "VA",
    "postalCode": "22304"
  },
  "telephone": "434-337-5919",
  "amenityFeature": [
    { "@type": "LocationFeatureSpecification", "name": "Resort-Style Pool", "value": true },
    { "@type": "LocationFeatureSpecification", "name": "24-Hour Fitness Center", "value": true }
  ],
  "priceRange": "$1,467 - $2,521/mo",
  "numberOfAvailableAccommodation": 7
}
```

**2. FAQPage**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Does Foxchase allow pets?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, Foxchase is a pet-friendly community with an on-site dog park..."
      }
    }
  ]
}
```
This triggers Google's FAQ rich results AND gets pulled into AI-generated answers.

**3. BreadcrumbList**
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://foxchaseofalexandriaapts.com" },
    { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://foxchaseofalexandriaapts.com/blog" },
    { "@type": "ListItem", "position": 3, "name": "Article Title", "item": "https://foxchaseofalexandriaapts.com/blog/slug" }
  ]
}
```

### Blog Pages (3 schemas)

1. **Article** — headline, author, datePublished, dateModified, publisher
2. **FAQPage** — all FAQ pairs from the article
3. **WebPage** — page-level metadata with breadcrumbs

---

## Semantic HTML Requirements

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>SEO Title (different from H1, under 60 chars)</title>
  <meta name="description" content="Under 155 characters...">
  <link rel="canonical" href="https://exact-page-url">
  <meta property="og:title" content="...">
  <meta property="og:description" content="...">
  <meta property="og:image" content="https://cdn-url/image.webp">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{ schemas here }</script>
</head>
<body>
  <header><!-- Navigation --></header>
  <main>
    <article>
      <h1>Display Title (only ONE h1 per page)</h1>
      <section id="pricing">
        <h2>What Does It Cost to Live at Foxchase?</h2>
      </section>
      <section id="amenities">
        <h2>What Amenities Does Foxchase Offer?</h2>
      </section>
      <section id="faq">
        <h2>Frequently Asked Questions</h2>
        <h3>Does Foxchase allow pets?</h3>
      </section>
    </article>
  </main>
  <footer><!-- Contact, legal --></footer>
</body>
</html>
```

### Rules
- One `<h1>` per page — the display title
- `<title>` tag uses the SEO title (must differ from H1)
- Heading hierarchy never skips levels (no h1 then h3)
- Every `<section>` has an `id` attribute for anchor navigation
- H2 headings in question format match People Also Ask queries
- All images have `width` and `height` attributes (prevents layout shift)
- External links get `target="_blank" rel="noopener"`
- Internal links do NOT get `target="_blank"`

---

## Performance Requirements (Google Ranking Factor)

| Metric | Target | Why |
|--------|--------|-----|
| Time to First Byte (TTFB) | Under 200ms | Vercel CDN edge handles this with static files |
| Largest Contentful Paint (LCP) | Under 2.5s | Optimize hero/featured images (WebP, compressed) |
| Cumulative Layout Shift (CLS) | Under 0.1 | Set width/height on ALL images, no late-loading content |
| First Input Delay (FID) | Under 100ms | Minimal JavaScript on content pages |
| Total page weight | Under 500KB | Light pages rank better and load faster on mobile |
| First Load JS bundle | Under 160KB | Keep client-side JS minimal |

### Image Requirements
- Format: WebP (we provide all images in WebP)
- Hero/featured images: `loading="eager"` (load immediately)
- All other images: `loading="lazy"` (load on scroll)
- Always set explicit `width` and `height` attributes
- Serve via CDN with `Cache-Control: public, max-age=31536000, immutable`

---

## What We Do NOT Want

| Approach | Problem |
|----------|---------|
| React SPA / Create React App | Content invisible to all AI crawlers — empty `<div id="root">` |
| Client-side API fetching (`useEffect` + `fetch`) | Content loads after JS executes — AI crawlers see nothing |
| `'use client'` on content components | Defeats server rendering — content not in initial HTML |
| WordPress with page builders | Bloated, slow, usually blocks AI bots, limited schema control |
| iframes for content sections | Crawlers don't follow iframes — content is invisible |
| Content behind authentication/login | Crawlers can't authenticate — content is invisible |
| Lazy-loading text content | Crawlers don't scroll — only above-fold HTML is guaranteed |
| JavaScript-dependent routing (hash routes) | `/#/page` URLs are invisible to crawlers |
| `<meta name="robots" content="noindex">` on blog pages | Explicitly tells crawlers to ignore the page |
| Blocking AI bots in robots.txt | Competitors do this — we gain advantage by NOT doing it |

---

# PART 2: Developer Guide — How to Build the Sites

How the existing property pages work and how to add the 5 AIR communities.

---

## Tech Stack

- **Next.js 15+** with App Router
- **TypeScript** (strict mode)
- **Framer Motion 11+** for animations
- **CSS custom properties** for styling (no Tailwind, no CSS modules)
- **Static export** deployed on **Vercel**

## How Property Pages Work

**Step 1: All property data lives in a TypeScript file**

`src/data/operators.ts` defines a typed interface (`PropertyData`) with every field a property page needs: name, address, floor plans, amenities, FAQs, pricing, images, meta tags, neighborhood info, etc.

Each community's data is a separate file under `src/data/operators/[operator-name]/`.

**Step 2: Pages are generated at build time**

`src/app/[operator]/[slug]/page.tsx` uses `generateStaticParams()` to list every operator + property combination. Next.js builds a separate HTML file for each one.

**Step 3: Components compose the page**

Each property page is built from 10 reusable components:
1. `Header` — navigation + branding
2. `Hero` — hero image, headline, promo banner
3. `RentCalculator` — all-in pricing breakdown
4. `FloorPlans` — interactive floor plan gallery
5. `Amenities` — community + apartment features
6. `Neighborhood` — nearby attractions with distances
7. `Gallery` — image lightbox
8. `FAQ` — accordion with structured data
9. `TourCTA` — call-to-action for scheduling
10. `Footer` — links, legal, contact

Plus `AIAssistant` (chat widget) and `StoryLayout` (for guide/article pages).

**Step 4: Build outputs pure HTML**

`npm run build` generates an `out/` directory with static HTML files. Vercel serves these from its CDN edge network. No Node.js server needed at runtime.

## File Structure

```
operator-pages/
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Root layout (fonts, global CSS)
│   │   ├── page.tsx                # Homepage
│   │   └── [operator]/
│   │       ├── page.tsx            # Operator landing
│   │       └── [slug]/page.tsx     # Property page (SSG via generateStaticParams)
│   ├── components/                 # 13 reusable React components
│   ├── data/                       # Static operator data (TypeScript)
│   └── lib/                        # Utilities, animation presets
├── public/
│   ├── robots.txt                  # AI crawler permissions
│   ├── llms.txt                    # LLM-readable site summary
│   ├── sitemap.xml                 # All pages listed
│   └── images/                     # Per-operator image folders
├── out/                            # Static export output (built HTML)
├── next.config.ts                  # output: 'export'
└── vercel.json                     # Headers, routing
```

## To Add a New Community (e.g., Foxchase)

1. Create `src/data/operators/air-communities/foxchase.ts` with all property data following the `PropertyData` interface
2. Add property images to `public/images/air-communities/`
3. Register the property in the operator's index so `generateStaticParams()` picks it up
4. Run `npm run build` — verify the HTML file appears in `out/`
5. Push to GitHub — Vercel auto-deploys

---

# PART 3: Blog CMS Requirement Specification

What the CMS needs to accept, how the API works, and how published pages must render.

---

## The 5 Community Websites

Each community gets its own blog section. Same CMS architecture, deployed per site.

| Community | Current Domain | Blog URL Pattern |
|---|---|---|
| Foxchase | foxchaseofalexandriaapts.com | /blog/[slug] |
| Citi Lakes | citilakesapartments.com | /blog/[slug] |
| Sorrel / LUX at Sorrel | livesorrelapartments.com | /blog/[slug] |
| Verdant Peachtree Creek | verdantpeachtreecreekapts.com | /blog/[slug] |
| Villages at Raleigh Beach | thevillagesatraleighbeach.com | /blog/[slug] |

---

## What We Send You (The Payload)

Every article from our pipeline produces two files:

### File 1: Article Markdown (`09-[slug]-final-enriched.md`)

A markdown file with YAML frontmatter at the top, article body in the middle, and JSON-LD schema blocks at the end:

```
---
title: "What Renters Should Know About Foxchase Apartments in Alexandria, VA"
seo_title: "Foxchase Apartments Alexandria VA: Honest 2026 Review"
meta_description: "Foxchase Apartments sits on 88 wooded acres in Alexandria, VA..."
slug: "foxchase-apartments-alexandria-va-what-renters-should-know"
primary_keyword: "foxchase apartments alexandria"
secondary_keywords: ["fox chase apartments", "foxchase apartments", ...]
schema_types: ["Article", "FAQPage", "WebPage"]
word_count_target: 2800
last_reviewed: "September 2026"
date_published: 2026-09-01
date_modified: 2026-09-01
author: "AIR Communities"
---

# H1 Title Here

Article body in markdown...

## H2 Sections...

### H3 FAQ Questions...

---

## FAQ Schema (JSON-LD)
```json
{ "@context": "https://schema.org", "@type": "FAQPage", ... }
```

## Article Schema (JSON-LD)
```json
{ "@context": "https://schema.org", "@type": "Article", ... }
```

## WebPage Schema (JSON-LD)
```json
{ "@context": "https://schema.org", "@type": "WebPage", ... }
```
```

### File 2: Featured Image (`[slug]-featured.webp`)

- Format: WebP
- Dimensions: 1200 x 628px
- Max size: 200KB
- Companion metadata file: `[slug]-featured.json` with alt text and generation details

---

## CMS Database Schema

### Blog Posts Table

| Field | Type | Required | Source (from our file) | Notes |
|---|---|---|---|---|
| `id` | UUID | Auto | Auto-generated | Primary key |
| `title` | String (256) | Yes | frontmatter `title` | The H1 title. Displayed as page heading. |
| `seo_title` | String (60) | Yes | frontmatter `seo_title` | Goes in `<title>` tag. MUST be different from `title`. Max 60 chars. |
| `meta_description` | String (160) | Yes | frontmatter `meta_description` | Goes in `<meta name="description">`. Max 155 chars. |
| `slug` | String (128) | Yes | frontmatter `slug` | URL path: `/blog/[slug]`. Lowercase, hyphenated, unique per site. |
| `body_markdown` | Text | Yes | Article body (between frontmatter and schema sections) | Raw markdown content. Your CMS renders to HTML. |
| `body_html` | Text | Yes | Converted from markdown | Pre-rendered HTML for the page. Convert server-side. |
| `post_summary` | String (300) | Yes | First paragraph, plain text | For blog index cards, social sharing, RSS. |
| `primary_keyword` | String (128) | Yes | frontmatter `primary_keyword` | For internal tracking. Not displayed to users. |
| `secondary_keywords` | JSON Array | No | frontmatter `secondary_keywords` | For internal tracking. |
| `author` | String (128) | Yes | frontmatter `author` | Displayed as author name on the page. |
| `date_published` | Date | Yes | frontmatter `date_published` | ISO 8601 format (YYYY-MM-DD). |
| `date_modified` | Date | Yes | frontmatter `date_modified` | Updated when article is refreshed. |
| `last_reviewed` | String (32) | Yes | frontmatter `last_reviewed` | "September 2026" format. Displayed in article footer. |
| `featured_image_url` | String (512) | Yes | Uploaded image URL | After image upload, store the CDN URL here. |
| `featured_image_alt` | String (256) | Yes | From image metadata JSON | Alt text for the featured image. |
| `schema_faq` | Text (JSON) | Yes | FAQ Schema JSON-LD block | Raw JSON string. Injected into page `<head>`. |
| `schema_article` | Text (JSON) | Yes | Article Schema JSON-LD block | Raw JSON string. Injected into page `<head>`. |
| `schema_webpage` | Text (JSON) | Yes | WebPage Schema JSON-LD block | Raw JSON string. Injected into page `<head>`. |
| `status` | String | Yes | Set via API | `draft`, `published`, `archived`. Default: `draft`. |
| `community_id` | String (64) | Yes | Identifies which community site | e.g., `foxchase`, `citilakes`, `sorrel`, `verdant`, `villages` |
| `word_count` | Integer | No | Computed from body | Auto-calculated on save. |
| `created_at` | Timestamp | Auto | Auto | Record creation time. |
| `updated_at` | Timestamp | Auto | Auto | Last update time. |

### SQL (if using PostgreSQL / Supabase / Neon)

```sql
create table blog_posts (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  seo_title varchar(60) not null,
  meta_description varchar(160) not null,
  slug varchar(128) not null,
  body_markdown text not null,
  body_html text not null,
  post_summary varchar(300) not null,
  primary_keyword varchar(128),
  secondary_keywords jsonb default '[]',
  author varchar(128) not null default 'AIR Communities',
  date_published date not null,
  date_modified date not null,
  last_reviewed varchar(32),
  featured_image_url text,
  featured_image_alt varchar(256),
  schema_faq text,
  schema_article text,
  schema_webpage text,
  status varchar(16) not null default 'draft',
  community_id varchar(64) not null,
  word_count integer,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),

  unique(community_id, slug)
);

create index idx_blog_community_status on blog_posts(community_id, status);
create index idx_blog_slug on blog_posts(slug);
create index idx_blog_published on blog_posts(date_published desc);
```

---

## API Endpoints Required

### Base URL
```
https://[community-domain]/api/blog
```
or if centralized:
```
https://cms.airoperator.com/api/blog
```

### Authentication

Use API key authentication. We send the key in the header:
```
Authorization: Bearer [API_KEY]
```

Generate one API key per community site. Store securely. Share with the content team via secure channel (not email).

---

### Endpoint 1: Create Article (Draft)

```
POST /api/blog/posts
Content-Type: multipart/form-data
Authorization: Bearer [API_KEY]
```

**Why multipart/form-data:** We send the featured image as a file upload alongside the JSON payload in a single request.

**Request body:**

| Part | Type | Description |
|---|---|---|
| `data` | JSON string | All article fields (see below) |
| `featured_image` | File (WebP) | The featured image file (1200x628, under 200KB) |

**JSON `data` structure:**

```json
{
  "title": "What Renters Should Know About Foxchase Apartments in Alexandria, VA",
  "seo_title": "Foxchase Apartments Alexandria VA: Honest 2026 Review",
  "meta_description": "Foxchase Apartments sits on 88 wooded acres in Alexandria, VA with 4 pools, townhomes, and rents from $1,487. Here is what 835+ resident reviews reveal.",
  "slug": "foxchase-apartments-alexandria-va-what-renters-should-know",
  "body_markdown": "# What Renters Should Know...\n\nFoxchase Apartments covers 88 wooded acres...",
  "post_summary": "Foxchase Apartments covers 88 wooded acres in Seminary Hill, Alexandria, making it the largest apartment community in the city.",
  "primary_keyword": "foxchase apartments alexandria",
  "secondary_keywords": ["fox chase apartments", "foxchase apartments"],
  "author": "AIR Communities",
  "date_published": "2026-09-01",
  "date_modified": "2026-09-01",
  "last_reviewed": "September 2026",
  "featured_image_alt": "Foxchase Apartments 88-acre wooded campus in Alexandria VA with garden-style brick buildings among mature trees",
  "schema_faq": "{ \"@context\": \"https://schema.org\", \"@type\": \"FAQPage\", ... }",
  "schema_article": "{ \"@context\": \"https://schema.org\", \"@type\": \"Article\", ... }",
  "schema_webpage": "{ \"@context\": \"https://schema.org\", \"@type\": \"WebPage\", ... }",
  "status": "draft",
  "community_id": "foxchase"
}
```

**Response (success):**
```json
{
  "success": true,
  "post": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "slug": "foxchase-apartments-alexandria-va-what-renters-should-know",
    "status": "draft",
    "featured_image_url": "https://cdn.foxchaseofalexandriaapts.com/blog/foxchase-apartments-alexandria-featured.webp",
    "preview_url": "https://foxchaseofalexandriaapts.com/blog/foxchase-apartments-alexandria-va-what-renters-should-know?preview=true",
    "created_at": "2026-09-01T18:30:00Z"
  }
}
```

**Response (error):**
```json
{
  "success": false,
  "error": {
    "code": "DUPLICATE_SLUG",
    "message": "A post with slug 'foxchase-apartments-alexandria-va-what-renters-should-know' already exists. Use PUT to update."
  }
}
```

---

### Endpoint 2: Update Article

```
PUT /api/blog/posts/[id]
Content-Type: multipart/form-data
Authorization: Bearer [API_KEY]
```

Same payload as create. Only send fields that changed. Featured image is optional on update (keep existing if not sent).

**Response:**
```json
{
  "success": true,
  "post": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "slug": "foxchase-apartments-alexandria-va-what-renters-should-know",
    "status": "draft",
    "updated_at": "2026-09-15T10:00:00Z"
  }
}
```

---

### Endpoint 3: Publish / Unpublish

```
PATCH /api/blog/posts/[id]/status
Content-Type: application/json
Authorization: Bearer [API_KEY]
```

```json
{
  "status": "published"
}
```

Valid statuses: `draft`, `published`, `archived`

---

### Endpoint 4: Get Article

```
GET /api/blog/posts/[id]
Authorization: Bearer [API_KEY]
```

Returns the full post object. Used to verify content was pushed correctly.

---

### Endpoint 5: List Articles

```
GET /api/blog/posts?community_id=foxchase&status=published&limit=20&offset=0
Authorization: Bearer [API_KEY]
```

Returns paginated list. Used for content audits and status checks.

---

### Endpoint 6: Delete Article

```
DELETE /api/blog/posts/[id]
Authorization: Bearer [API_KEY]
```

Soft delete (sets status to `archived`). Never hard delete content.

---

### Endpoint 7: Upload Image Only

```
POST /api/blog/images
Content-Type: multipart/form-data
Authorization: Bearer [API_KEY]
```

| Part | Type | Description |
|---|---|---|
| `image` | File | WebP image file |
| `alt_text` | String | Alt text for the image |
| `community_id` | String | Which community site |

**Response:**
```json
{
  "success": true,
  "image_url": "https://cdn.foxchaseofalexandriaapts.com/blog/foxchase-apartments-alexandria-featured.webp",
  "alt_text": "Foxchase Apartments 88-acre wooded campus..."
}
```

Used when we need to upload an image separately (e.g., replacing a featured image without updating the whole article).

---

## How the Published Blog Page Must Render

### Page URL
```
https://foxchaseofalexandriaapts.com/blog/foxchase-apartments-alexandria-va-what-renters-should-know
```

### HTML Head (SEO critical)

```html
<head>
  <title>Foxchase Apartments Alexandria VA: Honest 2026 Review</title>
  <meta name="description" content="Foxchase Apartments sits on 88 wooded acres...">
  <link rel="canonical" href="https://foxchaseofalexandriaapts.com/blog/foxchase-apartments-alexandria-va-what-renters-should-know">

  <!-- Open Graph -->
  <meta property="og:title" content="Foxchase Apartments Alexandria VA: Honest 2026 Review">
  <meta property="og:description" content="Foxchase Apartments sits on 88 wooded acres...">
  <meta property="og:image" content="https://cdn.foxchaseofalexandriaapts.com/blog/foxchase-apartments-alexandria-featured.webp">
  <meta property="og:url" content="https://foxchaseofalexandriaapts.com/blog/[slug]">
  <meta property="og:type" content="article">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Foxchase Apartments Alexandria VA: Honest 2026 Review">
  <meta name="twitter:description" content="Foxchase Apartments sits on 88 wooded acres...">
  <meta name="twitter:image" content="https://cdn.foxchaseofalexandriaapts.com/blog/foxchase-apartments-alexandria-featured.webp">

  <!-- JSON-LD Schemas (inject all three from the schema fields) -->
  <script type="application/ld+json">
    { "@context": "https://schema.org", "@type": "FAQPage", ... }
  </script>
  <script type="application/ld+json">
    { "@context": "https://schema.org", "@type": "Article", ... }
  </script>
  <script type="application/ld+json">
    { "@context": "https://schema.org", "@type": "WebPage", ... }
  </script>
</head>
```

### Page Body Structure

```html
<article>
  <!-- Featured Image -->
  <img
    src="[featured_image_url]"
    alt="[featured_image_alt]"
    width="1200" height="628"
    loading="eager"
  >

  <!-- Article metadata bar -->
  <div class="article-meta">
    <span class="author">By [author]</span>
    <span class="date">Published [date_published]</span>
    <span class="updated">Last reviewed [last_reviewed]</span>
    <span class="reading-time">[word_count / 238] min read</span>
  </div>

  <!-- Article body (rendered from body_html) -->
  <div class="article-body">
    [body_html goes here]
  </div>
</article>
```

### Markdown to HTML Conversion Rules

Use a standard library (marked, remark, markdown-it). Important rules:

| Markdown | HTML Output | Notes |
|---|---|---|
| `# H1` | `<h1>` | Only one per article. This is the title. |
| `## H2` | `<h2>` | Major sections |
| `### H3` | `<h3>` | FAQ questions and subsections |
| `**bold**` | `<strong>` | Used for comparison labels |
| `[text](url)` | `<a href="url">text</a>` | All links. External links get `target="_blank" rel="noopener"` |
| `- item` | `<p><strong>Label:</strong> text</p>` OR `<ul><li>` | Both formats may appear. Render normally. |
| `1. item` | `<ol><li>` | Numbered lists |
| Code blocks | Skip rendering | Schema JSON blocks should NOT appear in the body. They go in `<head>`. |
| `---` | `<hr>` | Section dividers |

**Critical:** The body_markdown we send does NOT include the frontmatter or schema blocks. We strip those before sending. You receive only the article content between the frontmatter and the first schema section.

### External Links

All external links in the article must render with:
```html
<a href="https://..." target="_blank" rel="noopener">anchor text</a>
```

Internal links (to the same community site) should NOT have `target="_blank"`.

---

## Blog Index Page

### URL
```
https://foxchaseofalexandriaapts.com/blog
```

### What it shows
- Grid or list of all published blog posts, newest first
- Each card shows: featured image, title, post_summary, date_published, reading time
- Clicking a card goes to `/blog/[slug]`
- Pagination (12 posts per page)

### SEO for index page
- Title: `Blog | Foxchase of Alexandria Apartments`
- Meta description: `Renter guides, neighborhood insights, and apartment tips for Foxchase of Alexandria residents and prospective renters.`
- Canonical: `https://foxchaseofalexandriaapts.com/blog`

---

## Sitemap Integration

Every published blog post must be included in the site's XML sitemap.

```xml
<url>
  <loc>https://foxchaseofalexandriaapts.com/blog/foxchase-apartments-alexandria-va-what-renters-should-know</loc>
  <lastmod>2026-09-01</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.8</priority>
</url>
```

The sitemap must auto-update when posts are published or updated. This is critical for Google indexing.

---

## Image Handling

### Upload Flow
1. We send the WebP image as part of the `POST /api/blog/posts` multipart request
2. Your server stores it on Vercel Blob Storage, Cloudflare R2, or S3
3. Return the CDN URL in the response
4. Store the CDN URL in the `featured_image_url` field

### Image Requirements
- Accept: WebP format (we always send WebP)
- Max file size: 500KB (our images are under 200KB but give buffer)
- Store original dimensions (1200x628)
- Serve via CDN with caching headers (`Cache-Control: public, max-age=31536000, immutable`)
- Generate an `og:image` URL that's accessible to social media crawlers (no auth required)

### Image File Naming
We suggest: `blog/[slug]-featured.webp`
Example: `blog/foxchase-apartments-alexandria-va-what-renters-should-know-featured.webp`

---

## Caching Strategy
- Blog pages: ISR (Incremental Static Regeneration) with 60-second revalidation
- Images: CDN with immutable caching (1 year)
- API responses: no cache (always fresh for our pipeline)

---

## RSS Feed

Generate an RSS feed at:
```
https://foxchaseofalexandriaapts.com/blog/rss.xml
```

Include: title, description, link, pubDate, featured image for each published post. Auto-update when posts are published.

---

## What We Handle vs What You Handle

### We handle (content team / Claude Code pipeline):
- Keyword research and content strategy
- Writing the complete article (markdown)
- QA and compliance checks
- Generating the featured image (WebP, compressed)
- Generating all 3 JSON-LD schema blocks
- Calling your API to create/update posts
- Deciding when to publish (status change)

### You handle (dev team):
- Building the CMS database and API endpoints
- Markdown to HTML conversion
- Image upload and CDN storage
- Page rendering (blog index + blog post pages)
- Injecting schemas into `<head>`
- Open Graph and Twitter Card meta tags
- XML sitemap generation
- RSS feed generation
- SSL, caching, performance optimization
- API key management and authentication

---

## Deployment Plan

### Phase 1: Foxchase (first site)
1. Build CMS + API on Vercel
2. Deploy to foxchaseofalexandriaapts.com (or a staging URL first)
3. We push the Foxchase test article via API
4. Verify: page renders, schemas in `<head>`, image loads, sitemap includes it, OG tags correct
5. Go live

### Phase 2: Roll out to remaining 4 communities
Same CMS codebase, different `community_id` and domain config:
- citilakesapartments.com
- livesorrelapartments.com
- verdantpeachtreecreekapts.com
- thevillagesatraleighbeach.com

### Phase 3: Automation
- Webhook: notify us when a post is published (for rank tracking setup)
- Webhook: notify us when traffic milestones are hit (GA4 integration, future)

---

## Testing Checklist (for dev team)

Before handing off, verify:

- [ ] `POST /api/blog/posts` creates a draft with image upload
- [ ] `PUT /api/blog/posts/[id]` updates an existing post
- [ ] `PATCH /api/blog/posts/[id]/status` publishes a draft
- [ ] `GET /api/blog/posts/[id]` returns full post data
- [ ] `GET /api/blog/posts?community_id=foxchase` returns list
- [ ] `curl [page-url]` shows ALL text content (zero JS dependency)
- [ ] Blog page renders at `/blog/[slug]` with correct HTML
- [ ] `<title>` tag uses `seo_title` (NOT `title`)
- [ ] `<meta description>` renders correctly
- [ ] All 3 JSON-LD schemas appear in `<head>` as `<script type="application/ld+json">`
- [ ] Featured image loads from CDN
- [ ] Open Graph image works (test with Facebook Sharing Debugger)
- [ ] Twitter Card works (test with Twitter Card Validator)
- [ ] External links have `target="_blank" rel="noopener"`
- [ ] Internal links do NOT have `target="_blank"`
- [ ] XML sitemap includes published posts
- [ ] RSS feed includes published posts
- [ ] Page passes Core Web Vitals (test with PageSpeed Insights)
- [ ] Slug uniqueness enforced (duplicate slug returns error, not 500)
- [ ] Draft posts are NOT visible to public (require `?preview=true` token)
- [ ] API returns proper error codes (400, 401, 404, 409, 500)
- [ ] `robots.txt` allows GPTBot, ClaudeBot, PerplexityBot
- [ ] `llms.txt` exists at site root
- [ ] Page weight under 500KB total

---

## Example: Full API Call from Claude Code

This is exactly what we will run from our pipeline to push a finished article:

```bash
curl -X POST https://foxchaseofalexandriaapts.com/api/blog/posts \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F 'data={
    "title": "What Renters Should Know About Foxchase Apartments in Alexandria, VA",
    "seo_title": "Foxchase Apartments Alexandria VA: Honest 2026 Review",
    "meta_description": "Foxchase Apartments sits on 88 wooded acres in Alexandria, VA with 4 pools, townhomes, and rents from $1,487. Here is what 835+ resident reviews reveal.",
    "slug": "foxchase-apartments-alexandria-va-what-renters-should-know",
    "body_markdown": "# What Renters Should Know...\n\nFull article body here...",
    "post_summary": "Foxchase Apartments covers 88 wooded acres in Seminary Hill, Alexandria...",
    "primary_keyword": "foxchase apartments alexandria",
    "secondary_keywords": ["fox chase apartments", "foxchase apartments"],
    "author": "AIR Communities",
    "date_published": "2026-09-01",
    "date_modified": "2026-09-01",
    "last_reviewed": "September 2026",
    "featured_image_alt": "Foxchase Apartments 88-acre wooded campus in Alexandria VA",
    "schema_faq": "{...}",
    "schema_article": "{...}",
    "schema_webpage": "{...}",
    "status": "draft",
    "community_id": "foxchase"
  }' \
  -F "featured_image=@foxchase-apartments-alexandria-featured-v2.webp"
```

---

## Questions for Dev Team

Please confirm or discuss:

1. **Hosting:** Are all 5 community sites being rebuilt on Vercel, or are we adding a blog layer to existing sites?
2. **Domain:** Will the blog live on the main domain (`/blog/[slug]`) or a subdomain?
3. **Auth:** Is Bearer token auth acceptable, or do you need OAuth/JWT?
4. **Image storage:** Vercel Blob, Cloudflare R2, or S3? We just need a CDN URL back.
5. **Staging:** Can we get a staging URL to test the API before going live?
6. **Timeline:** When can we expect the Foxchase API endpoint ready for testing?

---

*This document is the contract between the content team and the dev team. If the system matches this spec, we can push content from our pipeline to any community site with zero manual steps. Social media connector and content dashboard specs will be added as a separate document.*
