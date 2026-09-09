# Build Map: What We Build vs What Tom Builds

---

## OUR BUILD

One Vercel serverless project. That's it.

```
brightplace-webhook-handler/
├── api/
│   └── webhook.ts
├── agents/
│   ├── brief-agent.ts
│   ├── writing-agent.ts
│   ├── update-agent.ts
│   ├── social-agent.ts
│   ├── gbp-post-agent.ts
│   ├── reply-agent.ts
│   ├── qna-agent.ts
│   └── image-agent.ts
├── lib/
│   ├── claude.ts
│   ├── cms.ts
│   └── prompts/
│       ├── brief-prompt.md
│       ├── writing-prompt.md
│       ├── social-prompt.md
│       ├── reply-prompt.md
│       ├── update-prompt.md
│       ├── qna-prompt.md
│       └── gbp-post-prompt.md
├── package.json
└── vercel.json
```

### Files We Need to Create

| # | File | What It Does | Status |
|---|------|-------------|--------|
| 1 | `api/webhook.ts` | Receives all webhooks from Tom, routes to correct agent | Need to build |
| 2 | `lib/claude.ts` | Anthropic SDK wrapper — calls Claude API | Need to build |
| 3 | `lib/cms.ts` | API client — pushes results back to Tom's CMS | Need to build (depends on Tom's API) |
| 4 | `agents/brief-agent.ts` | Picks keyword, creates content brief, returns JSON | Need to build |
| 5 | `agents/writing-agent.ts` | Takes brief + profile + note, returns full article | Need to build |
| 6 | `agents/update-agent.ts` | Takes existing article + user feedback, returns revised article | Need to build |
| 7 | `agents/social-agent.ts` | Takes published article + profile, returns 2-3 social posts | Need to build |
| 8 | `agents/gbp-post-agent.ts` | Takes published article + profile, returns GBP update post | Need to build |
| 9 | `agents/reply-agent.ts` | Takes review + profile, returns reply draft | Need to build |
| 10 | `agents/qna-agent.ts` | Takes community data, returns Q&A suggestions | Need to build |
| 11 | `agents/image-agent.ts` | Takes article/post context, returns image prompt or generated image | Need to build |
| 12 | `lib/prompts/brief-prompt.md` | Prompt template for brief agent | **Exists** — adapt from `Agents/brief-check-agent.md` |
| 13 | `lib/prompts/writing-prompt.md` | Prompt template for writing agent | **Exists** — adapt from `Agents/seo-writing-agent.md` |
| 14 | `lib/prompts/social-prompt.md` | Prompt template for social post creation | Need to create |
| 15 | `lib/prompts/reply-prompt.md` | Prompt template for review replies | Need to create |
| 16 | `lib/prompts/update-prompt.md` | Prompt template for article updates | Need to create |
| 17 | `lib/prompts/qna-prompt.md` | Prompt template for Q&A generation | Need to create |
| 18 | `lib/prompts/gbp-post-prompt.md` | Prompt template for GBP posts | Need to create |
| 19 | `package.json` | Dependencies: `@anthropic-ai/sdk`, `next` | Need to create |
| 20 | `vercel.json` | Deployment config | Need to create |

### Our Build Summary

| Category | Count | Notes |
|----------|-------|-------|
| API routes | 1 | Single webhook endpoint handles everything |
| Agent files | 8 | Each wraps a Claude API call with the right prompt |
| Prompt templates | 7 | 2 exist (adapt from current agents), 5 new |
| Library files | 2 | Claude SDK client + Tom's CMS API client |
| Config files | 2 | package.json + vercel.json |
| **Total files** | **20** | |

### Dependencies

| Package | Purpose |
|---------|---------|
| `@anthropic-ai/sdk` | Call Claude API |
| `next` | Vercel serverless functions |

### Environment Variables We Need

```
ANTHROPIC_API_KEY=sk-ant-...
CMS_API_URL=https://cms.airoperator.com/api
CMS_API_KEY=...
WEBHOOK_SECRET=... (to verify Tom's webhooks are legit)
```

---

## TOM'S BUILD

Full web application: CMS + Dashboard + Publishing + Integrations.

### Database Tables

