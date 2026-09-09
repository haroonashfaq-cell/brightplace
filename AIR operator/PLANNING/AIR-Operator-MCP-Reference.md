# AIR Operator — Consolidated MCP & System Reference

Version: 1.0 (consolidates AIR-Operator-Strategy-and-Alignment.md v1, Complete-Build-Spec.md v3.1, rendering-requirements.md, Developer CMS Requirement Doc.md [superseded parts], AIR-Operator-Dashboard-Design-Reference.html)
Audience: Claude Code agent sessions operating this system. Optimized for retrieval/ingestion, not human narrative.
Tags used below: `[EXISTING]` = already in Complete-Build-Spec v3.1. `[NEW]` = added in this pass, not yet built, low-ambiguity extension of existing pattern. `[OPEN]` = genuinely undecided, needs a product/infra decision before spec'ing further — do not build against this without confirming.

---

## 0. System Identity

**What this is:** content + visibility system for 5 AIR Communities apartment properties. brightplace's AI agents (run from Claude Code CLI) create all content and control site/dashboard data via one MCP server. Dev team builds the MCP server, CMS database, site rendering, and dashboard UI. Community managers approve/edit content in the dashboard.

**Canonical `community_id` values** — use exactly these strings everywhere, hyphenated:

| community_id | Community | Subdomain | Location |
|---|---|---|---|
| `foxchase` | Foxchase | foxchase.brightplace.ai | Alexandria, VA |
| `citi-lakes` | Citi Lakes | citi-lakes.brightplace.ai | Orlando, FL |
| `sorrel` | Sorrel / LUX at Sorrel | sorrel.brightplace.ai | Jacksonville, FL |
| `verdant-peachtree-creek` | Verdant Peachtree Creek | verdant-peachtree-creek.brightplace.ai | Atlanta, GA |
| `villages-at-raleigh-beach` | Villages at Raleigh Beach | villages-at-raleigh-beach.brightplace.ai | Raleigh, NC |

Do NOT use unhyphenated forms (`citilakes`) or the legacy live domains (`citilakesapartments.com` etc.) — those appear in the superseded `Developer CMS Requirement Doc.md` only.

**Responsibility split:**

| brightplace agents (via MCP) | Dev team |
|---|---|
| Keyword research, content strategy, briefs | MCP server implementation (§2 below) |
| Writing articles, social captions, GBP posts/replies/Q&A | CMS database (§3) |
| QA / Fair Housing compliance | Rendering — blog + property pages (§1, §4, §5) |
| Featured images + all JSON-LD schemas | Image storage/CDN, markdown→HTML |
| Publish/unpublish decisions (status via MCP) | Sitemap, RSS, robots.txt/llms.txt serving |
| GBP suggestion-check logic, portfolio insight generation | Dashboard UI shell, auth/roles, OAuth flows, token encryption |
| Site theme + non-blog page copy (via MCP, see §2.9) | SSL, caching, perf, infra |

**Reference implementation:** `OPERATOR-PAGES/` in this project already implements this rendering pattern for 2 working operators. Start there, don't rebuild from scratch.

**Scale plan:** 5 communities now (manual CLI trigger, poll-based) → 20 in 6 months (light automation) → 50-100 in 12 months (serverless webhook, zero-human-trigger). The events table (§2.8) is designed to support all three phases without a schema change — phase 1 polls it, phase 3 adds webhook firing on top of the same table.

---

## 1. Rendering & SEO Rules (non-negotiable)

**Architecture:** Next.js 15+, App Router, TypeScript strict, SSG (property pages) / ISR 60s revalidate (blog), Vercel. No Tailwind/CSS modules — CSS custom properties. Framer Motion 11+ for progressive-enhancement animation only.

**Rule:** Server Components default. `'use client'` only for animation/accordion/lightbox/interactive widgets. If JS is disabled, 100% of content must still render. Test: `curl [url]` must show everything; disabling JS in-browser must not hide any text/pricing/image/data.

### Crawlers (corrected — do not repeat the AI-Overviews/Google-Extended conflation found in older drafts)

| Crawler | Operator | Executes JS? | Note |
|---|---|---|---|
| GPTBot | OpenAI | No | |
| ClaudeBot | Anthropic | No | |
| PerplexityBot | Perplexity | No | |
| Googlebot | Google Search | No | **This is what gates AI Overviews and AI Mode** — they retrieve from the regular Search index, there is no separate AI Overviews crawler |
| Google-Extended | Google | N/A — robots.txt token, not a fetching crawler | Only controls Gemini training/grounding use of content. Does NOT affect Search or AI Overviews inclusion |
| GoogleOther | Google | No | General-purpose, non-Search |
| Bingbot | Microsoft Copilot | Limited | |
| AppleBot | Siri/Spotlight | No | |

