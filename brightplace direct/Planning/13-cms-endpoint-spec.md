# CMS Endpoint Spec — What We Need From Dev Team

**Date:** August 27, 2026
**From:** Haroon
**To:** Tom & Dennis
**Subject:** Build a CMS with API endpoints in each operator site

---

## What We Need

Build a simple CMS inside each operator's Vercel site. Give us API endpoints. We POST content, it appears as a page. Like Webflow CMS but built into the Next.js site.

**We handle:** writing content, formatting it, sending it to the endpoint
**You handle:** storing it, rendering it as a page, SEO schemas, sitemap

---

## Endpoints We Need

### 1. Create Article
```
POST /api/cms/articles
Authorization: Bearer {api_key}

Body:
{
  "title": "One Canal Apartments Boston: Pricing and What to Know",
  "slug": "one-canal-boston-guide",
  "meta_title": "One Canal Boston: Pricing & Guide | brightplace",
  "meta_description": "One Canal apartments in Boston...",
  "property_slug": "one-canal",
  "author": "brightplace Research",
  "date_published": "2026-08-28",
  "read_time": "7 min",
  "primary_keyword": "one canal apartments boston",
  "thumbnail_url": "/images/air-communities/one-canal-thumb.jpg",
  "featured_image_url": "/images/air-communities/one-canal-hero.jpg",
  "featured_image_alt": "One Canal apartments overlooking the Charles River in Boston",
  "content_html": "<p>One Canal is a luxury apartment...</p><h2>What floor plans are available?</h2>...",
  "faqs": [
    {
      "question": "What is the cheapest apartment at One Canal?",
      "answer": "Studio apartments start at $2,400 per month (as of Q3 2026)."
    },
    {
      "question": "Is One Canal pet-friendly?",
      "answer": "Yes. One Canal allows pets with breed restrictions and monthly pet rent."
    }
  ],
  "status": "published"
}

Response:
{
  "success": true,
  "id": "article_abc123",
  "url": "https://aircommunities.brightplace.ai/air-communities/one-canal-boston-guide",
  "message": "Article published successfully"
}
```

### 2. Update Article
```
PUT /api/cms/articles/{id}
Authorization: Bearer {api_key}

Body: (same fields as create, only send changed fields)

Response:
{
  "success": true,
  "id": "article_abc123",
  "url": "...",
  "message": "Article updated"
}
```

### 3. List Articles
```
GET /api/cms/articles
Authorization: Bearer {api_key}

Query params: ?operator=air-communities&status=published

Response:
{
  "articles": [
    {
      "id": "article_abc123",
      "title": "One Canal Apartments Boston...",
      "slug": "one-canal-boston-guide",
      "status": "published",
      "url": "...",
      "date_published": "2026-08-28"
    }
  ],
  "total": 1
}
```

### 4. Delete Article
```
DELETE /api/cms/articles/{id}
Authorization: Bearer {api_key}

Response:
{
  "success": true,
  "message": "Article deleted"
}
```

### 5. Upload Image
```
POST /api/cms/images
Authorization: Bearer {api_key}
Content-Type: multipart/form-data

Body:
  file: (binary image)
  operator: "air-communities"
  property: "one-canal"
  filename: "one-canal-hero.jpg"

Response:
{
  "success": true,
  "url": "/images/air-communities/one-canal-hero.jpg",
  "size": "245KB"
}
```

### 6. Create/Update Property
```
POST /api/cms/properties
Authorization: Bearer {api_key}

Body:
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
  "hero_image": "/images/air-communities/one-canal-hero.jpg",
  "floor_plans": [...],
  "amenities": [...],
  "faqs": [...],
  "distances": [...]
}

Response:
{
  "success": true,
  "url": "https://aircommunities.brightplace.ai/air-communities/one-canal"
}
```

---

## What the CMS Should Handle Automatically

When we POST an article, the site should automatically:

| Task | How |
|---|---|
| Create the page at the right URL | Route: `/[operator]/[slug]` |
| Render our HTML content properly | Tables, images, CTAs, FAQ cards |
| Generate Article JSON-LD schema | From title, author, date, description |
| Generate FAQPage JSON-LD schema | From the faqs array we send |
| Generate BreadcrumbList schema | From operator → property → article |
| Add OG + Twitter meta tags | From meta_title, meta_description, featured_image |
| Set canonical URL | From the page URL |
| Update sitemap.xml | Add the new URL |
| Update llms.txt | Add the new article entry |
| Make it server-rendered HTML | All content in the HTML source for AI crawlers |

**We should NOT need to send schemas, meta tags, or sitemap entries. The CMS generates those from the data we provide.**

---

## HTML Content We Send

Our agents output formatted HTML. Here's what we'll send in `content_html`:

### Regular Paragraphs
```html
<p>One Canal is a luxury apartment community in Boston's West End neighborhood.</p>
```

### Headings (H2 only, H1 comes from title)
```html
<h2>What floor plans does One Canal offer?</h2>
```

