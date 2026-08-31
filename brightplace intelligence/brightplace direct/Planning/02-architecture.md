# 02 — Architecture

## System Overview

```
┌─────────────────────────────────────────────────┐
│              OPERATOR DASHBOARD                  │
│         (app.brightplace.ai/direct)              │
│                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │ Keywords │ │ Articles │ │   Analytics      │ │
│  │ Research │ │ Pipeline │ │   & Reports      │ │
│  └────┬─────┘ └────┬─────┘ └───────┬──────────┘ │
└───────┼────────────┼───────────────┼────────────┘
        │            │               │
┌───────▼────────────▼───────────────▼────────────┐
│              CONTENT ENGINE (Backend)             │
│                                                   │
│  Keyword Agent → Brief Agent → Writing Agent      │
│       ↓              ↓             ↓              │
│  Semrush API    Auto-generate   Claude API        │
│                                    ↓              │
│                              QA Agent             │
│                                    ↓              │
│                            Image Agent            │
│                                    ↓              │
│                           Publish Agent           │
│                          ↓          ↓             │
│                    Next.js/Vercel  Webflow/WP     │
└───────────────────────────────────────────────────┘
        │                               │
┌───────▼───────┐              ┌────────▼────────┐
│   DATA LAYER  │              │  OPERATOR SITE  │
│   (Supabase)  │              │    (Vercel)     │
│               │              │                 │
│ - Operators   │              │ - Property pages│
│ - Properties  │              │ - Blog articles │
│ - Keywords    │              │ - Sitemap/SEO   │
│ - Articles    │              │ - Analytics     │
│ - Analytics   │              │                 │
└───────────────┘              └─────────────────┘
```

## Current State (Manual Testing)

```
You (laptop) → Claude Code → Agents (markdown) → Git push → Vercel auto-deploy
                    ↓
              Semrush MCP (keyword data)
```

## Production State (Target)

```
Operator (browser) → Dashboard UI → Backend API → Agents (code) → Auto-deploy
                                        ↓
                                  Claude API (writing/QA)
                                  Semrush API (keywords)
                                  Vercel API (deploy)
                                  Supabase (data)
```

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Next.js (Vercel) | Operator dashboard |
| Backend | Node.js API routes or Railway | Agent orchestration |
| Database | Supabase | Operators, properties, keywords, articles |
| AI | Claude API (Anthropic) | Writing + QA agents |
| Keywords | Semrush API | Volume, KD, competitor data |
| Deployment | Vercel | Operator site hosting + dashboard |
| Analytics | Vercel Analytics + GSC API | Traffic + keyword tracking |
| Auth | Supabase Auth | Operator login |

## Database Schema (Supabase)

```sql
-- Operators
operators (
  id, name, slug, brand_guidelines, business_context,
  markets, website_url, created_at
)

-- Properties
properties (
  id, operator_id, name, slug, city, state,
  address, floor_plans, amenities, pricing,
  hero_image, created_at
)

-- Keywords
keywords (
  id, operator_id, property_id,
  keyword, volume, kd, intent, tier,
  suggested_title, reasoning,
  status: suggested | approved | writing | published | rejected,
  created_at
)

-- Articles
articles (
  id, operator_id, property_id, keyword_id,
  title, slug, meta_title, meta_description,
  content_md, content_html,
  status: draft | qa_passed | published,
  published_url, published_at,
  created_at
)

-- Analytics (daily snapshots)
analytics (
  id, article_id, date,
  page_views, unique_visitors,
  cta_clicks, search_impressions,
  avg_position
)
```

## API Endpoints

```
POST /api/keywords/research    → Runs Keyword Agent for operator
GET  /api/keywords/:operator   → List keyword suggestions
POST /api/keywords/:id/approve → Operator approves keyword
POST /api/articles/generate    → Runs Brief + Writing + QA pipeline
GET  /api/articles/:operator   → List articles with status
POST /api/articles/:id/publish → Runs Publish Agent
GET  /api/analytics/:operator  → Traffic + lead data
```
