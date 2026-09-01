# Product Idea: Autonomous SEO Agent Platform

**Status:** Brainstorming
**Created:** September 2026

---

## The Idea

A platform where businesses connect their website and get end-to-end SEO handled by AI agents — keyword research, content production, technical audits, and ongoing optimization — all running through a dashboard they can see and approve.

---

## Three Build Phases

### Phase 1: MCP-Connected CLI (works today)
- Run SUPER SEO agents in Claude Code
- Push content to client CMS via API
- Manual orchestration, you run everything
- **Revenue model:** SEO agency retainer per client

### Phase 2: Client Dashboard (build next)
- Next.js app on Vercel
- Client onboards: enters URL, business info, competitors
- Dashboard shows: keyword research, content pipeline, audit reports
- Content auto-pushes to their CMS as drafts
- Human approves before publish
- **Revenue model:** SaaS subscription per site ($99-499/mo)

### Phase 3: Fully Autonomous (endgame)
- Cron-triggered agents run on schedule
- Weekly keyword scans, monthly audits, auto-draft articles
- Slack/email notifications for approvals
- Client just reviews and clicks "publish"
- **Revenue model:** SaaS + usage-based pricing for API calls

---

## Key Discussions Needed

- [ ] Tech stack decisions (Vercel + Next.js + Claude API?)
- [ ] CMS integrations to support (Webflow, WordPress, Vercel CMS, Contentful?)
- [ ] Pricing model and tiers
- [ ] How much human review before publish?
- [ ] API cost management (Semrush, Claude, CMS calls)
- [ ] Multi-tenant architecture
- [ ] First pilot client?

---

## Files in This Folder

- `README.md` — This file (product overview)
- Future: `architecture.md`, `pricing.md`, `mvp-spec.md`, `pilot-plan.md`
