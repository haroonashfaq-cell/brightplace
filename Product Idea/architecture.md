# SUPER SEO SaaS — MVP Architecture Document

**Version:** 1.0
**Date:** September 2026
**Status:** Planning
**Codename:** SuperSEO

---

## 1. Product Vision

A SaaS dashboard that gives any business AI-powered SEO — keyword research, content production, technical audits, and ongoing optimization — powered by the SUPER SEO agent team. Users onboard their website, see keyword opportunities, click to generate articles, review and approve content, and push to their CMS. Everything traceable, everything auditable.

**One-liner:** "Plug in your website. Get SEO done by AI agents you can watch work."

---

## 2. User Roles

| Role | Description | Permissions |
|---|---|---|
| **Owner** | Platform admin (you) | Full access, manage all clients, billing, system config |
| **Client** | Business owner or marketing manager | Manage their own projects, approve content, view reports |
| **Operator** | Internal team member who runs agents on behalf of clients | Run pipelines, review outputs, push to CMS |

**MVP:** Owner + Client roles only. Operator role added when you hire.

---

## 3. Tech Stack

### Frontend
| Component | Technology | Rationale |
|---|---|---|
| Framework | **Next.js 15 (App Router)** | Full-stack React, SSR, API routes, Vercel-native |
| Styling | **Tailwind CSS + shadcn/ui** | Fast to build, professional look, fully customizable |
| State | **TanStack Query** | Server state management, caching, real-time refetch |
| Forms | **React Hook Form + Zod** | Type-safe validation at the boundary |
| Charts | **Recharts** | Keyword volume charts, audit scores, pipeline progress |
| Real-time | **Supabase Realtime** | Pipeline progress streaming to the UI |
| Auth | **Supabase Auth** | Email/password + OAuth (Google), row-level security |

### Backend
| Component | Technology | Rationale |
|---|---|---|
| API | **Next.js Route Handlers** | Co-located with frontend, edge-ready |
| AI Engine | **Claude API (Anthropic SDK)** | Powers all SEO agents — research, writing, QA |
| Image Gen | **OpenAI API (GPT Image 2)** | Featured image generation |
| SEO Data | **Semrush API** | Keyword metrics, competitor data, backlink research |
| Job Queue | **Inngest** | Durable step functions for long-running pipelines |
| CMS Push | **Webflow API / WordPress REST API** | Content publishing to client sites |

### Infrastructure
| Component | Technology | Rationale |
|---|---|---|
| Hosting | **Vercel** | Zero-config deploys, edge functions, free tier |
| Database | **Supabase (PostgreSQL)** | Free tier, auth, storage, realtime, row-level security |
| File Storage | **Supabase Storage** | Articles, images, research files |
| DNS/CDN | **Vercel Edge Network** | Global CDN, automatic HTTPS |
| Monitoring | **Vercel Analytics + Sentry** | Performance + error tracking |

### External APIs
| API | Purpose | Cost Model |
|---|---|---|
| Claude API | Agent brain (research, writing, QA, briefs) | Per-token (~$15/1M input, $75/1M output for Opus) |
| OpenAI API | Image generation (GPT Image 2) | ~$0.04-0.08 per image |
| Semrush API | Keyword data, competitor analysis, backlinks | Subscription or per-query |
| Webflow API | CMS publishing | Included with Webflow plan |
| WordPress REST API | CMS publishing | Free (self-hosted) |

---

## 4. Database Schema (Supabase / PostgreSQL)

### Core Tables

