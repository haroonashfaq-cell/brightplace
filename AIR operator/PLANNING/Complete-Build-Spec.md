# AIR Operator: Complete Build Specification

**Version:** 2.0
**Date:** September 2026
**For:** Development Team
**From:** brightplace Content/SEO Team

---

# PART 1: WHAT WE'RE BUILDING

5 community websites on brightplace subdomains. Each has a blog with CMS. We control everything from Claude Code CLI via an MCP server the dev team builds.

## Site Structure

```
foxchase.brightplace.ai
foxchase.brightplace.ai/blog
foxchase.brightplace.ai/blog/how-to-rent-an-apartment-at-foxchase

citi-lakes.brightplace.ai
citi-lakes.brightplace.ai/blog
citi-lakes.brightplace.ai/blog/[slug]

verdant-peachtree-creek.brightplace.ai
verdant-peachtree-creek.brightplace.ai/blog
verdant-peachtree-creek.brightplace.ai/blog/[slug]

villages-at-raleigh-beach.brightplace.ai
villages-at-raleigh-beach.brightplace.ai/blog
villages-at-raleigh-beach.brightplace.ai/blog/[slug]

sorrel.brightplace.ai
sorrel.brightplace.ai/blog
sorrel.brightplace.ai/blog/[slug]
```

## How We Connect

The dev team builds an **MCP server** (Model Context Protocol). We add it to our Claude Code CLI config. Our agents call MCP tools directly — no manual API calls, no curl commands, no middleware.

```
Claude Code CLI
  ↕ MCP connection
Dev Team's MCP Server
  ↕ talks to
CMS Database + Site Rendering + Social Publishing + GBP Integration
```

**From our CLI we can:**
- Push a complete blog post (markdown, HTML, image, schemas, meta tags) → it appears on the site
- Update any page's SEO (title, description, schemas, canonical)
- Manage robots.txt, sitemap.xml, llms.txt
- Create/edit/delete social posts, GBP posts, review replies, Q&As
- Fetch pending events (approvals, new reviews, update requests)
- Mark events as processed
- Read stats and performance data
- Preview how a page renders before publishing
- Control blog page templates

---

# PART 2: RENDERING & SEO REQUIREMENTS

Non-negotiable rules. If these aren't followed, AI crawlers can't read our content.

## AI Crawlers Don't Execute JavaScript

| Crawler | Operator | Executes JS? |
|---------|----------|-------------|
| GPTBot | OpenAI (ChatGPT) | No |
| ClaudeBot | Anthropic (Claude) | No |
| PerplexityBot | Perplexity AI | No |
| Google-Extended | Google (AI Overviews) | No |
| Googlebot | Google (search) | Limited |
| Bingbot | Microsoft (Copilot) | Limited |

Every AI crawler fetches raw HTML. Content hidden behind JavaScript is invisible.

## Architecture

```
Framework:     Next.js 15+ with App Router
Language:      TypeScript
Rendering:     SSG for property pages / ISR for blog pages (revalidate: 60)
Deployment:    Vercel
```

## The Rule: Content in HTML, Motion in JS

- **Server Components (default):** All text, pricing, FAQs, blog content, meta tags, schemas — in raw HTML
- **Client Components (`'use client'`):** Only for animations, accordions, lightboxes, interactive widgets
- **Test:** `curl https://foxchase.brightplace.ai/blog/slug | grep "content"` — must show everything

## robots.txt (every site root)

```
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: AppleBot
Allow: /

Sitemap: https://[subdomain].brightplace.ai/sitemap.xml
```

## llms.txt (every site root)

```
# [Community Name] Apartments
> One-line description

## Blog
- [Title](/blog/slug): Summary
- [Title](/blog/slug): Summary

## Contact
Website, phone
```

## Headers (vercel.json)

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Robots-Tag", "value": "index, follow" },
        { "key": "X-Content-Type-Options", "value": "nosniff" }
      ]
    }
  ]
}
```

## Semantic HTML

```html
<html lang="en">
<head>
  <title>[seo_title] — different from H1, under 60 chars</title>
  <meta name="description" content="Under 155 chars">
  <link rel="canonical" href="https://foxchase.brightplace.ai/blog/[slug]">
  <meta property="og:title" content="...">
  <meta property="og:description" content="...">
  <meta property="og:image" content="...">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{ schema }</script>
</head>
<body>
  <header>...</header>
  <main>
    <article>
      <h1>Only ONE h1</h1>
      <section id="section-name"><h2>...</h2></section>
    </article>
  </main>
  <footer>...</footer>
</body>
</html>
```

**Rules:** One `<h1>`. `<title>` differs from H1. No heading skips. All images have width/height. External links: `target="_blank" rel="noopener"`. Internal links: no `target="_blank"`.

## Performance Targets

| Metric | Target |
|--------|--------|
| TTFB | Under 200ms |
| LCP | Under 2.5s |
| CLS | Under 0.1 |
| FID | Under 100ms |
| Page weight | Under 500KB |

## What NOT to Do

- No client-side rendering (content invisible to AI)
- No `useEffect` + `fetch` for content
- No hash routing (`/#/page`)
- No `noindex` on any page
- No blocking AI bots in robots.txt

