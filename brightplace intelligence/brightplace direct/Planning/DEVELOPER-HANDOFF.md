# brightplace direct — Developer Handoff Document

**Date:** August 27, 2026
**From:** Content Team
**Version:** 1.0

---

## Project Overview

brightplace direct is a content engine that publishes SEO-optimized articles to operator apartment websites. The content team writes articles using AI agents. The developer team builds the sites and CMS infrastructure that receives and renders the content.

**First client:** AIR Communities (5 communities selected, contract signed)

**What we need:** A CMS built into each operator's Vercel site with API endpoints. We POST content to the endpoint, it appears as a fully rendered, SEO-optimized page. Like Webflow CMS but built into the Next.js site.

---

## PART 1: What We're Building

### The Operator Site Structure

```
aircommunities.brightplace.ai/
├── /                                    ← Homepage (operator intro, communities, stories)
├── /air-communities                     ← Communities listing
├── /air-communities/one-canal           ← Property page (built from template)
├── /air-communities/one-canal-guide     ← Article page (published via CMS API)
├── /air-communities/indigo-west
├── /air-communities/indigo-west-guide
├── /sitemap.xml                         ← Auto-updated when content is added
├── /robots.txt                          ← Allows all AI crawlers
└── /llms.txt                            ← AI-readable content index
```

### Two Types of Pages

| Type | Created By | How |
|---|---|---|
| **Property pages** | Developer team builds from template + data | Template rendering |
| **Article pages** | Content team publishes via CMS API | CMS stores + renders |

---

## PART 2: The 5 AIR Communities (Immediate Build)

These 5 property pages need to be built from the site template:

| # | Property | City, State | Address |
|---|---|---|---|
| 1 | One Canal | Boston, MA | 1 Canal Street, 02114 |
| 2 | Indigo West | Orlando, FL | 6101 Raleigh Street, 32835 |
| 3 | One Boynton | Boynton Beach, FL | 1351 S Federal Hwy, 33435 |
| 4 | 3400 Avenue of the Arts | Costa Mesa, CA | 3400 Avenue of the Arts, 92626 |
| 5 | Citigate | Jacksonville, FL | 8451 Gate Pkwy W, 32216 |

We will provide the property data (floor plans, amenities, pricing, images) as JSON files for each. These pages use the same template as Oak Trail and Lakeview on the existing demo site.

---

## PART 3: CMS API Endpoints

### Overview

We need 6 API endpoints on each operator site. We call these from our content system to publish and manage articles.

**Base URL:** `https://[operator].brightplace.ai/api/cms/`
**Auth:** `Authorization: Bearer {api_key}` header on every request

---

### Endpoint 1: Create Article (CRITICAL — Need First)

```
POST /api/cms/articles

Headers:
  Authorization: Bearer sk_air_xxxxxxxxxxxxx
  Content-Type: application/json

Request Body:
{
  "title": "One Canal Apartments Boston: Pricing, Amenities, and What to Know",
  "slug": "one-canal-boston-guide",
  "meta_title": "One Canal Boston: Pricing & Amenities | brightplace",
  "meta_description": "One Canal in Boston's West End. Floor plans from $2,400/mo with rooftop pool, fitness center, and pet-friendly policy.",
  "property_slug": "one-canal",
  "author": "brightplace Research",
  "date_published": "2026-08-28",
  "read_time": "8 min",
  "primary_keyword": "one canal apartments boston",
  "thumbnail_url": "/images/air-communities/one-canal-thumb.jpg",
  "featured_image_url": "/images/air-communities/one-canal-hero.jpg",
  "featured_image_alt": "One Canal apartments in Boston's West End",
  "content_html": "<p>One Canal is a luxury apartment community...</p><h2>What floor plans are available?</h2><p>...</p>",
  "faqs": [
    {
      "question": "What is the cheapest apartment at One Canal?",
      "answer": "Studio apartments start at $2,400 per month (as of Q3 2026)."
    },
    {
      "question": "Is One Canal pet-friendly?",
      "answer": "Yes, One Canal allows pets with breed restrictions and monthly pet rent."
    }
  ],
  "status": "published"
}

Success Response (201):
{
  "success": true,
  "id": "art_xxxxxxxxxxxx",
  "url": "https://aircommunities.brightplace.ai/air-communities/one-canal-boston-guide",
  "message": "Article published"
}

Error Response (400/401/500):
{
  "success": false,
  "error": "Invalid slug format",
  "code": "VALIDATION_ERROR"
}
```