| # | Table | Purpose |
|---|-------|---------|
| 1 | `communities` | The 5 (→100) community profiles |
| 2 | `community_profiles` | Positioning, differentiators, neighborhood, things we never say, user-filled fields |
| 3 | `blog_posts` | Articles (already specced in technical doc) |
| 4 | `content_briefs` | Keyword briefs awaiting approval |
| 5 | `social_posts` | Instagram + Facebook post drafts/scheduled/published |
| 6 | `gbp_posts` | Google Business Profile update posts |
| 7 | `gbp_reviews` | Google reviews + reply drafts |
| 8 | `gbp_qna` | Q&A suggestions + published Q&As |
| 9 | `webhook_events` | Log of all events fired + responses received |
| 10 | `users` | Dashboard login accounts (team + community managers) |
| 11 | `scheduled_jobs` | Cron triggers (brief generation, review polling, Q&A refresh) |

### API Endpoints

**Content Briefs**
| # | Method | Endpoint | Who Calls | Purpose |
|---|--------|----------|-----------|---------|
| 1 | `POST` | `/api/briefs` | Us | Push new brief |
| 2 | `GET` | `/api/briefs?community_id=X&status=pending` | Dashboard | List briefs |
| 3 | `GET` | `/api/briefs/[id]` | Dashboard + Us | Get brief detail |
| 4 | `PATCH` | `/api/briefs/[id]/status` | Dashboard | Approve/skip (fires webhook to us) |

**Blog Posts (already specced)**
| # | Method | Endpoint | Who Calls | Purpose |
|---|--------|----------|-----------|---------|
| 5 | `POST` | `/api/blog/posts` | Us | Create article |
| 6 | `PUT` | `/api/blog/posts/[id]` | Us | Update article |
| 7 | `PATCH` | `/api/blog/posts/[id]/status` | Dashboard | Publish/unpublish (fires webhook to us on publish) |
| 8 | `GET` | `/api/blog/posts/[id]` | Dashboard + Us | Get article |
| 9 | `GET` | `/api/blog/posts?community_id=X` | Dashboard | List articles |
| 10 | `DELETE` | `/api/blog/posts/[id]` | Dashboard | Archive |
| 11 | `POST` | `/api/blog/images` | Us | Upload image |

**Social Posts**
| # | Method | Endpoint | Who Calls | Purpose |
|---|--------|----------|-----------|---------|
| 12 | `POST` | `/api/social/posts` | Us | Push social post drafts |
| 13 | `GET` | `/api/social/posts?community_id=X` | Dashboard | List social posts |
| 14 | `GET` | `/api/social/posts/[id]` | Dashboard | Get post detail |
| 15 | `PATCH` | `/api/social/posts/[id]` | Dashboard | Edit caption/time |
| 16 | `PATCH` | `/api/social/posts/[id]/status` | Dashboard | Approve/reject (fires webhook on regenerate) |

**GBP Posts**
| # | Method | Endpoint | Who Calls | Purpose |
|---|--------|----------|-----------|---------|
| 17 | `POST` | `/api/gbp/posts` | Us | Push GBP post draft |
| 18 | `GET` | `/api/gbp/posts?community_id=X` | Dashboard | List GBP posts |
| 19 | `PATCH` | `/api/gbp/posts/[id]/status` | Dashboard | Approve → publishes to Google |

**GBP Reviews**
| # | Method | Endpoint | Who Calls | Purpose |
|---|--------|----------|-----------|---------|
| 20 | `GET` | `/api/gbp/reviews?community_id=X` | Dashboard | List reviews |
| 21 | `POST` | `/api/gbp/reviews/[id]/reply-draft` | Us | Push reply draft |
| 22 | `PATCH` | `/api/gbp/reviews/[id]/reply-status` | Dashboard | Approve → publishes reply |

**GBP Q&A**
| # | Method | Endpoint | Who Calls | Purpose |
|---|--------|----------|-----------|---------|
| 23 | `POST` | `/api/gbp/qna` | Us | Push Q&A suggestions |
| 24 | `GET` | `/api/gbp/qna?community_id=X` | Dashboard | List Q&As |
| 25 | `PATCH` | `/api/gbp/qna/[id]/status` | Dashboard | Approve → posts to Google |

**Community Profiles**
| # | Method | Endpoint | Who Calls | Purpose |
|---|--------|----------|-----------|---------|
| 26 | `POST` | `/api/profiles` | Us | Push pre-filled profile |
| 27 | `GET` | `/api/profiles/[community_id]` | Dashboard + Us | Get profile |
| 28 | `PUT` | `/api/profiles/[community_id]` | Dashboard | Update profile (fires webhook to us) |

**Dashboard Stats**
| # | Method | Endpoint | Who Calls | Purpose |
|---|--------|----------|-----------|---------|
| 29 | `GET` | `/api/stats/[community_id]` | Dashboard | Aggregated stats for header |