---

# PART 3: THE MCP SERVER

The dev team builds an MCP server that we connect to from Claude Code. This MCP server is the single interface for everything — content management, SEO control, events, stats.

## MCP Connection Config (our side)

We add this to our Claude Code MCP config:

```json
{
  "mcpServers": {
    "air-operator": {
      "url": "https://mcp.brightplace.ai/air-operator",
      "auth": {
        "type": "bearer",
        "token": "API_KEY"
      }
    }
  }
}
```

## All MCP Tools the Dev Team Must Build

### SITE MANAGEMENT

```
site_list
  → Returns all 5 community sites with domain, status, config

site_get
  params: { community_id: "foxchase" }
  → Returns site config: domain, blog_url, status, created_at

site_update_config
  params: { community_id: "foxchase", config: { ... } }
  → Updates site-level config
```

### SEO CONTROL (per site)

```
seo_get_robots_txt
  params: { community_id: "foxchase" }
  → Returns current robots.txt content

seo_update_robots_txt
  params: { community_id: "foxchase", content: "..." }
  → Overwrites robots.txt

seo_get_sitemap
  params: { community_id: "foxchase" }
  → Returns current sitemap.xml entries

seo_add_sitemap_entry
  params: { community_id: "foxchase", url: "/blog/slug", lastmod: "2026-09-03", priority: 0.8 }
  → Adds URL to sitemap

seo_remove_sitemap_entry
  params: { community_id: "foxchase", url: "/blog/slug" }
  → Removes URL from sitemap

seo_get_llms_txt
  params: { community_id: "foxchase" }
  → Returns current llms.txt content

seo_update_llms_txt
  params: { community_id: "foxchase", content: "..." }
  → Overwrites llms.txt

seo_get_page_meta
  params: { community_id: "foxchase", path: "/blog/slug" }
  → Returns title, description, canonical, OG tags, schemas for a page

seo_update_page_meta
  params: { community_id: "foxchase", path: "/blog/slug", title: "...", description: "...", canonical: "..." }
  → Updates meta tags for a specific page

seo_validate_page
  params: { community_id: "foxchase", path: "/blog/slug" }
  → Checks: is content in HTML? schemas present? heading hierarchy correct? images have dimensions? Returns pass/fail report
```

### BLOG CMS

```
blog_create_post
  params: {
    community_id: "foxchase",
    title: "...",
    seo_title: "...",
    meta_description: "...",
    slug: "how-to-rent-an-apartment-at-foxchase",
    body_markdown: "# Article...",
    body_html: "<h1>Article...</h1>...",
    post_summary: "...",
    primary_keyword: "...",
    secondary_keywords: ["..."],
    author: "AIR Communities",
    date_published: "2026-09-03",
    date_modified: "2026-09-03",
    last_reviewed: "September 2026",
    featured_image_alt: "...",
    schema_faq: "{ JSON }",
    schema_article: "{ JSON }",
    schema_webpage: "{ JSON }",
    status: "draft"
  }
  + featured_image file (WebP, 1200x628)
  → Creates post, returns { id, slug, preview_url, featured_image_url }

blog_get_post
  params: { community_id: "foxchase", post_id: "uuid" }
  → Returns full post object

blog_get_post_by_slug
  params: { community_id: "foxchase", slug: "how-to-rent-an-apartment-at-foxchase" }
  → Returns full post object

blog_list_posts
  params: { community_id: "foxchase", status: "published", limit: 20, offset: 0 }
  → Returns paginated list

blog_update_post
  params: { post_id: "uuid", fields to update... }
  → Updates specific fields. Image optional.

blog_delete_post
  params: { post_id: "uuid" }
  → Archives (soft delete)

blog_change_status
  params: { post_id: "uuid", status: "published" }
  → Changes status: draft / published / archived
  → If publishing: triggers sitemap update, RSS update, creates article_published event

blog_upload_image
  params: { community_id: "foxchase", alt_text: "..." }
  + image file
  → Returns { image_url }

blog_preview_post
  params: { post_id: "uuid" }
  → Returns the rendered HTML exactly as it would appear on the live site (for QA before publishing)

blog_get_template
  params: { community_id: "foxchase" }
  → Returns the current blog page template (layout, styles, components)

blog_update_template
  params: { community_id: "foxchase", template: { ... } }
  → Updates blog page template (layout, header/footer config, typography, colors)
```

### CONTENT BRIEFS