---

### Endpoint 2: Update Article

```
PUT /api/cms/articles/{id}

Headers:
  Authorization: Bearer sk_air_xxxxxxxxxxxxx

Request Body: (same fields as create, only include fields being updated)
{
  "content_html": "<p>Updated content...</p>",
  "date_modified": "2026-09-15"
}

Response (200):
{
  "success": true,
  "id": "art_xxxxxxxxxxxx",
  "url": "...",
  "message": "Article updated"
}
```

---

### Endpoint 3: List Articles

```
GET /api/cms/articles?status=published&property=one-canal

Headers:
  Authorization: Bearer sk_air_xxxxxxxxxxxxx

Response (200):
{
  "articles": [
    {
      "id": "art_xxxxxxxxxxxx",
      "title": "One Canal Apartments Boston...",
      "slug": "one-canal-boston-guide",
      "property_slug": "one-canal",
      "status": "published",
      "url": "https://aircommunities.brightplace.ai/air-communities/one-canal-boston-guide",
      "date_published": "2026-08-28",
      "date_modified": null
    }
  ],
  "total": 1
}
```

---

### Endpoint 4: Delete Article

```
DELETE /api/cms/articles/{id}

Headers:
  Authorization: Bearer sk_air_xxxxxxxxxxxxx

Response (200):
{
  "success": true,
  "message": "Article deleted and removed from sitemap"
}
```

---

### Endpoint 5: Upload Image

```
POST /api/cms/images

Headers:
  Authorization: Bearer sk_air_xxxxxxxxxxxxx
  Content-Type: multipart/form-data

Form Data:
  file: (binary image file)
  operator: "air-communities"
  property: "one-canal"
  filename: "one-canal-hero.jpg"

Response (201):
{
  "success": true,
  "url": "/images/air-communities/one-canal-hero.jpg",
  "size": "245KB",
  "dimensions": "1200x800"
}
```

---

### Endpoint 6: Create/Update Property

```
POST /api/cms/properties

Headers:
  Authorization: Bearer sk_air_xxxxxxxxxxxxx

Request Body:
{
  "operator": "air-communities",
  "slug": "one-canal",
  "name": "One Canal",
  "subtitle": "Boston's West End",
  "address": "1 Canal Street",
  "city": "Boston",
  "state": "MA",
  "zip": "02114",
  "phone": "(617) 555-0100",
  "email": "leasing@onecanal.com",
  "hero_image": "/images/air-communities/one-canal-hero.jpg",
  "hero_alt": "One Canal apartments in Boston",
  "hero_headline": "Luxury waterfront living in Boston's West End",
  "hero_description": "Studio, one, and two bedroom apartments...",
  "floor_plans": [
    { "name": "Studio", "tier": "Studio", "beds": 0, "baths": 1, "sqft": 450, "price": 2400, "img": "/images/air-communities/one-canal-studio.png", "imgAlt": "Studio floor plan" }
  ],
  "amenities": [
    { "title": "Rooftop pool", "description": "Heated pool with city views" }
  ],
  "faqs": [
    { "question": "...", "answer": "..." }
  ],
  "distances": [
    { "place": "North Station", "time": "5 min walk" }
  ],
  "hero_stats": [
    { "value": "5", "label": "Floor Plans" }
  ],
  "required_fees": [
    { "label": "Water / sewer / trash", "amount": 75 }
  ],
  "latitude": 42.3662,
  "longitude": -71.0603
}

Response (201):
{
  "success": true,
  "url": "https://aircommunities.brightplace.ai/air-communities/one-canal"
}
```

---

## PART 4: What the CMS Must Handle Automatically

When we POST an article, the site must auto-generate all of the following. **We should NOT need to send any of these — the CMS creates them from the data we provide.**