### robots.txt (every site root)
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
User-agent: GoogleOther
Allow: /
User-agent: Googlebot
Allow: /
User-agent: Bingbot
Allow: /
User-agent: AppleBot
Allow: /

Sitemap: https://[subdomain].brightplace.ai/sitemap.xml
```
Never block AI bots. Never `noindex` a live page.

### llms.txt (every site root)
```
# [Community Name] Apartments
> [one-line description]

## Property Pages
- [Page Name](/url): [location, floor plans, price range, top amenities]

## Blog
- [Title](/blog/slug): [summary]

## Contact
Website, phone
```

### Headers (vercel.json)
```json
{ "headers": [{ "source": "/(.*)", "headers": [
  { "key": "X-Robots-Tag", "value": "index, follow" },
  { "key": "X-Content-Type-Options", "value": "nosniff" }
]}]}
```

### Semantic HTML template
```html
<html lang="en">
<head>
  <title>[seo_title, differs from H1, <60 chars]</title>
  <meta name="description" content="[<155 chars]">
  <link rel="canonical" href="[exact page url]">
  <meta property="og:title" content="...">
  <meta property="og:description" content="...">
  <meta property="og:image" content="...">
  <meta property="og:type" content="article|website">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{ schema }</script>
</head>
<body>
  <header></header>
  <main><article>
    <h1>[only one]</h1>
    <section id="[slug]"><h2>[question-format when it targets PAA]</h2></section>
  </article></main>
  <footer></footer>
</body>
</html>
```
Rules: one `<h1>`; title ≠ H1; no heading-level skips; every `<section>` has an `id`; images have `width`+`height`; external links `target="_blank" rel="noopener"`; internal links no `target="_blank"`.

### JSON-LD schemas

**Blog pages (3):** Article, FAQPage, WebPage — see §4.

**Property/community landing pages (3) — `[was missing from Complete-Build-Spec until v3.1]`:**
```json
// ApartmentComplex
{ "@context":"https://schema.org", "@type":"ApartmentComplex", "name":"Foxchase Apartments",
  "address": {"@type":"PostalAddress","streetAddress":"...","addressLocality":"Alexandria","addressRegion":"VA","postalCode":"22304"},
  "telephone":"...", "amenityFeature":[{"@type":"LocationFeatureSpecification","name":"Resort-Style Pool","value":true}],
  "priceRange":"$1,467 - $2,521/mo", "numberOfAvailableAccommodation":7 }

// FAQPage — same shape as blog, seeded from the page's own FAQ section
// BreadcrumbList
{ "@context":"https://schema.org", "@type":"BreadcrumbList", "itemListElement":[
  {"@type":"ListItem","position":1,"name":"Home","item":"https://foxchase.brightplace.ai"},
  {"@type":"ListItem","position":2,"name":"Blog","item":"https://foxchase.brightplace.ai/blog"} ]}
```

### Performance targets
TTFB <200ms · LCP <2.5s · CLS <0.1 · FID <100ms · page weight <500KB · first-load JS <160KB.
Images: WebP, hero `loading="eager"`, rest `loading="lazy"`, explicit width/height, CDN `Cache-Control: public, max-age=31536000, immutable`.

### Never do
Client-side rendering for content · `useEffect`+`fetch` for content · hash routing · `noindex` on live pages · blocking AI bots · iframes for content · content behind auth · lazy-loaded text · WordPress page builders.

---

## 2. MCP Server — Full Tool Catalog

### 2.0 Connection
```json
{ "mcpServers": { "air-operator": { "url": "https://mcp.brightplace.ai/air-operator", "auth": { "type": "bearer", "token": "API_KEY" } } } }
```

### 2.1 Error envelope `[EXISTING, v3.1]` — applies to every tool
```json
{ "success": false, "error": { "code": "DUPLICATE_SLUG", "message": "..." } }
```
Codes: `DUPLICATE_SLUG`, `NOT_FOUND`, `VALIDATION_ERROR`, `UNAUTHORIZED`, `ACCOUNT_NOT_CONNECTED`, `RATE_LIMITED`, `UPSTREAM_FAILURE`.
Idempotency: `blog_create_post`, `social_create_post`, `gbp_create_post` — retry with same `community_id`+`slug` (or idempotency key) returns existing record with `success:true`, does not duplicate. Required because our workflow polls-and-retries (§6).

### 2.2 Site Management `[EXISTING]`
```
site_list → all 5 sites: domain, status, config
site_get(community_id) → domain, blog_url, status, created_at
site_update_config(community_id, config)
```

### 2.3 SEO Control `[EXISTING]`
```
seo_get_robots_txt(community_id) / seo_update_robots_txt(community_id, content)
seo_get_sitemap(community_id) / seo_add_sitemap_entry(community_id, url, lastmod, priority) / seo_remove_sitemap_entry(community_id, url)
seo_get_llms_txt(community_id) / seo_update_llms_txt(community_id, content)
seo_get_page_meta(community_id, path) → title, description, canonical, OG, schemas
seo_update_page_meta(community_id, path, {title, description, canonical})
seo_validate_page(community_id, path) → {content_in_html, schemas_present, h1_count, heading_hierarchy, images_have_dimensions, result: PASS|FAIL}
```

### 2.4 Blog CMS `[EXISTING]`
```
blog_create_post(community_id, title, seo_title, meta_description, slug, body_markdown, body_html,
  post_summary, primary_keyword, secondary_keywords[], author, date_published, date_modified,
  last_reviewed, featured_image_alt, schema_faq, schema_article, schema_webpage, status)
  + featured_image file (WebP 1200x628)
  → { id, slug, preview_url, featured_image_url }