```
brief_create
  params: {
    community_id: "foxchase",
    keyword: "pet friendly apartments alexandria va",
    volume: 590,
    difficulty: 21,
    tier: "Long Tail",
    seo_title: "...",
    h1: "...",
    word_count_target: 2000,
    faq_count: 10,
    publish_date: "2026-09-08",
    outline: [ { h2: "...", description: "..." } ],
    internal_links: ["pet policy", "floor plans"]
  }
  → Creates brief, returns { id, status: "pending" }

brief_list
  params: { community_id: "foxchase", status: "pending" }
  → Returns list of briefs

brief_get
  params: { brief_id: "uuid" }
  → Returns full brief with user_note if any

brief_update
  params: { brief_id: "uuid", fields to update... }
  → Updates brief

brief_delete
  params: { brief_id: "uuid" }
  → Deletes brief
```

### SOCIAL POSTS

```
social_create_post
  params: {
    community_id: "foxchase",
    blog_post_id: "uuid",
    platform: "instagram",
    post_type: "feed",
    caption: "...",
    hashtags: "#CherryCreek #DenverApartments",
    image_url: "..." or image_prompt: "...",
    link_url: "https://foxchase.brightplace.ai/blog/slug",
    cta_text: "Read the full guide",
    scheduled_at: "2026-09-09T11:00:00-06:00"
  }
  → Creates social post draft

social_create_batch
  params: { posts: [ ...array of post objects ] }
  → Creates multiple posts at once (IG feed + IG story + FB)

social_list
  params: { community_id: "foxchase", status: "draft", platform: "instagram" }
  → Returns filtered list

social_get
  params: { social_post_id: "uuid" }
  → Returns full post

social_update
  params: { social_post_id: "uuid", caption: "...", scheduled_at: "..." }
  → Updates post

social_delete
  params: { social_post_id: "uuid" }
  → Deletes post

social_change_status
  params: { social_post_id: "uuid", status: "approved" }
  → Changes status: draft / approved / scheduled / published / failed
```

### GBP POSTS

```
gbp_create_post
  params: {
    community_id: "foxchase",
    blog_post_id: "uuid",
    post_type: "update",
    body_text: "...",
    cta_type: "learn_more",
    cta_url: "...",
    image_url: "...",
    scheduled_at: "..."
  }
  → Creates GBP post draft

gbp_list_posts
  params: { community_id: "foxchase" }

gbp_get_post
  params: { gbp_post_id: "uuid" }

gbp_update_post
  params: { gbp_post_id: "uuid", fields... }

gbp_delete_post
  params: { gbp_post_id: "uuid" }

gbp_change_post_status
  params: { gbp_post_id: "uuid", status: "approved" }
  → Approved triggers publish to Google
```

### GBP REVIEWS + REPLIES

```
review_list
  params: { community_id: "foxchase", reply_status: "pending" }
  → Returns reviews (filterable by reply status)

review_get
  params: { review_id: "uuid" }
  → Returns review with reply draft

review_create_reply
  params: { review_id: "uuid", reply_text: "Thanks, Jenna!..." }
  → Pushes reply draft

review_update_reply
  params: { review_id: "uuid", reply_text: "..." }
  → Updates reply draft

review_delete_reply
  params: { review_id: "uuid" }
  → Deletes reply draft

review_approve_reply
  params: { review_id: "uuid" }
  → Approves and publishes reply to Google
```

### GBP Q&A

```
qna_create
  params: { community_id: "foxchase", question: "...", answer: "...", source: "chat_data" }

qna_create_batch
  params: { qnas: [ ...array ] }

qna_list
  params: { community_id: "foxchase", status: "suggested" }

qna_get
  params: { qna_id: "uuid" }

qna_update
  params: { qna_id: "uuid", answer: "..." }

qna_delete
  params: { qna_id: "uuid" }

qna_change_status
  params: { qna_id: "uuid", status: "approved" }
  → Approved triggers publish to Google
```

### COMMUNITY PROFILES

```
profile_create
  params: {
    community_id: "foxchase",
    positioning: "88-acre wooded community in Seminary Hill...",
    differentiators: ["4 pools", "Townhomes", "Wi-Fi included"],
    neighborhood_anchors: [ { name: "Old Town Alexandria", time: "10 min" } ],
    things_we_never_say: "Luxury without backing. Family-friendly (Fair Housing)."
  }

profile_get
  params: { community_id: "foxchase" }

profile_update
  params: { community_id: "foxchase", fields to update... }

profile_list
  → Returns all community profiles
```

### EVENTS (Two-Way Communication)

```
events_list_pending
  params: { community_id: "foxchase" } (optional — omit for all communities)
  → Returns all pending events

events_list_all
  params: { community_id: "foxchase", status: "pending", limit: 50 }
  → Returns filtered events

events_get
  params: { event_id: "uuid" }
  → Returns single event with full data

events_mark_processed
  params: { event_id: "uuid" }
  → Marks event as processed (won't show in pending list again)

events_mark_failed
  params: { event_id: "uuid", error: "reason" }
  → Marks event as failed with error message
```

**Events the system creates automatically:**

