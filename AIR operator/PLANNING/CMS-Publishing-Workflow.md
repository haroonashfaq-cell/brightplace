# CMS Publishing Workflow — AIR Operator via MCP

This document describes the complete end-to-end flow for publishing blog content to the brightplace CMS (Staging) through the MCP tools. Claude should follow this workflow exactly.

---

## Overview

```
Local Pipeline (stages 01-09)
    ↓
Stage 10: Prepare CMS payload from stage 09 markdown
    ↓
CMS: Create post → Save revision → Upload media → Approve → Publish
    ↓
Live on staging: https://[community].staging.brightplace.ai/blog/[slug]
```

---

## MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `operator_context_get` | Verify access, list communities, check roles |
| `blog_save_post` | Create a new post OR save a new revision to existing post |
| `blog_get_post` | Read post metadata, revision content, or published state |
| `blog_list_posts` | List posts for a community (editorial or published view) |
| `blog_list_revisions` | List all revisions for a post |
| `blog_validate_post` | Validate a revision against CMS publication rules |
| `blog_preview_post` | Get rendered HTML preview of a revision |
| `blog_change_status` | Submit/approve/publish/unpublish/archive |
| `media_save` | Create upload slot, trigger processing, or delete media |
| `media_get` | Check media status or list media assets |

---

## Step 1: Verify CMS Access

```
operator_context_get()
```

Confirm:
- You have the correct community_id (e.g., `citi-lakes`)
- Your roles include: editor, approver, publisher
- The community has `can_upload: true`

---

## Step 2: Prepare Content from Stage 09

Read the `09-[slug]-final-enriched.md` file. Extract:

| CMS Field | Source | Constraint |
|-----------|--------|------------|
| `title` | Frontmatter `title` | Max 300 chars |
| `seo_title` | Frontmatter `seo_title` | **Max 59 chars**, must differ from title |
| `meta_description` | Frontmatter `meta_description` | **Max 154 chars** |
| `summary` | Write from article intro | **Max 300 chars** |
| `slug` | Frontmatter `slug` | Lowercase, hyphenated: `^[a-z0-9]+(-[a-z0-9]+)*$` |
| `primary_keyword` | Frontmatter `primary_keyword` | Max 128 chars |
| `secondary_keywords` | Frontmatter `secondary_keywords` | Array of strings |
| `author_name` | Frontmatter `author` | Max 128 chars |
| `last_reviewed_on` | Frontmatter `date_published` | Date format: `YYYY-MM-DD` |
| `body_markdown` | Article body (below frontmatter) | See formatting rules below |
| `faqs` | FAQ section | Array of `{question, answer}` objects |

### Body Markdown Formatting Rules (CRITICAL)

The CMS renderer has specific rules. Violating them causes silent `VALIDATION_ERROR`:

| Rule | Details |
|------|---------|
| **No H1 headings** | Do NOT include `# Title` in body_markdown. The CMS generates H1 from the `title` field. Use `##` for sections. |
| **No horizontal rules** | Do NOT use `---` separators. The CMS rejects them (likely confused with YAML frontmatter). |
| **No frontmatter** | Strip the `---` YAML block before sending. Only send the body content. |
| **Markdown lists work** | `- item` bullet lists are fine. |
| **Bold works** | `**text**` is fine. |
| **Links work** | `[text](url)` is fine. |
| **Blank lines between sections** | Add a blank line before and after headings and between list groups. |

### FAQ Extraction

Extract FAQs into a separate array. Do NOT include them in body_markdown:

```json
[
  {"question": "Is there a pet weight limit?", "answer": "No. Citi Lakes does not impose a weight limit."},
  {"question": "How much is pet rent?", "answer": "$20 per month per pet."}
]
```

---

## Step 3: Create the Post

First-time creation uses `slug` + `initial_revision` + `community_id` + `request_key`:

```
blog_save_post(
  slug: "pet-friendly-apartments-orlando-no-weight-limit",
  community_id: "citi-lakes",
  request_key: "[uuid]",
  initial_revision: {
    title: "...",
    body_markdown: "short placeholder"
  }
)
```

**Important:** The initial creation works best with a minimal body. Save the full content in a follow-up revision (Step 4).

Returns: `post_id`, `revision_id`, `etag`

---

## Step 4: Save Full Revision

Now save the complete content with all SEO fields:

```
blog_save_post(
  post_id: "[post_id from step 3]",
  community_id: "citi-lakes",
  request_key: "[new uuid]",
  if_match: "[article etag]",
  base_revision_id: "[revision_id from step 3]",
  title: "...",
  seo_title: "...",
  meta_description: "...",
  summary: "...",
  primary_keyword: "...",
  secondary_keywords: ["...", "..."],
  author_name: "AIR Communities",
  last_reviewed_on: "2026-09-10",
  featured_image_asset_id: "[media_id]",
  featured_image_alt: "...",
  body_markdown: "[full article body]",
  faqs: [...]
)
```

**Always get the current article etag** with `blog_get_post` before saving. Stale etags are rejected.

---

## Step 5: Generate and Upload Featured Image

### 5a: Generate the image

```bash
python3 "SUPER SEO Agents/generate-image.py" \
  --title "Article Title" \
  --content "path/to/09-final-enriched.md" \
  --output "path/to/[slug]-featured.webp" \
  --alt "Descriptive alt text with keyword"
```

Or use a direct prompt from `08-image-prompts.md`.

### 5b: Create media record

```
media_save(
  filename: "[slug]-featured.webp",
  content_type: "image/webp",
  size_bytes: [exact file size in bytes],
  community_id: "[community-id]",
  operation: "create",
  request_key: "[uuid]"
)
```

