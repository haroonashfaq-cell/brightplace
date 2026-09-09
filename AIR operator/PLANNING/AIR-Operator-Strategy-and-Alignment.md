# AIR Operator: Complete Strategy, Alignment & Decision Log

**Created:** September 3, 2026
**Purpose:** Full record of every decision, plan, and alignment made during the AIR operator system design. This is the thinking behind the specs — why we chose what we chose, how the pieces connect, and where we're headed.

---

## What This Project Is

We're building a content + visibility system for AIR Communities' 5 apartment properties. Our AI agents create all content (blog articles, social posts, GBP updates, review replies, Q&As). The dev team builds the sites, CMS, dashboard, and integrations. Community managers approve content through a dashboard. The system is designed to scale to 100+ communities with zero human bottleneck on our side.

---

## The 5 Communities

| Community | Domain | Location |
|---|---|---|
| Foxchase | foxchase.brightplace.ai | Alexandria, VA |
| Citi Lakes | citi-lakes.brightplace.ai | Orlando, FL |
| Sorrel / LUX at Sorrel | sorrel.brightplace.ai | Jacksonville, FL |
| Verdant Peachtree Creek | verdant-peachtree-creek.brightplace.ai | Atlanta, GA |
| Villages at Raleigh Beach | villages-at-raleigh-beach.brightplace.ai | Raleigh, NC |

Staging sites are live at `[name].staging.brightplace.ai`. Themes not yet applied. Tour booking and agent not hooked up yet. Amplitude tracking is set up.

---

## Key Decisions Made

### 1. Static Rendering (SSG/ISR) — Not Client-Side

**Decision:** All content must be in raw HTML. No JavaScript required to see it.

**Why:** AI crawlers (GPTBot, ClaudeBot, PerplexityBot) don't execute JavaScript. If content is behind JS, it's invisible to every AI search engine. 90% of apartment sites block AI crawlers — we explicitly allow them via robots.txt. This is our competitive advantage.

**What this means for dev team:** Server Components by default. `'use client'` only for animations and interactive widgets. Blog pages use ISR with 60-second revalidation. Test: `curl [url]` must show all content.

### 2. MCP Server as the Connection Layer

**Decision:** Dev team builds an MCP (Model Context Protocol) server. We connect from Claude Code CLI.

**Why:** We already use Claude Code CLI with MCP for all our work. An MCP server gives us direct tool access — no curl commands, no middleware, no manual API calls. Our agents call MCP tools like `blog_create_post`, `events_list_pending`, `seo_validate_page` directly.

**What this means:** 73 MCP tools across 11 categories. This is the single interface between our content pipeline and the sites.

### 3. Events System for Two-Way Communication

**Decision:** Every dashboard action and scheduled trigger creates an event in an events table. We poll events from Claude Code to know what work is pending.

**Why:** We considered 3 options:
- Option 1 (polling from Claude Code) — works now, manual trigger
- Option 2 (webhook to queue, we poll) — middle ground
- Option 3 (serverless webhook handler, fully automated) — scales to 100 communities

**Current phase:** Option 1. We use Claude Code to poll `events_list_pending`, process each event with our agents, push results back. Manual trigger but automated processing.

**Future phase:** Option 3. Serverless webhook handler on Vercel receives events in real-time, calls Claude API, pushes results back automatically. Zero human on our side.

**The events table serves all phases.** Dev team builds it now for polling. Later, they add webhook firing on top of the same table — data model doesn't change.

### 4. Our Agents Are a Separate Product

**Decision:** The dev team never sees or accesses our content agents. They're our IP.

**Why:** Our SUPER SEO Agents (12-stage workflow, keyword research, writing, QA, etc.) are the engine that produces the content. The dev team only sees the output — finished articles, social posts, review replies pushed via MCP. The agent prompts, workflows, and intelligence stay on our side.

**What this means:** Clean separation. We push content. They render and publish it. They build the dashboard and integrations. We never share agent prompts or methodology.

### 5. UTM Attribution as the Primary Metric

**Decision:** Tour bookings attributed to content = the number that matters to operators.

**Why:** AIR doesn't care about SEO metrics or content volume. They care about: "How many people booked a tour because of your pages?" Every CTA carries UTM params. Every conversion traces back to the specific article, social post, or GBP update that drove it.

**Dashboard order reflects this:** Leads at top (biggest numbers), content attribution in middle (which content drives leads), visibility at bottom (traffic, AI citations — supporting metrics).

### 6. AI Citation Tracking

**Decision:** Detect and report when AI search engines (ChatGPT, Perplexity, Google AI Overviews) send visitors to our community sites.

**Why:** This is a new metric most apartment operators have never seen. Showing "ChatGPT sent 12 renters to your site this month" is a differentiator. It proves our rendering + AI crawler strategy works.

**How:** Check `document.referrer` for `chat.openai.com`, `perplexity.ai`, `bing.com/chat`, etc. Flag as `is_ai_referral` in lead attribution table.

---

## System Architecture

