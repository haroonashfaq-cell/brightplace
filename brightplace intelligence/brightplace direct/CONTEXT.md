# brightplace direct — Context File

**Last Updated:** August 27, 2026
**Status:** Planning + Manual Testing Phase

---

## What Is brightplace direct?

An AI-powered content engine for apartment operators. We research keywords, write SEO-optimized articles, and publish them to operator websites. The goal: drive organic traffic, AI citations, and leads for operators.

## What It Is NOT

- Not a website builder (developer team handles templates/sites)
- Not a CMS (content goes into the developer team's codebase)
- Not a listing platform (we write editorial content, not listings)

---

## Current State

### What Exists
- **Operator site live:** operator-pages.vercel.app
- **2 operators:** AIR Communities (Denver), Towne Properties (Cincinnati)
- **3 properties on site:** Oak Trail, Lakeview at Gateway Park, Harpers Point
- **4 articles published:** Oak Trail guide, Lakeview guide, Harpers Point guide, All-In Pricing explainer
- **6 content agents:** Keyword, Brief, Writing, QA, Image, Publish
- **Full portfolio analysis complete:** ALL 170 AIR communities checked via Semrush
- **5 new communities selected for build** (see below)
- **Design system:** brightplace tokens (Urbanist, Lato, orange/navy/teal)
- **SEO infrastructure:** JSON-LD, sitemap, robots.txt, llms.txt, 23-point audit
- **Developer-Team folder:** 8 generic agents + 4 skills (reusable for any project)

### What's Next
- [ ] Build property pages for 5 selected AIR communities
- [ ] Write 1-2 articles per community (10 total)
- [ ] Research keywords per community (using Semrush)
- [ ] QA and publish all content
- [ ] Update sitemap, llms.txt, homepage

### What's Missing (Future)
- [ ] UI dashboard for operators
- [ ] Automated pipeline (Claude API + Semrush API)
- [ ] Analytics dashboard
- [ ] Multi-operator content management
- [ ] Plug-and-play CMS adapters

---

## AIR Communities — LOCKED CLIENT

**Status:** Approved. Starting with 5 communities.
**Full analysis:** `Planning/08-air-communities-full-analysis.md` (all 170 communities)

### Selected 5 Communities

| # | Property | City, State | Volume | KD | Why |
|---|---|---|---|---|---|
| 1 | **One Canal** | Boston, MA | 1,300 | 8 | Lowest KD, easiest #1 |
| 2 | **Indigo West** | Orlando, FL | 1,300 | 28 | Huge renter market |
| 3 | **One Boynton** | Boynton Beach, FL | 1,300 | 28 | S. Florida growth |
| 4 | **3400 Avenue of the Arts** | Costa Mesa, CA | 1,000 | 28 | SoCal luxury |
| 5 | **Citigate** | Jacksonville, FL | 720 | 22 | Best vol/KD ratio |

### Existing Communities (Already on Site)

| Property | City | Volume | KD | Articles |
|---|---|---|---|---|
| Oak Trail | Denver, CO | — | — | 3 articles |
| Lakeview at Gateway Park | Denver, CO | 70 | 0 | 1 article |

### Next 5 (When Ready to Expand)

| Property | City | Volume | KD |
|---|---|---|---|
| Chestnut Hall | Philadelphia, PA | 880 | 26 |
| Eterno | Pompano Beach, FL | 590 | 23 |
| Latrobe | Washington, DC | 590 | 25 |
| Pacifica Park | Pacifica, CA | 390 | 19 |
| Vista | Philadelphia, PA | 320 | 13 |

---

## Towne Properties — DEMO CLIENT

**Status:** Demo page live. Not yet locked as paying client.
**Properties:** Harpers Point (Cincinnati, OH) — 720 vol, KD 39
**Articles:** 1 published (resort guide)

---

## Team

| Person | Role | Scope |
|---|---|---|
| Haroon | Content strategy + product | brightplace direct pipeline, agents, planning |
| Tom | Developer | Site templates, deployment, infrastructure |
| Dennis | Developer | Site templates, deployment, infrastructure |
| Claude | AI assistant | Keyword research, writing, QA, publishing |

---

## Related Systems

| System | Location | Purpose |
|---|---|---|
| brightplace intelligence | `brightplace intelligence/Agents/` | Content engine for brightplace.ai |
| brightplace direct | `brightplace intelligence/brightplace direct/` | Content engine for operator sites |
| operator-pages | `operator-pages/` | Next.js codebase for operator websites |
| Developer-Team | `Desktop/Developer-Team/` | Generic reusable agents for any project |
| seo-product | `seo-product/` | Future UI dashboard |

---

## Decisions Made

1. Content engine only — dev team handles templates/sites
2. Next.js/Vercel — server-rendered for SEO + AI crawlability
3. Semrush for real keyword data — KD + volume verified
4. Agents as markdown — portable, readable, versionable
5. Manual testing first — prove pipeline before building UI
6. Plug-and-play vision — content engine works with any CMS (future)
7. **AIR Communities locked** — starting with 5 communities
8. **All 170 AIR communities analyzed** — full Semrush data stored
9. **Selection criteria:** Volume 700+, KD under 30, zero editorial competition

---

## Planning Documents

| File | What |
|---|---|
| `01-product-vision.md` | What, why, who, revenue model |
| `02-architecture.md` | System diagram, tech stack, DB schema, APIs |
| `03-pipeline-detail.md` | Step-by-step with timing + error handling |
| `04-keyword-report-air-communities.md` | AIR keyword opportunities (top picks) |
| `05-keyword-report-towne-properties.md` | Towne keyword opportunities |
| `06-build-roadmap.md` | 5-phase roadmap |
| `07-production-architecture.md` | Local → production migration plan |
| `08-air-communities-full-analysis.md` | **ALL 170 communities with Semrush data** |

---

## Pending Action Items

### For Dev Team (Tom & Dennis)
- [ ] Build 5 property pages from templates (One Canal, Indigo West, One Boynton, 3400 Ave Arts, Citigate)
- [ ] Create CMS API endpoint: `POST /api/content/publish` (accepts article JSON, creates page)
- [ ] Create property API endpoint: `POST /api/content/property` (accepts property JSON, creates page)
- [ ] API authentication (token-based)
- [ ] Requirements doc sent: `Planning/09-developer-requirements.md`

### For Content Team (Haroon + Claude)
- [ ] Research property data for 5 communities (floor plans, amenities, pricing, neighborhood)
- [ ] Research keywords per community (Semrush)
- [ ] Write 1-2 articles per community after pages are built
- [ ] Source property images from AIR Communities websites

---

## Open Questions

1. Pricing model for operators? (Per article? Monthly? Per lead?)
2. Which CMS API option will dev team choose? (A: JSON files, B: Supabase, C: Headless CMS)
3. Do we need real property photos before building pages? (Ask AIR)
4. Should each operator have its own repo or share one?
5. API authentication method? (API key? JWT? Supabase auth?)
