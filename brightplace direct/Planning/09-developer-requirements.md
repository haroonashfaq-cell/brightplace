# Developer Requirements — From Content Team to Dev Team (Tom & Dennis)

**Date:** August 27, 2026
**From:** Haroon (Content Strategy)
**To:** Tom & Dennis (Developer Team)
**Priority:** High — AIR Communities is locked, 5 communities ready to build

---

## What We Need (Simple Version)

**Give us a CMS endpoint for each operator site so we can push content from Claude Code without touching the codebase.**

Right now to publish an article, we have to:
1. Write the article
2. Open the codebase
3. Edit TypeScript files
4. Add data to JSON
5. Run `npm run build`
6. Git commit + push
7. Wait for Vercel deploy

**What we want:**
1. Write the article
2. Send it to a CMS API
3. It appears on the site automatically

---

## What We Need From You

### 1. CMS API Endpoint (Critical)

We need ONE API endpoint per operator site that accepts article data and publishes it.

**Endpoint:** `POST /api/content/publish`

**What we send:**
```json
{
  "operator": "air-communities",
  "type": "article",
  "data": {
    "title": "One Canal Apartments Boston: Pricing and What to Know",
    "slug": "one-canal-boston-guide",
    "meta_title": "One Canal Boston: Pricing & Guide | brightplace",
    "meta_description": "One Canal apartments in Boston. Floor plans from $X/mo...",
    "content_html": "<h2>What floor plans does One Canal offer?</h2><p>...</p>",
    "featured_image": "/images/air-communities/one-canal-hero.jpg",
    "author": "brightplace Research",
    "date_published": "2026-08-28",
    "primary_keyword": "one canal apartments boston",
    "property_slug": "one-canal",
    "faqs": [
      { "question": "...", "answer": "..." }
    ]
  }
}
```

**What should happen:**
- Article page created at `/air-communities/one-canal-boston-guide`
- JSON-LD schemas auto-generated (Article, FAQPage, BreadcrumbList)
- Sitemap updated
- llms.txt updated
- Site rebuilds automatically

**Authentication:** API key or token so only we can publish.

### 2. Property Page Creation Endpoint

Same concept but for creating property pages (not articles).

**Endpoint:** `POST /api/content/property`

**What we send:**
```json
{
  "operator": "air-communities",
  "data": {
    "slug": "one-canal",
    "name": "One Canal",
    "subtitle": "Boston's West End",
    "address": "1 Canal Street",
    "city": "Boston",
    "state": "MA",
    "zip": "02114",
    "phone": "(617) 555-0100",
    "heroImage": "/images/air-communities/one-canal-hero.jpg",
    "floorPlans": [...],
    "amenities": [...],
    "faqs": [...],
    "distances": [...],
    "heroStats": [...]
  }
}
```

**What should happen:**
- Property page created at `/air-communities/one-canal`
- Full page with hero, rent calculator, floor plans, amenities, etc.
- All JSON-LD schemas generated
- Sitemap updated

### 3. Image Upload Endpoint

**Endpoint:** `POST /api/content/upload-image`

**What we send:** Image file + metadata
```json
{
  "operator": "air-communities",
  "property": "one-canal",
  "filename": "one-canal-hero.jpg",
  "file": [binary image data]
}
```

**What should happen:**
- Image stored in `/public/images/air-communities/one-canal-hero.jpg`
- Returns the URL path we can use in content

---

## Why We Need This

### Current Problem
Every time we write an article, we need to:
- Edit `src/data/stories.tsx` (TypeScript code)
- Know the component structure
- Run builds locally
- Handle git operations

**This means I (Haroon) need developer help for every single article.** That doesn't scale when we're writing 10+ articles per week across multiple operators.

### What This Solves
With a CMS API:
- Content team writes → sends to API → article is live
- No codebase knowledge needed
- No build commands needed
- No git operations needed
- Claude Code sends directly to the API
- Multiple operators can be managed simultaneously

---

## Technical Suggestions (You Decide Implementation)

### Option A: Next.js API Routes + JSON Files
- API routes in the Next.js app itself
- Content stored as JSON files in `/src/data/`
- On-demand ISR rebuilds changed pages
- Simplest to build, works with current architecture

### Option B: Next.js API Routes + Supabase
- API routes call Supabase to store content
- Pages read from Supabase at build time
- ISR or webhook triggers rebuild
- Better for scale, more complex

### Option C: Headless CMS (Sanity/Contentful)
- Content team uses CMS UI to create/edit
- Site pulls from CMS at build time
- Webhook triggers Vercel rebuild
- Most user-friendly but adds third-party dependency

### Our Preference
**Option A for now, Option B when we scale.** We just need a simple API that accepts JSON and creates pages. We don't need a visual CMS editor — Claude Code is our editor.

---

## What We Will Handle (Not Your Problem)

- Keyword research (Semrush)
- Content brief creation
- Article writing (Claude)
- Quality assurance
- Image prompt generation
- Deciding WHAT content to publish and WHEN

**You handle HOW it gets on the site. We handle WHAT goes on the site.**

---

## Timeline

| What | When |
|---|---|
| 5 property pages for AIR communities | Need from you ASAP |
| CMS API endpoint (articles) | Need within 1 week |
| CMS API endpoint (properties) | Can wait, we'll do first 5 manually |
| Image upload endpoint | Can wait, we'll use git for images initially |

---

## The 5 Communities We're Starting With

| # | Property | City | Address |
|---|---|---|---|
| 1 | One Canal | Boston, MA | 1 Canal Street |
| 2 | Indigo West | Orlando, FL | 6101 Raleigh Street |
| 3 | One Boynton | Boynton Beach, FL | 1351 S Federal Hwy |
| 4 | 3400 Avenue of the Arts | Costa Mesa, CA | 3400 Avenue of the Arts |
| 5 | Citigate | Jacksonville, FL | 8451 Gate Pkwy W |

For each we need:
1. Property page built (from template)
2. Property data researched and populated (we can provide JSON)
3. Images (we'll source from AIR Communities or their websites)

---

## Questions for You

1. Which option (A/B/C) do you prefer for the CMS API?
2. Can you build the API endpoint this week?
3. Do you need us to provide the property data in a specific format?
4. How should we handle authentication for the API?
5. Should we use the existing operator-pages repo or create a new repo per operator?
