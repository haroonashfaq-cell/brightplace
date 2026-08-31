# 10 — Scale Architecture: From 5 Communities to 500+

## The Vision

A fully automated SEO product that:
1. Lives inside ANY website (not just our Vercel sites)
2. Researches keywords automatically
3. Writes and publishes content without human intervention
4. Works for any industry (apartments, restaurants, hotels, SaaS, e-commerce)
5. Scales to 500+ properties / 10,000+ articles

---

## Is It Possible?

**Yes.** Every piece of this exists today. We just need to connect them.

| Component | Technology | Exists Today? |
|---|---|---|
| Keyword research at scale | Semrush API | Yes — we already use it |
| Auto-brief generation | Claude API + our Brief Agent | Yes — agent written, needs API call |
| Auto-article writing | Claude API + our Writing Agent | Yes — agent written, needs API call |
| Auto-QA | Claude API + our QA Agent | Yes — agent written, needs API call |
| Auto-image generation | DALL-E / Midjourney API | Yes |
| Auto-publish to any site | CMS adapters (REST API) | Partially — need to build adapters |
| Analytics tracking | Vercel Analytics + GSC API | Yes |
| AI citation monitoring | Periodic API queries | Buildable |

**Nothing here is science fiction.** It's connecting existing APIs in a pipeline.

---

## Architecture at 500 Communities

```
┌──────────────────────────────────────────────────────────────────┐
│                    brightplace direct ENGINE                      │
│                                                                  │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────────────┐   │
│  │  Scheduler   │   │  Job Queue  │   │   Agent Workers     │   │
│  │  (cron)      │──▶│  (Redis/    │──▶│   (Claude API)      │   │
│  │              │   │   BullMQ)   │   │                     │   │
│  │ - Monthly    │   │             │   │ - Keyword Worker     │   │
│  │   keyword    │   │ - keyword   │   │ - Brief Worker       │   │
│  │   refresh    │   │ - brief     │   │ - Writing Worker     │   │
│  │ - Daily      │   │ - write     │   │ - QA Worker          │   │
│  │   analytics  │   │ - qa        │   │ - Image Worker       │   │
│  │ - Weekly AI  │   │ - publish   │   │ - Publish Worker     │   │
│  │   citation   │   │ - analytics │   │                     │   │
│  └─────────────┘   └─────────────┘   └─────────────────────┘   │
│                                              │                   │
│                                              ▼                   │
│                          ┌───────────────────────────┐          │
│                          │     Publish Adapters       │          │
│                          │                           │          │
│                          │  ┌─────────┐ ┌─────────┐ │          │
│                          │  │Next.js/ │ │Webflow  │ │          │
│                          │  │Vercel   │ │CMS API  │ │          │
│                          │  └─────────┘ └─────────┘ │          │
│                          │  ┌─────────┐ ┌─────────┐ │          │
│                          │  │WordPress│ │Shopify  │ │          │
│                          │  │REST API │ │API      │ │          │
│                          │  └─────────┘ └─────────┘ │          │
│                          │  ┌─────────┐ ┌─────────┐ │          │
│                          │  │Sanity   │ │Custom   │ │          │
│                          │  │API      │ │Webhook  │ │          │
│                          │  └─────────┘ └─────────┘ │          │
│                          └───────────────────────────┘          │
└──────────────────────────────────────────────────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │    DATA LAYER        │
                    │    (Supabase)        │
                    │                     │
                    │ operators     500+   │
                    │ properties   5,000+  │
                    │ keywords    50,000+  │
                    │ articles    10,000+  │
                    │ analytics   daily    │
                    └─────────────────────┘
```

---

## How It Works at Scale

### Step 1: Onboard Operator (One-Time, 10 Minutes)

Operator provides:
- Brand name, voice guidelines, terminology
- Property list with addresses
- CMS connection (Webflow API key, WordPress login, Vercel project, or webhook URL)

System stores in Supabase. Done. No developer needed.

### Step 2: Auto-Research (Monthly, Fully Automated)

**Scheduler triggers keyword research for ALL operators.**

```
For each operator:
  For each property:
    → Call Semrush API: branded keywords ("[property] apartments")
    → Call Semrush API: location keywords ("apartments near [landmark]")
    → Call Semrush API: amenity keywords ("[amenity] apartments [city]")
    → Call Semrush API: get KD + volume for all
    → Filter: KD < 40, volume > 30, editorial SERP
    → Store in keywords table with status = "suggested"
    → Notify operator (email/dashboard) with new suggestions
```

**At 500 properties:** ~5,000 Semrush API calls/month. Cost: ~$50-100 in API credits.

### Step 3: Auto-Approve or Human Approve

Two modes:
- **Manual:** Operator reviews keywords in dashboard, clicks approve
- **Auto:** System auto-approves keywords matching criteria (KD < 25, volume > 100, branded)

For scale, most operators will set auto-approve rules. Only flag unusual keywords for review.

### Step 4: Auto-Write (Fully Automated)

**When keyword is approved, pipeline runs automatically:**

```
Keyword approved
  → Job Queue: "generate-brief"
    → Claude API call (Brief Agent prompt + keyword + property data)
    → Brief saved to Supabase

  → Job Queue: "write-article" (triggers after brief)
    → Claude API call (Writing Agent prompt + brief + brand context + property data)
    → Article saved to Supabase

  → Job Queue: "qa-article" (triggers after write)
    → Claude API call (QA Agent prompt + article + property data)
    → If PASS: status = "qa_passed"
    → If FAIL: auto-fix, re-run QA (max 3 retries)

  → Job Queue: "generate-image" (triggers after QA)
    → DALL-E API call or image selection from library
    → Image saved

  → Job Queue: "publish" (triggers after image)
    → Detect operator's CMS type
    → Call appropriate adapter (Webflow/WordPress/Vercel/webhook)
    → Verify published URL
    → Update sitemap + llms.txt
    → Status = "published"
```

