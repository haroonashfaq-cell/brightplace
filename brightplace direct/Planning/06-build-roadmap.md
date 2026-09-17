# 06 — Build Roadmap

## Phase 1: Manual Validation (NOW)
**Goal:** Prove the content pipeline works end-to-end
**Timeline:** This week

- [x] Keyword Agent: researched 10 keywords with Semrush data
- [x] Keyword reports created for both operators
- [ ] Write 2-3 new articles using approved keywords
- [ ] QA each article
- [ ] Publish to operator-pages.vercel.app
- [ ] Track initial indexing in Google Search Console

**Success criteria:** Articles published, indexed by Google within 7 days

---

## Phase 2: Operator Dashboard MVP (Next)
**Goal:** Operators can see keywords and articles in a web UI
**Timeline:** 2-3 weeks after Phase 1

### What to build:
- Login page (Supabase Auth)
- Keyword dashboard (table with volume, KD, approve/reject buttons)
- Article pipeline view (status: brief → writing → QA → published)
- Simple analytics (page views per article from Vercel Analytics)

### Tech:
- Next.js pages in seo-product/frontend
- Supabase for data
- Vercel for hosting

### NOT in MVP:
- Automated writing (still triggered manually via Claude API)
- Image generation
- Multi-CMS publishing
- Advanced analytics

---

## Phase 3: Automated Pipeline (After MVP)
**Goal:** Keyword approved → article published automatically
**Timeline:** 4-6 weeks after Phase 2

### What to build:
- API route that calls Claude API with Brief Agent prompt
- API route that calls Claude API with Writing Agent prompt
- API route that calls Claude API with QA Agent prompt
- Auto-publish: API creates file in repo, triggers Vercel deploy
- Semrush API integration for live keyword data

### This is where agents become code:
- Markdown agent files → system prompts for Claude API calls
- Pipeline orchestration via backend job queue
- Error handling and retry logic

---

## Phase 4: Multi-CMS Support (Future)
**Goal:** Content engine works with any website stack
**Timeline:** After Phase 3

### Publish adapters:
- Next.js/Vercel (exists)
- Webflow CMS API
- WordPress REST API
- Contentful/Sanity
- Generic webhook

### This makes brightplace direct plug-and-play:
- Operator has a WordPress site? We publish there.
- Operator has Webflow? We publish there.
- Operator has custom CMS? We send a webhook.

---

## Phase 5: Scale (Future)
**Goal:** 50+ operators, 1000+ articles
**Timeline:** After Phase 4

- Automated monthly keyword refresh per operator
- AI citation monitoring dashboard
- Lead attribution tracking
- White-label option (operator's brand, no brightplace mention)
- API for third-party integrations

---

## Summary

| Phase | Goal | Status |
|---|---|---|
| 1. Manual Validation | Prove pipeline works | In progress |
| 2. Dashboard MVP | Operators see data in UI | Planning |
| 3. Automated Pipeline | No manual intervention | Planning |
| 4. Multi-CMS | Plug-and-play publishing | Future |
| 5. Scale | 50+ operators | Future |
