# Visibility Engine — Complete Flow Planning

**Status:** Planning phase
**Reference:** Oak Trail Visibility Engine dashboard (HTML prototype)
**Scale target:** 100+ communities. Zero human bottleneck. Fully automated content pipeline with user approval layer.

---

## The Split

**We deliver content. Tom builds everything else.**

| We Do | Tom Does |
|-------|----------|
| Keyword research | CMS database + API |
| Content briefs | Dashboard UI |
| Blog articles + images | Blog rendering (ISR pages) |
| Social post copy + image prompts | Social media connections + publishing |
| GBP post drafts | GBP API integration + publishing |
| Review reply drafts | Review monitoring + reply posting |
| Q&A suggestions | Q&A posting to Google |
| **Agent automation (serverless)** | **Webhook system that triggers our agents** |

---

## Core Architecture: Fully Automated Two-Way System

This system must work at 100 communities with zero human intervention on our side. The only human in the loop is the community manager approving content on the dashboard.

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOM'S BUILD                                  │
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────────┐      │
│  │Dashboard │◄──►│  CMS DB  │◄──►│  Publishing Layer    │      │
│  │   UI     │    │          │    │  Blog (ISR)          │      │
│  └────┬─────┘    └────┬─────┘    │  Social (IG/FB)      │      │
│       │               │          │  GBP (Google API)     │      │
│       │          ┌────▼─────┐    └──────────────────────┘      │
│       │          │ Webhook  │                                   │
│       └─────────►│ Engine   │                                   │
│  (user action)   └────┬─────┘                                   │
└────────────────────────┼────────────────────────────────────────┘
                         │
                    webhook POST
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OUR BUILD                                    │
│                                                                 │
│  ┌──────────────────────────────────────────────┐              │
│  │  Webhook Handler (Vercel Serverless)          │              │
│  │                                               │              │
│  │  Receives event → Routes to correct agent     │              │
│  │  → Calls Claude API → Gets content back       │              │
│  │  → Pushes result to Tom's CMS API             │              │
│  └──────────────────────────────────────────────┘              │
│                         │                                       │
│           ┌─────────────┼─────────────┐                        │
│           ▼             ▼             ▼                         │
│     ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│     │ Writing  │  │ Social   │  │ Review   │  + more agents   │
│     │ Agent    │  │ Agent    │  │ Reply    │                   │
│     └──────────┘  └──────────┘  └──────────┘                  │
│                                                                 │
│     All agents call Claude API with the right prompt           │
│     + community profile + context from the event               │
└─────────────────────────────────────────────────────────────────┘
```

**The loop is fully automated:**

1. Tom's system detects an event (user approval, new review, schedule trigger)
2. Tom sends webhook to our serverless endpoint
3. Our handler routes to the right agent
4. Agent calls Claude API with the right prompt + context
5. Claude API returns the content
6. Our handler pushes result back to Tom's CMS
7. Dashboard updates automatically
8. No human on our side ever.

---

## What Tom Builds: Webhook Engine

Every user action and system event fires a webhook to our endpoint.

### Webhook Format

Tom sends a POST to our URL with this payload:

```json
{
  "event_id": "evt_abc123",
  "type": "brief_approved",
  "community_id": "foxchase",
  "timestamp": "2026-09-02T15:30:00Z",
  "data": {
    "brief_id": "brief_456",
    "keyword": "pet friendly apartments cherry creek",
    "user_note": "mention the dog run was resurfaced in August",
    "approved_by": "manager@foxchase.com"
  },
  "callback_url": "https://cms.airoperator.com/api/webhook-response"
}
```

The `callback_url` is where we push the result back. Or we use Tom's standard API endpoints.

### All Event Types Tom Must Fire

| Event Type | Trigger | What Our Agent Does | Result Pushed Back |
|---|---|---|---|
| `brief_approved` | User approves a content brief | Writing agent creates full article + image | Blog article + featured image |
| `article_update_requested` | User clicks "Request Update" with note | Update agent revises specific sections | Updated article |
| `article_published` | Article goes live on blog | Social agent creates 2-3 social posts + GBP post | Social posts + GBP draft |
| `social_regenerate` | User edits caption + clicks "Regenerate" | Social agent rewrites caption | Updated social post |
| `content_rejected` | User rejects any content with feedback | Relevant agent rewrites based on feedback | Revised content |
| `new_review` | Tom detects new Google review | Reply agent drafts response | Review reply draft |
| `review_reply_rejected` | User rejects reply draft with note | Reply agent rewrites | Revised reply |
| `profile_updated` | User updates community profile | No agent — data stored for future use | Acknowledgment only |
| `qna_request` | Monthly trigger or manual request | Q&A agent generates suggestions | Q&A pairs |
| `brief_request` | Scheduled trigger (e.g., every 2 weeks) | Keyword agent picks next target, brief agent creates brief | New content brief |

### Automatic Triggers (No User Action Needed)

These events fire on a schedule, not from user clicks:

| Trigger | Frequency | What Happens |
|---|---|---|
| New brief generation | Every 2 weeks per community | System triggers `brief_request` → our agent creates next brief → appears on dashboard |
| New review check | Every 6 hours | Tom polls GBP for new reviews → fires `new_review` for each → our agent drafts reply |
| Q&A refresh | Monthly | System triggers `qna_request` → our agent analyzes search data → pushes new suggestions |
| Stats refresh | Daily | Tom pulls GA4/GBP/social metrics → updates dashboard (no webhook to us) |

**At 100 communities this means:**
- ~200 briefs auto-generated per month (no human on our side)
- ~200 articles written per month (triggered by approvals)
- ~600 social posts created per month (auto-triggered on article publish)
- ~100 GBP posts per month
- Review replies as they come in (real-time)
- All automated. Only bottleneck is the community manager clicking Approve.

---

## What We Build: Webhook Handler

A small serverless app deployed on Vercel. This is the ONLY thing we deploy.

### Structure

```
brightplace-webhook-handler/
├── api/
│   └── webhook.ts           # Single endpoint that receives all events
├── agents/
│   ├── brief-agent.ts       # Creates content briefs from keyword data
│   ├── writing-agent.ts     # Writes full articles
│   ├── update-agent.ts      # Revises existing articles
│   ├── social-agent.ts      # Creates social posts for IG/FB
│   ├── gbp-post-agent.ts    # Creates GBP update posts
│   ├── reply-agent.ts       # Drafts review replies
│   ├── qna-agent.ts         # Generates Q&A suggestions
│   └── image-agent.ts       # Generates featured images
├── lib/
│   ├── claude.ts            # Anthropic SDK — calls Claude API
│   ├── cms.ts               # Tom's CMS API client — pushes results back
│   └── prompts/             # Agent prompts (the same ones we use in Claude Code today)
│       ├── writing-prompt.md
│       ├── social-prompt.md
│       ├── reply-prompt.md
│       └── ...
├── package.json
└── vercel.json
```

### How the Webhook Handler Works

```typescript
// api/webhook.ts
import { brief } from '../agents/brief-agent'
import { write } from '../agents/writing-agent'
import { social } from '../agents/social-agent'
import { reply } from '../agents/reply-agent'
import { update } from '../agents/update-agent'
import { qna } from '../agents/qna-agent'
import { gbpPost } from '../agents/gbp-post-agent'
import { cms } from '../lib/cms'

