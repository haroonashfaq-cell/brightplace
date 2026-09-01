# SuperSEO — Ultimate Vision: Fully Autonomous SEO Platform

**Version:** 1.0
**Date:** September 2026
**Status:** Long-term vision (post-MVP)
**Prerequisite:** Hybrid MVP (architecture.md) must be live and validated first

---

## The Endgame

A platform where a business connects their website once and never thinks about SEO again. AI agents handle everything — discovering opportunities, producing content, optimizing pages, building links, monitoring rankings, refreshing stale content, and adapting to algorithm changes. The business owner opens a dashboard, sees traffic growing, approves content with one tap, and watches revenue increase.

**One-liner:** "Connect your site. SEO runs itself."

---

## How It Differs from the Hybrid MVP

| Dimension | Hybrid MVP (architecture.md) | Ultimate Version |
|---|---|---|
| Who triggers work | Human clicks "Write Article" | System triggers automatically on schedule |
| Content production | One article at a time, manually initiated | Batch production — 10-50 articles/week queued automatically |
| Keyword discovery | Manual CSV import or on-demand agent | Continuous — weekly scans find new opportunities |
| Content freshness | Manual audits | Autonomous — agents detect stale content and auto-draft updates |
| Ranking monitoring | None (external tools) | Built-in — daily rank tracking with alert triggers |
| Algorithm response | Manual — you read about updates and adapt | Automatic — agents detect ranking drops and diagnose cause |
| Link building | Analysis only | Semi-autonomous — finds opportunities, drafts outreach, tracks responses |
| Client involvement | Reviews and approves each article | Sets preferences once, approves batches, gets weekly summary |
| Multi-site | One project at a time | Portfolio management — agencies run 50-500 sites |
| Revenue model | $99-499/mo subscription | $499-2,999/mo + usage-based + enterprise contracts |

---

## Architecture: The Autonomous Loop

The ultimate version runs on three continuous loops, each on different timescales:

