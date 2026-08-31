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
- **3 properties:** Oak Trail, Lakeview at Gateway Park, Harpers Point
- **4 articles published:** Oak Trail guide, Lakeview guide, Harpers Point guide, All-In Pricing explainer
- **6 content agents:** Keyword, Brief, Writing, QA, Image, Publish
- **Keyword research done:** 10 keywords identified with Semrush KD/volume data
- **Design system:** brightplace tokens (Urbanist, Lato, orange/navy/teal)
- **SEO infrastructure:** JSON-LD, sitemap, robots.txt, llms.txt, 23-point audit

### What's Missing
- [ ] UI dashboard for operators (currently runs via Claude Code on local machine)
- [ ] Automated pipeline (currently manual step-by-step)
- [ ] Semrush API integration (currently manual MCP queries)
- [ ] Claude API integration for writing/QA (currently interactive)
- [ ] Operator onboarding flow
- [ ] Analytics dashboard
- [ ] Multi-operator content management

---

## Operators

### AIR Communities
- **Site:** operator-pages.vercel.app/air-communities
- **Properties:** Oak Trail (Denver), Lakeview at Gateway Park (Denver)
- **Markets:** Denver, CO
- **Articles:** 3 published
- **Keywords researched:** 6 opportunities identified

### Towne Properties
- **Site:** operator-pages.vercel.app/towne-properties
- **Properties:** Harpers Point (Cincinnati)
- **Markets:** Cincinnati, OH
- **Articles:** 1 published
- **Keywords researched:** 4 opportunities identified

---

## Keyword Research Results (Semrush Verified)

### Top Opportunities by Ease

| Keyword | Volume | KD | Operator | Status |
|---|---|---|---|---|
| lakeview at gateway park | 70 | 0 | AIR | Article exists |
| apartments near cherry creek state park | 30 | 0 | AIR | Article exists (partial) |
| dog friendly apartments denver | 70 | 13 | AIR | Not written |
| pet friendly apartments cherry creek | 50 | 19 | AIR | Not written |
| gateway park apartments denver | 140 | 20 | AIR | Not written |
| apartments near denver airport | 260 | 27 | AIR | Not written |
| luxury apartments cincinnati | 720 | 28 | Towne | Not written |
| montgomery ohio apartments | 50 | 32 | Towne | Not written |
| harpers point apartments | 720 | 39 | Towne | Article exists (partial) |

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
| seo-product | `seo-product/` | Future UI dashboard (frontend + backend + supabase) |

---

## Decisions Made

1. **Content engine only** — we don't build templates, developer team does
2. **Next.js/Vercel stack** — server-rendered for SEO + AI crawlability
3. **No client-side rendering** for content — all text in HTML source
4. **Semrush for keyword data** — real KD + volume, not estimates
5. **Agents as markdown** — portable, readable, versionable
6. **Manual testing first** — prove the pipeline works before building UI
7. **Plug-and-play vision** — content engine should work with any CMS (future)

---

## Open Questions

1. How will operators approve keywords? (UI needed)
2. Where does brand context live? (Supabase? JSON files?)
3. How do we auto-publish without manual git push? (API route? Webhook?)
4. How do we track AI citations at scale? (Weekly monitoring?)
5. Pricing model for operators? (Per article? Monthly subscription? Per lead?)