export async function POST(request) {
  const event = await request.json()

  // Verify webhook signature (security)
  if (!verifySignature(event, request.headers)) {
    return Response.json({ error: 'unauthorized' }, { status: 401 })
  }

  // Fetch community profile (every agent needs this context)
  const profile = await cms.getProfile(event.community_id)

  switch (event.type) {

    case 'brief_request':
      // Auto-triggered: generate next content brief
      const newBrief = await brief(event.community_id, profile)
      await cms.pushBrief(newBrief)
      break

    case 'brief_approved':
      // User approved brief → write the article
      const briefData = await cms.getBrief(event.data.brief_id)
      const article = await write(briefData, profile, event.data.user_note)
      await cms.pushArticle(article)
      break

    case 'article_published':
      // Article went live → create social posts + GBP post
      const post = await cms.getArticle(event.data.post_id)
      const socialPosts = await social(post, profile)
      const gbpDraft = await gbpPost(post, profile)
      await cms.pushSocialPosts(socialPosts)
      await cms.pushGBPPost(gbpDraft)
      break

    case 'article_update_requested':
      // User wants changes → update agent revises
      const existing = await cms.getArticle(event.data.post_id)
      const updated = await update(existing, event.data.user_note, profile)
      await cms.pushArticle(updated)
      break

    case 'social_regenerate':
      // User edited caption and wants a rewrite
      const socialPost = await cms.getSocialPost(event.data.social_post_id)
      const rewritten = await social.rewrite(socialPost, event.data.user_note, profile)
      await cms.updateSocialPost(event.data.social_post_id, rewritten)
      break

    case 'new_review':
      // New Google review → draft a reply
      const replyDraft = await reply(event.data, profile)
      await cms.pushReplyDraft(event.data.review_id, replyDraft)
      break

    case 'review_reply_rejected':
      // User rejected our reply → rewrite with feedback
      const revisedReply = await reply.revise(event.data, profile)
      await cms.pushReplyDraft(event.data.review_id, revisedReply)
      break

    case 'content_rejected':
      // Any content rejected with feedback → relevant agent rewrites
      await handleRejection(event.data, profile)
      break

    case 'qna_request':
      // Monthly trigger → generate Q&A suggestions
      const qnas = await qna(event.community_id, profile)
      await cms.pushQnAs(qnas)
      break

    case 'profile_updated':
      // No agent needed — just acknowledge
      break
  }

  return Response.json({ received: true, event_id: event.event_id })
}
```

### Each Agent Calls Claude API

```typescript
// agents/writing-agent.ts
import Anthropic from '@anthropic-ai/sdk'
import { writingPrompt } from '../lib/prompts/writing-prompt'