```
┌─────────────────────────────────────────────────────────────┐
│                    THE THREE LOOPS                           │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ LOOP 1: DISCOVERY (runs weekly)                      │    │
│  │                                                       │    │
│  │  Keyword Scanner Agent                                │    │
│  │  → Scans Semrush for new opportunities                │    │
│  │  → Monitors competitor new content                    │    │
│  │  → Checks PAA changes for tracked keywords            │    │
│  │  → Detects trending topics in the industry            │    │
│  │  → Scores and queues new keyword opportunities        │    │
│  │                                                       │    │
│  │  Output: "12 new keyword opportunities found this     │    │
│  │  week. 3 are P1 (auto-queued). 9 need review."       │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ LOOP 2: PRODUCTION (runs daily)                      │    │
│  │                                                       │    │
│  │  Content Pipeline Orchestrator                        │    │
│  │  → Picks next keyword from priority queue             │    │
│  │  → Runs full pipeline (research → write → QA → image) │    │
│  │  → Queues completed articles for review               │    │
│  │  → Auto-publishes if client enabled auto-approve      │    │
│  │  → Refreshes stale articles (update data, add FAQs)   │    │
│  │                                                       │    │
│  │  Output: "2 new articles drafted. 1 article refreshed.│    │
│  │  3 articles awaiting your approval."                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ LOOP 3: OPTIMIZATION (runs daily + triggered)        │    │
│  │                                                       │    │
│  │  SEO Monitor Agent                                    │    │
│  │  → Tracks rankings daily for all target keywords      │    │
│  │  → Detects ranking drops (triggers diagnosis agent)   │    │
│  │  → Monitors AI Overview citations                     │    │
│  │  → Checks competitor movements                        │    │
│  │  → Runs technical audits monthly                      │    │
│  │  → Monitors backlink profile changes                  │    │
│  │  → Detects Google algorithm updates (auto-adapts)     │    │
│  │                                                       │    │
│  │  Output: "Ranking for 'fox chase apartments' dropped  │    │
│  │  from #3 to #7. Diagnosis: competitor published longer │    │
│  │  article with fresher data. Fix: content refresh      │    │
│  │  queued automatically."                               │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## New Agents (Beyond MVP)

### Autonomous Agents (run on schedule, no human trigger)

| Agent | Schedule | What It Does |
|---|---|---|
| **Keyword Scanner** | Weekly | Scans Semrush + SERPs for new keyword opportunities, scores them, auto-queues P1 keywords |
| **Competitor Monitor** | Weekly | Tracks competitor new content, ranking changes, backlink gains. Alerts on threats. |
| **Rank Tracker** | Daily | Checks ranking position for all target keywords. Triggers alerts on drops > 3 positions. |
| **Freshness Monitor** | Weekly | Scans all published articles for stale data (prices, stats older than 2 quarters). Queues refresh tasks. |
| **AI Citation Monitor** | Weekly | Checks if published articles are cited in AI Overviews, ChatGPT, Perplexity. Tracks citation share. |
| **Algorithm Detector** | Daily | Monitors SEO news feeds and Google Search Status Dashboard. Detects updates. Triggers portfolio-wide audit if major update detected. |
| **Content Refresher** | Triggered | Takes a stale article, web searches for current data, rewrites outdated sections, runs QA, queues for approval. |
| **Ranking Diagnosis** | Triggered | When rank drops > 3 positions: analyzes what changed (competitor content, algorithm update, technical issue, link loss), recommends fix. |

### Link Building Agents (semi-autonomous)

| Agent | What It Does |
|---|---|
| **Link Prospector** | Finds link opportunities: broken links on competitor pages, resource pages in the niche, unlinked brand mentions. Scores by feasibility. |
| **Outreach Drafter** | Writes personalized outreach emails for each link prospect. Saves drafts for human review before sending. |
| **Link Tracker** | Monitors sent outreach: tracks responses, follows up automatically after 7 days, logs acquired links. |
| **Digital PR Agent** | Identifies newsworthy angles from the client's data/content. Drafts press releases and journalist pitches. |

### Content Intelligence Agents

| Agent | What It Does |
|---|---|
| **Topic Cluster Architect** | Analyzes all published content + keyword data. Maps pillar-cluster relationships. Identifies gaps in topical authority. Recommends the next 10 articles to strengthen clusters. |
| **Cannibalization Detector** | Continuously monitors for keyword cannibalization across the site. Recommends merge, differentiate, or redirect. |
| **Content ROI Analyzer** | Connects GA4/GSC data to each article. Calculates: traffic, conversions, revenue attributed to each piece. Ranks content by ROI. Recommends where to invest more. |
| **SERP Feature Optimizer** | Monitors featured snippets, PAA boxes, AI Overviews for target keywords. Detects when format changes. Auto-adjusts content structure to recapture features. |

---

## New Infrastructure

### 1. Job Scheduler (Cron Engine)

```
┌─────────────────────────────────────────┐
│           CRON SCHEDULE                  │
├──────────────────┬──────────────────────┤
│ Every 6 hours    │ Rank tracker          │
│ Every day 2 AM   │ Algorithm detector    │
│ Every Monday     │ Keyword scanner       │
│ Every Monday     │ Competitor monitor    │
│ Every Monday     │ AI citation monitor   │
│ Every Wednesday  │ Freshness monitor     │
│ Every 1st of mo  │ Technical audit       │
│ Every 1st of mo  │ Content ROI report    │
│ On rank drop     │ Ranking diagnosis     │
│ On stale detect  │ Content refresher     │
│ On queue ready   │ Content pipeline      │
└──────────────────┴──────────────────────┘
```

**Implementation:** Vercel Cron Jobs + Inngest for durable execution. Each cron triggers an Inngest function that runs the relevant agent.

### 2. Event Bus (Reactive Triggers)

Beyond scheduled jobs, agents react to events:

```
EVENT: ranking_dropped
  → IF drop > 5 positions → trigger ranking_diagnosis (urgent)
  → IF drop > 3 positions → trigger ranking_diagnosis (normal)
  → IF keyword is P1 → notify client via Slack/email immediately

EVENT: competitor_published
  → IF topic overlaps our content → trigger content_refresh
  → IF topic is a gap we haven't covered → queue keyword for production

EVENT: algorithm_update_detected
  → trigger portfolio_wide_audit
  → trigger ranking_check for all P1 keywords
  → notify client: "Google update detected. Running diagnostics."

EVENT: article_published
  → add to rank_tracker (start tracking in 48 hours)
  → schedule freshness_check (in 90 days)
  → add to ai_citation_monitor

EVENT: stale_content_detected
  → IF auto_refresh enabled → trigger content_refresher
  → ELSE → notify client: "3 articles need data updates"

EVENT: link_opportunity_found
  → score feasibility
  → IF score > 7 → draft outreach email → queue for review
  → ELSE → log for monthly link report