blog_get_post(community_id, post_id) / blog_get_post_by_slug(community_id, slug)
blog_list_posts(community_id, status, limit, offset)
blog_update_post(post_id, ...fields) — image optional
blog_delete_post(post_id) → soft delete (archived)
blog_change_status(post_id, status: draft|published|archived)
  → publishing triggers: sitemap update, RSS update, `article_published` event
blog_upload_image(community_id, alt_text) + file → { image_url }
blog_preview_post(post_id) → rendered HTML (signed preview token required, see §4)
blog_get_template(community_id) / blog_update_template(community_id, template)
  → layout, header/footer, typography, colors, image display, meta bar, CTA sections, related posts, share buttons
```

### 2.5 Content Briefs `[EXISTING]`
```
brief_create(community_id, keyword, volume, difficulty, tier, seo_title, h1, word_count_target,
  faq_count, publish_date, outline[{h2, description}], internal_links[])
brief_list(community_id, status) / brief_get(brief_id) / brief_update(brief_id, ...) / brief_delete(brief_id)
```

### 2.6 Social — Account Connection (OAuth) `[EXISTING]`
```
social_get_connection_status(community_id) → { instagram:{connected,handle,expires_at}, facebook:{connected} }
social_get_auth_url(community_id, platform) → { auth_url }
social_oauth_callback(community_id, platform, code) → { connected, account_handle }
social_disconnect_account(community_id, platform)
social_refresh_token(community_id, platform) — scheduled, pre-expiry
```
If not connected, publish attempts return `ACCOUNT_NOT_CONNECTED`, not a silent fallback to a shared account.

### 2.7 Social Posts `[EXISTING]`
```
social_create_post(community_id, blog_post_id, platform, post_type, caption, hashtags, image_url|image_prompt,
  link_url, cta_text, scheduled_at)
social_create_batch(posts[]) — e.g. IG feed + IG story + FB in one call
social_list(community_id, status, platform) / social_get(id) / social_update(id, ...) / social_delete(id)
social_change_status(id, status: draft|approved|scheduled|published|failed)
```

### 2.8 GBP — Posts, Reviews, Q&A, Suggestions `[EXISTING]`
```
gbp_create_post(community_id, blog_post_id, post_type, body_text, cta_type, cta_url, image_url, scheduled_at)
gbp_list_posts(community_id) / gbp_get_post(id) / gbp_update_post(id,...) / gbp_delete_post(id)
gbp_change_post_status(id, status) — approved triggers publish to Google

review_list(community_id, reply_status) / review_get(id)
review_create_reply(id, reply_text) / review_update_reply(id, reply_text) / review_delete_reply(id)
review_approve_reply(id) — publishes to Google

qna_create(community_id, question, answer, source) / qna_create_batch(qnas[])
qna_list(community_id, status) / qna_get(id) / qna_update(id, answer) / qna_delete(id)
qna_change_status(id, status) — approved triggers publish to Google

gbp_list_suggestions(community_id, status) → [{id, check_type, severity, message, suggested_action}]
gbp_get_suggestion(id) / gbp_dismiss_suggestion(id, reason)
gbp_recompute_suggestions(community_id) — weekly + on-demand
```
Check types: `photo_cadence` (<~10 new photos/90d) · `posting_frequency` (<1 post/7d) · `review_response` (unreplied >48h or templated) · `profile_completeness` (missing field / generic category) · `qna_coverage` (<5 seeded, or gaps vs `community_profiles.tour_questions`).

### 2.9 GBP Live Profile Write `[NEW]` — closes a real gap
The suggestion tools above only ever produce recommendations; nothing writes an accepted suggestion to the actual live Google Business Profile. This is required for the "AI suggests → accept → deploys to Google" flow (see design reference HTML, GBP tab).
```
gbp_get_profile(community_id)
  → { description, primary_category, categories[], hours, attributes, photo_count_90d, address, phone }
  (live-fetched from Google Business Profile API via the OAuth connection in §2.6/GBP equivalent)