**Webhooks**
| # | Method | Endpoint | Who Calls | Purpose |
|---|--------|----------|-----------|---------|
| 30 | `POST` | `/api/webhooks/register` | Us (one-time) | Register our webhook URL |
| 31 | `GET` | `/api/webhooks/events?status=pending` | Us (fallback) | Poll events if webhook fails |

### Dashboard Pages

| # | Page | What It Shows |
|---|------|--------------|
| 1 | Login | Email/password auth |
| 2 | Community Switcher | Dropdown or sidebar to switch between communities |
| 3 | SEO/AEO Tab | Stats row, brief cards (approve/skip), article pipeline list, calendar |
| 4 | Social Media Tab | Week context note, post preview cards (approve/edit), scheduling |
| 5 | Google Business Tab | Profile health ring, GBP post drafts, review replies, Q&A suggestions, photo alerts |
| 6 | Community Profile (modal/page) | Editable profile fields, completeness meter |
| 7 | Brief Detail (modal) | Full brief with H2 outline, targeting data, user note field |
| 8 | Article Preview | View rendered article before publish |
| 9 | Social Post Editor | Edit caption, change time, preview how it looks on IG/FB |

### Integrations Tom Handles

| # | Integration | Purpose | How |
|---|-------------|---------|-----|
| 1 | Instagram | Publish feed posts + stories | Meta Graph API or unified API (Tom's choice) |
| 2 | Facebook | Publish page posts | Meta Graph API or unified API |
| 3 | Google Business Profile — Posts | Publish update/offer posts | GBP Local Posts API |
| 4 | Google Business Profile — Reviews | Monitor new reviews, post replies | GBP Reviews API |
| 5 | Google Business Profile — Q&A | Post Q&As to listing | GBP API |
| 6 | Google Business Profile — Insights | Pull views, calls, directions | GBP Performance API |
| 7 | GA4 or Vercel Analytics | Pull blog traffic stats | GA4 Data API or Vercel API |
| 8 | Our Webhook Endpoint | Fire events to trigger our agents | HTTP POST to our URL |

### Scheduled Jobs Tom Runs

| # | Job | Frequency | What It Does |
|---|-----|-----------|-------------|
| 1 | Brief generation trigger | Every 2 weeks per community | Fires `brief_request` webhook to us |
| 2 | Review polling | Every 6 hours | Checks GBP for new reviews, fires `new_review` webhook |
| 3 | Q&A refresh trigger | Monthly per community | Fires `qna_request` webhook to us |
| 4 | Stats refresh | Daily | Pulls GA4/GBP/social metrics, updates dashboard |
| 5 | Social post publisher | Minute-level check | Fires queued social posts at their scheduled time |
| 6 | GBP post publisher | Minute-level check | Fires queued GBP posts at their scheduled time |

### Tom's Build Summary

| Category | Count |
|----------|-------|
| Database tables | 11 |
| API endpoints | 31 |
| Dashboard pages/views | 9 |
| External integrations | 8 |
| Scheduled jobs | 6 |
| Webhook event types | 10 |

---

## Side-by-Side Comparison

| | Us | Tom |
|---|---|---|
| **Deploy** | 1 Vercel project | 1 Vercel project (larger) |
| **Files** | ~20 | Full web app |
| **Database** | None | 11 tables |
| **API endpoints** | 1 (webhook receiver) | 31 |
| **External APIs** | Claude API only | IG, FB, GBP, GA4 |
| **UI** | None | Full dashboard |
| **Scheduled jobs** | None | 6 |
| **Auth** | Webhook signature verification | User login system |

---

## Build Order

### Phase 1: Blog (already specced)
**Tom:** CMS database + blog API endpoints + blog page rendering
**Us:** Nothing new yet (we push via Claude Code manually for now)

### Phase 2: Dashboard + Briefs
**Tom:** Dashboard UI (SEO tab) + briefs table + briefs API + webhook engine
**Us:** Webhook handler + brief agent + writing agent

### Phase 3: Social
**Tom:** Social posts table + social API + social publishing integration + dashboard social tab
**Us:** Social agent + social prompt template

### Phase 4: Google Business Profile
**Tom:** GBP tables + GBP API endpoints + GBP integrations + dashboard GBP tab + review monitor
**Us:** GBP post agent + reply agent + Q&A agent + their prompt templates

### Phase 5: Scale
**Tom:** Community switcher + multi-tenant support + scheduled jobs
**Us:** Optimize agents for speed + handle 100 communities worth of webhook volume