| Event Type | Trigger | Data Payload |
|---|---|---|
| `brief_approved` | Dashboard user approves brief | brief_id, keyword, user_note |
| `article_update_requested` | Dashboard user requests refresh | post_id, user_note |
| `article_published` | Article goes live | post_id, slug, community_id |
| `social_regenerate` | User edits + clicks regenerate | social_post_id, edited_caption, user_note |
| `content_rejected` | User rejects content | content_type, content_id, rejection_reason |
| `new_review` | Review monitor finds new review | community_id, reviewer_name, rating, review_text |
| `review_reply_rejected` | User rejects reply | review_id, rejection_reason |
| `profile_updated` | User updates profile | community_id, changed_fields |
| `qna_request` | Monthly trigger | community_id |
| `brief_request` | Bi-weekly trigger | community_id |

### STATS

```
stats_get
  params: { community_id: "foxchase" }
  → Returns: articles_live, briefs_pending, organic_visits_30d, ai_citations

stats_blog
  params: { community_id: "foxchase" }
  → Returns: per-article views, rankings, AI citations

stats_social
  params: { community_id: "foxchase" }
  → Returns: posts published, likes, comments, reach per post

stats_gbp
  params: { community_id: "foxchase" }
  → Returns: rating, review_count, profile_views, direction_requests, calls, last_photo_upload
```

---

## MCP Tools Summary

| Category | Tools | Count |
|----------|-------|-------|
| Site Management | site_list, site_get, site_update_config | 3 |
| SEO Control | robots.txt, sitemap, llms.txt, page meta, validate | 11 |
| Blog CMS | create, get, list, update, delete, status, image, preview, template | 11 |
| Content Briefs | create, list, get, update, delete | 5 |
| Social Posts | create, batch, list, get, update, delete, status | 7 |
| GBP Posts | create, list, get, update, delete, status | 6 |
| GBP Reviews | list, get, create_reply, update_reply, delete_reply, approve_reply | 6 |
| GBP Q&A | create, batch, list, get, update, delete, status | 7 |
| Community Profiles | create, get, update, list | 4 |
| Events | list_pending, list_all, get, mark_processed, mark_failed | 5 |
| Stats | get, blog, social, gbp | 4 |
| **Total** | | **69 tools** |

---

# PART 4: DATABASE

## Tables

### blog_posts
```sql
create table blog_posts (
  id uuid primary key default gen_random_uuid(),
  community_id varchar(64) not null,
  title text not null,
  seo_title varchar(60) not null,
  meta_description varchar(160) not null,
  slug varchar(128) not null,
  body_markdown text not null,
  body_html text not null,
  post_summary varchar(300) not null,
  primary_keyword varchar(128),
  secondary_keywords jsonb default '[]',
  author varchar(128) default 'AIR Communities',
  date_published date not null,
  date_modified date not null,
  last_reviewed varchar(32),
  featured_image_url text,
  featured_image_alt varchar(256),
  schema_faq text,
  schema_article text,
  schema_webpage text,
  status varchar(16) default 'draft',
  word_count integer,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  unique(community_id, slug)
);
```

### content_briefs
```sql
create table content_briefs (
  id uuid primary key default gen_random_uuid(),
  community_id varchar(64) not null,
  keyword text not null,
  volume integer,
  difficulty integer,
  tier varchar(32),
  seo_title varchar(60),
  h1 text,
  word_count_target integer default 2000,
  faq_count integer default 10,
  publish_date date,
  outline jsonb default '[]',
  internal_links jsonb default '[]',
  user_note text,
  status varchar(16) default 'pending',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
```

### social_posts
```sql
create table social_posts (
  id uuid primary key default gen_random_uuid(),
  community_id varchar(64) not null,
  blog_post_id uuid references blog_posts(id),
  platform varchar(16) not null,
  post_type varchar(16) not null,
  caption text not null,
  hashtags text,
  image_url text,
  image_alt text,
  image_prompt text,
  link_url text,
  cta_text text,
  scheduled_at timestamptz,
  published_at timestamptz,
  external_post_id text,
  metrics jsonb default '{}',
  status varchar(16) default 'draft',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
```

### gbp_posts
```sql
create table gbp_posts (
  id uuid primary key default gen_random_uuid(),
  community_id varchar(64) not null,
  blog_post_id uuid references blog_posts(id),
  post_type varchar(16) default 'update',
  body_text text not null,
  cta_type varchar(16),
  cta_url text,
  image_url text,
  scheduled_at timestamptz,
  published_at timestamptz,
  status varchar(16) default 'draft',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
```

### gbp_reviews
```sql
create table gbp_reviews (
  id uuid primary key default gen_random_uuid(),
  community_id varchar(64) not null,
  google_review_id text,
  reviewer_name text,
  rating integer,
  review_text text,
  review_date timestamptz,
  reply_text text,
  reply_status varchar(16) default 'pending',
  reply_published_at timestamptz,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
```

