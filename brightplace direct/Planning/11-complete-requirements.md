# 11 — Complete Requirements Document

## Everything We Need to Build brightplace direct as a Product

---

## PART 1: ACCOUNTS & API KEYS NEEDED

### Must Have (Before Building)

| Service | What | Why | Cost | Who Sets Up |
|---|---|---|---|---|
| **Anthropic (Claude API)** | API key | Powers all writing, QA, brief generation agents | $0.30/article | Haroon |
| **Semrush API** | API key from existing plan | Keyword research: volume, KD, competitor data | Already have plan | Haroon |
| **Supabase** | Project + keys | Database: operators, properties, keywords, articles, analytics | Free tier → $25/mo | Tom/Dennis |
| **Vercel** | Team account + deploy hooks | Hosts operator sites + dashboard | $20/mo Pro | Tom/Dennis |
| **GitHub** | Repo access + API token | Code storage, triggers deploys, publish adapter for Vercel | Free | Already have |

### Nice to Have (Phase 2+)

| Service | What | Why | Cost |
|---|---|---|---|
| **OpenAI (DALL-E)** | API key | Auto-generate featured images | $0.04/image |
| **Google Search Console API** | OAuth credentials | Track keyword rankings, impressions, clicks per article | Free |
| **Google Analytics / Vercel Analytics** | API access | Track page views, CTA clicks | Free with Vercel |
| **Resend or SendGrid** | API key | Email monthly reports to operators | Free tier |
| **Redis / Upstash** | Connection string | Job queue for pipeline orchestration (BullMQ) | Free tier → $10/mo |
| **Webflow API** | API token per operator site | Publish adapter for Webflow sites | Included in Webflow plan |
| **WordPress REST API** | Application password per site | Publish adapter for WordPress sites | Free |

---

## PART 2: TOOLS & SOFTWARE NEEDED

### Development Tools

| Tool | Purpose | Who Uses |
|---|---|---|
| **Claude Code (current)** | Run agents locally during testing phase | Haroon |
| **VS Code or Cursor** | Code editor for dev team | Tom/Dennis |
| **Node.js 18+** | Runtime for backend API | Tom/Dennis |
| **pnpm or npm** | Package manager | Tom/Dennis |
| **Git** | Version control | Everyone |
| **Postman or Insomnia** | Test API endpoints | Everyone |

### Infrastructure

| Tool | Purpose | Who Manages |
|---|---|---|
| **Vercel** | Hosts: operator sites + dashboard + API routes | Tom/Dennis |
| **Supabase** | Hosts: database + auth + file storage | Tom/Dennis |
| **GitHub Actions** | CI/CD: auto-deploy on push, run scheduled jobs | Tom/Dennis |
| **Upstash Redis** | Job queue for async pipeline (serverless, Vercel-compatible) | Tom/Dennis |

### Content Tools

| Tool | Purpose | Who Uses |
|---|---|---|
| **Semrush** | Keyword research data | Haroon + automated via API |
| **Claude API** | Content generation | Automated pipeline |
| **Unsplash / DALL-E** | Images (stock or generated) | Automated |

---

## PART 3: DATABASE SCHEMA (Supabase)

