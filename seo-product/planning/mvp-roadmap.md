# MVP Scope & Development Roadmap

**Last Updated:** August 2026

---

## MVP Definition

Ship the core pipeline first. Everything else is Phase 2+.

```
MVP Pipeline:
Project Setup → Keyword Gap Finder → Research Engine → Content Brief → Writing Agent → QA Agent → Export
```

---

## Phase 1: MVP (Weeks 1-10)

### Week 1-2: Foundation

- [ ] Project scaffolding (Next.js frontend + FastAPI backend)
- [ ] Supabase setup (database, auth, storage)
- [ ] Redis setup (Upstash for task queue)
- [ ] Database schema (users, projects, keywords, briefs, articles)
- [ ] Auth flow (email + Google login)
- [ ] Project creation (enter domain, set niche, store brand context)

### Week 3-4: Keyword Intelligence

- [ ] DataForSEO API integration
- [ ] Competitor discovery (enter domain → find top competitors)
- [ ] Keyword gap analysis (their keywords vs yours)
- [ ] Keyword table UI (volume, KD, intent, with filters + sort)
- [ ] Long-tail keyword finder (click keyword → expand related terms)
- [ ] Keyword selection + save to project

### Week 5-6: Research Engine

- [ ] SERP Analysis Agent (scrape top 10, extract format/depth/gaps)
- [ ] PAA Extraction (from SERP data)
- [ ] AI Mode Analysis Agent (query ChatGPT + Claude, extract citations)
- [ ] Reddit Research Agent (search + analyze discussions)
- [ ] Research report compilation (structured MD/JSON)
- [ ] Research progress UI (WebSocket live updates)

### Week 7-8: Brief + Writing + QA

- [ ] Brief Generator Agent (research + context → structured brief)
- [ ] Brief preview/edit UI
- [ ] Writing Agent (brief → full article with ranking optimizations)
- [ ] Live article preview with SEO score sidebar
- [ ] Section-level regeneration (click H2 → rewrite just that section)
- [ ] QA Agent (brand compliance, SEO structure, link audit, math check)
- [ ] QA report UI with pass/fail indicators

### Week 9-10: Polish + Export

- [ ] Article export (Markdown, HTML, JSON)
- [ ] Copy-to-clipboard for article body
- [ ] Project dashboard (list of all articles with status)
- [ ] Settings page (brand rules, QA rules, API keys)
- [ ] Basic usage tracking (articles created this month)
- [ ] Bug fixes, performance optimization, testing

### MVP Deliverables

- Working web app at [product-domain].com
- User can: create project → find keyword gaps → research a keyword → generate brief → write article → run QA → export
- No CMS publishing yet (export only)
- No image generation yet
- No site audit dashboard yet
- Single user (no teams)

---

## Phase 2: Integrations + Publishing (Weeks 11-16)

### Week 11-12: CMS Integrations (Tier 1)

- [ ] WordPress integration (OAuth + REST API push)
- [ ] Webflow integration (OAuth + CMS API push)
- [ ] "Publish" button in article view
- [ ] Draft vs Published toggle
- [ ] Image upload to CMS before article push

### Week 13-14: Image Generation + Site Audit

- [ ] Image generation agent (3 options per article)
- [ ] Image preview + download + CMS upload
- [ ] Site audit crawler (technical issues, schema check, AI readiness)
- [ ] Audit dashboard UI (health score, issue list, fix suggestions)

### Week 15-16: More CMS + Polish

- [ ] Shopify integration
- [ ] Ghost integration
- [ ] Content history (versions, rollback)
- [ ] Improved SEO scoring algorithm
- [ ] Onboarding flow improvements

---

## Phase 3: Team + Scale (Weeks 17-22)

### Week 17-18: Team Features

- [ ] Team workspaces (invite members, assign roles)
- [ ] Multi-project support (one team, many websites)
- [ ] Content calendar view
- [ ] Assignment workflow (assign keyword → writer)

### Week 19-20: More Integrations

- [ ] HubSpot integration
- [ ] Wix integration
- [ ] Google Search Console integration (performance tracking)
- [ ] Google Analytics integration (traffic data)

### Week 21-22: Advanced Features

- [ ] Custom QA rule builder (user creates own rules)
- [ ] Watermark risk scoring and recommendations
- [ ] Competitor monitoring (track their new content)
- [ ] Content refresh alerts (articles > 90 days old)

---

## Phase 4: Enterprise + API (Weeks 23+)

- [ ] White-label option (agency branding)
- [ ] API access for programmatic content generation
- [ ] Multi-language support
- [ ] Advanced analytics (ranking tracking, ROI)
- [ ] Webhook integrations
- [ ] SSO / SAML authentication
- [ ] Priority support tier

---

## Technical Priorities by Phase

| Phase | Focus | Risk |
|---|---|---|
| Phase 1 | Core pipeline works end-to-end | Agent reliability, API costs |
| Phase 2 | Users can publish without leaving the app | CMS API quirks, auth flows |
| Phase 3 | Teams can collaborate on content production | Permission models, real-time sync |
| Phase 4 | Enterprise sales, API monetization | Scale, security, compliance |

---

## Success Metrics by Phase

| Phase | Metric | Target |
|---|---|---|
| Phase 1 | Users who complete full pipeline (keyword → export) | 50+ in first month |
| Phase 2 | Articles published directly to CMS | 200+ in first month |
| Phase 3 | Teams with 2+ active members | 20+ teams |
| Phase 4 | API calls per month | 10,000+ |