### Data Tables
```html
<div class="data-card">
  <h4>One Canal floor plans and pricing (as of Q3 2026)</h4>
  <div class="data-row"><span>Studio (450 ft²)</span><span>$2,400/mo</span></div>
  <div class="data-row"><span>1 Bed (650 ft²)</span><span>$3,200/mo</span></div>
  <div class="data-row"><span>2 Bed (1,050 ft²)</span><span>$4,500/mo</span></div>
</div>
```

### CTA Cards
```html
<a href="/air-communities/one-canal#pricing" class="cta-inline">
  <div class="cta-icon">→</div>
  <div>
    <p><strong>Build your all-in price at One Canal</strong></p>
    <p class="cta-subtitle">Interactive rent calculator with add-ons</p>
  </div>
</a>
```

### Images
```html
<div class="image-block">
  <img src="/images/air-communities/one-canal-pool.jpg" alt="Rooftop pool at One Canal Boston" />
  <p class="image-caption">Rooftop pool overlooking the Charles River</p>
</div>
```

### Bold-Label Bullets (Not `<ul><li>`)
```html
<p><strong>Pet policy:</strong> Dogs and cats welcome with breed restrictions. Monthly pet rent applies.</p>
<p><strong>Parking:</strong> Garage parking available at $300/mo. Valet option available.</p>
<p><strong>Laundry:</strong> In-unit washer and dryer in every apartment.</p>
```

### FAQ Section (Rendered from `faqs` array, not in content_html)
The CMS should render FAQs from the `faqs` JSON array we send separately, NOT from the content_html. This way:
- FAQs are structured data (easy to generate schema)
- FAQ rendering is consistent across all articles
- We don't need to format FAQ HTML ourselves

---

## CSS Classes We Use in content_html

The CMS/site needs these CSS classes styled:

| Class | What It Styles |
|---|---|
| `.data-card` | White card with border, padding, shadow |
| `.data-card h4` | Card title |
| `.data-row` | Flex row with space-between for label + value |
| `.cta-inline` | Inline CTA card with border, background, hover effect |
| `.cta-icon` | Orange circle icon in CTA |
| `.cta-subtitle` | Muted text below CTA title |
| `.image-block` | Full-width image container with rounded corners |
| `.image-caption` | Centered italic caption below image |

**These already exist in the current StoryLayout component.** Just make sure the CMS article renderer includes the same CSS.

---

## Authentication

Simple API key per operator site.

```
Authorization: Bearer sk_air_xxxxxxxxxxxxxxxxxxxx
```

- One key per operator
- Key stored in environment variable on the site
- We store the key in our system to call the endpoint
- Key can be rotated from the site's admin

---

## Storage Options (You Decide)

### Option A: Supabase (Recommended)
- Articles stored in Supabase table
- Images stored in Supabase Storage
- Next.js reads from Supabase at request time (ISR with revalidate)
- No git operations needed
- Scales infinitely

### Option B: JSON Files + GitHub API
- Articles stored as JSON files in the repo
- Images in public/ folder
- Next.js reads files at build time
- Git push triggers Vercel rebuild
- Simpler but slower (rebuild on every article)

### Option C: Vercel KV or Blob
- Articles in Vercel KV (key-value store)
- Images in Vercel Blob Storage
- Native Vercel integration
- Simple but vendor-locked

**Our preference: Option A (Supabase).** It's the most flexible, already in our stack, and scales without rebuild delays.

---

## Testing Checklist

After the CMS is built, we test by posting one article and verifying:

- [ ] Article page renders at correct URL
- [ ] Title, meta tags, OG correct
- [ ] content_html renders with proper styling (tables, CTAs, images)
- [ ] FAQs render as card components
- [ ] Article JSON-LD schema present in HTML source
- [ ] FAQPage JSON-LD schema present with all Q&As
- [ ] BreadcrumbList schema correct
- [ ] Sitemap includes the new URL
- [ ] llms.txt includes the new article
- [ ] AI chat bot appears on the page
- [ ] Property CTA card at bottom links correctly
- [ ] Table of contents sidebar works
- [ ] Mobile responsive
- [ ] `curl [url] | grep "[article title]"` returns the content (server-rendered)

---

## Summary

**We need 6 endpoints:**

| # | Method | Endpoint | Priority |
|---|---|---|---|
| 1 | POST | `/api/cms/articles` | Critical — need this first |
| 2 | PUT | `/api/cms/articles/:id` | High |
| 3 | GET | `/api/cms/articles` | High |
| 4 | DELETE | `/api/cms/articles/:id` | Medium |
| 5 | POST | `/api/cms/images` | Medium |
| 6 | POST | `/api/cms/properties` | Medium |

**We send formatted HTML + metadata. CMS handles rendering, schemas, sitemap, everything else.**

Once endpoint #1 works, we can start publishing content for all 5 AIR communities immediately.