```sql
-- ============================================================
-- USERS & AUTH (Supabase Auth handles most of this)
-- ============================================================

create table public.profiles (
  id uuid references auth.users primary key,
  email text not null,
  full_name text,
  role text not null default 'client', -- 'owner', 'client', 'operator'
  avatar_url text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- ============================================================
-- PROJECTS (one per client website)
-- ============================================================

create table public.projects (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid references public.profiles(id) not null,
  name text not null,                          -- "Foxchase Apartments"
  url text not null,                           -- "https://foxchaseofalexandriaapts.com"
  industry text,                               -- "real estate", "plumbing", "dental"
  description text,                            -- business description
  target_audience text,                        -- who the content is for
  geographic_focus text,                       -- "Alexandria, VA"
  brand_voice text,                            -- voice/tone guidelines
  brand_rules jsonb default '{}',              -- banned words, style rules, etc.
  sitemap_urls jsonb default '[]',             -- cached sitemap pages
  competitors jsonb default '[]',              -- [{name, url}]
  cms_type text,                               -- 'webflow', 'wordpress', 'custom'
  cms_config jsonb default '{}',               -- API keys, collection IDs, etc.
  status text default 'active',                -- 'active', 'paused', 'archived'
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- ============================================================
-- LINK TARGETS (internal + external links per project)
-- ============================================================

create table public.link_targets (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references public.projects(id) on delete cascade,
  url text not null,
  anchor_text text,                            -- suggested anchor text
  link_type text not null,                     -- 'internal', 'external_authority', 'cta'
  page_title text,                             -- title of the target page
  verified boolean default false,              -- sitemap-verified
  last_verified_at timestamptz,
  created_at timestamptz default now()
);

-- ============================================================
-- KEYWORDS (imported from CSV or discovered by agents)
-- ============================================================

create table public.keywords (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references public.projects(id) on delete cascade,
  keyword text not null,
  volume integer,
  kd integer,                                  -- keyword difficulty 0-100
  cpc numeric(10,2),
  intent text,                                 -- 'informational', 'commercial', 'transactional', 'navigational'
  category text,                               -- 'branded', 'competitor', 'city+apartments', etc.
  opportunity_score numeric(10,2),
  difficulty text,                             -- 'easy', 'medium', 'hard'
  relevant boolean default true,
  relevance_note text,
  tier text,                                   -- 'T1', 'T2', 'T3'
  status text default 'discovered',            -- 'discovered', 'briefed', 'writing', 'published', 'rejected'
  data_source text,                            -- 'semrush', 'manual', 'agent'
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create index idx_keywords_project on public.keywords(project_id);
create index idx_keywords_status on public.keywords(status);
create index idx_keywords_volume on public.keywords(volume desc);

-- ============================================================
-- ARTICLES (the content pipeline)
-- ============================================================

create table public.articles (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references public.projects(id) on delete cascade,
  keyword_id uuid references public.keywords(id),

  -- metadata
  title text,                                  -- H1 title
  seo_title text,                              -- SEO title (different from H1)
  meta_description text,
  slug text,
  primary_keyword text,
  secondary_keywords jsonb default '[]',
  word_count integer,

  -- pipeline status
  status text default 'queued',
  -- 'queued' -> 'researching' -> 'briefed' -> 'writing' -> 'qa' -> 'review' -> 'approved' -> 'published'

  -- pipeline stage outputs (stored as markdown text)
  keyword_research text,                       -- 01-keyword-research.md content
  community_research text,                     -- 02-community-research.md content
  content_brief text,                          -- 03-content-brief.md content
  brief_check text,                            -- 04-brief-check.md content
  draft_content text,                          -- 05-draft.md content
  qa_report text,                              -- 06-qa-report.md content
  schema_markup text,                          -- 07-schema.md content (JSON-LD)
  image_prompts text,                          -- 08-image-prompts.md content
  final_content text,                          -- 09-final-enriched.md content

  -- image
  featured_image_url text,                     -- Supabase Storage URL for .webp
  featured_image_alt text,
  featured_image_metadata jsonb default '{}',

  -- QA results
  qa_score integer,                            -- e.g., 58/60
  qa_passed boolean default false,
  qa_issues jsonb default '[]',                -- [{check, status, detail}]

  -- publishing
  cms_item_id text,                            -- Webflow/WordPress item ID after push
  cms_url text,                                -- live URL after publishing
  published_at timestamptz,

  -- timestamps
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  researched_at timestamptz,
  briefed_at timestamptz,
  drafted_at timestamptz,
  qa_at timestamptz,
  approved_at timestamptz
);

create index idx_articles_project on public.articles(project_id);
create index idx_articles_status on public.articles(status);

-- ============================================================
-- PIPELINE RUNS (job tracking for long-running agent tasks)
-- ============================================================

create table public.pipeline_runs (
  id uuid primary key default gen_random_uuid(),
  article_id uuid references public.articles(id) on delete cascade,
  stage text not null,                         -- 'keyword_research', 'community_research', 'brief', 'brief_check', 'writing', 'qa', 'image', 'final_assembly'
  status text default 'pending',               -- 'pending', 'running', 'completed', 'failed'
  started_at timestamptz,
  completed_at timestamptz,
  duration_ms integer,
  tokens_used integer,                         -- Claude API tokens consumed
  cost_estimate numeric(10,4),                 -- estimated cost in USD
  error_message text,                          -- if failed
  output_preview text,                         -- first 500 chars of output
  created_at timestamptz default now()
);

create index idx_pipeline_article on public.pipeline_runs(article_id);

-- ============================================================
-- AUDITS (technical SEO, on-page, local, content audits)
-- ============================================================

create table public.audits (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references public.projects(id) on delete cascade,
  audit_type text not null,                    -- 'technical', 'on_page', 'backlink', 'local', 'content_portfolio'
  target_url text,                             -- URL audited (or 'full_site')
  status text default 'pending',               -- 'pending', 'running', 'completed', 'failed'
  score integer,                               -- health score 0-100
  report_content text,                         -- full markdown report
  findings jsonb default '[]',                 -- structured findings [{severity, issue, fix}]
  critical_count integer default 0,
  high_count integer default 0,
  medium_count integer default 0,
  low_count integer default 0,
  tokens_used integer,
  created_at timestamptz default now(),
  completed_at timestamptz
);

create index idx_audits_project on public.audits(project_id);

-- ============================================================
-- API USAGE TRACKING (cost management)
-- ============================================================

create table public.api_usage (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references public.projects(id),
  service text not null,                       -- 'claude', 'openai_image', 'semrush', 'webflow'
  operation text,                              -- 'keyword_research', 'write_article', 'generate_image', etc.
  tokens_input integer,
  tokens_output integer,
  cost_usd numeric(10,4),
  article_id uuid references public.articles(id),
  audit_id uuid references public.audits(id),
  created_at timestamptz default now()
);

create index idx_usage_project on public.api_usage(project_id);
create index idx_usage_date on public.api_usage(created_at);

-- ============================================================
-- ROW LEVEL SECURITY (clients see only their own data)
-- ============================================================

alter table public.projects enable row level security;
alter table public.keywords enable row level security;
alter table public.articles enable row level security;
alter table public.audits enable row level security;
alter table public.link_targets enable row level security;

-- Clients can only see their own projects
create policy "Users see own projects" on public.projects
  for select using (owner_id = auth.uid());

-- Clients can only see keywords for their projects
create policy "Users see own keywords" on public.keywords
  for select using (project_id in (
    select id from public.projects where owner_id = auth.uid()
  ));

-- Same pattern for articles, audits, link_targets
create policy "Users see own articles" on public.articles
  for select using (project_id in (
    select id from public.projects where owner_id = auth.uid()
  ));

create policy "Users see own audits" on public.audits
  for select using (project_id in (
    select id from public.projects where owner_id = auth.uid()
  ));

-- Owner role sees everything
create policy "Owner sees all projects" on public.projects
  for all using (
    exists (select 1 from public.profiles where id = auth.uid() and role = 'owner')
  );
```