Returns: `media_id`, `upload_url` (S3 presigned), `expires_at` (~15 min)

### 5c: Upload bytes to S3

```bash
curl -X PUT \
  -H "Content-Type: image/webp" \
  -H "Content-Length: [size_bytes]" \
  --data-binary @"path/to/image.webp" \
  "[upload_url]"
```

Must return HTTP 200.

### 5d: Trigger processing

```
media_save(
  community_id: "[community-id]",
  operation: "process",
  media_id: "[media_id]",
  if_match: "[media etag]"
)
```

### 5e: Wait for ready

```
media_get(community_id: "[community-id]", media_id: "[media_id]")
```

Poll until `status: "ready"` (usually 3-5 seconds). The response includes `width`, `height`, and `variants` (hero + inline).

### 5f: Attach to revision

Include in Step 4's `blog_save_post`:
- `featured_image_asset_id`: the media_id
- `featured_image_alt`: descriptive alt text

---

## Step 6: Review and Approve

The CMS enforces a review workflow: `draft → in_review → approved`

### 6a: Submit for review

```
blog_change_status(
  community_id: "citi-lakes",
  post_id: "[post_id]",
  revision_id: "[revision_id]",
  target: "revision",
  review_status: "in_review",
  if_match: "[revision etag]"
)
```

### 6b: Approve

```
blog_change_status(
  community_id: "citi-lakes",
  post_id: "[post_id]",
  revision_id: "[revision_id]",
  target: "revision",
  review_status: "approved",
  if_match: "[updated revision etag]"
)
```

**Approval validates the revision.** If validation fails, it returns the failing checks. All of these must pass:

| Check | Requirement |
|-------|-------------|
| REQUIRED_TITLE | Title must be set |
| REQUIRED_BODY_MARKDOWN | Body must be set |
| REQUIRED_SEO_TITLE | SEO title must be set (max 59 chars) |
| REQUIRED_META_DESCRIPTION | Meta description must be set (max 154 chars) |
| REQUIRED_SUMMARY | Summary must be set (max 300 chars) |
| REQUIRED_AUTHOR_NAME | Author name must be set |
| REQUIRED_FEATURED_IMAGE_ALT | Alt text for featured image |
| REQUIRED_FAQS | At least one FAQ |
| DISTINCT_TITLE | SEO title must differ from H1 |
| HEADING_HIERARCHY | No heading level skips in body |
| FEATURED_IMAGE | Ready 1200x628 hero image required |
| MEDIA_READY | All referenced assets must be ready |

---

## Step 7: Publish

```
blog_change_status(
  community_id: "citi-lakes",
  target: "article",
  post_id: "[post_id]",
  published_revision_id: "[approved revision_id]",
  if_match: "[article etag]"
)
```

**Must use the article etag** (not revision etag). Get it fresh with `blog_get_post`.

Returns a delivery job. The article is now live at:
`https://[community].staging.brightplace.ai/blog/[slug]`

---

## Step 8: Verify

```
blog_get_post(community_id: "citi-lakes", post_id: "[post_id]")
```

Confirm:
- `published_revision_id` matches what you published
- `first_published_at` is set
- `delivery.status` is not `failed`

---

## Complete Sequence Diagram

```
1. operator_context_get()           → verify access
2. blog_save_post(slug, initial)    → create post (get post_id)
3. generate-image.py                → create featured image
4. media_save(create)               → get upload_url
5. curl PUT to S3                   → upload image bytes
6. media_save(process)              → trigger image processing
7. media_get()                      → wait for status: ready
8. blog_save_post(full content)     → save complete revision with image
9. blog_change_status(in_review)    → submit for review
10. blog_change_status(approved)    → approve revision
11. blog_get_post()                 → get fresh article etag
12. blog_change_status(publish)     → publish to staging
13. blog_get_post()                 → verify publication
```

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `VALIDATION_ERROR` (no details) | Body contains `---` or `# H1` | Remove horizontal rules and H1 from body_markdown |
| `VALIDATION_ERROR` (string_too_long) | summary > 300, seo_title > 59, or meta_description > 154 | Shorten the field |
| `VALIDATION_ERROR` (approval fails) | Missing required fields | Check the `checks` array — add summary, featured image, alt text |
| `STALE_ETAG` | Etag doesn't match current version | Re-fetch with blog_get_post and use the latest etag |
| `INVALID_REQUEST` (schema mismatch) | Mixing CreatePost and SaveRevision fields | For creates: use slug + initial_revision. For updates: use post_id + if_match |

---

## Community IDs

| Community | ID |
|-----------|-----|
| 3400 Avenue of the Arts | `3400-avenue-of-the-arts` |
| Citi Lakes | `citi-lakes` |
| Citigate | `citigate` |
| Foxchase | `foxchase` |
| Indigo West | `indigo-west` |
| One Boynton | `one-boynton` |
| One Canal | `one-canal` |
| Sorrel | `sorrel` |
| Verdant Peachtree Creek | `verdant-peachtree-creek` |
| Villages at Raleigh Beach | `villages-at-raleigh-beach` |

---

## Key Constraints Cheat Sheet

| Field | Max Length | Format |
|-------|-----------|--------|
| title | 300 | Free text |
| seo_title | **59** | Free text, must differ from title |
| meta_description | **154** | Free text |
| summary | **300** | Free text |
| slug | 128 | `^[a-z0-9]+(-[a-z0-9]+)*$` |
| primary_keyword | 128 | Free text |
| author_name | 128 | Free text |
| featured_image_alt | 256 | Free text |
| body_markdown | 200,000 | Markdown (no H1, no `---`) |
| featured_image | — | 1200x628, WebP/JPEG/PNG, ready status |
| request_key | — | UUID, unique per call |
