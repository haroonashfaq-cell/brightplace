# CMS & Data Source Integrations

**Last Updated:** August 2026

---

## CMS Publishing Integrations

### Integration Matrix

| Platform | API Method | Auth Type | Image Upload | SEO Fields | Complexity |
|---|---|---|---|---|---|
| WordPress | REST API v2 | Application Passwords / JWT | Media endpoint | Yoast/RankMath meta API | Medium |
| Webflow | CMS API (REST) | OAuth2 | Asset API (separate call) | Built-in CMS fields | Medium |
| Shopify | Admin API (REST/GraphQL) | Custom App OAuth | File upload API | Metafields | Low |
| Ghost | Admin API | JWT (admin key) | Image upload endpoint | Built-in meta fields | Low |
| HubSpot | CMS API (REST) | OAuth2 or Private App | File Manager API | Built-in SEO fields | Medium |
| Wix | Blog API (REST) | OAuth2 | Media Manager API | SEO settings API | Medium |
| Squarespace | No public blog API | N/A | N/A | N/A | Not automatable |
| Custom CMS | Webhook | User-defined | User-defined | User-defined | Low |

---

## How Each Integration Works

### WordPress Integration

```
Connection Flow:
1. User enters WordPress site URL
2. User creates Application Password in WP Admin (Users → Profile → Application Passwords)
3. OR installs our lightweight auth plugin for OAuth
4. System validates connection, discovers post types and categories
5. User maps our fields to their WP fields

Publishing Flow:
1. Upload featured image → POST /wp-json/wp/v2/media (multipart)
2. Create post → POST /wp-json/wp/v2/posts
   - title, content (HTML), excerpt, status (draft/publish)
   - featured_media (image ID from step 1)
   - categories, tags
3. Set SEO meta → POST /wp-json/yoast/v1/posts/{id}
   - OR /wp-json/rankmath/v1/posts/{id}
   - title, description, focus keyword
4. Return post URL to user

Key Considerations:
- Yoast SEO REST API requires Yoast Premium OR our plugin
- RankMath has free REST API support
- Custom fields via ACF can be set via meta API
- Gutenberg blocks: we push HTML, WP wraps in Classic block
```

### Webflow Integration

```
Connection Flow:
1. OAuth2 authorization — user clicks "Connect Webflow"
2. Redirects to Webflow consent screen
3. Callback returns access token (stored encrypted)
4. System discovers: sites → collections → fields
5. User selects target collection and maps fields

Publishing Flow:
1. Upload image → POST /sites/{site_id}/assets (multipart)
2. Create CMS item → POST /collections/{collection_id}/items
   - fieldData: name, slug, post-body (HTML), seo-title,
     meta-description, focus-keyword, post-summary
   - featured_media: asset reference from step 1
   - isDraft: true/false
3. Optional: Publish → POST /collections/{id}/items/publish
4. Return live URL to user

Key Considerations:
- Webflow RichText strips <script> tags (no inline schema)
- Webflow RichText strips <ul><li> content (use <p><strong> instead)
- No <h1> in post-body (CMS uses "name" field as H1)
- Max 60 items per bulk create/update call
- Rate limit: 60 requests per minute
- Image must be uploaded as asset first, then referenced
```

### Shopify Integration

```
Connection Flow:
1. Create Custom App in Shopify Admin → API credentials
2. OR public app OAuth flow
3. System discovers blogs (most stores have 1 blog: "News")
4. User selects target blog

Publishing Flow:
1. Create article → POST /admin/api/2024-01/blogs/{blog_id}/articles.json
   - title, body_html, author, tags
   - published: true/false
   - image: { src: URL or base64 }
   - metafields for SEO (title_tag, description_tag)
2. Return article URL

Key Considerations:
- Shopify blog is simple (no custom CMS fields)
- SEO via metafields: title_tag, description_tag
- Image can be inline base64 or external URL
- Limited formatting control compared to WordPress/Webflow
```

### Ghost Integration