---

## 5. API Routes

### Project Management
```
POST   /api/projects                    Create new project (onboard a client)
GET    /api/projects                    List all projects for current user
GET    /api/projects/:id                Get project details
PUT    /api/projects/:id                Update project (description, brand rules, CMS config)
DELETE /api/projects/:id                Archive project
POST   /api/projects/:id/fetch-sitemap  Crawl and cache the client's sitemap
POST   /api/projects/:id/import-keywords Upload keyword CSV
```

### Keywords
```
GET    /api/projects/:id/keywords                List keywords (filterable by volume, KD, status, tier)
PUT    /api/projects/:id/keywords/:kid           Update keyword status (approve, reject, prioritize)
POST   /api/projects/:id/keywords/discover       Run keyword discovery agent for seed terms
GET    /api/projects/:id/keywords/stats           Keyword summary (total, by tier, by status)
```

### Content Pipeline
```
POST   /api/projects/:id/articles                 Start article pipeline for a keyword
GET    /api/projects/:id/articles                  List all articles (filterable by status)
GET    /api/projects/:id/articles/:aid             Get article with all pipeline outputs
GET    /api/projects/:id/articles/:aid/stage/:num  Get specific stage output (01-09)
POST   /api/projects/:id/articles/:aid/approve     Approve article for publishing
POST   /api/projects/:id/articles/:aid/reject      Reject with feedback (re-enters pipeline)
POST   /api/projects/:id/articles/:aid/publish     Push approved article to CMS
GET    /api/projects/:id/articles/:aid/progress     SSE stream of pipeline progress
```