const client = new Anthropic()

export async function write(brief, profile, userNote) {
  const response = await client.messages.create({
    model: 'claude-sonnet-4-6',
    max_tokens: 8000,
    messages: [{
      role: 'user',
      content: writingPrompt
        .replace('{{BRIEF}}', JSON.stringify(brief))
        .replace('{{PROFILE}}', JSON.stringify(profile))
        .replace('{{USER_NOTE}}', userNote || 'none')
    }]
  })

  // Parse the article from Claude's response
  return parseArticle(response.content[0].text)
}
```

---

## The Complete Automated Loop

Here's how a single piece of content flows through the system with zero human intervention on our side:

```
Week 1, Monday (automatic):
  Tom's scheduler fires "brief_request" for Foxchase
    → Our webhook handler receives it
    → Brief agent calls Claude API
    → Claude picks best keyword, creates brief
    → Handler pushes brief to Tom's CMS
    → Dashboard shows "New brief — Needs review"

Week 1, Tuesday (community manager):
  Manager opens dashboard, sees brief
  Clicks "Approve", adds note "mention new lobby renovation"
    → Tom fires "brief_approved" webhook
    → Our handler receives it
    → Writing agent calls Claude API with brief + profile + note
    → Claude writes full 2,000-word article
    → Handler pushes article to Tom's CMS
    → Dashboard shows "Article scheduled for Monday"

Week 2, Monday (automatic):
  Tom's scheduler publishes the article at 9 AM
    → Tom fires "article_published" webhook
    → Our handler receives it
    → Social agent calls Claude API
    → Claude creates 3 posts (IG feed, IG story, FB page)
    → GBP agent calls Claude API
    → Claude creates GBP update post
    → Handler pushes all 4 posts to Tom's CMS
    → Dashboard shows "3 social posts + 1 GBP post — Needs review"

Week 2, Tuesday (community manager):
  Manager opens dashboard, reviews social posts
  Approves all 3 social posts and the GBP post
    → Tom schedules them at their designated times
    → Posts go out automatically over the week