### gbp_qna
```sql
create table gbp_qna (
  id uuid primary key default gen_random_uuid(),
  community_id varchar(64) not null,
  question text not null,
  answer text not null,
  source varchar(32),
  google_qna_id text,
  status varchar(16) default 'suggested',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
```

### community_profiles
```sql
create table community_profiles (
  id uuid primary key default gen_random_uuid(),
  community_id varchar(64) not null unique,
  positioning text,
  differentiators jsonb default '[]',
  neighborhood_anchors jsonb default '[]',
  things_we_never_say text,
  tour_questions text,
  resident_feedback text,
  profile_completeness integer default 0,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
```

### events
```sql
create table events (
  id uuid primary key default gen_random_uuid(),
  event_type varchar(32) not null,
  community_id varchar(64) not null,
  status varchar(16) default 'pending',
  data jsonb default '{}',
  error text,
  processed_at timestamptz,
  created_at timestamptz default now()
);
create index idx_events_status on events(status);
create index idx_events_community on events(community_id, status);
```

### site_config
```sql
create table site_config (
  id uuid primary key default gen_random_uuid(),
  community_id varchar(64) not null unique,
  domain text not null,
  robots_txt text,
  llms_txt text,
  blog_template jsonb default '{}',
  site_status varchar(16) default 'active',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
```

### lead_attribution
```sql
create table lead_attribution (
  id uuid primary key default gen_random_uuid(),
  community_id varchar(64) not null,
  lead_type varchar(32) not null,
  utm_source varchar(64),
  utm_medium varchar(64),
  utm_campaign varchar(256),
  utm_content varchar(64),
  referrer_url text,
  landing_page text,
  is_ai_referral boolean default false,
  ai_source varchar(32),
  session_id text,
  created_at timestamptz default now()
);
create index idx_leads_community on lead_attribution(community_id);
create index idx_leads_type on lead_attribution(community_id, lead_type);
create index idx_leads_source on lead_attribution(utm_source);
```

**Total: 10 tables**

---

# PART 5: BLOG PAGE RENDERING

## How It Works

Our agents produce a complete article: markdown, HTML, image, schemas, meta tags. We push all of it via `blog_create_post`. The dev team's system:

1. Stores everything in the database
2. Converts markdown to HTML server-side (if we didn't send body_html)
3. Renders the blog page using the blog template
4. Injects schemas into `<head>`
5. Sets all meta tags
6. Serves via ISR (static + 60s revalidation)

## Blog Page Template

The dev team creates a blog page template. We can view and modify it via `blog_get_template` and `blog_update_template`. The template defines:

- Page layout (header, article body, sidebar, footer)
- Typography (fonts, sizes, line heights)
- Color scheme
- Image display (featured image placement, sizing)
- Article meta bar (author, date, reading time)
- CTA sections
- Related posts section
- Social sharing buttons

Our content fills this template. The template is consistent across all posts for a community but can differ between communities.

## HTML Head (auto-generated from our payload)

```html
<head>
  <title>[seo_title]</title>
  <meta name="description" content="[meta_description]">
  <link rel="canonical" href="https://foxchase.brightplace.ai/blog/[slug]">
  <meta property="og:title" content="[seo_title]">
  <meta property="og:description" content="[meta_description]">
  <meta property="og:image" content="[featured_image_url]">
  <meta property="og:url" content="https://foxchase.brightplace.ai/blog/[slug]">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">[schema_faq]</script>
  <script type="application/ld+json">[schema_article]</script>
  <script type="application/ld+json">[schema_webpage]</script>
</head>
```

## Page Body

```html
<article>
  <img src="[featured_image_url]" alt="[featured_image_alt]" width="1200" height="628" loading="eager">
  <div class="article-meta">
    <span>By [author]</span>
    <span>Published [date_published]</span>
    <span>Last reviewed [last_reviewed]</span>
    <span>[word_count / 238] min read</span>
  </div>
  <div class="article-body">[body_html]</div>
</article>
```

## Auto-Updates on Publish

When `blog_change_status` sets a post to `published`:
- Sitemap auto-adds the URL
- RSS feed auto-includes the post
- llms.txt should be updated (we handle this via `seo_update_llms_txt`)
- `article_published` event created in events table

## Blog Index Page

`https://foxchase.brightplace.ai/blog`
- Grid of published posts, newest first
- Card: featured image, title, summary, date, reading time
- Pagination: 12 per page
- SEO: unique title + description + canonical

## Markdown → HTML

Server-side conversion using marked/remark/markdown-it. External links get `target="_blank" rel="noopener"`. Internal links: no `target="_blank"`.

## Images

- WebP format, 1200x628
- CDN with `Cache-Control: public, max-age=31536000, immutable`
- OG image URL must be publicly accessible

## Caching

- Blog pages: ISR, 60-second revalidation
- Images: CDN immutable, 1 year
- API/MCP: no cache

---

# PART 6: DASHBOARD UI

The dev team also builds a dashboard for community managers to review and approve content.

## Pages

| Page | What It Shows |
|------|--------------|
| Login | Email/password, role-based access |
| Community Switcher | Switch between 5 communities |
| SEO/AEO Tab | Stats, brief cards (approve/skip), article pipeline, calendar |
| Social Tab | Post preview cards (approve/edit/delete), scheduling |
| GBP Tab | Profile health, GBP drafts, review replies, Q&A suggestions |
| Community Profile | Editable profile, completeness meter |
| Brief Detail Modal | Full brief, H2 outline, user note field, approve button |
| Article Preview | Rendered view before publish |
| Social Post Editor | Edit caption, change time, preview per platform |

## Dashboard Actions That Create Events

Every action a user takes on the dashboard creates an event in the events table. We poll events via `events_list_pending` from Claude Code to know what to do.

---

# PART 7: HOW WE WORK FROM CLAUDE CODE

## Example: Full Blog Post Workflow

```
Step 1: Check what's pending
  → events_list_pending()
  → "brief_approved for foxchase — keyword: pet friendly apartments"

Step 2: Get the brief + profile
  → brief_get(brief_id)
  → profile_get("foxchase")

Step 3: Run writing agent (our agents, locally)
  → Produces: markdown, HTML, image, schemas

Step 4: Push to site
  → blog_create_post({ community_id: "foxchase", title: "...", body_markdown: "...", body_html: "...", ... })
  → Returns: { id, slug, preview_url }

Step 5: Preview before publish
  → blog_preview_post(post_id)
  → Review rendered page

Step 6: Publish
  → blog_change_status(post_id, "published")
  → Site is live, sitemap updated, article_published event created

Step 7: Create social posts
  → social_create_batch([ ig_feed, ig_story, fb_post ])

Step 8: Create GBP post
  → gbp_create_post({ ... })

Step 9: Update llms.txt
  → seo_update_llms_txt("foxchase", updated_content)

Step 10: Mark original event as processed
  → events_mark_processed(event_id)
```

## Example: Handle New Review

```
  → events_list_pending()
  → "new_review for foxchase — Jenna M., 5 stars"

  → review_get(review_id)
  → profile_get("foxchase")
  → Run reply agent locally
  → review_create_reply(review_id, "Thanks, Jenna!...")
  → events_mark_processed(event_id)
```

## Example: Update Article SEO

```
  → seo_get_page_meta("foxchase", "/blog/slug")
  → See current title, description, schemas
  → seo_update_page_meta("foxchase", "/blog/slug", { title: "New Title", description: "New desc" })
```

## Example: Validate a Page

```
  → seo_validate_page("foxchase", "/blog/slug")
  → Returns: { content_in_html: true, schemas_present: 3, h1_count: 1, heading_hierarchy: "valid", images_have_dimensions: true, result: "PASS" }
```

---

# PART 8: DEPLOYMENT PLAN

### Phase 1: Foxchase Blog
- Build site at foxchase.brightplace.ai
- Build blog CMS (database + rendering)
- Build MCP server with blog tools + events tools
- We test: push article via MCP, verify rendering + SEO
- Go live

### Phase 2: SEO Control + Briefs
- Add SEO tools to MCP (robots.txt, sitemap, llms.txt, page meta, validate)
- Add brief tools to MCP
- Add community profile tools
- We test: full brief → article → publish → SEO verify loop

### Phase 3: Dashboard
- Build dashboard UI (SEO tab, brief approval, article pipeline)
- Dashboard actions create events
- We test: approve brief on dashboard → event appears → we process via CLI

### Phase 4: Social Media
- Add social post tools to MCP
- Build social publishing integration
- Add dashboard social tab
- We test: push social posts, approve, verify publishing

### Phase 5: Google Business Profile
- Add GBP tools to MCP (posts, reviews, Q&A)
- Build GBP integrations
- Add dashboard GBP tab
- We test: push GBP content, review replies, Q&As

### Phase 6: Roll Out to All 5 Communities
- Deploy same system to remaining 4 subdomains
- citi-lakes.brightplace.ai
- verdant-peachtree-creek.brightplace.ai
- villages-at-raleigh-beach.brightplace.ai
- sorrel.brightplace.ai

### Phase 7: Scale
- Scheduled jobs (auto brief generation, review monitoring)
- Multi-community batch operations from CLI
- Performance optimization for 100+ communities

---

# PART 9: TESTING CHECKLIST

### Rendering
- [ ] `curl` shows all content (zero JS dependency)
- [ ] One `<h1>`, `<title>` differs from H1
- [ ] All 3 JSON-LD schemas in `<head>`
- [ ] Semantic HTML structure
- [ ] OG + Twitter Card tags correct
- [ ] Canonical URL set

### AI Crawler Access
- [ ] robots.txt allows GPTBot, ClaudeBot, PerplexityBot
- [ ] llms.txt exists
- [ ] X-Robots-Tag header present

### Performance
- [ ] Page under 500KB
- [ ] Core Web Vitals green
- [ ] TTFB under 200ms

### MCP Server
- [ ] All 69 tools callable from Claude Code
- [ ] Auth works (valid key accepted, invalid rejected)
- [ ] Create/read/update/delete works for every content type
- [ ] Events created on dashboard actions
- [ ] Events created on scheduled triggers
- [ ] Mark processed works (events don't reappear)
- [ ] Batch operations work (social_create_batch, qna_create_batch)
- [ ] seo_validate_page returns accurate results
- [ ] blog_preview_post returns rendered HTML
- [ ] Sitemap auto-updates on publish
- [ ] RSS auto-updates on publish

### Dashboard
- [ ] Community switcher works
- [ ] Approval flows create events
- [ ] Edit flows work for all content types
- [ ] Stats display correctly
- [ ] Lead counts display at top of dashboard
- [ ] Source attribution breakdown works
- [ ] Top performing content by conversions shows correctly

### UTM Tracking & Attribution
- [ ] UTM params captured from URL on page load
- [ ] UTM params persist across session (cookie/session storage)
- [ ] Tour booking captures UTM attribution
- [ ] Call click captures UTM attribution
- [ ] Directions click captures UTM attribution
- [ ] AI referral detection works (ChatGPT, Perplexity, Google AI)
- [ ] `lead_attribution` table populated on every conversion event
- [ ] `stats_leads` MCP tool returns correct data
- [ ] `stats_attribution` MCP tool returns correct data
- [ ] `stats_ai_citations` MCP tool returns correct data
- [ ] Amplitude events firing correctly for all conversion events

---

# PART 10: UTM TRACKING & LEAD ATTRIBUTION

This is the metric that matters to operators. Every tour booked, call made, or direction requested must be attributed back to the content that drove it.

## UTM Structure

Every CTA link in our content carries UTM parameters:

| Parameter | Values | Purpose |
|---|---|---|
| `utm_source` | `blog`, `social_ig`, `social_fb`, `gbp`, `agent` | Which channel |
| `utm_medium` | `cta`, `inline_link`, `post`, `story`, `reply` | How they clicked |
| `utm_campaign` | `[article-slug]` or `[keyword]` | Which content piece |
| `utm_content` | `top_cta`, `mid_cta`, `end_cta`, `faq_link`, `link_in_bio` | Which CTA position |

**Example CTA URL from a blog post:**
```
https://foxchase.staging.brightplace.ai/tour?utm_source=blog&utm_medium=cta&utm_campaign=pet-friendly-apartments-foxchase&utm_content=mid_cta
```

**Example from Instagram post:**
```
https://foxchase.staging.brightplace.ai/tour?utm_source=social_ig&utm_medium=post&utm_campaign=pet-friendly-apartments-foxchase&utm_content=link_in_bio
```

## What Gets Tracked as a Lead

| Lead Type | Trigger | How to Capture |
|---|---|---|
| `tour_booked` | User completes tour booking form | Capture UTM params from URL on form submit |
| `tour_requested` | User starts tour booking (even if not completed) | Capture on form open |
| `call_made` | User clicks phone number | Click event + UTM from current session |
| `directions_requested` | User clicks directions/maps link | Click event + UTM from current session |
| `application_started` | User begins rental application | Capture UTM from session |
| `contact_form_submitted` | User submits contact form | Capture UTM from URL |
| `agent_tour_conversion` | AI chat leads to tour booking | UTM source = `agent` |

## UTM Capture Logic

When a visitor lands on any page with UTM params:
1. Store UTM params in session/cookie (persists across page navigation)
2. When a conversion event fires (tour booked, call made, etc.), attach the stored UTM params
3. Write a row to `lead_attribution` table
4. Fire Amplitude event with UTM properties

**Important:** UTM params from the FIRST touch should persist for the whole session. If someone lands on `/blog/pet-friendly?utm_source=blog` then navigates to `/tour`, the tour booking still attributes to the blog post.

## AI Referral Detection

Detect when visitors come from AI search engines. Check `document.referrer` or `Referer` header:

| Referrer Contains | AI Source |
|---|---|
| `chat.openai.com` | `chatgpt` |
| `chatgpt.com` | `chatgpt` |
| `perplexity.ai` | `perplexity` |
| `google.com` (with AI Overview click patterns) | `google_ai` |
| `bing.com/chat` | `copilot` |
| `claude.ai` | `claude` |

When detected, set `is_ai_referral = true` and `ai_source` in the lead attribution record. This proves our content is being surfaced by AI search engines.

## Amplitude Events to Track

### Site Engagement
| Event | Properties |
|---|---|
| `page_viewed` | community_id, path, referrer, utm_source, utm_medium, utm_campaign, is_ai_referral |
| `blog_post_viewed` | community_id, slug, title, primary_keyword |
| `blog_scroll_depth` | community_id, slug, depth (25/50/75/100) |
| `blog_time_on_page` | community_id, slug, seconds |
| `cta_clicked` | community_id, cta_type, cta_position, destination_url, utm_params |
| `internal_link_clicked` | community_id, from_page, to_page |
| `external_link_clicked` | community_id, from_page, destination_url |

### Conversion Events (critical — these prove ROI)
| Event | Properties |
|---|---|
| `tour_requested` | community_id, utm_source, utm_campaign, is_ai_referral |
| `tour_booked` | community_id, utm_source, utm_campaign, is_ai_referral, tour_date |
| `call_initiated` | community_id, utm_source, utm_campaign |
| `directions_requested` | community_id, utm_source, utm_campaign |
| `application_started` | community_id, utm_source, utm_campaign |
| `contact_form_submitted` | community_id, utm_source, utm_campaign |

### AI Agent Events
| Event | Properties |
|---|---|
| `agent_chat_opened` | community_id |
| `agent_message_sent` | community_id, message_topic (if classifiable) |
| `agent_tour_conversion` | community_id (chat led to tour booking) |
| `agent_handoff_to_human` | community_id, reason |

### Floor Plans & Listings
| Event | Properties |
|---|---|
| `floor_plan_viewed` | community_id, plan_name, beds, baths, price |
| `listing_viewed` | community_id, listing_id |
| `pricing_calculator_used` | community_id |
| `filter_applied` | community_id, filter_type, filter_value |

### Social & GBP Attribution
| Event | Properties |
|---|---|
| `social_referral_landed` | community_id, platform (instagram/facebook), post_id |
| `gbp_referral_landed` | community_id, post_id |
| `ai_referral_landed` | community_id, ai_source (chatgpt/perplexity/google_ai) |

## MCP Tools for Tracking

Add these to the MCP server:

```
stats_leads
  params: { community_id: "foxchase", period: "30d" }
  → Returns: {
      tours_booked: 12,
      tours_by_source: { blog: 8, social_ig: 2, social_fb: 1, gbp: 1 },
      calls_made: 31,
      directions_requested: 8,
      applications_started: 4
    }

stats_attribution
  params: { community_id: "foxchase", period: "30d" }
  → Returns: {
      top_content_by_tours: [
        { title: "Pet-Friendly Living at Foxchase", slug: "...", tours: 4 },
        { title: "What Renters Should Know", slug: "...", tours: 3 }
      ],
      top_cta_positions: { mid_cta: 5, end_cta: 4, top_cta: 3 },
      source_breakdown: { blog: 67%, social: 25%, gbp: 8% }
    }

stats_ai_citations
  params: { community_id: "foxchase", period: "30d" }
  → Returns: {
      total_ai_referrals: 23,
      by_source: { chatgpt: 12, perplexity: 8, google_ai: 3 },
      top_landing_pages: [
        { path: "/blog/pet-friendly-apartments", visits: 9 },
        { path: "/blog/what-renters-should-know", visits: 7 }
      ]
    }

stats_traffic
  params: { community_id: "foxchase", period: "30d" }
  → Returns: {
      total_visits: 847,
      by_source: { organic: 412, ai_referral: 23, social: 156, direct: 189, other: 67 },
      month_over_month_growth: "+38%"
    }
```

**Updated MCP tools total: 69 + 4 = 73 tools**

## Operator Dashboard — What They See

The dashboard is ordered by what operators care about MOST:

### Top Section: Leads (biggest numbers, most prominent)
```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│    12    │  │     4    │  │    31    │  │     8    │
│  Tours   │  │  Leases  │  │  Calls   │  │ Direc-   │
│  Booked  │  │ Started  │  │   Made   │  │ tions    │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
```

### Middle Section: Where Leads Came From
```
Blog articles  ████████████████░░  8 tours
Social posts   ████████░░░░░░░░░  3 tours
GBP updates    ██░░░░░░░░░░░░░░  1 tour
AI agent chat  ████░░░░░░░░░░░░  2 tours
```

### Middle Section: Top Performing Content
```
1. "Pet-Friendly Living at Foxchase" → 4 tours booked
2. "What Renters Should Know" → 3 tours booked
3. IG post: dog run morning → 2 tours booked
```

### Bottom Section: Visibility (supporting metrics)
```
847 visits · +38% MoM · 5 AI citations · 3 articles live · 12 social posts
```

---

# PART 11: QUESTIONS FOR DEV TEAM

1. **Database:** Supabase, Neon, or Vercel Postgres?
2. **Image storage:** Vercel Blob, Cloudflare R2, or S3?
3. **MCP hosting:** Same Vercel project as the sites, or separate?
4. **Social integration:** Which approach for IG/FB publishing?
5. **GBP access:** OAuth access to Google Business Profile for all 5?
6. **Staging:** Can we get staging MCP endpoint to test before live?
7. **Timeline:** When can Foxchase MCP + blog be ready for testing?

---

*Build the MCP server to this spec. Our agents connect from Claude Code CLI and handle all content creation. The MCP is the single interface between our content pipeline and your sites. Everything flows through it.*