### Pipeline Execution (internal, called by Inngest jobs)
```
POST   /api/pipeline/research           Run keyword + community research
POST   /api/pipeline/brief              Generate content brief
POST   /api/pipeline/brief-check        Validate the brief
POST   /api/pipeline/write              Write the article
POST   /api/pipeline/qa                 Run QA checks
POST   /api/pipeline/image              Generate image prompts + create image
POST   /api/pipeline/assemble           Final assembly with QA fixes
```

### Audits
```
POST   /api/projects/:id/audits                   Start an audit (type: technical, on_page, local, backlink, content)
GET    /api/projects/:id/audits                    List all audits
GET    /api/projects/:id/audits/:aid               Get audit report
```

### Usage & Billing
```
GET    /api/projects/:id/usage                     API usage stats (tokens, cost, by service)
GET    /api/usage/summary                           Total usage across all projects (owner only)
```

---

## 6. Page Structure (Next.js App Router)

```
app/
├── (auth)/
│   ├── login/page.tsx                    Login
│   └── signup/page.tsx                   Signup
│
├── (dashboard)/
│   ├── layout.tsx                        Dashboard shell (sidebar + header)
│   │
│   ├── projects/
│   │   ├── page.tsx                      Project list (cards with status)
│   │   ├── new/page.tsx                  Onboard new client
│   │   └── [id]/
│   │       ├── page.tsx                  Project overview (stats, recent activity)
│   │       ├── keywords/
│   │       │   └── page.tsx              Keyword table (sort, filter, bulk actions)
│   │       ├── articles/
│   │       │   ├── page.tsx              Article pipeline board (kanban or table view)
│   │       │   └── [articleId]/
│   │       │       ├── page.tsx          Article detail (all stages, preview, approve/reject)
│   │       │       └── preview/page.tsx  Full article preview (rendered markdown)
│   │       ├── audits/
│   │       │   ├── page.tsx              Audit history + run new audit
│   │       │   └── [auditId]/page.tsx    Audit report detail
│   │       ├── links/page.tsx            Link targets manager
│   │       └── settings/page.tsx         Project settings (CMS, brand rules, competitors)
│   │
│   ├── usage/page.tsx                    API usage dashboard (owner only)
│   └── settings/page.tsx                 Account settings
│
├── api/                                  All API routes (see section 5)
├── layout.tsx                            Root layout
└── page.tsx                              Landing page / marketing site
```

---

## 7. Pipeline Architecture (Inngest)

Each article triggers a durable workflow with retries and observability.