Meanwhile (automatic, ongoing):
  Tom detects new Google review at 2 PM
    → Tom fires "new_review" webhook
    → Our handler receives it
    → Reply agent calls Claude API with review + community profile
    → Claude drafts professional reply
    → Handler pushes draft to Tom's CMS
    → Dashboard shows "New review — reply drafted"

  Manager sees it, clicks "Approve"
    → Tom posts the reply to Google

Next month (automatic):
  Tom fires "qna_request" for Foxchase
    → Our handler receives it
    → Q&A agent analyzes search data + chat queries
    → Generates 3-5 new Q&A pairs
    → Handler pushes to Tom's CMS
    → Dashboard shows "5 Q&A suggestions"

  Manager approves them → Tom posts to GBP listing
```

**Every 2 weeks, per community, the entire cycle repeats automatically. The community manager's only job is clicking Approve or editing captions.**

---

## Scale Math: 100 Communities

| Activity | Per Community/Month | At 100 Communities |
|---|---|---|
| Content briefs generated | 2 | 200 |
| Articles written (after approval) | 2 | 200 |
| Social posts created | 6 | 600 |
| GBP update posts | 2 | 200 |
| Review replies drafted | ~4 (avg) | ~400 |
| Q&A suggestions | 3-5 | 300-500 |

**Total Claude API calls per month at 100 communities: ~1,900**
**Total human effort on our side: zero**
**Total human effort per community manager: ~15 minutes/week (approve + review)**

---

## The 3 Channels (What We Send)

### Channel 1: Blog — What We Send

**Brief payload:**
```json
{
  "community_id": "foxchase",
  "keyword": "pet friendly apartments cherry creek denver",
  "volume": 590,
  "difficulty": 21,
  "tier": "Long Tail",
  "seo_title": "Pet-Friendly Apartments in Cherry Creek: Oak Trail Guide",
  "h1": "Pet-Friendly Living at Oak Trail in Cherry Creek",
  "word_count_target": 2000,
  "faq_count": 10,
  "publish_date": "2026-09-08",
  "outline": [
    { "h2": "Which Cherry Creek apartments allow large dogs?", "description": "No-weight-limit policy vs typical 50 lb caps." },
    { "h2": "What does pet rent cost at Oak Trail?", "description": "$35/mo pet rent + $250 deposit, dated Q3 2026." },
    { "h2": "Where are the nearest dog parks and trails?", "description": "On-site dog run, Cherry Creek Trail, Pulaski Park." }
  ],
  "internal_links": ["pet policy", "floor plans", "pricing calculator", "tour booking"],
  "status": "pending"
}
```

**Article payload:** Same as the blog CMS spec (already documented in the technical spec).

### Channel 2: Social Media — What We Send

```json
{
  "community_id": "foxchase",
  "blog_post_id": "a1b2c3d4-...",
  "platform": "instagram",
  "post_type": "feed",
  "caption": "Cherry Creek mornings hit different when the dog run is 40 steps from your door. Oak Trail is pet-friendly the real way — no weight limits on most floor plans, wash station on-site.",
  "hashtags": "#CherryCreek #DenverApartments #PetFriendlyDenver #OakTrail",
  "image_prompt": "Golden retriever at the Oak Trail dog run, morning light, Cherry Creek neighborhood",
  "link_url": "https://foxchaseofalexandriaapts.com/blog/pet-friendly-apartments",
  "cta_text": "Read the full guide",
  "scheduled_at": "2026-09-09T11:00:00-06:00",
  "status": "draft"
}
```

We send 2-3 posts per article:

| Post | Platform | Type | Timing |
|------|----------|------|--------|
| 1 | Instagram | Feed post | 1-2 days after article |
| 2 | Instagram | Story | 2-3 days after article |
| 3 | Facebook | Page post | Same week |

### Channel 3: Google Business Profile — What We Send

**GBP update post:**
```json
{
  "community_id": "foxchase",
  "blog_post_id": "a1b2c3d4-...",
  "post_type": "update",
  "body_text": "New on the blog: everything pet owners ask before touring Foxchase — pet rent, breed policy, and the best walking routes.",
  "cta_type": "learn_more",
  "cta_url": "https://foxchaseofalexandriaapts.com/blog/pet-friendly-apartments",
  "image_url": "https://cdn.domain.com/blog/featured-image.webp",
  "scheduled_at": "2026-09-08T09:00:00-04:00",
  "status": "draft"
}
```

**Review reply draft:**
```json
{
  "community_id": "foxchase",
  "google_review_id": "abc123",
  "reviewer_name": "Jenna M.",
  "rating": 5,
  "review_text": "Maintenance fixed our disposal same day...",
  "reply_draft": "Thanks, Jenna! Same-day fixes are the goal — we'll pass this along to the maintenance team.",
  "status": "pending"
}
```

**Q&A suggestion:**
```json
{
  "community_id": "foxchase",
  "question": "Is parking included in rent?",
  "answer": "Covered parking is $75/mo; one surface spot is included with every lease (as of Q3 2026).",
  "source": "chat_data",
  "frequency": 14,
  "status": "suggested"
}
```

---

## Community Profile — What We Pre-Fill

```json
{
  "community_id": "foxchase",
  "positioning": "88-acre wooded apartment community in Seminary Hill — largest in Alexandria, 10 minutes from Historic Old Town, under 10 miles from D.C.",
  "differentiators": [
    "4 pools and 3 fitness centers",
    "Townhome options with in-home W/D",
    "Newly renovated with quartz countertops",
    "Wi-Fi included in rent",
    "88 wooded acres"
  ],
  "neighborhood_anchors": [
    { "name": "Historic Old Town Alexandria", "time": "10 min" },
    { "name": "Inova Alexandria Hospital", "time": "3 min" },
    { "name": "Fort Ward Park", "time": "5 min" },
    { "name": "Washington D.C.", "time": "15 min" }
  ],
  "things_we_never_say": "Luxury without specific feature backing it. Family-friendly or any household-type language (Fair Housing). Competitor names in negative frame.",
  "profile_completeness": 80
}
```

User-only fields (dashboard shows these highlighted for the community manager to fill):
- **What do prospects ask most on tours?**
- **What do current residents say they love?**

When the manager fills these, Tom fires `profile_updated` webhook. Our agents use this data in all future content.

---

## What Tom Builds — Complete List

| Component | Purpose |
|---|---|
| **CMS database** | Stores all content (briefs, articles, social posts, GBP drafts, reviews, Q&As, profiles) |
| **REST API** | Endpoints for us to push content + endpoints for dashboard |
| **Webhook engine** | Fires webhooks to our serverless endpoint on every event |
| **Dashboard UI** | 3-tab interface (SEO, Social, GBP) with approval flows, calendar, stats |
| **Blog rendering** | Next.js ISR pages at `/blog/[slug]` |
| **Social publishing** | Connects to Instagram + Facebook, posts at scheduled time |
| **GBP integration** | Connects to Google Business Profile API for posts, replies, Q&As, stats |
| **Scheduling engine** | Fires auto-triggers (brief generation, review checks, Q&A refresh) |
| **Stats/analytics** | Pulls from GA4/Vercel/GBP/social, displays on dashboard |
| **Auth system** | Login for team + community managers |
| **Community switcher** | Switch between communities in dashboard |
| **Review monitor** | Polls GBP for new reviews every 6 hours, fires webhook |

## What We Build — Complete List

| Component | Purpose |
|---|---|
| **Webhook handler** | Single Vercel serverless app that receives all events |
| **Agent suite** | 8 agents that call Claude API (brief, writing, update, social, GBP post, reply, Q&A, image) |
| **Agent prompts** | The prompt files each agent uses (same ones we use in Claude Code today, converted to templates) |
| **CMS client** | Simple API client that pushes results back to Tom's CMS |

Our entire build is one small Vercel project. Tom's build is larger but it's standard web app + API + integrations.

---

## What's Left to Do

- [ ] Finalize this flow with Haroon and team
- [ ] Convert our existing Claude Code agent prompts into API-callable templates
- [ ] Build the webhook handler (small Vercel project)
- [ ] Write the full technical spec for Tom (dashboard + social + GBP endpoints + webhook contract)
- [ ] Add dashboard + social spec to the consolidated technical doc
- [ ] Test with Foxchase first, then roll out
