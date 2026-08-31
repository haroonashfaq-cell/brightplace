# Tech Stack

**Last Updated:** August 2026

---

## Architecture: Agent-Based Microservices

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND                          │
│            Next.js 14+ (App Router)                  │
│         React + Tailwind + shadcn/ui                 │
│              Deployed on Vercel                      │
└──────────────────────┬──────────────────────────────┘
                       │ API calls
┌──────────────────────▼──────────────────────────────┐
│                    BACKEND                           │
│              FastAPI (Python 3.12)                    │
│           Deployed on Railway / Render               │
│                                                      │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐       │
│  │ Auth       │ │ Projects   │ │ Billing    │       │
│  │ Service    │ │ Service    │ │ Service    │       │
│  └────────────┘ └────────────┘ └────────────┘       │
└──────────────────────┬──────────────────────────────┘
                       │ Task queue
┌──────────────────────▼──────────────────────────────┐
│               AGENT ORCHESTRATOR                     │
│          BullMQ (Redis) Job Queue                    │
│                                                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │ Audit    │ │ Research │ │ Brief    │            │
│  │ Agent    │ │ Agent    │ │ Agent    │            │
│  ├──────────┤ ├──────────┤ ├──────────┤            │
│  │ Reddit   │ │ Writing  │ │ QA      │            │
│  │ Agent    │ │ Agent    │ │ Agent   │            │
│  ├──────────┤ ├──────────┤ ├──────────┤            │
│  │ Image    │ │ Publish  │ │ Keyword │            │
│  │ Agent    │ │ Agent    │ │ Agent   │            │
│  └──────────┘ └──────────┘ └──────────┘            │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                  DATA LAYER                          │
│                                                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │PostgreSQL│ │  Redis   │ │ S3/R2   │            │
│  │(Supabase)│ │ (Cache + │ │(Files + │            │
│  │          │ │  Queue)  │ │ Images) │            │
│  └──────────┘ └──────────┘ └──────────┘            │
└─────────────────────────────────────────────────────┘
```

---

## Stack Choices

| Layer | Technology | Why |
|---|---|---|
| Frontend | Next.js 14+ (App Router) | SSR for SEO of own product, React ecosystem, Vercel deploy, streaming UI for real-time agent output |
| UI Components | shadcn/ui + Tailwind | Fast to build, professional, accessible, customizable |
| Backend API | FastAPI (Python 3.12) | Python required for AI/ML libraries, scraping tools, data processing. FastAPI is async, fast, typed |
| Agent Framework | Claude Agent SDK or LangGraph | Orchestrates multi-step agent workflows with tool use |
| LLM Provider | Anthropic Claude API (primary) + OpenAI (fallback) | Claude for writing quality. OpenAI for AI Mode analysis |
| Task Queue | BullMQ (Redis-backed) | Research + writing jobs take 30-120 seconds. Async processing with progress via WebSockets |
| Real-time Updates | WebSockets (Socket.io) | Live progress as agents work |
| Database | PostgreSQL via Supabase | Projects, articles, briefs, keyword data, user settings. Auth + DB + realtime + storage in one |
| Cache | Redis (Upstash) | Cache SERP results, keyword data, competitor analysis (24h expiry) |
| File Storage | Cloudflare R2 or S3 | Generated images, exported briefs, HTML files |
| Auth | Supabase Auth or Clerk | Google/email login, team management, role-based access |
| Payments | Stripe | Subscription billing, usage metering |
| Deployment | Vercel (frontend) + Railway (backend) + Upstash (Redis) | All serverless/managed, auto-scaling |
| Image Generation | OpenAI DALL-E 3 API or Ideogram API | Featured images from prompts |

---

## Key Technical Decisions

### Why Python backend, not Node?
All heavy lifting is Python: web scraping (BeautifulSoup, Playwright), AI APIs (anthropic SDK, openai SDK), data processing (pandas for keyword analysis), agent framework. Node frontend + Python backend is the standard for AI products.

### Why not a monolith?
Each agent is independent. Research Agent can run while Reddit Agent runs simultaneously. BullMQ lets you queue, parallelize, and retry individual agents without blocking the user.

### Why WebSockets?
When a user clicks "Research This Keyword," the process takes 60-90 seconds across 5 agents. They need live progress, not a spinner. WebSocket pushes: "SERP analysis complete... Reddit research found 8 threads... Brief generation starting..."

---

## Database Schema (Core Tables)

```sql
-- Users & Auth
users (id, email, name, plan, created_at)
teams (id, name, owner_id)
team_members (team_id, user_id, role)

-- Projects (one per website)
projects (id, team_id, domain, niche, brand_context,
          cms_type, cms_credentials_encrypted, created_at)

-- Keywords
keywords (id, project_id, keyword, volume, kd, intent,
          status, serp_data_json, ai_mode_data_json,
          researched_at)

-- Content Pipeline
briefs (id, project_id, keyword_id, title, structure_json,
        status, created_at, approved_at)

articles (id, brief_id, content_md, content_html,
          seo_score, qa_report_json, status,
          published_url, created_at)

-- Research Data
research_reports (id, keyword_id, serp_analysis_json,
                  ai_mode_json, reddit_json, paa_json,
                  created_at)

-- QA Rules
qa_rules (id, project_id, rule_type, rule_text,
          is_active, created_at)

-- Audit
site_audits (id, project_id, score, issues_json,
             ai_readiness_json, created_at)
```

---

## Cost Per Article (Estimated)

| Service | Cost |
|---|---|
| DataForSEO (keyword + SERP data) | $0.10-0.20 |
| Claude API (research + brief + writing + QA) | $0.30-0.80 |
| OpenAI API (AI Mode analysis + image) | $0.10-0.30 |
| Reddit scraping | $0.00 (RSS/JSON free) |
| **Total per article** | **$0.50-1.30** |