```
┌─────────────────────────────────────────────────────────────┐
│                    ARTICLE PIPELINE                          │
│                                                              │
│  Trigger: POST /api/projects/:id/articles {keyword_id}       │
│                                                              │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐    │
│  │ Step 1:      │   │ Step 2:      │   │ Step 3:      │    │
│  │ Keyword      │──▶│ Community    │──▶│ Content      │    │
│  │ Research     │   │ Research     │   │ Brief        │    │
│  │              │   │              │   │              │    │
│  │ Claude API   │   │ Claude API   │   │ Claude API   │    │
│  │ + Web Search │   │ + Web Search │   │ + Sitemap    │    │
│  │              │   │              │   │              │    │
│  │ → 01.md      │   │ → 02.md      │   │ → 03.md      │    │
│  └──────────────┘   └──────────────┘   └──────────────┘    │
│         │                                     │              │
│         │              ┌──────────────┐       │              │
│         │              │ Step 4:      │       │              │
│         └─────────────▶│ Brief Check  │◀──────┘              │
│                        │              │                      │
│                        │ Claude API   │                      │
│                        │ → 04.md      │                      │
│                        └──────┬───────┘                      │
│                               │                              │
│                     ┌─────────▼─────────┐                    │
│                     │ Step 5:           │                    │
│                     │ SEO Writing       │                    │
│                     │                   │                    │
│                     │ Claude API        │                    │
│                     │ (longest step)    │                    │
│                     │ → 05-draft.md     │                    │
│                     └─────────┬─────────┘                    │
│                               │                              │
│              ┌────────────────┼────────────────┐             │
│              ▼                ▼                 ▼             │
│     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │
│     │ Step 6:      │ │ Step 7:      │ │ Step 8:      │     │
│     │ QA           │ │ Image        │ │ (reserved)   │     │
│     │              │ │ Prompts +    │ │              │     │
│     │ Claude API   │ │ Generation   │ │              │     │
│     │ → 06.md      │ │              │ │              │     │
│     │              │ │ Claude API + │ │              │     │
│     │              │ │ OpenAI API   │ │              │     │
│     │              │ │ → 08.md      │ │              │     │
│     │              │ │ → .webp      │ │              │     │
│     └──────┬───────┘ └──────┬───────┘ └──────────────┘     │
│            │                │                                │
│            └────────┬───────┘                                │
│                     ▼                                        │
│            ┌──────────────┐                                  │
│            │ Step 9:      │                                  │
│            │ Final        │                                  │
│            │ Assembly     │                                  │
│            │              │                                  │
│            │ Apply QA     │                                  │
│            │ fixes        │                                  │
│            │ → 09-final.md│                                  │
│            └──────┬───────┘                                  │
│                   │                                          │
│                   ▼                                          │
│            Status: "review"                                  │
│            (waiting for human approval)                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Inngest Function Definition (pseudocode)

```typescript
inngest.createFunction(
  { id: "article-pipeline", name: "Article Pipeline" },
  { event: "article/pipeline.start" },
  async ({ event, step }) => {
    const { articleId, projectId, keyword } = event.data;

    // Step 1: Keyword Research
    const keywordResearch = await step.run("keyword-research", async () => {
      return await callClaude({
        systemPrompt: loadAgent("keyword-research-agent.md"),
        userPrompt: `Research keyword "${keyword}" for project...`,
      });
    });
    await saveStageOutput(articleId, "keyword_research", keywordResearch);

    // Step 2: Community Research
    const communityResearch = await step.run("community-research", async () => {
      return await callClaude({
        systemPrompt: loadAgent("community-research-agent.md"),
        userPrompt: `Research communities for "${keyword}"...`,
      });
    });
    await saveStageOutput(articleId, "community_research", communityResearch);

    // Step 3: Content Brief
    const brief = await step.run("content-brief", async () => {
      return await callClaude({
        systemPrompt: loadAgent("content-brief-agent.md"),
        userPrompt: `Create brief using: ${keywordResearch} + ${communityResearch}`,
      });
    });
    await saveStageOutput(articleId, "content_brief", brief);

    // Step 4: Brief Check
    const briefCheck = await step.run("brief-check", async () => {
      return await callClaude({
        systemPrompt: loadAgent("brief-check-agent.md"),
        userPrompt: `Check this brief: ${brief}`,
      });
    });
    await saveStageOutput(articleId, "brief_check", briefCheck);

    // Step 5: Writing (longest step)
    const draft = await step.run("writing", async () => {
      return await callClaude({
        systemPrompt: loadAgent("seo-writing-agent.md"),
        userPrompt: `Write article from brief: ${brief}
                     Community research: ${communityResearch}
                     Link targets: ${linkTargets}`,
        maxTokens: 8000,
      });
    });
    await saveStageOutput(articleId, "draft_content", draft);

    // Step 6 + 7: QA and Image (parallel)
    const [qaReport, imageResult] = await Promise.all([
      step.run("qa", async () => {
        return await callClaude({
          systemPrompt: loadAgent("qa-agent.md"),
          userPrompt: `QA this article: ${draft}`,
        });
      }),
      step.run("image", async () => {
        const prompts = await callClaude({
          systemPrompt: loadAgent("image-prompt-agent.md"),
          userPrompt: `Generate image prompts for: ${draft}`,
        });
        const image = await generateImage(prompts.recommendedPrompt);
        return { prompts, image };
      }),
    ]);
    await saveStageOutput(articleId, "qa_report", qaReport);
    await saveStageOutput(articleId, "image_prompts", imageResult.prompts);

    // Step 9: Final Assembly
    const finalArticle = await step.run("final-assembly", async () => {
      return applyQAFixes(draft, qaReport);
    });
    await saveStageOutput(articleId, "final_content", finalArticle);

    // Update status to "review"
    await updateArticleStatus(articleId, "review");
    await sendNotification(projectId, `Article "${keyword}" ready for review`);
  }
);
```

---

## 8. Key UI Components

### 8a. Project Dashboard
```
┌─────────────────────────────────────────────────────────┐
│  Foxchase Apartments                    [Settings] [Audit] │
│  foxchaseofalexandriaapts.com           Active              │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Keywords │  │ Articles │  │ Audits   │  │ API Cost │ │
│  │   247    │  │    3     │  │    1     │  │  $12.40  │ │
│  │ tracked  │  │ pipeline │  │ complete │  │ this mo  │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│                                                           │
│  Recent Activity                                          │
│  ● Article "fox chase apartments" → QA Passed → Review    │
│  ● Keyword discovery found 32 new opportunities           │
│  ● Technical audit completed: Score 74/100                │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### 8b. Keyword Table
```
┌─────────────────────────────────────────────────────────┐
│  Keywords                    [Import CSV] [Discover New] │
│  Filter: [Volume ▼] [KD ▼] [Status ▼] [Tier ▼]         │
├──────────────────────┬──────┬────┬────────┬─────────────┤
│  Keyword             │ Vol  │ KD │ Status │ Action      │
├──────────────────────┼──────┼────┼────────┼─────────────┤
│  foxchase            │4,400 │ 45 │Published│ View        │
│  fox chase apartments│2,900 │ 32 │Published│ View        │
│  apartments alexandria│3,600│ 44 │Queued  │ [Write] [x] │
│  townhomes alexandria│ 720 │ 15 │Discovered│[Write] [x] │
│  sinclaire seminary  │1,000 │ 24 │Discovered│[Write] [x] │
└──────────────────────┴──────┴────┴────────┴─────────────┘
│  Showing 5 of 247     [< 1 2 3 ... 25 >]                │
└─────────────────────────────────────────────────────────┘
```