```

### 3. Notification System

```
┌─────────────────────────────────────────────────┐
│              NOTIFICATION CHANNELS               │
├─────────────────┬───────────────────────────────┤
│ In-App          │ Bell icon with badge count     │
│                 │ Activity feed on dashboard      │
├─────────────────┼───────────────────────────────┤
│ Email           │ Weekly digest (every Monday)   │
│                 │ Urgent alerts (rank drops)     │
│                 │ Articles ready for review      │
├─────────────────┼───────────────────────────────┤
│ Slack           │ Real-time channel integration  │
│                 │ #seo-alerts for urgent items   │
│                 │ #seo-digest for weekly summary │
│                 │ Approval buttons in Slack      │
├─────────────────┼───────────────────────────────┤
│ SMS (optional)  │ Only for critical: site down,  │
│                 │ massive rank drops, security   │
└─────────────────┴───────────────────────────────┘
```

### 4. Analytics Engine

New database tables for the ultimate version:

```sql
-- ============================================================
-- RANK TRACKING
-- ============================================================

create table public.rank_snapshots (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references public.projects(id) on delete cascade,
  keyword_id uuid references public.keywords(id),
  keyword text not null,
  position integer,                            -- 1-100, null if not ranking
  previous_position integer,
  change integer,                              -- positive = improved, negative = dropped
  url text,                                    -- which URL ranks
  serp_features jsonb default '[]',            -- ['featured_snippet', 'ai_overview', 'paa', 'local_pack']
  ai_overview_cited boolean default false,
  checked_at timestamptz default now()
);

create index idx_rank_project_date on public.rank_snapshots(project_id, checked_at);

-- ============================================================
-- COMPETITOR TRACKING
-- ============================================================

create table public.competitor_snapshots (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references public.projects(id) on delete cascade,
  competitor_url text not null,
  new_pages jsonb default '[]',                -- [{url, title, keyword, date}]
  ranking_changes jsonb default '[]',          -- [{keyword, old_position, new_position}]
  new_backlinks integer default 0,
  checked_at timestamptz default now()
);

-- ============================================================
-- CONTENT HEALTH
-- ============================================================

create table public.content_health (
  id uuid primary key default gen_random_uuid(),
  article_id uuid references public.articles(id) on delete cascade,
  freshness_score integer,                     -- 0-100
  stale_claims jsonb default '[]',             -- [{claim, date_stamped, current_reality}]
  broken_links jsonb default '[]',             -- [{url, status_code}]
  ranking_position integer,
  ai_cited boolean default false,
  last_refreshed_at timestamptz,
  next_refresh_due timestamptz,
  checked_at timestamptz default now()
);

-- ============================================================
-- LINK BUILDING
-- ============================================================

create table public.link_prospects (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references public.projects(id) on delete cascade,
  target_url text not null,                    -- page we want a link from
  target_domain text not null,
  domain_authority integer,
  prospect_type text,                          -- 'broken_link', 'resource_page', 'unlinked_mention', 'guest_post', 'digital_pr'
  contact_email text,
  feasibility_score integer,                   -- 1-10
  outreach_status text default 'identified',   -- 'identified', 'drafted', 'sent', 'replied', 'acquired', 'rejected'
  outreach_draft text,                         -- email draft
  outreach_sent_at timestamptz,
  follow_up_at timestamptz,
  link_acquired boolean default false,
  link_url text,                               -- our URL that got the link
  created_at timestamptz default now()
);

-- ============================================================
-- REVENUE ATTRIBUTION
-- ============================================================