gbp_apply_suggestion(suggestion_id, accept: boolean, edited_value?: string)
  → if accept: writes the target field (description / primary_category / etc.) to the live profile via
    Google's Business Profile API, marks the suggestion `resolved`, returns { success, deployed_at, field, live_value }
  → if reject: marks suggestion `dismissed`, no write occurs
```
Requires GBP OAuth scope that allows profile-field writes, not just posts/reviews/Q&A (confirm scope with Google Business Profile API — `businessinformation.locations` or similar; this is broader than the read/post-only scope implied elsewhere in the doc — flag to dev).

### 2.10 Community Profiles `[EXISTING]`
```
profile_create(community_id, positioning, differentiators[], neighborhood_anchors[{name,time}], things_we_never_say)
profile_get(community_id) / profile_update(community_id, ...) / profile_list()
```
Fields also include `tour_questions`, `resident_feedback`, `profile_completeness` (int).

### 2.11 Events (two-way comms) `[EXISTING]`
```
events_list_pending(community_id?) — omit for all communities
events_list_all(community_id, status, limit) / events_get(id)
events_mark_processed(id) / events_mark_failed(id, error)
```
Auto-created event types: `brief_approved`, `article_update_requested`, `article_published`, `social_regenerate`, `content_rejected`, `new_review`, `review_reply_rejected`, `profile_updated`, `qna_request` (monthly trigger), `brief_request` (bi-weekly trigger). Payload columns match the trigger's natural fields (e.g. `article_update_requested`: `{post_id, user_note}`).

### 2.12 Stats (per-community) `[EXISTING]`
```
stats_get(community_id) → articles_live, briefs_pending, organic_visits_30d, ai_citations
stats_blog(community_id) → per-article views, rankings, AI citations
stats_social(community_id) → posts published, likes, comments, reach per post
stats_gbp(community_id) → rating, review_count, profile_views, direction_requests, calls, last_photo_upload

stats_seo_visibility(community_id, period) → each metric as {value, delta_pct}:
  { impressions, clicks, organic_keywords, ai_visibility: {citations, delta_pct} }
  — sourced from seo_visibility_snapshots (Search Console + Semrush + AI referral log, §3)

stats_overview(community_id, period) → single-community rollup:
  { leads: {tours_booked, leases_started, calls_made, directions_requested},
    visibility: {...same shape as stats_seo_visibility},
    social: {posts_published_30d, total_engagement, top_platform},
    gbp: {rating, profile_views, calls, open_suggestions_count} }

stats_leads(community_id, period) → tours_booked, tours_by_source{blog,social_ig,social_fb,gbp}, calls_made, directions_requested, applications_started
stats_attribution(community_id, period) → top_content_by_tours[], top_cta_positions{}, source_breakdown{}
stats_ai_citations(community_id, period) → total_ai_referrals, by_source{}, top_landing_pages[]
stats_traffic(community_id, period) → total_visits, by_source{}, month_over_month_growth
```

### 2.13 Portfolio Rollup `[NEW]` — closes the biggest gap
No existing tool aggregates across all 5 communities. Required for the portfolio Home screen (design reference HTML).
```
stats_portfolio_overview(period)
  → {
      communities: [
        { community_id, sessions, tours, tour_rate, status_flags: ["feed_sync_pending", "agent_not_connected", ...] },
        ... one per community
      ],
      totals: { sessions, tours, tour_rate, communities_live, units_total }
    }
```
`status_flags` should be a fixed enum dev defines from underlying signals (feed sync age, OAuth connection state, agent-hookup state) — not free text, so the dashboard can render consistent badges.

### 2.14 Dashboard Insight & Attention Feed `[NEW]` — closes the "dashboard editing through our agents" gap
The portfolio Home's orange insight banner ("Citi Lakes is carrying Orlando...") and the "Needs Attention" list are narrative, agent-authored content — not something dev's backend can generate on its own. No tool currently exists for brightplace agents to push this. New table + tools:
```
insight_create(scope: "portfolio"|community_id, headline, body, cta_community_id?, expires_at?)
  → pushes the narrative insight card our agents write after cross-community analysis
insight_list(scope, status: "active"|"dismissed"|"archived")
insight_dismiss(insight_id) / insight_archive(insight_id)

attention_item_create(community_id, severity: "low"|"medium"|"high", message)
  → pushes one "Needs Attention" bullet (e.g. "feed sync pending 9 days; pricing shown is stale")
attention_item_list(status: "open"|"resolved")
attention_item_resolve(attention_item_id)
```
Cadence: our agents run a portfolio analysis pass (frequency TBD — likely daily or on-demand via CLI) and push 1 insight + N attention items per pass. Dev's dashboard just renders whatever is `active`/`open` — no independent logic on dev's side to compute these narratively (dev CAN and should independently compute the underlying flags like `feed_sync_pending`, but the human-readable insight text is ours to author and push).

### 2.15 Website Design & Non-Blog Page Content `[NEW]` — closes the "website design control" gap
`blog_get_template`/`blog_update_template` (§2.4) only cover the blog. Nothing currently lets agents control the homepage, floor-plans page, amenities page, neighborhood page, or sitewide theme — these have zero MCP surface in the prior spec despite being most of "the website."
```
site_get_theme(community_id) → { colors: {primary, secondary, accent}, fonts: {display, body}, logo_url, favicon_url }
site_update_theme(community_id, theme) — applies across property pages AND blog template