### 8c. Article Pipeline View
```
┌─────────────────────────────────────────────────────────┐
│  Article: What Renters Should Know About Foxchase...     │
│  Keyword: fox chase apartments │ Status: Review          │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Pipeline Progress                                        │
│  ✅ Research    ✅ Brief    ✅ Writing    ✅ QA    ✅ Image │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Tabs: [Preview] [Research] [Brief] [QA Report]      │ │
│  │       [Image] [Schema] [Raw Markdown]               │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │                                                      │ │
│  │  # What Renters Should Know About Foxchase...       │ │
│  │                                                      │ │
│  │  Foxchase Apartments covers 88 wooded acres in      │ │
│  │  Seminary Hill, Alexandria, making it the largest... │ │
│  │                                                      │ │
│  │  [rendered markdown preview continues...]            │ │
│  │                                                      │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  QA Score: 58/60 ✅        Word Count: 4,142              │
│  Internal Links: 9         External Links: 6              │
│  FAQs: 12                  Image: Generated ✅            │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  ✅ Approve   │  │  ✏️ Request   │  │  ❌ Reject    │   │
│  │  & Publish   │  │  Changes     │  │              │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### 8d. Audit Report View
```
┌─────────────────────────────────────────────────────────┐
│  Technical SEO Audit: foxchaseofalexandriaapts.com       │
│  Score: 74/100                  Date: Sep 1, 2026        │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │Critical │ │  High   │ │ Medium  │ │  Low    │       │
│  │   2     │ │   5     │ │   8     │ │   12   │       │
│  │  🔴     │ │  🟠     │ │  🟡     │ │  🟢    │       │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘       │
│                                                           │
│  Critical Issues                                          │
│  ● No XML sitemap found                    [How to fix]  │
│  ● 3 pages return 404                      [How to fix]  │
│                                                           │
│  High Priority                                            │
│  ● LCP 4.2s (target: under 2.5s)          [How to fix]  │
│  ● Missing canonical tags on 12 pages     [How to fix]  │
│  ...                                                      │
└─────────────────────────────────────────────────────────┘
```

---

## 9. Agent Integration Layer

The agents run as Claude API calls. Each agent file (.md) becomes a system prompt.

```typescript
// lib/agents.ts

import Anthropic from "@anthropic-ai/sdk";
import { readFileSync } from "fs";
import path from "path";

const client = new Anthropic();

const AGENTS_DIR = path.join(process.cwd(), "agents");

export async function runAgent(
  agentName: string,
  userPrompt: string,
  options?: {
    maxTokens?: number;
    temperature?: number;
    tools?: Anthropic.Tool[];
  }
) {
  const systemPrompt = readFileSync(
    path.join(AGENTS_DIR, `${agentName}.md`),
    "utf-8"
  );

  const response = await client.messages.create({
    model: "claude-sonnet-4-6",  // Use Sonnet for speed, Opus for quality
    max_tokens: options?.maxTokens ?? 4096,
    temperature: options?.temperature ?? 0.3,
    system: systemPrompt,
    messages: [{ role: "user", content: userPrompt }],
  });

  return response.content[0].type === "text"
    ? response.content[0].text
    : "";
}

