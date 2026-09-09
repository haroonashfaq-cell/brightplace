# API Endpoints We Need From Tom

**Purpose:** Full CRUD access from Claude Code to every content type across all channels.
**Auth:** `Authorization: Bearer [API_KEY]` on every request.
**Base URL:** `https://cms.airoperator.com/api` (or per-community domain)

---

## 1. Events Queue (How We Know What To Do)

This is how we see what work is pending — approvals, update requests, new reviews, rejections, etc.

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `GET` | `/api/events?community_id=foxchase&status=pending` | List all pending events for a community |
| `GET` | `/api/events?status=pending` | List ALL pending events across all communities |
| `GET` | `/api/events/[event_id]` | Get single event detail |
| `PATCH` | `/api/events/[event_id]` | Mark event as `processed` or `failed` (so we don't process it twice) |

**Event payload returned:**

```json
{
  "event_id": "evt_abc123",
  "type": "brief_approved",
  "community_id": "foxchase",
  "status": "pending",
  "timestamp": "2026-09-03T15:30:00Z",
  "data": {
    "brief_id": "brief_456",
    "keyword": "pet friendly apartments cherry creek",
    "user_note": "mention the dog run was resurfaced",
    "approved_by": "manager@foxchase.com"
  }
}
```

**Event types Tom fires into this queue:**

| Type | When | What We Do |
|------|------|-----------|
| `brief_approved` | User approves a brief | Run writing agent, push article |
| `article_update_requested` | User wants article refreshed | Run update agent, push revised article |
| `article_published` | Article goes live | Run social agent + GBP agent, push posts |
| `social_regenerate` | User edits caption + wants rewrite | Run social agent, push updated post |
| `content_rejected` | User rejects any content with note | Run relevant agent, push revision |
| `new_review` | Tom detects new Google review | Run reply agent, push draft reply |
| `review_reply_rejected` | User rejects our reply draft | Run reply agent again, push revised reply |
| `profile_updated` | User updates community profile | No agent — we just note the change |
| `qna_request` | Monthly or manual trigger | Run Q&A agent, push suggestions |
| `brief_request` | Scheduled or manual trigger | Run brief agent, push new brief |

---

## 2. Community Profiles

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `POST` | `/api/profiles` | Create a new community profile |
| `GET` | `/api/profiles?community_id=foxchase` | Get profile for a community |
| `GET` | `/api/profiles` | List all community profiles |
| `PUT` | `/api/profiles/[community_id]` | Update full profile |
| `PATCH` | `/api/profiles/[community_id]` | Update specific fields |

---

## 3. Content Briefs

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `POST` | `/api/briefs` | Create a new brief |
| `GET` | `/api/briefs?community_id=foxchase&status=pending` | List briefs (filterable by community + status) |
| `GET` | `/api/briefs/[id]` | Get single brief |
| `PUT` | `/api/briefs/[id]` | Update a brief (full replace) |
| `PATCH` | `/api/briefs/[id]` | Update specific fields |
| `DELETE` | `/api/briefs/[id]` | Delete a brief |

---

## 4. Blog Posts

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `POST` | `/api/blog/posts` | Create article (multipart — includes image) |
| `GET` | `/api/blog/posts?community_id=foxchase&status=published` | List articles (filterable) |
| `GET` | `/api/blog/posts/[id]` | Get single article |
| `PUT` | `/api/blog/posts/[id]` | Update article (multipart — can include new image) |
| `PATCH` | `/api/blog/posts/[id]` | Update specific fields (title, body, status, etc.) |
| `DELETE` | `/api/blog/posts/[id]` | Archive article (soft delete) |
| `PATCH` | `/api/blog/posts/[id]/status` | Change status: draft / published / archived |
| `POST` | `/api/blog/images` | Upload image separately |

---

## 5. Social Posts

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `POST` | `/api/social/posts` | Create a social post draft |
| `POST` | `/api/social/posts/batch` | Create multiple posts at once (2-3 per article) |
| `GET` | `/api/social/posts?community_id=foxchase&status=draft` | List social posts (filterable by community, status, platform) |
| `GET` | `/api/social/posts/[id]` | Get single post |
| `PUT` | `/api/social/posts/[id]` | Update full post (caption, hashtags, image, time) |
| `PATCH` | `/api/social/posts/[id]` | Update specific fields |
| `DELETE` | `/api/social/posts/[id]` | Delete a post |
| `PATCH` | `/api/social/posts/[id]/status` | Change status: draft / approved / scheduled / published / failed |

**Social post payload:**

```json
{
  "community_id": "foxchase",
  "blog_post_id": "a1b2c3d4-...",
  "platform": "instagram",
  "post_type": "feed",
  "caption": "Cherry Creek mornings hit different when the dog run is 40 steps from your door...",
  "hashtags": "#CherryCreek #DenverApartments #PetFriendlyDenver",
  "image_url": "https://cdn.domain.com/social/image.webp",
  "image_alt": "Dog at Oak Trail dog run",
  "link_url": "https://foxchaseofalexandriaapts.com/blog/slug",
  "cta_text": "Read the full guide",
  "scheduled_at": "2026-09-09T11:00:00-06:00",
  "status": "draft"
}
```

---

## 6. GBP Posts

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `POST` | `/api/gbp/posts` | Create a GBP post draft |
| `GET` | `/api/gbp/posts?community_id=foxchase` | List GBP posts |
| `GET` | `/api/gbp/posts/[id]` | Get single post |
| `PUT` | `/api/gbp/posts/[id]` | Update post |
| `PATCH` | `/api/gbp/posts/[id]` | Update specific fields |
| `DELETE` | `/api/gbp/posts/[id]` | Delete post |
| `PATCH` | `/api/gbp/posts/[id]/status` | Change status: draft / approved / published |

**GBP post payload:**

```json
{
  "community_id": "foxchase",
  "blog_post_id": "a1b2c3d4-...",
  "post_type": "update",
  "body_text": "New on the blog: everything pet owners ask before touring Foxchase...",
  "cta_type": "learn_more",
  "cta_url": "https://foxchaseofalexandriaapts.com/blog/slug",
  "image_url": "https://cdn.domain.com/blog/featured.webp",
  "scheduled_at": "2026-09-08T09:00:00-04:00",
  "status": "draft"
}
```

---

## 7. GBP Reviews + Replies

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `GET` | `/api/gbp/reviews?community_id=foxchase` | List all reviews |
| `GET` | `/api/gbp/reviews?community_id=foxchase&reply_status=pending` | List reviews needing replies |
| `GET` | `/api/gbp/reviews/[id]` | Get single review with reply draft |
| `POST` | `/api/gbp/reviews/[id]/reply` | Create/push a reply draft |
| `PUT` | `/api/gbp/reviews/[id]/reply` | Update reply draft |
| `DELETE` | `/api/gbp/reviews/[id]/reply` | Delete reply draft |
| `PATCH` | `/api/gbp/reviews/[id]/reply/status` | Change reply status: pending / approved / published |

**Reply payload:**

```json
{
  "reply_text": "Thanks, Jenna! Same-day fixes are the goal — we'll pass this along to the maintenance team.",
  "status": "pending"
}
```

---

## 8. GBP Q&A

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `POST` | `/api/gbp/qna` | Create a Q&A suggestion |
| `POST` | `/api/gbp/qna/batch` | Create multiple Q&As at once |
| `GET` | `/api/gbp/qna?community_id=foxchase` | List Q&As |
| `GET` | `/api/gbp/qna/[id]` | Get single Q&A |
| `PUT` | `/api/gbp/qna/[id]` | Update Q&A |
| `DELETE` | `/api/gbp/qna/[id]` | Delete Q&A |
| `PATCH` | `/api/gbp/qna/[id]/status` | Change status: suggested / approved / published |

**Q&A payload:**

```json
{
  "community_id": "foxchase",
  "question": "Is parking included in rent?",
  "answer": "Covered parking is $75/mo; one surface spot is included with every lease (as of Q3 2026).",
  "source": "chat_data",
  "status": "suggested"
}
```

---

## 9. Dashboard Stats (Read Only)

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `GET` | `/api/stats/[community_id]` | Get all stats for a community |
| `GET` | `/api/stats/[community_id]/blog` | Blog stats: articles live, views, rankings |
| `GET` | `/api/stats/[community_id]/social` | Social stats: posts published, engagement |
| `GET` | `/api/stats/[community_id]/gbp` | GBP stats: rating, views, calls, reviews |

---

## Total Count

| Channel | Endpoints |
|---------|-----------|
| Events Queue | 4 |
| Community Profiles | 5 |
| Content Briefs | 6 |
| Blog Posts | 8 |
| Social Posts | 8 |
| GBP Posts | 6 |
| GBP Reviews + Replies | 7 |
| GBP Q&A | 6 |
| Stats | 4 |
| **Total** | **54** |

---

## How We Use This From Claude Code

**Step 1: Check what needs to be done**
```
"Check pending events for all communities"
→ GET /api/events?status=pending
→ Shows: 2 briefs approved, 1 new review, 1 social regenerate request
```

**Step 2: Process each event**
```
"Process the approved brief for Foxchase"
→ GET /api/briefs/[id] (fetch the brief)
→ GET /api/profiles/foxchase (fetch community profile)
→ Run writing agent with brief + profile
→ POST /api/blog/posts (push finished article)
→ PATCH /api/events/[event_id] (mark event as processed)
```

**Step 3: Create social posts after article**
```
"Create social posts for the new Foxchase article"
→ GET /api/blog/posts/[id] (fetch the article)
→ Run social agent
→ POST /api/social/posts/batch (push 3 posts: IG feed, IG story, FB)
→ POST /api/gbp/posts (push GBP update)
```

**Step 4: Handle a review**
```
"Draft reply for the new Foxchase review"
→ GET /api/gbp/reviews/[id] (fetch the review)
→ GET /api/profiles/foxchase (fetch profile for tone/context)
→ Run reply agent
→ POST /api/gbp/reviews/[id]/reply (push draft)
→ PATCH /api/events/[event_id] (mark processed)
```

**Step 5: Update something**
```
"Update the Foxchase pet article — pet deposit changed to $300"
→ GET /api/blog/posts/[id] (fetch current article)
→ Run update agent with the change note
→ PUT /api/blog/posts/[id] (push updated article)
```

**Step 6: Delete something**
```
"Delete the scheduled Facebook post for Foxchase"
→ DELETE /api/social/posts/[id]
```

**Step 7: Check stats**
```
"Show me Foxchase performance"
→ GET /api/stats/foxchase
→ Shows: 3 articles live, 412 visits, 7 AI citations, 4.3 rating on Google
```