```sql
-- ========================
-- OPERATORS
-- ========================
CREATE TABLE operators (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  brand_voice TEXT,              -- "professional", "casual", "editorial"
  brand_guidelines JSONB,        -- colors, fonts, terminology, banned words
  business_context TEXT,          -- company description, mission
  markets TEXT[],                 -- ["Boston", "Orlando", "Jacksonville"]
  website_url TEXT,               -- "aircommunities.brightplace.ai"
  cms_type TEXT NOT NULL,         -- "vercel", "webflow", "wordpress", "webhook"
  cms_credentials JSONB,          -- encrypted: API key, deploy hook, etc.
  status TEXT DEFAULT 'active',   -- active, paused, churned
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ========================
-- PROPERTIES (Communities)
-- ========================
CREATE TABLE properties (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  operator_id UUID REFERENCES operators(id),
  name TEXT NOT NULL,
  slug TEXT NOT NULL,
  address TEXT,
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  zip TEXT,
  phone TEXT,
  latitude DECIMAL,
  longitude DECIMAL,
  floor_plans JSONB,              -- [{name, beds, baths, sqft, price}]
  amenities JSONB,                -- [{title, description}]
  pet_policy TEXT,
  neighborhood_description TEXT,
  hero_image_url TEXT,
  page_url TEXT,                  -- live URL on operator site
  search_volume INT,              -- branded keyword volume
  keyword_difficulty INT,         -- branded keyword KD
  status TEXT DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(operator_id, slug)
);

-- ========================
-- KEYWORDS
-- ========================
CREATE TABLE keywords (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  operator_id UUID REFERENCES operators(id),
  property_id UUID REFERENCES properties(id),  -- NULL for operator-level keywords
  keyword TEXT NOT NULL,
  search_volume INT,
  keyword_difficulty INT,
  cpc DECIMAL,
  search_intent TEXT,              -- "informational", "navigational", "transactional"
  tier TEXT,                       -- "quick_win", "long_tail", "informational", "gap"
  suggested_title TEXT,
  suggested_angle TEXT,
  reasoning TEXT,
  status TEXT DEFAULT 'suggested', -- suggested, approved, rejected, writing, published
  approved_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ========================
-- ARTICLES
-- ========================
CREATE TABLE articles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  operator_id UUID REFERENCES operators(id),
  property_id UUID REFERENCES properties(id),
  keyword_id UUID REFERENCES keywords(id),
  title TEXT NOT NULL,
  slug TEXT NOT NULL,
  meta_title TEXT,                 -- under 60 chars
  meta_description TEXT,           -- under 155 chars
  primary_keyword TEXT,
  secondary_keywords TEXT[],
  content_markdown TEXT,           -- full article in markdown
  content_html TEXT,               -- converted HTML
  brief_json JSONB,                -- the brief that was generated
  qa_report JSONB,                 -- QA pass/fail results
  featured_image_url TEXT,
  featured_image_alt TEXT,
  author TEXT DEFAULT 'brightplace Research',
  word_count INT,
  faqs JSONB,                      -- [{question, answer}] for schema
  published_url TEXT,              -- live URL after publishing
  status TEXT DEFAULT 'draft',     -- draft, brief, writing, qa_pass, qa_fail, published
  published_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(operator_id, slug)
);

-- ========================
-- PIPELINE JOBS
-- ========================
CREATE TABLE pipeline_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  article_id UUID REFERENCES articles(id),
  job_type TEXT NOT NULL,           -- "brief", "write", "qa", "image", "publish"
  status TEXT DEFAULT 'queued',     -- queued, processing, completed, failed
  input_data JSONB,
  output_data JSONB,
  error_message TEXT,
  retries INT DEFAULT 0,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ========================
-- ANALYTICS (daily snapshots)
-- ========================
CREATE TABLE analytics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  article_id UUID REFERENCES articles(id),
  date DATE NOT NULL,
  page_views INT DEFAULT 0,
  unique_visitors INT DEFAULT 0,
  avg_time_on_page INT,            -- seconds
  bounce_rate DECIMAL,
  cta_clicks JSONB,                -- {tour: 5, call: 2, email: 1}
  search_impressions INT DEFAULT 0,
  search_clicks INT DEFAULT 0,
  avg_position DECIMAL,
  ai_citations INT DEFAULT 0,      -- detected mentions in AI responses
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(article_id, date)
);

-- ========================
-- OPERATOR REPORTS (monthly)
-- ========================
CREATE TABLE reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  operator_id UUID REFERENCES operators(id),
  period TEXT NOT NULL,             -- "2026-08"
  total_articles INT,
  total_page_views INT,
  total_cta_clicks INT,
  total_search_impressions INT,
  total_ai_citations INT,
  top_articles JSONB,              -- [{title, views, clicks}]
  top_keywords JSONB,              -- [{keyword, position, impressions}]
  recommendations JSONB,           -- [{type, description}]
  report_html TEXT,                -- rendered HTML report
  sent_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

---

## PART 4: API ENDPOINTS NEEDED

### Content API (For Claude Code / Automated Pipeline)

```
Authentication: Bearer token (per operator)

POST   /api/operators                     Create operator
GET    /api/operators                     List all operators
GET    /api/operators/:id                 Get operator details

POST   /api/properties                    Create property
GET    /api/properties?operator=:id       List properties for operator
PUT    /api/properties/:id                Update property data

