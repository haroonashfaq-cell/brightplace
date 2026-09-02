# Developer CMS Requirement Document — AIR Operator Blog System

**Version:** 1.0
**Date:** September 2026
**For:** Development team building the blog CMS on Vercel for AIR operator community websites
**From:** Content/SEO team (Claude Code pipeline)

---

## 1. What This Document Is

We have an AI-powered content pipeline that produces publish-ready blog articles for each AIR operator community website. The pipeline outputs a markdown file with frontmatter, article body, FAQ section, JSON-LD schemas, and a compressed WebP featured image.

**We need your team to build a CMS on Vercel with a REST API endpoint so we can push finished articles directly from our pipeline to the live website.**

This document specifies exactly what the CMS needs to accept, how the API should work, and what the published page should render.

---

## 2. The 5 Community Websites

Each community gets its own blog section. Same CMS architecture, deployed per site.

| Community | Current Domain | Blog URL Pattern |
|---|---|---|
| Foxchase | foxchaseofalexandriaapts.com | /blog/[slug] |
| Citi Lakes | citilakesapartments.com | /blog/[slug] |
| Sorrel / LUX at Sorrel | livesorrelapartments.com | /blog/[slug] |
| Verdant Peachtree Creek | verdantpeachtreecreekapts.com | /blog/[slug] |
| Villages at Raleigh Beach | thevillagesatraleighbeach.com | /blog/[slug] |

If these sites are being rebuilt on Vercel, the blog lives at `[domain]/blog/[slug]`. If you add a subdomain approach, `blog.[domain]/[slug]` works too. Just keep the pattern consistent.

---

## 3. What We Send You (The Payload)

Every article from our pipeline produces two files:

### File 1: Article Markdown (`09-[slug]-final-enriched.md`)

A markdown file with YAML frontmatter at the top, article body in the middle, and JSON-LD schema blocks at the end. Here is the exact structure:

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

## 4. CMS Database Schema

The blog CMS needs one main table for articles. Here are the fields your CMS must support:

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

## 5. API Endpoints Required

We need these REST API endpoints to push content from Claude Code.

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

## 6. How the Published Blog Page Must Render

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

Your CMS must convert markdown to HTML. Use a standard library (marked, remark, markdown-it). Important rules:

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

## 7. Blog Index Page

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

## 8. Sitemap Integration

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

## 9. Image Handling

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

## 10. Performance Requirements

| Metric | Target | Why |
|---|---|---|
| Time to First Byte | Under 200ms | Vercel edge should handle this |
| Largest Contentful Paint | Under 2.5s | Featured image must be optimized |
| Cumulative Layout Shift | Under 0.1 | Set width/height on all images |
| First Input Delay | Under 100ms | Minimal JavaScript on blog pages |
| Page size | Under 500KB total | Light pages rank better |

### Caching Strategy
- Blog pages: ISR (Incremental Static Regeneration) with 60-second revalidation
- Images: CDN with immutable caching (1 year)
- API responses: no cache (always fresh for our pipeline)

---

## 11. RSS Feed

Generate an RSS feed at:
```
https://foxchaseofalexandriaapts.com/blog/rss.xml
```

Include: title, description, link, pubDate, featured image for each published post. Auto-update when posts are published.

---

## 12. What We Handle vs What You Handle

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

## 13. Deployment Plan

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

## 14. Testing Checklist (for dev team)

Before handing off, verify:

- [ ] `POST /api/blog/posts` creates a draft with image upload
- [ ] `PUT /api/blog/posts/[id]` updates an existing post
- [ ] `PATCH /api/blog/posts/[id]/status` publishes a draft
- [ ] `GET /api/blog/posts/[id]` returns full post data
- [ ] `GET /api/blog/posts?community_id=foxchase` returns list
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

---

## 15. Example: Full API Call from Claude Code

This is exactly what we will run from our pipeline to push a finished article:

```bash
# Parse the final enriched markdown file
# Extract frontmatter, body, and schemas
# Send to the CMS API

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

## 16. Questions for Dev Team

Please confirm or discuss:

1. **Hosting:** Are all 5 community sites being rebuilt on Vercel, or are we adding a blog layer to existing sites?
2. **Domain:** Will the blog live on the main domain (`/blog/[slug]`) or a subdomain?
3. **Auth:** Is Bearer token auth acceptable, or do you need OAuth/JWT?
4. **Image storage:** Vercel Blob, Cloudflare R2, or S3? We just need a CDN URL back.
5. **Staging:** Can we get a staging URL to test the API before going live?
6. **Timeline:** When can we expect the Foxchase API endpoint ready for testing?

---

*This document is the contract between the content team and the dev team. If the API matches this spec, we can push content from our pipeline to any community site with zero manual steps.*