### SEO (Auto-Generated Per Article)

| What | Generated From |
|---|---|
| `<title>` tag | `meta_title` field |
| `<meta name="description">` | `meta_description` field |
| `<link rel="canonical">` | Page URL |
| `og:title`, `og:description`, `og:image` | `meta_title`, `meta_description`, `featured_image_url` |
| `twitter:card`, `twitter:title`, etc. | Same as OG |

### JSON-LD Schemas (Auto-Generated Per Article)

**Schema 1: Article**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[title]",
  "description": "[meta_description]",
  "author": { "@type": "Organization", "name": "brightplace" },
  "datePublished": "[date_published]",
  "dateModified": "[date_modified or date_published]",
  "mainEntityOfPage": "[page URL]",
  "image": "[featured_image_url]"
}
```

**Schema 2: FAQPage**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[faq.question]",
      "acceptedAnswer": { "@type": "Answer", "text": "[faq.answer]" }
    }
  ]
}
```

**Schema 3: BreadcrumbList**
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "brightplace", "item": "https://brightplace.ai" },
    { "@type": "ListItem", "position": 2, "name": "[operator name]", "item": "[operator URL]" },
    { "@type": "ListItem", "position": 3, "name": "[article title]", "item": "[article URL]" }
  ]
}
```

### Site Infrastructure (Auto-Updated)

| What | When |
|---|---|
| `sitemap.xml` | Add new URL when article created, remove when deleted |
| `llms.txt` | Add article entry when created, remove when deleted |
| Operator stories section | Show new article in the stories grid on operator page |

---

## PART 5: HTML Content Format

We send pre-formatted HTML in `content_html`. The site needs these CSS classes styled to match the existing StoryLayout design.

### Paragraphs
```html
<p>Regular paragraph text with <strong>bold</strong> and <a href="/link">links</a>.</p>
```

### Headings (H2 Only — H1 comes from title)
```html
<h2>What floor plans does One Canal offer?</h2>
```

### Data Tables
```html
<div class="data-card">
  <h4>One Canal pricing (as of Q3 2026)</h4>
  <div class="data-row"><span>Studio (450 ft²)</span><span>$2,400/mo</span></div>
  <div class="data-row"><span>1 Bed (650 ft²)</span><span>$3,200/mo</span></div>
  <div class="data-row"><span>2 Bed (1,050 ft²)</span><span>$4,500/mo</span></div>
</div>
```

### Inline CTA Cards
```html
<a href="/air-communities/one-canal#pricing" class="cta-inline">
  <div class="cta-icon">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--bp-orange)" stroke-width="2"><path d="M5 12h14m-7-7 7 7-7 7"/></svg>
  </div>
  <div>
    <p><strong>Build your all-in price at One Canal</strong></p>
    <p class="cta-subtitle">Interactive rent calculator</p>
  </div>
</a>
```

### Images
```html
<div class="image-block">
  <img src="/images/air-communities/one-canal-pool.jpg" alt="Rooftop pool at One Canal" width="1200" height="675" loading="lazy" />
  <p class="image-caption">Rooftop pool with Charles River views</p>