POST   /api/keywords/research             Trigger keyword research for operator
GET    /api/keywords?operator=:id         List keyword suggestions
PUT    /api/keywords/:id/approve          Approve keyword
PUT    /api/keywords/:id/reject           Reject keyword

POST   /api/articles/generate             Trigger full pipeline (brief→write→QA→publish)
POST   /api/articles                      Create article manually (send content)
GET    /api/articles?operator=:id         List articles with status
GET    /api/articles/:id                  Get article with content
PUT    /api/articles/:id                  Update article
POST   /api/articles/:id/publish          Trigger publish only

POST   /api/images/upload                 Upload image
GET    /api/images?operator=:id           List images

GET    /api/analytics?operator=:id        Get analytics data
GET    /api/reports?operator=:id          Get monthly reports
POST   /api/reports/:operator/generate    Generate monthly report
```

### Webhook Endpoints (For CMS Callbacks)

```
POST   /api/webhooks/published            CMS confirms article is live
POST   /api/webhooks/analytics            Receive analytics data push
```

---

## PART 5: PIPELINE WORKER SPECS

### Each worker is a serverless function or background job:

**1. Keyword Research Worker**
```
Input:  operator_id
Calls:  Semrush API (phrase_related, phrase_questions, phrase_kdi, phrase_these)
Output: Array of keyword objects saved to keywords table
Cost:   ~$0.10 per operator (API calls)
Time:   30-60 seconds
```

**2. Brief Generation Worker**
```
Input:  keyword_id + operator context + property data
Calls:  Claude API (claude-sonnet-4-20250514 with brief-agent.md as system prompt)
Output: Brief JSON saved to articles table
Cost:   ~$0.05 (1K input tokens, 2K output tokens)
Time:   10-15 seconds
```

**3. Article Writing Worker**
```
Input:  article_id (with brief) + brand guidelines + property data
Calls:  Claude API (claude-sonnet-4-20250514 with writing-agent.md as system prompt)
Output: Article markdown + HTML saved to articles table
Cost:   ~$0.15 (3K input tokens, 4K output tokens)
Time:   30-60 seconds
```

**4. QA Worker**
```
Input:  article_id (with content) + property data
Calls:  Claude API (claude-sonnet-4-20250514 with qa-agent.md as system prompt)
Output: QA report JSON, status updated
Cost:   ~$0.10 (4K input tokens, 1K output tokens)
Time:   15-20 seconds
If fail: auto-fix call (~$0.10 more), max 3 retries
```

**5. Image Generation Worker**
```
Input:  article title + primary keyword + property type
Calls:  DALL-E API or image library lookup
Output: Image URL saved to articles table
Cost:   ~$0.04 (DALL-E) or $0 (library)
Time:   10-30 seconds
```

**6. Publish Worker**
```
Input:  article_id (with content + image)
Calls:  CMS adapter based on operator.cms_type
  - Vercel: GitHub API → create file → deploy hook
  - Webflow: CMS Collection Item API
  - WordPress: REST API /wp-json/wp/v2/posts
  - Webhook: POST to operator's URL