**Time per article: 3-5 minutes, fully automated.**
**At 500 properties, 2 articles each: 1,000 articles in ~3 days of processing.**

### Step 5: Auto-Analytics (Daily, Fully Automated)

```
Daily cron:
  For each published article:
    → Pull page views from analytics (Vercel/GA API)
    → Pull search impressions from Google Search Console API
    → Store in analytics table

Weekly cron:
  For each operator:
    → Check AI citations (query ChatGPT/Perplexity with target keywords)
    → Store citation data

Monthly:
  → Generate operator report
  → Email to operator
  → Flag underperforming articles for refresh
```

---

## "Lives in Any Site" — The Adapter System

The key to plug-and-play is the **Publish Adapter** pattern:

```typescript
interface PublishAdapter {
  type: 'vercel' | 'webflow' | 'wordpress' | 'shopify' | 'webhook'

  // Connection
  connect(credentials: CmsCredentials): Promise<boolean>

  // Publishing
  publishArticle(article: Article): Promise<{ url: string; success: boolean }>
  publishProperty(property: Property): Promise<{ url: string; success: boolean }>
  uploadImage(image: ImageData): Promise<{ url: string }>

  // Verification
  verifyPublished(url: string): Promise<{ live: boolean; seo: SeoCheck }>

  // Sitemap
  updateSitemap(urls: string[]): Promise<boolean>
}
```

### Adapter: Vercel/Next.js
```
- Creates JSON data file in repo via GitHub API
- Triggers Vercel rebuild via deploy hook
- Verifies after deploy
```

### Adapter: Webflow
```
- Calls Webflow CMS API to create collection item
- Maps fields: name, slug, post-body, seo-title, meta-description
- Publishes via Webflow publish API
```

### Adapter: WordPress
```
- Calls WP REST API: POST /wp-json/wp/v2/posts
- Sets: title, slug, content, excerpt, status, meta (Yoast/RankMath)
- Uploads featured image via media endpoint
```

### Adapter: Shopify
```
- Calls Shopify Storefront API for blog posts
- Maps to Shopify blog article format
```

### Adapter: Generic Webhook
```
- POST to operator's webhook URL with article JSON
- Operator's system handles rendering
- We verify the published URL after
```

**Operator connects once. We publish forever.**

---

## Cost at Scale

### 500 Properties, 2 Articles Each = 1,000 Articles

| Service | Monthly Cost | Notes |
|---|---|---|
| Claude API | $200-400 | ~$0.30 per article (brief + write + QA) |
| Semrush API | $100 | 5,000 keyword lookups |
| Supabase | $25 | Pro plan handles millions of rows |
| Vercel | $20 | Pro plan for dashboard |
| Image generation | $50-100 | DALL-E at $0.04/image |
| **Total** | **$400-650/mo** | |

**Cost per article: ~$0.50-0.65**

If we charge operators $50-100/article, that's **98% margin**.
If subscription: $500/mo per operator for 10 articles = $250K/mo at 500 operators.

---

## What Needs to Be Built (In Order)

### Phase 1: CMS API (Now — Tom & Dennis)
- Single endpoint that accepts article JSON
- Works for our current 5 AIR communities
- Simple API key auth

### Phase 2: Job Queue + Workers (Next Month)
- BullMQ or similar job queue
- Claude API integration (agents become API calls)
- Semrush API integration
- Sequential pipeline: keyword → brief → write → QA → publish

### Phase 3: Dashboard (Month 2)
- Operator login
- Keyword review/approve UI
- Article pipeline status view
- Basic analytics

### Phase 4: Publish Adapters (Month 3)
- Vercel adapter (current, refine)
- Webflow adapter
- WordPress adapter
- Generic webhook adapter

### Phase 5: Full Automation (Month 4)
- Auto-approve rules
- Scheduled keyword research
- Auto-publish pipeline
- Monthly reporting
- AI citation monitoring

### Phase 6: Multi-Industry (Month 5+)
- Remove apartment-specific assumptions
- Generic "business" and "location" data models
- Industry-specific writing agent variants
- Works for: restaurants, hotels, dentists, law firms, e-commerce

---

## Can We Do This?

**Yes. Here's the honest assessment:**

| Question | Answer |
|---|---|
| Does the AI writing quality scale? | Yes — Claude API is the same quality at 1 or 10,000 articles |
| Does Semrush data scale? | Yes — API handles millions of lookups |
| Can we publish to any CMS? | Yes — every major CMS has an API |
| Is 500 operators realistic? | Yes — it's a $250K/mo business at $500/operator |
| What's the bottleneck? | Image generation and QA accuracy at scale |
| What's the risk? | Google detecting mass AI content. Mitigation: entity-dense, data-specific, property-unique content that AI-detectors can't flag because it contains real data |

---

## The Key Insight

**This is not a website product. It's a content API.**

The website is just the display layer. The real product is:
1. Automated keyword research
2. Automated content generation (with real data, not fluff)
3. Automated publishing to any platform
4. Automated performance tracking

The operator doesn't care HOW the content gets on their site. They care that it ranks, drives traffic, and generates leads.

**brightplace direct = Content-as-a-Service for any business with a website.**