```
OUR SIDE                              DEV TEAM'S SIDE
(Content Pipeline)                    (Sites + CMS + Dashboard)

SUPER SEO Agents                      5 Community Sites (Next.js/Vercel)
  ↓ create content                      ↑ renders pages
Claude Code CLI                       CMS Database (10 tables)
  ↕ MCP connection                      ↑ stores content
Dev Team's MCP Server ──────────────→ Blog (ISR) + Social + GBP
  (73 tools)                          Dashboard (3 tabs: SEO, Social, GBP)
                                      Events Table (two-way comms)
                                      Amplitude (tracking)
                                      UTM Attribution (lead tracking)
```

---

## What We Built (Intelligence Layer)

### Research per community (in `AIR operator/` folder)
- `context.md` — property overview, key highlights, location
- `research.md` — extended research: floor plans, pricing, amenities, pet policies, nearby employers, unique selling points
- `keywords.csv` — keyword universe (original from Semrush + 136 research-generated keywords added)
- `serp-research.md` — SERP analysis per community

### Foxchase full pipeline (proof of concept)
- `foxchase-intelligence/fox-chase-apartments/01-keyword-research.md`
- `foxchase-intelligence/fox-chase-apartments/02-community-research.md`
- `foxchase-intelligence/fox-chase-apartments/03-content-brief.md`
- `foxchase-intelligence/fox-chase-apartments/04-brief-check.md`
- `foxchase-intelligence/fox-chase-apartments/05-fox-chase-apartments-draft.md`
- `foxchase-intelligence/fox-chase-apartments/06-qa-report.md`
- `foxchase-intelligence/fox-chase-apartments/08-image-prompts.md`
- `foxchase-intelligence/fox-chase-apartments/09-fox-chase-apartments-final-enriched.md`

### Spec documents
- `Complete-Build-Spec.md` — THE consolidated doc for dev team (rendering, MCP, database, endpoints, dashboard, tracking)
- `AIR-Operator-Complete-Technical-Spec.md` — earlier version (rendering + dev guide + CMS only)
- `developer-guide.md` — standalone dev guide
- `rendering-requirements.md` — standalone rendering requirements
- `Developer CMS Requirement Doc.md` — standalone CMS API spec
- `dashboard-and-social-planning.md` — Visibility Engine flow planning
- `build-map.md` — what we build vs what dev team builds
- `api-endpoints-for-tom.md` — REST endpoint listing (superseded by MCP tools in Complete-Build-Spec)

---

## The 3 Content Channels

### Channel 1: SEO/AEO (Blog)
Our agents create keyword-targeted blog articles. Each article goes through: keyword research → content brief → brief approval → writing → QA → image generation → publish. Articles are optimized for Google featured snippets, People Also Ask, and AI search engine citations.

### Channel 2: Social Media (Instagram + Facebook)
When a blog article publishes, our agents create 2-3 social posts: IG feed post, IG story, FB page post. Each links back to the article with UTM tracking. Community manager approves captions before posting.

### Channel 3: Google Business Profile
GBP update posts tied to new blog content. Review reply drafts when new Google reviews come in. Q&A suggestions seeded on the GBP listing from search/chat data analysis.

---

## Dashboard Vision

The Visibility Engine dashboard (HTML prototype created during planning) has 3 tabs:

**SEO/AEO Tab:** Stats row, content brief cards (approve/skip), article pipeline with status chips, monthly calendar view.

**Social Media Tab:** Week context note, post preview cards per platform (IG/FB), approve/edit/delete/schedule controls.

**Google Business Tab:** Profile health ring (rating, reviews, views, calls), GBP post drafts, review reply drafts, Q&A suggestions, photo refresh alerts.

**Community Profile:** Pre-filled from our research (positioning, differentiators, neighborhood anchors). Two fields only the community manager can fill: "What do prospects ask on tours?" and "What do residents love?"

---

## Scale Plan

| Phase | Communities | Our Side | System |
|---|---|---|---|
| Now | 5 | Claude Code manual | Polling events |
| 6 months | 20 | Claude Code + light automation | Polling + some scheduled jobs |
| 12 months | 50-100 | Serverless webhook handler | Full automation, zero human |

At 100 communities per month:
- 200 briefs auto-generated
- 200 articles written
- 600 social posts created
- 200 GBP posts
- ~400 review replies
- ~1,900 Claude API calls
- ~15 min/week per community manager (approve only)
- Zero time from our team

---

## Open Items

- [ ] Theming/UI alignment on staging sites
- [ ] Amplitude events review — ensure all conversion events from Part 10 are tracked before launch
- [ ] UTM tracking implementation before launch
- [ ] MCP server build (Phase 1: blog endpoints for Foxchase)
- [ ] Tour booking hookup
- [ ] AI agent hookup
- [ ] Listings sourcing discussion
- [ ] Social media agents — need to create prompt templates
- [ ] GBP agents — need to create prompt templates
- [ ] Review reply agent — need to create prompt template
- [ ] Dashboard build timeline

---

## Team

- **Content/SEO Pipeline:** Managed via Claude Code CLI with SUPER SEO Agents
- **Development:** Sites, CMS, MCP server, dashboard, integrations
- **Tracking:** Amplitude (already set up), UTM attribution (needs implementation)

---

*This document is the complete context of the AIR operator project. Every decision, every plan, every alignment — all in one place. Reference this before starting any new work on the project.*