</div>
```

### Bold-Label Info Points (Not ul/li — those get stripped)
```html
<p><strong>Pet policy:</strong> Dogs and cats welcome. Breed restrictions apply. Monthly pet rent quoted at application.</p>
<p><strong>Parking:</strong> Garage parking available at $300/mo.</p>
<p><strong>Laundry:</strong> In-unit washer and dryer in every apartment.</p>
```

### FAQ Section
**Not in content_html.** FAQs are sent as a separate `faqs` JSON array. The CMS renders them using the existing FAQ card design (white cards with border, bold question, regular answer text).

---

## PART 6: CSS Classes Reference

These classes already exist in the current site's StoryLayout. The CMS article renderer needs the same styles:

```css
/* Data card */
.data-card { padding: 20px 24px; border-radius: 12px; background: white; border: 1px solid #E3DDCF; margin: 22px 0; box-shadow: 0 1px 3px rgba(26,39,68,.04), 0 6px 20px rgba(26,39,68,.07); }
.data-card h4 { font-family: 'Urbanist'; font-weight: 600; font-size: 14px; color: #1A2744; margin: 0 0 12px; }
.data-row { display: flex; justify-content: space-between; padding: 9px 0; border-bottom: 1px dashed rgba(227,221,207,0.5); font-family: 'Lato'; font-size: 14px; }
.data-row:last-child { border-bottom: none; }

/* CTA inline card */
.cta-inline { display: flex; align-items: center; gap: 12px; padding: 16px 20px; border-radius: 12px; background: #F3ECDE; border: 1px solid #E3DDCF; margin: 22px 0; text-decoration: none; }
.cta-inline:hover { border-color: #00BCD4; }
.cta-subtitle { font-size: 13px; color: #5C6580; }

/* Image block */
.image-block { margin: 28px 0; border-radius: 12px; overflow: hidden; }
.image-block img { width: 100%; height: auto; display: block; }
.image-caption { font-family: 'Lato'; font-size: 12px; color: #5C6580; text-align: center; margin: 8px 0 0; font-style: italic; }

/* FAQ item (rendered from faqs array) */
.faq-item { padding: 18px 20px; margin-bottom: 10px; border-radius: 12px; background: white; border: 1px solid #E3DDCF; }
.faq-item strong { font-family: 'Urbanist'; font-weight: 600; font-size: 15px; display: block; margin-bottom: 6px; color: #1A2744; }
.faq-item p { font-size: 14px; margin: 0; line-height: 1.6; color: #2B3655; }
```

---

## PART 7: Article Page Layout

When the CMS renders an article, the page should include:

```
┌─────────────────────────────────────────┐
│ Progress bar (orange, top of viewport)  │
├─────────────────────────────────────────┤
│ Header: breadcrumb + "View property"    │
├─────────────────────────────────────────┤
│ Hero image (featured_image_url)         │
├─────────────────────────────────────────┤
│ Article header card:                    │
│   - Category badge                      │
│   - Title (from title field)            │
│   - Author avatar + name + date + time  │
├──────────┬──────────────────────────────┤
│ Table of │ Article body                 │
│ Contents │ (from content_html)          │
│ sidebar  │                              │
│ (auto    │ Tables, CTAs, images         │
│  from    │                              │
│  H2s)    │ FAQ section                  │
│          │ (from faqs array)            │
│ Property │                              │
│ mini     │ Author box                   │
│ card     │                              │
│          │ Property CTA card            │
├──────────┴──────────────────────────────┤
│ Footer                                  │
├─────────────────────────────────────────┤
│ AI Chat bubble (bottom-right)           │
└─────────────────────────────────────────┘
```

The existing StoryLayout component on the demo site (operator-pages.vercel.app) is the reference for this layout.

---

## PART 8: Authentication

### API Key Per Operator

```
Authorization: Bearer sk_air_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

- Generate one API key per operator site
- Store in environment variable on the Vercel site
- Content team stores the key to make API calls
- Keys should be rotatable (regenerate if compromised)
- All endpoints require valid auth — return 401 if missing/invalid

### Rate Limiting

| Endpoint | Limit |
|---|---|
| POST articles | 50 per hour |
| PUT articles | 100 per hour |
| GET articles | 500 per hour |
| POST images | 20 per hour |

---

## PART 9: Data Storage

### Recommended: Supabase

| Table | Purpose |
|---|---|
| `articles` | Stores all article data (title, slug, content, metadata, FAQs) |
| `images` | Stores image references and URLs |
| `properties` | Stores property data (already exists as JSON, migrate to DB) |

### Why Supabase Over File-Based

| Factor | JSON Files | Supabase |
|---|---|---|
| Speed to publish | Slow (git push + rebuild) | Instant (ISR revalidation) |
| Query articles | Read all files | SQL query |
| Scale to 1000+ articles | Slow builds | No build needed |
| Update one article | Rebuild entire site | Revalidate one page |
| Search/filter | Not possible | SQL WHERE clause |

### ISR (Incremental Static Regeneration)

With Supabase, use Next.js ISR so pages are:
- Pre-rendered on first visit
- Revalidated when content changes (on-demand revalidation via API call)
- No full site rebuild needed

```typescript
// In the article page component
export const revalidate = 3600 // Revalidate every hour

// Or on-demand: call this after publishing
// POST /api/revalidate?path=/air-communities/one-canal-guide
```

---

## PART 10: Server-Side Rendering Requirement (CRITICAL)

**Every article page MUST be server-rendered.** This is non-negotiable.

When a bot (Google, ChatGPT, Perplexity, Claude) fetches the page, the full article text must be in the HTML response WITHOUT executing JavaScript.

**Test:** `curl https://[site]/air-communities/one-canal-guide | grep "One Canal"`

If the article text appears in the curl output, it's server-rendered. If not, it's broken.

This means:
- Article content must be fetched on the server (in a Server Component or getServerSideProps)
- Not fetched client-side with useEffect or fetch() in the browser
- JSON-LD schemas must be in the HTML `<head>`, not injected by JS

---

## PART 11: Testing Checklist

After the CMS is built, test by publishing one article and verify ALL of the following:

### Page Renders
- [ ] Article loads at correct URL
- [ ] Title displays correctly
- [ ] Author section shows name, date, read time
- [ ] Featured image displays in hero
- [ ] Content HTML renders with proper styling
- [ ] Data tables render as cards (not raw HTML)
- [ ] CTA inline cards render with orange icon
- [ ] Images render with captions
- [ ] FAQ cards render from faqs array
- [ ] Table of contents sidebar auto-generated from H2s
- [ ] AI chat bot appears

### SEO
- [ ] `<title>` tag matches meta_title
- [ ] `<meta name="description">` matches meta_description
- [ ] `<link rel="canonical">` points to page URL
- [ ] OG tags complete (title, description, image, url)
- [ ] Twitter card tags complete
- [ ] Article JSON-LD schema in HTML source
- [ ] FAQPage JSON-LD schema in HTML source with all Q&As
- [ ] BreadcrumbList JSON-LD schema correct

### Infrastructure
- [ ] sitemap.xml includes the new URL
- [ ] llms.txt includes the new article
- [ ] Operator stories page shows the new article card
- [ ] `curl [url]` returns full article text (server-rendered)
- [ ] Page works on mobile (375px viewport)

### API
- [ ] POST returns 201 with article ID and URL
- [ ] PUT updates content without creating duplicate
- [ ] GET lists articles with correct metadata
- [ ] DELETE removes page and updates sitemap
- [ ] 401 returned when auth header missing
- [ ] 400 returned when required fields missing

---

## PART 12: Priority and Timeline

| Priority | What | When |
|---|---|---|
| **P0** | 5 property pages built from template | This week |
| **P0** | `POST /api/cms/articles` endpoint working | This week |
| **P1** | `GET /api/cms/articles` endpoint | Next week |
| **P1** | `PUT /api/cms/articles/:id` endpoint | Next week |
| **P1** | `POST /api/cms/images` endpoint | Next week |
| **P2** | `DELETE /api/cms/articles/:id` | When needed |
| **P2** | `POST /api/cms/properties` | When needed (first 5 done manually) |
| **P2** | Auto sitemap + llms.txt updates | Next week |

**Once `POST /api/cms/articles` works, we can start publishing content for all 5 communities immediately.**

---

## PART 13: Reference

### Existing Demo Site
**URL:** https://operator-pages.vercel.app
**Repo:** https://github.com/haroonashfaq-cell/OPERATOR-PAGES

This site has the current design, components, and layout. The CMS article pages should look identical to the existing story pages on this site.

### Existing Story Pages (Design Reference)
- https://operator-pages.vercel.app/air-communities/oak-trail-cherry-creek-guide
- https://operator-pages.vercel.app/towne-properties/harpers-point-resort-guide

These are the target design. New CMS-published articles should render with the same layout, typography, spacing, and components.

---

## Questions

1. Which storage approach will you use? (Supabase recommended)
2. Can the article endpoint be ready this week?
3. Do you need the property data JSONs in a specific format?
4. How should we handle image uploads — Supabase Storage or Vercel Blob?
5. Should we use one shared Supabase project or one per operator?