```
Connection Flow:
1. User creates Custom Integration in Ghost Admin
2. Provides Admin API key
3. System creates JWT from API key for auth
4. Discovers tags and authors

Publishing Flow:
1. Upload image → POST /ghost/api/admin/images/upload/
2. Create post → POST /ghost/api/admin/posts/
   - title, html (body), custom_excerpt
   - feature_image (URL from step 1)
   - tags, authors
   - meta_title, meta_description
   - status: draft/published
3. Return post URL

Key Considerations:
- Ghost uses mobiledoc internally but accepts HTML
- JWT token must be regenerated (short-lived)
- Ghost has excellent SEO fields built-in
- Clean, simple API — easiest integration
```

### HubSpot Integration

```
Connection Flow:
1. OAuth2 flow or Private App token
2. System discovers blog groups
3. User selects target blog

Publishing Flow:
1. Upload image → File Manager API
2. Create post → POST /cms/v3/blogs/posts
   - name, postBody (HTML), metaDescription
   - featuredImage, slug
   - contentGroupId (blog ID)
   - state: DRAFT/PUBLISHED
3. Return post URL

Key Considerations:
- HubSpot CMS API requires Marketing Hub Professional+
- Rich content modules may not render from raw HTML
- Blog SEO handled via built-in fields
```

---

## SEO Data Source Integrations

### DataForSEO API (Primary — Recommended for MVP)

```
Endpoints We Use:
├── /keywords_data/google/search_volume/live
│   └── Keyword volume, CPC, competition
├── /dataforseo_labs/google/keyword_suggestions/live
│   └── Long-tail keyword discovery
├── /dataforseo_labs/google/competitors_domain/live
│   └── Competitor discovery by domain
├── /dataforseo_labs/google/domain_intersection/live
│   └── Keyword gap analysis (they rank, you don't)
├── /serp/google/organic/live/regular
│   └── SERP results with PAA, AI Overview, snippets
└── /on_page/task_post
    └── Site audit (crawl + technical checks)

Cost: ~$0.002-0.005 per API call
Monthly estimate: $50-150 for moderate usage
```

### Google Search Console API

```
What We Get:
- Pages indexed by Google
- Impressions, clicks, CTR, average position per page
- Queries driving traffic to each page
- Index coverage issues

Connection: OAuth2 (user authorizes Google account)
Use: Site audit dashboard, performance tracking
```

### Google Analytics 4 API

```
What We Get:
- Page traffic (sessions, users, pageviews)
- Engagement metrics (time on page, bounce rate)
- Conversion events
- Traffic sources

Connection: OAuth2 (same Google account)
Use: Performance tracking, ROI measurement
```

---

## Integration Architecture

```
┌──────────────────────────────────────────┐
│           PUBLISH AGENT                   │
│                                          │
│  1. Receives: article HTML, meta,        │
│     image, target CMS config             │
│                                          │
│  2. Routes to CMS adapter:              │
│     ┌─────────────────────┐             │
│     │ cms_adapters/       │             │
│     │ ├── wordpress.py    │             │
│     │ ├── webflow.py      │             │
│     │ ├── shopify.py      │             │
│     │ ├── ghost.py        │             │
│     │ ├── hubspot.py      │             │
│     │ └── webhook.py      │             │
│     └─────────────────────┘             │
│                                          │
│  3. Each adapter handles:               │
│     a. Auth (OAuth/JWT/API key)          │
│     b. Image upload (platform-specific)  │
│     c. Content format conversion         │
│     d. SEO field mapping                 │
│     e. Draft vs Published toggle         │
│                                          │
│  4. Returns: published URL + status      │
└──────────────────────────────────────────┘
```

---

## User Settings (per project)

```json
{
  "cms": {
    "type": "webflow",
    "site_id": "69d6907887b739e09622100f",
    "collection_id": "69fcfcef26d35b66ba874f9d",
    "access_token": "[encrypted]",
    "field_mapping": {
      "title": "name",
      "body": "post-body",
      "seo_title": "seo-title",
      "meta_description": "meta-description",
      "keyword": "focus-keyword",
      "summary": "post-summary",
      "image": "main-image"
    },
    "publish_as_draft": true
  },
  "data_source": {
    "type": "dataforseo",
    "api_login": "[encrypted]",
    "api_password": "[encrypted]"
  },
  "google": {
    "search_console_connected": true,
    "analytics_connected": true,
    "property_url": "https://www.brightplace.ai"
  }
}
```