create table public.content_revenue (
  id uuid primary key default gen_random_uuid(),
  article_id uuid references public.articles(id) on delete cascade,
  period text not null,                        -- '2026-09', '2026-10', etc.
  organic_sessions integer,
  organic_clicks integer,
  impressions integer,
  avg_position numeric(5,1),
  conversions integer,
  revenue numeric(12,2),
  cost_to_produce numeric(10,2),               -- API costs for this article
  roi numeric(10,2),                           -- (revenue - cost) / cost
  source text default 'gsc',                   -- 'gsc', 'ga4', 'manual'
  created_at timestamptz default now()
);
```

---

## New Dashboard Pages (Beyond MVP)

### SEO Command Center (Home)
```
┌─────────────────────────────────────────────────────────┐
│  SEO Command Center                   [All Projects ▼]   │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌──────────┐ │
│  │ Organic   │ │ Keywords  │ │ Articles  │ │ AI       │ │
│  │ Traffic   │ │ Ranking   │ │ Published │ │ Citations│ │
│  │ ▲ 23%    │ │ 147 / 300 │ │ 34 live   │ │ 12 cited │ │
│  │ vs last  │ │ in top 10 │ │ 8 draft   │ │ ▲ 4 new  │ │
│  │ month    │ │           │ │           │ │          │ │
│  └───────────┘ └───────────┘ └───────────┘ └──────────┘ │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Traffic Trend (12 months)                            │ │
│  │  ▁▂▃▃▄▅▅▆▆▇▇█                                      │ │
│  │  Oct Nov Dec Jan Feb Mar Apr May Jun Jul Aug Sep     │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  Alerts This Week                                         │
│  🔴 "fox chase apartments" dropped #3 → #7 (diagnosis    │
│     running)                                              │
│  🟡 5 articles have data older than 2 quarters            │
│  🟢 3 new articles auto-drafted and ready for review      │
│  🟢 Competitor "The Fields" published new pricing page    │
│                                                           │
│  Agent Activity (last 7 days)                             │
│  ● Keyword Scanner: 18 new opportunities found            │
│  ● Content Pipeline: 3 articles drafted                   │
│  ● Rank Tracker: 247 keywords checked                     │
│  ● Freshness Monitor: 2 articles flagged for refresh      │
│  ● Link Prospector: 7 new prospects identified            │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Rank Tracker Dashboard
```
┌─────────────────────────────────────────────────────────┐
│  Rank Tracker                              Period: 30d   │
├──────────────────┬──────┬──────┬────────┬───────────────┤
│  Keyword         │ Now  │ Was  │ Change │ SERP Features │
├──────────────────┼──────┼──────┼────────┼───────────────┤
│  foxchase        │  #2  │  #4  │  ▲ +2  │ AI Overview ✅│
│  fox chase apts  │  #7  │  #3  │  ▼ -4  │ 🔴 Diagnose  │
│  apartments alex │  #14 │  #18 │  ▲ +4  │ PAA ✅        │
│  townhomes alex  │  #5  │  #5  │  ━ 0   │ Local Pack    │
│  seminary hill   │  #3  │  —   │  NEW   │ AI Overview ✅│
└──────────────────┴──────┴──────┴────────┴───────────────┘
│                                                           │
│  Position Distribution                                    │
│  #1-3: ██████░░░░ 12 keywords                            │
│  #4-10: ████████░░ 35 keywords                           │
│  #11-20: ██████░░░░ 48 keywords                          │
│  #21-50: ████░░░░░░ 52 keywords                          │
│  Not ranking: ░░░░░░░░░░ 100 keywords                    │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Content Health Dashboard
```
┌─────────────────────────────────────────────────────────┐
│  Content Health                    [Run Full Audit]       │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Portfolio: 34 published articles                         │
│  🟢 Healthy (24)  🟡 Needs refresh (7)  🔴 Stale (3)   │
│                                                           │
│  Articles Needing Attention                               │
│                                                           │
│  🔴 "foxchase apartments pricing" — rent data 3Q old     │
│     [Auto-Refresh] [Manual Edit] [Dismiss]               │
│                                                           │
│  🔴 "seminary hill neighborhood" — 2 broken links        │
│     [Fix Links] [View Report]                            │
│                                                           │
│  🟡 "townhomes alexandria va" — competitor added new     │
│     comparison data we don't have                        │
│     [Enrich Content] [View Competitor]                   │
│                                                           │
│  Top Performing Content (by ROI)                          │
│  1. "fox chase apartments" — 2,400 clicks/mo — ROI: 47x │
│  2. "foxchase reviews" — 890 clicks/mo — ROI: 31x       │
│  3. "seminary hill guide" — 540 clicks/mo — ROI: 22x    │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Link Building Dashboard
```
┌─────────────────────────────────────────────────────────┐
│  Link Building                                            │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Pipeline                                                 │
│  Identified: 47  │  Drafted: 12  │  Sent: 8  │  Won: 3  │
│                                                           │
│  Recent Wins                                              │
│  ✅ alexandriava.gov/housing → linked to our renter guide │
│  ✅ seminayhillblog.com → mentioned in neighborhood post  │
│  ✅ inova.org/community → listed as nearby housing        │
│                                                           │
│  Ready for Outreach (drafts need approval)                │
│  📧 washingtonpost.com/real-estate — broken link opp      │
│     [Preview Email] [Approve & Send] [Edit]              │
│  📧 dcurbanmom.com/forum — resource page opportunity      │
│     [Preview Email] [Approve & Send] [Edit]              │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Weekly Digest (Email / Slack)
```
┌─────────────────────────────────────────────────────────┐
│  📊 SuperSEO Weekly Digest — Foxchase Apartments         │
│  Week of Sep 1-7, 2026                                    │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  TRAFFIC: 4,280 organic sessions (▲ 12% vs last week)    │
│                                                           │
│  RANKINGS:                                                │
│  ▲ 3 keywords improved    ▼ 1 keyword dropped            │
│  Best mover: "seminary hill apartments" #18 → #9         │
│  Alert: "fox chase apartments" #3 → #7 (fix in progress) │
│                                                           │
│  CONTENT:                                                 │
│  ✅ 2 new articles published                              │
│  📝 3 articles drafted (awaiting your approval)           │
│  🔄 1 article refreshed with Q3 2026 data                │
│                                                           │
│  LINKS:                                                   │
│  🔗 1 new backlink acquired (alexandriava.gov)            │
│  📧 4 outreach emails sent, 1 response received          │
│                                                           │
│  AI CITATIONS:                                            │
│  🤖 Cited in 3 AI Overviews this week (▲ 1 new)         │
│                                                           │
│  NEXT WEEK'S PLAN:                                        │
│  → Auto-queued: "apartments near inova hospital"          │
│  → Refresh due: "foxchase pricing guide" (data stale)    │
│  → Audit scheduled: Monthly technical audit               │
│                                                           │
│  [Open Dashboard →]                                       │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## Pricing Tiers (Ultimate Version)