page_list(community_id) → non-blog pages for this community (home, floor-plans, amenities, neighborhood, contact, ...)
page_get_content(community_id, page_slug) → { title, seo_title, meta_description, sections[], schemas }
page_update_content(community_id, page_slug, { sections[], seo_title?, meta_description? })
  — sections is an ordered array, e.g. [{type:"hero", heading, body_html, image_url}, {type:"amenities_grid", items[]}, {type:"faq", items[]}]
page_get_template(community_id, page_slug) → layout/component config for that page type
page_update_template(community_id, page_slug, template)
```
Backing table: `site_pages` (§3).

---

## 3. Database Schema

13 tables carried over from Complete-Build-Spec v3.1, plus 3 new tables for §2.13–2.15.

```sql
-- EXISTING
create table blog_posts (
  id uuid primary key default gen_random_uuid(), community_id varchar(64) not null,
  title text not null, seo_title varchar(60) not null, meta_description varchar(160) not null,
  slug varchar(128) not null, body_markdown text not null, body_html text not null,
  post_summary varchar(300) not null, primary_keyword varchar(128), secondary_keywords jsonb default '[]',
  author varchar(128) default 'AIR Communities', date_published date not null, date_modified date not null,
  last_reviewed varchar(32), featured_image_url text, featured_image_alt varchar(256),
  schema_faq text, schema_article text, schema_webpage text, status varchar(16) default 'draft',
  word_count integer, created_at timestamptz default now(), updated_at timestamptz default now(),
  unique(community_id, slug)
);

create table content_briefs (
  id uuid primary key default gen_random_uuid(), community_id varchar(64) not null, keyword text not null,
  volume integer, difficulty integer, tier varchar(32), seo_title varchar(60), h1 text,
  word_count_target integer default 2000, faq_count integer default 10, publish_date date,
  outline jsonb default '[]', internal_links jsonb default '[]', user_note text,
  status varchar(16) default 'pending', created_at timestamptz default now(), updated_at timestamptz default now()
);

create table social_accounts (
  id uuid primary key default gen_random_uuid(), community_id varchar(64) not null,
  platform varchar(16) not null, account_handle varchar(128),
  access_token text, refresh_token text, -- encrypted at rest
  token_expires_at timestamptz, connected_at timestamptz, status varchar(16) default 'disconnected',
  created_at timestamptz default now(), updated_at timestamptz default now(), unique(community_id, platform)
);

create table social_posts (
  id uuid primary key default gen_random_uuid(), community_id varchar(64) not null,
  blog_post_id uuid references blog_posts(id), platform varchar(16) not null, post_type varchar(16) not null,
  caption text not null, hashtags text, image_url text, image_alt text, image_prompt text,
  link_url text, cta_text text, scheduled_at timestamptz, published_at timestamptz,
  external_post_id text, metrics jsonb default '{}', status varchar(16) default 'draft',
  created_at timestamptz default now(), updated_at timestamptz default now()
);

create table gbp_posts (
  id uuid primary key default gen_random_uuid(), community_id varchar(64) not null,
  blog_post_id uuid references blog_posts(id), post_type varchar(16) default 'update', body_text text not null,
  cta_type varchar(16), cta_url text, image_url text, scheduled_at timestamptz, published_at timestamptz,
  status varchar(16) default 'draft', created_at timestamptz default now(), updated_at timestamptz default now()
);

create table gbp_reviews (
  id uuid primary key default gen_random_uuid(), community_id varchar(64) not null, google_review_id text,
  reviewer_name text, rating integer, review_text text, review_date timestamptz, reply_text text,
  reply_status varchar(16) default 'pending', reply_published_at timestamptz,
  created_at timestamptz default now(), updated_at timestamptz default now()
);

create table gbp_qna (
  id uuid primary key default gen_random_uuid(), community_id varchar(64) not null,
  question text not null, answer text not null, source varchar(32), google_qna_id text,
  status varchar(16) default 'suggested', created_at timestamptz default now(), updated_at timestamptz default now()
);

create table gbp_suggestions (
  id uuid primary key default gen_random_uuid(), community_id varchar(64) not null,
  check_type varchar(32) not null, severity varchar(16) default 'medium', message text not null,
  suggested_action text, status varchar(16) default 'open', dismissed_reason text,
  created_at timestamptz default now(), updated_at timestamptz default now()
);
create index idx_gbp_suggestions_community on gbp_suggestions(community_id, status);

