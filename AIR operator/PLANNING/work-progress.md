# AIR Operator — Work Progress

**Last Updated:** September 9, 2026

---

## Completed Tasks

### September 1, 2026
- [x] Created AIR operator folder structure
- [x] Created 5 community folders (Foxchase, Citi Lakes, Verdant Peachtree Creek, Sorrel LUX at Sorrel, Villages at Raleigh Beach)
- [x] Created `context.md` for all 5 original communities
- [x] Researched all 5 communities (websites, property data, floor plans, amenities, pet policies, employers, attractions)
- [x] Created `research.md` for all 5 original communities
- [x] Moved keyword CSVs into respective community folders
- [x] Analyzed keyword gaps and added 136 research-generated keywords across all 5 CSVs
- [x] Renamed community folders with "Intelligence" suffix (except Foxchase)
- [x] Created intelligence subfolder structure matching Foxchase pattern

### September 2, 2026
- [x] Created `developer-guide.md` — how to build the sites (tech stack, architecture, components)
- [x] Created `rendering-requirements.md` — SSG, AI crawler rules, robots.txt, llms.txt, JSON-LD, semantic HTML, performance targets
- [x] Created `Developer CMS Requirement Doc.md` — blog CMS API spec (7 endpoints, SQL schema, page rendering rules)
- [x] Created `AIR-Operator-Complete-Technical-Spec.md` — first consolidated doc (rendering + dev guide + CMS)
- [x] Created `dashboard-and-social-planning.md` — Visibility Engine flow (SEO, Social, GBP channels)
- [x] Created `build-map.md` — what we build vs what dev team builds (our 20 files vs their 31 endpoints)
- [x] Created `api-endpoints-for-tom.md` — all REST endpoints for CLI-to-site communication

### September 3, 2026
- [x] Updated `Complete-Build-Spec.md` v2.0 — rewritten with subdomain structure, MCP server, full site control, 73 MCP tools
- [x] Added UTM tracking & lead attribution section to spec (lead_attribution table, Amplitude events, AI referral detection)
- [x] Updated testing checklist with 11 tracking/attribution items
- [x] Created update message for dev team with doc summary
- [x] Created `AIR-Operator-Strategy-and-Alignment.md` — complete decision log and project context

### September 7, 2026
- [x] Reviewed `AIR-Operator-MCP-Reference.md` (v1.0 consolidated by team member — 16 tables, ~85 MCP tools, corrected crawler info)
- [x] Created 5 new agent files in `AIR operator/Agents/`:
  - `article-update-agent.md` — surgical article revisions
  - `social-post-agent.md` — IG feed + IG story + FB page post creation with UTM
  - `gbp-post-agent.md` — Google Business Profile update posts
  - `review-reply-agent.md` — review reply drafts (rating-aware, never templated)
  - `qna-agent.md` — GBP Q&A generation from keyword/chat/review data
- [x] Copied SUPER SEO Agent files into `AIR operator/Agents/Writing Agents/` (12 files)
- [x] Created `Writing Agents/` subfolder for content pipeline agents
- [x] Updated memory files with new agent locations and MCP Reference as source of truth

### September 8-9, 2026
- [x] Created 5 new community folders: One Canal, Indigo West, One Boynton, 3400 Avenue of the Arts, Citigate
- [x] Created `context.md` for all 5 new communities (property data from web research)
- [x] Created `research.md` for all 5 new communities (extended research: floor plans, pricing, pet policies, employers, neighborhoods, unique selling points)
- [x] Created `community-keyword-research-agent.md` — reusable 8-phase keyword research process for onboarding new communities
- [x] Ran Semrush keyword research for all 5 new communities (branded, city-level, competitor, pet-friendly, questions)
- [x] Built scored keyword CSVs for all 5 new communities with full format (Opportunity Score, Difficulty, Intent, Category, Tier, Content Tier, Relevance)
  - One Canal: 85 keywords
  - Indigo West: 50 keywords
  - One Boynton: 58 keywords
  - 3400 Avenue of the Arts: 63 keywords
  - Citigate: 70 keywords
- [x] Committed and pushed all work to GitHub (47 files, 9,357 lines)

---