Output: published_url saved, status = "published"
Cost:   $0 (API calls to CMS)
Time:   30-120 seconds (depends on CMS rebuild time)
```

**7. Analytics Worker (Daily Cron)**
```
Input:  all published articles
Calls:  Vercel Analytics API + Google Search Console API
Output: Daily row in analytics table per article
Cost:   $0
Time:   5-10 minutes for all articles
```

**Total cost per article through full pipeline: ~$0.45-0.55**

---

## PART 6: FRONTEND PAGES NEEDED (Dashboard)

### Operator Dashboard

| Page | What It Shows |
|---|---|
| `/dashboard` | Overview: total articles, total traffic, recent activity |
| `/dashboard/keywords` | Keyword suggestions table (approve/reject buttons) |
| `/dashboard/articles` | Article pipeline (status: brief → writing → QA → published) |
| `/dashboard/analytics` | Traffic charts, top articles, CTA clicks |
| `/dashboard/reports` | Monthly reports archive |
| `/dashboard/properties` | Property list with edit capability |
| `/dashboard/settings` | Brand guidelines, CMS connection, API keys |

### Admin Dashboard (Our Internal)

| Page | What It Shows |
|---|---|
| `/admin` | All operators overview |
| `/admin/operators/:id` | Operator detail + pipeline status |
| `/admin/pipeline` | Job queue monitor (running, failed, completed) |
| `/admin/costs` | API usage + cost tracking per operator |

---

## PART 7: SECURITY REQUIREMENTS

| Concern | Solution |
|---|---|
| API authentication | Bearer tokens per operator, rotatable |
| CMS credentials storage | Encrypted in Supabase (pgcrypto or Vault) |
| Operator isolation | Row-level security in Supabase (operator can only see own data) |
| Rate limiting | Per-operator API rate limits (prevent abuse) |
| Content approval | Optional human-in-the-loop before publish |
| API key rotation | Dashboard UI to regenerate tokens |
| Audit log | Track all publish actions with timestamps |

---

## PART 8: THIRD-PARTY INTEGRATIONS

### Required Integrations

| Service | Integration Type | What For |
|---|---|---|
| Claude API (Anthropic) | REST API | Writing, QA, brief generation |
| Semrush | REST API | Keyword data |
| GitHub | REST API | File creation for Vercel adapter |
| Vercel | Deploy Hooks | Trigger rebuilds after publish |

### Optional Integrations (Phase 2+)

| Service | Integration Type | What For |
|---|---|---|
| Webflow | REST API | CMS publish adapter |
| WordPress | REST API | CMS publish adapter |
| Shopify | Storefront API | Blog publish adapter |
| Google Search Console | OAuth + API | Ranking tracking |
| Google Analytics | GA4 API | Traffic data |
| DALL-E (OpenAI) | REST API | Image generation |
| Resend | REST API | Email reports |
| Slack | Webhook | Team notifications |
| Stripe | REST API | Operator billing (future) |

---

## PART 9: WHAT WE NEED FROM EACH PERSON

### From Tom & Dennis (Developer Team)

**Immediate (This Week):**
1. Set up Supabase project with schema from Part 3
2. Build `POST /api/articles` endpoint (accepts article JSON, creates page)
3. Build Vercel publish adapter (create file via GitHub API + deploy hook)
4. API key auth middleware
5. Deploy 5 AIR community property pages (we provide data)

**Next Sprint:**
6. Build job queue with Upstash Redis
7. Connect Claude API for automated brief/write/QA
8. Build `/dashboard/keywords` page
9. Build `/dashboard/articles` page

### From Haroon (Content Team)

**Immediate (This Week):**
1. Research property data for 5 AIR communities (floor plans, amenities, pricing)
2. Source images from AIR community websites
3. Provide property JSON files to dev team
4. Test article publish endpoint once built

**Next Sprint:**
5. Run keyword research for each community
6. Write first batch of articles
7. Define auto-approve rules for keywords
8. Test full pipeline end-to-end

### From Claude (AI)

**Now:** Execute agents manually via Claude Code
**Phase 2:** Execute agents via API calls from backend workers
**Phase 3:** Fully autonomous — scheduler triggers, no human needed

---

## PART 10: TIMELINE

| Week | Dev Team | Content Team |
|---|---|---|
| **Week 1** | Supabase schema + API endpoint + 5 property pages | Research 5 communities + provide data JSONs |
| **Week 2** | Publish adapter (Vercel) + auth middleware | Write 2 articles per community (10 total) + test API |
| **Week 3** | Job queue + Claude API integration | Keyword research for next 5 communities |
| **Week 4** | Dashboard MVP (keywords + articles pages) | Write more articles, test auto-pipeline |
| **Month 2** | Webflow adapter + auto-publish + analytics | Onboard 2nd operator, expand content |
| **Month 3** | WordPress adapter + monthly reports + billing | Scale to 50+ properties |

---

## SUMMARY: What We Need to Buy/Sign Up For

| Service | Action | Cost | Priority |
|---|---|---|---|
| Anthropic Claude API | Sign up, get API key | Pay-per-use (~$0.30/article) | Now |
| Supabase | Create project | Free → $25/mo | Now |
| Upstash Redis | Create account | Free → $10/mo | Week 2 |
| Vercel Pro | Upgrade if needed | $20/mo | Already have |
| Domain (per operator) | Set up subdomain | Free (DNS) | Per operator |
| DALL-E API | Sign up (optional) | $0.04/image | Phase 2 |
| Google Search Console | Verify domains | Free | Phase 2 |
| Resend (email) | Sign up | Free tier | Phase 3 |
| Stripe (billing) | Sign up | 2.9% per transaction | Phase 4 |