create table seo_visibility_snapshots (
  id uuid primary key default gen_random_uuid(), community_id varchar(64) not null, snapshot_date date not null,
  impressions integer default 0, clicks integer default 0, organic_keywords integer default 0,
  ai_citations integer default 0, source varchar(32), created_at timestamptz default now(),
  unique(community_id, snapshot_date, source)
);
create index idx_visibility_community_date on seo_visibility_snapshots(community_id, snapshot_date);

create table community_profiles (
  id uuid primary key default gen_random_uuid(), community_id varchar(64) not null unique,
  positioning text, differentiators jsonb default '[]', neighborhood_anchors jsonb default '[]',
  things_we_never_say text, tour_questions text, resident_feedback text, profile_completeness integer default 0,
  created_at timestamptz default now(), updated_at timestamptz default now()
);

create table events (
  id uuid primary key default gen_random_uuid(), event_type varchar(32) not null, community_id varchar(64) not null,
  status varchar(16) default 'pending', data jsonb default '{}', error text, processed_at timestamptz,
  created_at timestamptz default now()
);
create index idx_events_status on events(status);
create index idx_events_community on events(community_id, status);

create table site_config (
  id uuid primary key default gen_random_uuid(), community_id varchar(64) not null unique, domain text not null,
  robots_txt text, llms_txt text, blog_template jsonb default '{}',
  theme jsonb default '{}', -- [NEW] colors/fonts/logo — backs site_get_theme / site_update_theme
  site_status varchar(16) default 'active', created_at timestamptz default now(), updated_at timestamptz default now()
);

create table lead_attribution (
  id uuid primary key default gen_random_uuid(), community_id varchar(64) not null, lead_type varchar(32) not null,
  utm_source varchar(64), utm_medium varchar(64), utm_campaign varchar(256), utm_content varchar(64),
  referrer_url text, landing_page text, is_ai_referral boolean default false, ai_source varchar(32),
  session_id text, created_at timestamptz default now()
);
create index idx_leads_community on lead_attribution(community_id);
create index idx_leads_type on lead_attribution(community_id, lead_type);
create index idx_leads_source on lead_attribution(utm_source);

-- NEW
create table site_pages (
  id uuid primary key default gen_random_uuid(), community_id varchar(64) not null,
  page_slug varchar(64) not null, -- 'home' | 'floor-plans' | 'amenities' | 'neighborhood' | 'contact'
  title text, seo_title varchar(60), meta_description varchar(160),
  sections jsonb not null default '[]', -- ordered [{type, heading, body_html, image_url, ...}]
  schema_apartment_complex text, schema_faq text, schema_breadcrumb text,
  template jsonb default '{}', -- layout/component config for this page, mirrors blog_template pattern
  status varchar(16) default 'published',
  created_at timestamptz default now(), updated_at timestamptz default now(),
  unique(community_id, page_slug)
);

create table portfolio_insights (
  id uuid primary key default gen_random_uuid(), scope varchar(16) not null default 'portfolio',
  headline text, body text not null, cta_community_id varchar(64),
  status varchar(16) default 'active', expires_at timestamptz, created_at timestamptz default now()
);

create table attention_items (
  id uuid primary key default gen_random_uuid(), community_id varchar(64) not null,
  severity varchar(16) default 'medium', message text not null, status varchar(16) default 'open',
  created_at timestamptz default now(), resolved_at timestamptz
);
create index idx_attention_community_status on attention_items(community_id, status);
```

**Total: 16 tables** (13 existing + `site_pages`, `portfolio_insights`, `attention_items`).

---

## 4. Blog Page Rendering

Pipeline on `blog_create_post`: store → convert markdown→HTML server-side if `body_html` absent → render via blog template → inject 3 schemas into `<head>` → set meta tags → serve via ISR (60s revalidate).

```html
<head>
  <title>[seo_title]</title>
  <meta name="description" content="[meta_description]">
  <link rel="canonical" href="https://[subdomain].brightplace.ai/blog/[slug]">
  <meta property="og:title" content="[seo_title]">
  <meta property="og:description" content="[meta_description]">
  <meta property="og:image" content="[featured_image_url]">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">[schema_faq]</script>
  <script type="application/ld+json">[schema_article]</script>
  <script type="application/ld+json">[schema_webpage]</script>
</head>
<body><article>
  <img src="[featured_image_url]" alt="[featured_image_alt]" width="1200" height="628" loading="eager">
  <div class="article-meta">
    <span>By [author]</span><span>Published [date_published]</span>
    <span>Last reviewed [last_reviewed]</span><span>[word_count/238] min read</span>
  </div>
  <div class="article-body">[body_html]</div>