// Agent-specific wrappers
export const agents = {
  keywordResearch: (prompt: string) =>
    runAgent("keyword-research-agent", prompt, { maxTokens: 8000 }),

  communityResearch: (prompt: string) =>
    runAgent("community-research-agent", prompt, { maxTokens: 6000 }),

  contentBrief: (prompt: string) =>
    runAgent("content-brief-agent", prompt, { maxTokens: 8000 }),

  briefCheck: (prompt: string) =>
    runAgent("brief-check-agent", prompt, { maxTokens: 4000 }),

  seoWriter: (prompt: string) =>
    runAgent("seo-writing-agent", prompt, { maxTokens: 12000 }),

  qaAgent: (prompt: string) =>
    runAgent("qa-agent", prompt, { maxTokens: 8000 }),

  imagePrompts: (prompt: string) =>
    runAgent("image-prompt-agent", prompt, { maxTokens: 4000 }),

  technicalAudit: (prompt: string) =>
    runAgent("technical-seo-agent", prompt, { maxTokens: 8000 }),

  onPageAudit: (prompt: string) =>
    runAgent("on-page-seo-agent", prompt, { maxTokens: 6000 }),
};
```

---

## 10. Cost Estimation Per Article

| Stage | Model | Est. Tokens | Est. Cost |
|---|---|---|---|
| Keyword Research | Sonnet | ~8K in / ~4K out | $0.14 |
| Community Research | Sonnet | ~6K in / ~3K out | $0.10 |
| Content Brief | Sonnet | ~10K in / ~4K out | $0.16 |
| Brief Check | Sonnet | ~8K in / ~2K out | $0.10 |
| SEO Writing | **Opus** | ~15K in / ~8K out | $1.35 |
| QA | Sonnet | ~12K in / ~4K out | $0.18 |
| Image Prompts | Sonnet | ~4K in / ~2K out | $0.07 |
| Image Generation | GPT Image 2 | — | $0.08 |
| **Total per article** | | | **~$2.18** |

At $2.18 per article, a $99/mo plan covers ~45 articles. A $499/mo plan covers ~228 articles. Healthy margin.

---

## 11. MVP Build Plan (6 weeks)

### Week 1: Foundation
- [ ] Init Next.js 15 + Tailwind + shadcn/ui
- [ ] Set up Supabase (database, auth, storage)
- [ ] Create database schema (run SQL from section 4)
- [ ] Build auth flow (login, signup, protected routes)
- [ ] Build dashboard layout (sidebar, header, navigation)

### Week 2: Projects & Keywords
- [ ] Project CRUD (create, list, detail, settings)
- [ ] Onboarding flow (enter URL → auto-fetch sitemap → discover competitors)
- [ ] Keyword CSV import
- [ ] Keyword table with sort/filter
- [ ] Keyword discovery agent integration

### Week 3: Content Pipeline
- [ ] Article creation from keyword
- [ ] Inngest pipeline setup (all 9 steps)
- [ ] Claude API integration (agent system prompts)
- [ ] Pipeline progress streaming (SSE or Supabase Realtime)
- [ ] Stage output storage and retrieval

### Week 4: Article Review
- [ ] Article detail page (tabbed view: preview, research, brief, QA, image)
- [ ] Markdown preview renderer
- [ ] QA report display
- [ ] Approve / Request Changes / Reject flow
- [ ] Image generation integration (OpenAI API)

### Week 5: Publishing & Audits
- [ ] CMS integration (Webflow API — create/update draft items)
- [ ] One-click publish flow
- [ ] Technical SEO audit page
- [ ] On-page audit page
- [ ] Audit report display

### Week 6: Polish & Launch
- [ ] API usage tracking dashboard
- [ ] Error handling and retry logic
- [ ] Loading states and progress indicators
- [ ] Mobile responsive cleanup
- [ ] Landing page
- [ ] Deploy to Vercel production
- [ ] Onboard first pilot client

---

## 12. Future Roadmap (Post-MVP)

### Phase 2 additions (months 2-3)
- [ ] WordPress CMS integration
- [ ] Contentful CMS integration
- [ ] Bulk article generation (queue 10+ keywords at once)
- [ ] Content calendar view
- [ ] Team/multi-user with role-based access
- [ ] Stripe billing integration
- [ ] White-label mode (agencies resell to their clients)

### Phase 3 additions (months 4-6)
- [ ] Autonomous mode (cron-triggered keyword discovery, monthly audits)
- [ ] Slack/email notifications for approvals
- [ ] Competitor monitoring (track competitor content changes)
- [ ] Rank tracking integration
- [ ] AI Overview citation monitoring
- [ ] Content refresh automation (flag stale articles, auto-update)
- [ ] API for external integrations

### Phase 4 (6+ months)
- [ ] Multi-language content generation
- [ ] Video script generation
- [ ] Social media content from articles
- [ ] Client-facing analytics dashboard
- [ ] Enterprise SSO (SAML)

---

## 13. Security Considerations

- **API keys** stored in environment variables, never in client-side code
- **Row-level security** in Supabase ensures clients only see their own data
- **CMS credentials** encrypted at rest in the database
- **Rate limiting** on all API routes (Vercel Edge middleware)
- **Input sanitization** with Zod on all user inputs
- **CORS** restricted to the app domain
- **No client-side Claude calls** — all AI runs server-side
- **Audit log** for all publish actions (who approved, when)

---

## 14. File Structure

```
superseo/
├── app/
│   ├── (auth)/login/page.tsx
│   ├── (auth)/signup/page.tsx
│   ├── (dashboard)/layout.tsx
│   ├── (dashboard)/projects/page.tsx
│   ├── (dashboard)/projects/new/page.tsx
│   ├── (dashboard)/projects/[id]/page.tsx
│   ├── (dashboard)/projects/[id]/keywords/page.tsx
│   ├── (dashboard)/projects/[id]/articles/page.tsx
│   ├── (dashboard)/projects/[id]/articles/[articleId]/page.tsx
│   ├── (dashboard)/projects/[id]/audits/page.tsx
│   ├── (dashboard)/projects/[id]/audits/[auditId]/page.tsx
│   ├── (dashboard)/projects/[id]/links/page.tsx
│   ├── (dashboard)/projects/[id]/settings/page.tsx
│   ├── (dashboard)/usage/page.tsx
│   ├── api/projects/route.ts
│   ├── api/projects/[id]/route.ts
│   ├── api/projects/[id]/keywords/route.ts
│   ├── api/projects/[id]/articles/route.ts
│   ├── api/projects/[id]/audits/route.ts
│   ├── api/pipeline/[stage]/route.ts
│   ├── layout.tsx
│   └── page.tsx
├── agents/                            -- SUPER SEO agent .md files (system prompts)
│   ├── keyword-research-agent.md
│   ├── community-research-agent.md
│   ├── content-brief-agent.md
│   ├── brief-check-agent.md
│   ├── seo-writing-agent.md
│   ├── qa-agent.md
│   ├── schema-agent.md
│   ├── image-prompt-agent.md
│   ├── technical-seo-agent.md
│   ├── on-page-seo-agent.md
│   ├── backlink-agent.md
│   ├── local-seo-agent.md
│   └── content-audit-agent.md
├── lib/
│   ├── agents.ts                      -- Claude API wrapper for agents
│   ├── supabase/
│   │   ├── client.ts                  -- Browser client
│   │   ├── server.ts                  -- Server client
│   │   └── admin.ts                   -- Service role client
│   ├── openai.ts                      -- Image generation
│   ├── semrush.ts                     -- Semrush API wrapper
│   ├── cms/
│   │   ├── webflow.ts                 -- Webflow API
│   │   └── wordpress.ts               -- WordPress REST API
│   ├── pipeline.ts                    -- Pipeline orchestration helpers
│   └── utils.ts                       -- Shared utilities
├── components/
│   ├── ui/                            -- shadcn/ui components
│   ├── keyword-table.tsx
│   ├── article-pipeline.tsx
│   ├── article-preview.tsx
│   ├── audit-report.tsx
│   ├── pipeline-progress.tsx
│   └── markdown-renderer.tsx
├── inngest/
│   ├── client.ts                      -- Inngest client
│   └── functions/
│       ├── article-pipeline.ts        -- Full article pipeline function
│       ├── keyword-discovery.ts       -- Keyword discovery function
│       └── site-audit.ts             -- Audit function
├── supabase/
│   └── migrations/
│       └── 001_initial_schema.sql     -- Database schema from section 4
├── public/
├── .env.local                         -- API keys (never committed)
├── next.config.ts
├── tailwind.config.ts
├── package.json
└── README.md
```

---

*This document is the source of truth for the SuperSEO SaaS MVP. Update it as decisions are made.*