### September 9, 2026 (continued)
- [x] Wrote first article for ALL 10 communities (10 articles total, full pipeline: brief + draft + image prompts)
  1. 3400 AotA: "580 Anton Costa Mesa" (KD 13, Vol 880) — competitor comparison
  2. One Boynton: "Sealofts at Boynton Village" (KD 13, Vol 1,000) — competitor comparison
  3. Sorrel: "Peppertree Lane Jacksonville" (KD 12, Vol 720) — competitor comparison
  4. Indigo West: "Apartments Near Valencia College Orlando" (KD 12) — location guide
  5. Foxchase: "Cameron Court Apartments Alexandria" (KD 13, Vol 1,600) — competitor comparison
  6. Verdant: "Trestle Tree Atlanta" (KD 13, Vol 720) — competitor comparison
  7. Citigate: "Apartments by Town Center Jacksonville" (KD 15, Vol 880) — location guide
  8. Villages: "Inexpensive Apartments Raleigh NC" (KD 20, Vol 1,000) — value guide
  9. One Canal: "2 Bedroom Apartments Boston" (KD 15, Vol 1,000) — city guide
  10. Citi Lakes: "2 Bedroom Apartments Orlando" (KD 23, Vol 1,000) — city guide

---

## In Progress

- [ ] Deep keyword research for new 5 communities (target: 200+ per community — currently at 50-85)
- [ ] Competitor organic research via Semrush

---

## Not Started (Upcoming)

### Content Production
- [ ] First blog article for Foxchase (proof of concept using full agent pipeline)
- [ ] First blog articles for original 5 communities
- [ ] First blog articles for new 5 communities
- [ ] Social post creation for published articles (social-post-agent)
- [ ] GBP post creation for published articles (gbp-post-agent)

### Agent Development
- [ ] Social post agent — test with real article and refine prompt
- [ ] GBP post agent — test with real article and refine prompt
- [ ] Review reply agent — test with real Google reviews
- [ ] Q&A agent — test with real community data
- [ ] Article update agent — test with revision request

### Dev Team (Waiting On)
- [ ] Staging sites theming/UI alignment
- [ ] MCP server build (Phase 1: blog endpoints for Foxchase)
- [ ] Events system + events API
- [ ] UTM tracking + lead attribution implementation (before launch)
- [ ] Tour booking hookup
- [ ] AI agent hookup
- [ ] Dashboard build (SEO tab first)
- [ ] Social publishing integration
- [ ] GBP integration
- [ ] Amplitude events verification (all conversion events from spec)

### Future Phases
- [ ] Serverless webhook handler (Phase 3 automation — when scaling beyond 10 communities)
- [ ] Portfolio rollup dashboard (cross-community metrics)
- [ ] Portfolio insight agent (cross-community narrative analysis)
- [ ] Attention item agent (flagging issues across communities)

---

## Community Status Summary

| Community | Context | Research | Keywords | Keywords Count | Blog Content | Social | GBP |
|---|---|---|---|---|---|---|---|
| Foxchase | Done | Done | Done | 364 | 2 articles | Not started | Not started |
| Citi Lakes | Done | Done | Done | 348 | 1 article | Not started | Not started |
| Sorrel LUX at Sorrel | Done | Done | Done | 658 | 1 article | Not started | Not started |
| Verdant Peachtree Creek | Done | Done | Done | 410 | 1 article | Not started | Not started |
| Villages at Raleigh Beach | Done | Done | Done | 313 | 1 article | Not started | Not started |
| One Canal | Done | Done | Done | 85 | 1 article | Not started | Not started |
| Indigo West | Done | Done | Done | 50 | 1 article | Not started | Not started |
| One Boynton | Done | Done | Done | 58 | 1 article | Not started | Not started |
| 3400 Avenue of the Arts | Done | Done | Done | 63 | 1 article | Not started | Not started |
| Citigate | Done | Done | Done | 70 | 1 article | Not started | Not started |

---

## Key Documents

| Document | Location | Status |
|---|---|---|
| MCP Reference (source of truth) | `AIR-Operator-MCP-Reference.md` | v1.0 complete |
| Complete Build Spec | `PLANNING/Complete-Build-Spec.md` | v2.0 complete |
| Strategy & Alignment | `PLANNING/AIR-Operator-Strategy-and-Alignment.md` | v1.0 complete |
| Dashboard Planning | `PLANNING/dashboard-and-social-planning.md` | v1.0 complete |
| Build Map | `PLANNING/build-map.md` | v1.0 complete |
| Community Keyword Research Agent | `Agents/community-keyword-research-agent.md` | v1.0 ready to use |