</article></body>
```

**Draft visibility `[EXISTING, v3.1]`:** `draft`/`archived` posts return 404 to anonymous requests and crawlers (not a rendered `noindex` page — that leaks the URL). `preview_url` and `blog_preview_post` carry a signed `?preview=[token]` only the dashboard/CLI can generate.

**Publish side-effects:** sitemap auto-add, RSS auto-include, `article_published` event created. We separately call `seo_update_llms_txt`.

Blog index (`/blog`): grid, newest first, 12/page, card = image+title+summary+date+reading-time.

Markdown→HTML: server-side (marked/remark/markdown-it). External links `target="_blank" rel="noopener"`; internal links not. Images: WebP, CDN immutable 1yr cache.

---

## 5. Non-Blog Page Rendering `[NEW section]`

Property pages (home, floor-plans, amenities, neighborhood, contact) render from `site_pages.sections` (§3) through the page's `template` (§2.15), same two-layer model as blog: Server Components for all copy/pricing/amenity lists/FAQ, Client Components only for lightboxes/accordions/rent calculator/AI chat widget/parallax. SSG at deploy time (not ISR — these change less often than blog; `page_update_content` should trigger a targeted rebuild/revalidation of just that page, not a full site rebuild).

Site theme (`site_config.theme`) cascades into both property-page templates and the blog template — one source of truth for colors/fonts/logo per community.

---

## 6. Content-Engine → MCP Workflow Patterns

Trigger model today: **manual** — a human runs Claude Code, which polls `events_list_pending()`. Phase 3 (50-100 communities) moves this to a serverless webhook that calls the same tools automatically; the tool contracts don't change, only what invokes them.

**Full blog post:**
```
events_list_pending() → brief_approved(foxchase, keyword)
brief_get(brief_id); profile_get(foxchase)
[run writing agent locally] → markdown, HTML, image, schemas
blog_create_post({...}) → {id, slug, preview_url}
blog_preview_post(post_id) [QA]
blog_change_status(post_id, "published")
social_create_batch([ig_feed, ig_story, fb_post])
gbp_create_post({...})
seo_update_llms_txt(foxchase, updated_content)
events_mark_processed(event_id)
```

**New review:** `events_list_pending()` → `review_get` + `profile_get` → [reply agent locally] → `review_create_reply` → `events_mark_processed`.

**SEO meta update:** `seo_get_page_meta` → `seo_update_page_meta`.

**Page validation:** `seo_validate_page(community_id, path)` → `{content_in_html, schemas_present, h1_count, heading_hierarchy, images_have_dimensions, result}`.

**Portfolio analysis pass `[NEW, cadence TBD]`:** pull `stats_portfolio_overview()` + per-community `stats_overview()` → [analysis, our agents] → `insight_create()` for the cross-community narrative + `attention_item_create()` per flagged issue.

**GBP suggestion → deploy `[NEW]`:** `gbp_list_suggestions(community_id)` → community manager (dashboard) or our agent reviews → `gbp_apply_suggestion(suggestion_id, accept: true)` → writes live profile field, returns `deployed_at`.

**Website design change:** `page_get_content`/`page_get_template` → edit → `page_update_content`/`page_update_template`; `site_get_theme` → edit → `site_update_theme`.

---

## 7. UTM & Lead Attribution

**UTM params on every CTA:** `utm_source` (blog/social_ig/social_fb/gbp/agent) · `utm_medium` (cta/inline_link/post/story/reply) · `utm_campaign` (article-slug or keyword) · `utm_content` (top_cta/mid_cta/end_cta/faq_link/link_in_bio).

Capture: store UTM from URL in session/cookie on landing → attach to any conversion event (tour_booked, call_made, directions_requested, application_started, contact_form_submitted, agent_tour_conversion) → write `lead_attribution` row → fire Amplitude event. First-touch UTM persists for the whole session (a `/tour` booking after landing on `/blog/x?utm_source=blog` still attributes to the blog post).

**AI referral detection** (`document.referrer` / `Referer`): `chat.openai.com`/`chatgpt.com`→chatgpt · `perplexity.ai`→perplexity · `google.com` w/ AI Overview click pattern→google_ai · `bing.com/chat`→copilot · `claude.ai`→claude. Sets `is_ai_referral`+`ai_source` on the lead_attribution row.

**Amplitude events** (fire client-side, properties include `community_id` + UTM fields + `is_ai_referral` where relevant):
- Engagement: `page_viewed`, `blog_post_viewed`, `blog_scroll_depth`, `blog_time_on_page`, `cta_clicked`, `internal_link_clicked`, `external_link_clicked`
- Conversion (critical): `tour_requested`, `tour_booked`, `call_initiated`, `directions_requested`, `application_started`, `contact_form_submitted`
- AI agent: `agent_chat_opened`, `agent_message_sent`, `agent_tour_conversion`, `agent_handoff_to_human`
- Listings: `floor_plan_viewed`, `listing_viewed`, `pricing_calculator_used`, `filter_applied`
- Social/GBP/AI attribution: `social_referral_landed`, `gbp_referral_landed`, `ai_referral_landed`

---

## 8. Deployment Phases

1. Foxchase blog: site + CMS + MCP (blog + events tools) → push test article via MCP, verify render/SEO → live
2. SEO control + briefs: robots/sitemap/llms/page-meta/validate tools, community profile tools → full brief→article→publish→validate loop
3. Dashboard: SEO tab, brief approval, article pipeline; dashboard actions create events
4. Social: OAuth connect, social post tools, dashboard social tab
5. GBP: posts/reviews/Q&A/suggestions tools, dashboard GBP tab, `gbp_apply_suggestion` live-write
6. Roll out to remaining 4 subdomains (same codebase, different `community_id`+domain config)
7. Scale: scheduled jobs (auto brief generation, review monitoring), multi-community batch ops, perf at 100+ communities
8. `[NEW phase]` Portfolio layer: `stats_portfolio_overview`, `insight_*`/`attention_item_*` tools, portfolio Home screen
9. `[NEW phase]` Non-blog page control: `site_pages` table, `page_*`/`site_theme_*` tools

---

## 9. Testing Checklist (condensed)

**Rendering:** curl shows all content · one h1, title≠h1 · 3 JSON-LD schemas present (blog: Article/FAQ/WebPage; property: ApartmentComplex/FAQ/Breadcrumb) · OG+Twitter tags · canonical set.

**Crawlers:** robots.txt allows GPTBot/ClaudeBot/PerplexityBot/Googlebot/Google-Extended/GoogleOther/Bingbot/AppleBot · llms.txt exists · X-Robots-Tag present · draft/archived return 404 anonymously, preview needs signed token.

**Performance:** <500KB page, Core Web Vitals green, TTFB <200ms.

**MCP:** all tools callable + auth enforced · CRUD works per content type · events fire on dashboard actions and scheduled triggers · mark-processed prevents reappearance · batch ops work · `seo_validate_page`/`blog_preview_post` accurate · sitemap/RSS auto-update on publish · error envelope + idempotency behave as specified (§2.1) · `gbp_apply_suggestion` actually writes the live profile field and is reflected in `gbp_get_profile` on next read.

**OAuth:** auth_url valid both platforms · callback stores encrypted tokens · refresh runs pre-expiry · disconnect clears status · expired ≠ connected in status check.

**UTM/attribution:** UTM captured + persists across session · every conversion type writes `lead_attribution` · AI referral detection works for all 5 sources · `stats_leads`/`stats_attribution`/`stats_ai_citations` return correct shapes · Amplitude fires for all listed events.

**Portfolio/design (new):** `stats_portfolio_overview` totals reconcile with the sum of per-community `stats_overview` · `insight_create`/`attention_item_create` show up via `_list` immediately · `page_update_content`/`site_update_theme` reflect on the live page without a full redeploy.

---

## 10. Left to the Developer's Discretion `[DEV DECIDES]`

These are flagged, not blocking, and not ours to dictate — brightplace defers to whatever the dev team finds simplest to build/operate. Pick any reasonable approach and note the choice back in this doc (or its successor) once built, so our agents know what shape to expect.

1. **Ask brightplace** (chat drawer in the design reference): no backing tool exists yet. Dev's call whether this is an LLM layered over the existing `stats_*`/`gbp_*`/`blog_*` tools at query time, or a simpler templated/canned-response system — whichever is simpler to stand up first.
2. **GA4 as a data source:** the design reference's visibility chart shows Sessions/Engaged Sessions (GA4 metrics); `stats_seo_visibility` currently only sources Search Console + Semrush + AI referral log. Dev's call whether GA4 becomes a new `stats_ga4` tool or a 4th `source` value in `seo_visibility_snapshots`, and how GA4 property access/OAuth is wired up per community.
3. **Listings / floor plans / pricing / availability data:** referenced throughout (property page content, `floor_plan_viewed` Amplitude event, ApartmentComplex schema's `numberOfAvailableAccommodation`) but never resolved — likely an AIR ILS/PMS feed rather than agent-authored content. Dev's call on feed vs. manual entry vs. syndication API, and whatever `listings_*` MCP tools (if any) that implies.
4. **GBP OAuth scope for live writes:** `gbp_apply_suggestion` (§2.9) needs write access to profile fields (description, category) — broader than posting/replying. Dev confirms this scope is obtainable via Google's Business Profile API and included in whatever OAuth grant gets set up.
5. **Portfolio insight cadence:** `insight_create`/`attention_item_create` (§2.14) have no defined trigger frequency — dev's call whether a daily scheduled pass or on-demand-only is simpler to support first.
6. **`page_update_content` revalidation:** property pages are SSG, not ISR — dev's call on the rebuild mechanism for a single-page update (targeted on-demand revalidation vs. full redeploy).