| Plan | Price | Included | Target |
|---|---|---|---|
| **Starter** | $99/mo | 1 project, 10 articles/mo, weekly keyword scan, rank tracking (50 keywords), email digest | Solo business owner |
| **Growth** | $499/mo | 3 projects, 50 articles/mo, daily rank tracking (300 keywords), link prospecting, competitor monitoring, Slack integration, content refresh | Growing business or small agency |
| **Agency** | $1,499/mo | 15 projects, 200 articles/mo, white-label dashboard, client-facing reports, team seats (5), priority support, custom brand rules per project | Marketing agency |
| **Enterprise** | $2,999/mo | Unlimited projects, unlimited articles, dedicated infrastructure, SSO/SAML, SLA, API access, custom integrations, dedicated account manager | Large agency or in-house team |

### Usage-Based Add-Ons
| Add-On | Price |
|---|---|
| Extra articles beyond plan limit | $3/article |
| Extra rank tracking keywords | $0.02/keyword/day |
| Extra projects beyond plan limit | $49/project/mo |
| Premium image generation (GPT Image 2 HD) | $0.15/image |
| Backlink monitoring | $29/domain/mo |
| GA4 + GSC integration | Included in Growth+ |

### Estimated Unit Economics
| Metric | Value |
|---|---|
| Cost per article (API) | ~$2.18 |
| Cost per rank check (API) | ~$0.003 |
| Cost per keyword scan (API) | ~$0.05 |
| Gross margin on Starter plan | ~78% |
| Gross margin on Growth plan | ~85% |
| Gross margin on Agency plan | ~90% |
| Break-even | ~20 paying customers on Growth plan |

---

## Client Autonomy Levels

Clients choose how much control they want:

### Level 1: Full Control (default)
- Every article requires manual approval
- Every outreach email requires manual approval
- Weekly digest is informational only
- Client makes all decisions

### Level 2: Guided Autonomy
- P1 keywords auto-enter the pipeline (no approval to start research)
- Articles still require approval before publishing
- Content refreshes auto-draft but require approval
- Link outreach drafts auto-send after 48 hours if not rejected

### Level 3: Full Autonomy
- P1 keywords auto-produce articles and auto-publish after QA passes
- Content refreshes auto-publish
- Link outreach auto-sends
- Client gets weekly digest with what happened
- Emergency brake: any ranking drop > 10 positions pauses auto-publish and alerts client

---

## Technical Architecture Additions

### 1. Multi-Tenant Isolation

```
┌─────────────────────────────────────────┐
│            LOAD BALANCER                 │
├─────────┬─────────┬─────────┬──────────┤
│ Tenant A│ Tenant B│ Tenant C│ Tenant D │
│ (Solo)  │ (Growth)│ (Agency)│(Enterp.) │
├─────────┼─────────┼─────────┼──────────┤
│ Shared  │ Shared  │ Shared  │ Dedicated│
│ infra   │ infra   │ infra   │ infra    │
├─────────┼─────────┼─────────┼──────────┤
│ Shared  │ Shared  │ Shared  │ Dedicated│
│ DB pool │ DB pool │ DB pool │ DB       │
├─────────┼─────────┼─────────┼──────────┤
│ Rate:   │ Rate:   │ Rate:   │ Rate:    │
│ 5 req/m │ 20 req/m│ 50 req/m│ Unlimited│
└─────────┴─────────┴─────────┴──────────┘
```

### 2. Agent Model Routing

Not every task needs the most expensive model:

| Task | Model | Why |
|---|---|---|
| Keyword research | Sonnet | Fast, structured output |
| Community research | Sonnet | Speed over depth |
| Content brief | Sonnet | Structured planning |
| Brief check | Haiku | Simple pass/fail validation |
| **Article writing** | **Opus** | Quality matters most here |
| QA | Sonnet | Pattern matching, structured checks |
| Image prompts | Haiku | Short creative output |
| Rank diagnosis | Sonnet | Analytical reasoning |
| Content refresh | Sonnet | Targeted edits, not full rewrite |
| Outreach drafts | Sonnet | Persuasive but templated |

**Cost optimization:** Using Opus only for writing and Sonnet/Haiku for everything else drops the per-article cost from ~$2.18 to ~$1.50.

### 3. Caching & Efficiency

| What | Cache Duration | Why |
|---|---|---|
| Sitemap data | 24 hours | Sites don't change hourly |
| Keyword metrics | 7 days | Semrush data refreshes weekly |
| SERP results | 24 hours | SERPs shift daily |
| Competitor data | 7 days | Competitor content changes weekly |
| Rank positions | 6 hours | Checked 4x daily |
| AI Overview status | 24 hours | Changes slowly |

### 4. Webhook System (for integrations)

```
POST https://api.superseo.ai/webhooks

Events:
  article.drafted       → payload: {articleId, title, keyword, wordCount}
  article.approved      → payload: {articleId, approvedBy, publishTarget}
  article.published     → payload: {articleId, liveUrl, cmsItemId}
  ranking.dropped       → payload: {keyword, oldPosition, newPosition, url}
  ranking.improved      → payload: {keyword, oldPosition, newPosition}
  audit.completed       → payload: {auditId, score, criticalIssues}
  link.acquired         → payload: {prospectId, linkUrl, targetDomain}
  content.stale         → payload: {articleId, staleClaims[]}
  algorithm.detected    → payload: {updateName, severity, affectedKeywords}
```

Clients can connect these to Zapier, Make, n8n, or their own systems.

---

## Migration Path: MVP → Ultimate

| Quarter | Milestone | Revenue Target |
|---|---|---|
| **Q4 2026** | MVP live, 5 pilot clients on hybrid model | $2,500/mo |
| **Q1 2027** | Add rank tracking, content health monitoring | $10,000/mo (20 clients) |
| **Q2 2027** | Add autonomous loops (keyword scanner, freshness monitor) | $25,000/mo (40 clients) |
| **Q3 2027** | Add link building pipeline, competitor monitoring | $50,000/mo (60 clients) |
| **Q4 2027** | Add white-label agency mode, Stripe billing, enterprise features | $100,000/mo (100+ clients) |
| **2028** | Full autonomy mode, API marketplace, international support | $250,000+/mo |

---

## Competitive Moat

Why this is hard to copy:

1. **Agent quality compounds.** Every article produced teaches the agents. Writing guidelines get refined, QA catches get sharper, image prompts get more accurate. A new competitor starts from zero.

2. **Data flywheel.** More clients → more ranking data → better keyword recommendations → better articles → more clients. The platform gets smarter with scale.

3. **Vertical expertise.** Starting with property management (AIR operator) gives deep vertical knowledge. Expand to other verticals with the same depth. Each vertical's learnings improve the whole platform.

4. **Integration depth.** CMS integrations, rank tracking, link monitoring, GA4/GSC connections — each integration adds switching cost. Clients who are wired in don't leave.

5. **Trust through transparency.** Every article shows its full research trail (01-09 files). Clients can see exactly how the AI made every decision. This builds trust that "magic black box" competitors can't match.

---

*This document is the north star. Build the MVP first (architecture.md). Validate with paying clients. Then build toward this vision one quarter at a time.*
