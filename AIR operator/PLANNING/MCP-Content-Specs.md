# MCP Content Specs — Build Instructions for Tom

**Version:** 1.2
**Date:** 16 September 2026
**Author:** brightplace (Haroon)
**Audience:** Tom / dev team
**Companion to:** `AIR-Operator-MCP-Reference copy.md` (the reference spec — still the source of truth for intent, but see §2: it no longer matches what you built)

---

## 1. Why this doc exists

On 16 Sep 2026 we published the first real AIR article end-to-end through the staging MCP:
`foxchase.staging.brightplace.ai/blog/foxchase-apartments-alexandria-va-what-renters-should-know`

It worked. The blog CMS, briefs, media and review chain are solid — in several places better than the reference spec asked for. This doc is not a complaint about that.

This doc covers two things the live run exposed:

1. **Friction in what you already built** — small, cheap fixes that cost us real time (§4).
2. **What isn't built yet that blocks our actual mandate** — we are an SEO and AI-visibility product, and right now the MCP gives us no way to control sitemaps, robots.txt, llms.txt or page metadata (§5). We can publish articles but we cannot make them discoverable, which is the entire point.

Everything below is scoped to **content, SEO, indexing and the publishing pipeline**. Social, GBP, stats and dashboard tooling are not specified here — §10 shortlists them so the full remaining surface is visible in one place.

**How to read priorities:** P0 = blocks or badly slows current work. P1 = blocks the SEO mandate. P2 = converts manual CLI work into a pipeline.

---

## 2. Corrections — the reference doc is stale on the blog CMS

Before anything else: **`AIR-Operator-MCP-Reference copy.md` §2.4 no longer describes what exists.** You built something different and mostly better. Nobody has written the real contract down, which means our agents keep coding against a fiction.

| Reference spec §2.4 says | What staging actually does |
|---|---|
| `blog_create_post(...)` + `blog_update_post(...)` | `blog_save_post` — one tool, create or new revision |
| Flat `status: draft\|published\|archived` | Immutable revisions + review chain (`draft` → `in_review` → `approved`) + separate article lifecycle (`active`/`archived`) + explicit `published_revision_id` |
| `body_html` field | Does not exist — server renders markdown |
| `schema_faq`, `schema_article`, `schema_webpage` | Do not exist — CMS generates **four** schemas (Article, WebPage w/ speakable, FAQPage, BreadcrumbList) |
| `author` | `author_name` |
| `date_published`, `date_modified` | Do not exist — derived from publish events |
| `blog_upload_image` + file | Four-step media pipeline (§4.4) |
| `blog_preview_post` → signed `preview_url` | Returns an HTML blob, no URL (see §4.5) |
| `blog_delete_post` | Does not exist — use `blog_change_status` lifecycle |
| No validation tool | `blog_validate_post` with 13 named checks |
| — | `job_get` / `job_retry`, `operator_context_get` — new, undocumented |

**Also drifted in the reference doc, please treat these as authoritative instead:**

- **§0 community table lists 5 communities. Staging serves 10.** Add `3400-avenue-of-the-arts`, `citigate`, `indigo-west`, `one-boynton`, `one-canal`. Note §1's GA4 section already says "all 10 community sites" — the doc contradicts itself.
- **Hostnames are `*.staging.brightplace.ai`**, not `*.brightplace.ai`, on staging.
- **Field caps disagree between the schema and the API.** §3's SQL says `seo_title varchar(60)` / `meta_description varchar(160)` — the documented SEO best-practice limits. The live API enforces **59** and **154**. brightplace's position: **the documented 60/160 are correct**, so please align the API to the schema. Some flexibility above that is fine if there is an implementation reason (a reserved render-time suffix would explain 59/154 — if so, document it rather than silently trimming). Our agents will write to ≤150 regardless, since Google truncates by pixel width and the margin is free.

**Ask:** when you next change the tool surface, regenerate a short `MCP-CONTRACT.md` describing only what is callable. Keep the reference doc for intent. They age at completely different rates, which is how we got here.

---

## 3. Live baseline — verified 16 Sep 2026

So we agree on the starting point. 14 tools, all confirmed working on staging:

**Blog (7):** `blog_save_post` · `blog_get_post` · `blog_list_posts` · `blog_list_revisions` · `blog_preview_post` · `blog_validate_post` · `blog_change_status`
**Briefs (3):** `brief_save` · `brief_get` · `brief_list`
**Media (2):** `media_save` · `media_get`
**Platform (2):** `job_get` · `operator_context_get`

Verified publish chain:

```
blog_save_post(slug, initial_revision, request_key)        → post_id, revision_id, ETag
media_save(create) → HTTP PUT to presigned S3 → media_save(process) → poll media_get until ready
blog_save_post(post_id, featured_image_asset_id, if_match) → new revision
blog_validate_post(post_id, revision_id)                   → result: pass (13/13)
blog_change_status(target=revision, review_status=in_review, if_match=<revision ETag>)
blog_change_status(target=revision, review_status=approved, if_match=<revision ETag>)
blog_change_status(target=article, published_revision_id, if_match=<article ETag>)
job_get(job_id)                                            → publication_reconcile succeeded
```

Rendering verified via `blog_preview_post`: single H1 from `title`, correct heading hierarchy, external links auto-get `target="_blank" rel="noopener"`, canonical set to the staging host, four JSON-LD blocks present. **That part is genuinely good work.**

---

## 4. P0 — Fixes to what's already built

### 4.1 Populate `details` on error responses — highest value, lowest cost

**Problem.** Every error returns the code as its own message and a null detail:

```json
{"success": false, "error": {"code": "VALIDATION_ERROR", "message": "VALIDATION_ERROR", "details": null}}
```

Our first publish attempt failed with exactly this. There was no way to tell *what* was invalid. We isolated it by creating a throwaway post and bisecting the payload field by field — four wasted round trips to discover an undocumented rule (§4.2). At 34 articles across 10 communities, that pattern does not scale.

**Build.** Populate `details` with the failing field and the rule:

```json
{"success": false, "error": {
  "code": "VALIDATION_ERROR",
  "message": "body_markdown must not contain an H1; the CMS renders `title` as the page H1",
  "details": {"field": "body_markdown", "rule": "NO_H1_IN_BODY", "found_at_line": 1}
}}
```

Reference spec §2.1 already promises a meaningful `message`. This is bringing the implementation up to its own spec.

**Acceptance:** submit a body containing `# Heading`; the response names `body_markdown` and the rule.

### 4.2 Move undocumented content rules into the validator

**Problem.** Some rules are enforced at save time but appear in no check code and no documentation. Confirmed so far: **an H1 in `body_markdown` is a hard reject.** There may be others we haven't tripped.

`blog_validate_post` has 13 named checks, but only runs against an *already-saved* revision — so a rule that blocks the save can never be surfaced by the validator that exists to catch exactly this.

**Build.**
1. Add check codes for every content rule: `BODY_NO_H1`, and any sibling rules you're enforcing.
2. Add a **dry-run mode** accepting an unsaved revision body, so we can lint before writing:
   `blog_validate_post(community_id, revision: {title, body_markdown, faqs, ...})` → same check array, nothing persisted.

**Why it matters:** we want to validate 33 remaining drafts in a batch *before* creating 33 posts.

**Acceptance:** dry-run a body with an H1 → `passed: false` on `BODY_NO_H1`, no post created.

### 4.3 Fix the silent FAQ double-render

**Problem.** The CMS appends its own `<section id="frequently-asked-questions">` generated from the `faqs[]` array. If the body *also* contains an FAQ section (which every article our pipeline produces did), **every FAQ renders twice** — once from body markdown, once from the array.

Nothing warns. `blog_validate_post` passed 13/13 on a revision that would have shipped 12 duplicated Q&A pairs. We only caught it by reading the preview HTML by eye.

This is an SEO problem, not just cosmetic: duplicated content, and an FAQPage schema whose entities appear twice in the rendered body.

**Build — either is fine:**
- Renderer detects an FAQ-shaped trailing section in the body and suppresses it, **or**
- Validator emits `DUPLICATE_FAQ_SECTION` as a warning.

Prefer the validator — silent content mutation is worse than a warning.

**Acceptance:** a revision with FAQs in both body and array produces either one rendered set or a warning.

### 4.4 Document the media pipeline (and keep the presigned URL)

**Not a bug — this works well, and is badly under-documented.** The reference spec describes one tool (`blog_upload_image`). Reality:

```
media_save(operation=create, filename, content_type, size_bytes, request_key)
  → {media_id, upload: {method: PUT, upload_url: <presigned S3, 15min TTL>, required_headers}}
HTTP PUT the bytes to upload_url with Content-Type and Content-Length
media_save(operation=process, media_id, if_match)  → job_id, status: processing
media_get(media_id)  → status: ready, width, height, variants: {hero, inline}
```

The presigned URL is the right design — it meant we needed no separate Operator Hub credentials. Please document it, including:

- **A ready 1200×628 hero is a hard publish gate.** `REQUIRED_FEATURED_IMAGE_ALT` and `FEATURED_IMAGE` are both `severity: error`. An article cannot publish without one. This was a surprise and it matters for planning: **33 of our 34 finished articles currently have no generated image.**
- Accepted types: `image/jpeg`, `image/png`, `image/webp`. Max 20MB.
- Upload URL expiry (15 min observed).

**Decided: treat 1200×628 as a minimum, with server-side downscale to generate the `hero` variant.** Our generator emits exactly 1200×628 today so exact-match would work now, but it locks out higher-DPI heroes later, and you already run image processing to produce `hero` and `inline`. Low-stakes either way — it changes nothing about the 33 images we still owe.

### 4.5 Return a signed preview URL

**Problem.** Reference spec §4 promises `preview_url` carrying a signed token, and §9's test checklist says "preview needs signed token." The live `blog_preview_post` returns an HTML string in JSON instead.

This blocks the review model the whole system is designed around: **community managers approve content in the dashboard.** They cannot review an HTML blob in a tool response. And the staging site sits behind Vercel deployment protection, so an anonymous fetch of the article URL redirects to `vercel.com/login` — we could not open our own published article to check it.

**Build.** `blog_preview_post` additionally returns:
```json
{"preview_url": "https://foxchase.staging.brightplace.ai/blog/<slug>?preview=<signed-token>", "expires_at": "..."}
```
Token scoped to one revision, short TTL, bypasses both the draft-404 rule and Vercel protection.

**Acceptance:** the URL opens the exact revision in a browser with no session; drafts still 404 without the token.

### 4.6 Revision save is a full replace — document it, then soften it

**Problem.** `blog_save_post` replaces the entire revision. Optional fields not sent are **nulled out**, and `base_revision_id` does not inherit values — it only records lineage. We lost `seo_title` on a test revision by omitting it.

Consequence: changing one field means resending everything, including a 20KB `body_markdown`. Attaching a featured image to our Foxchase article required a full re-send of the whole article.

**Build.**
1. Document the replace semantics explicitly — this is the single most surprising behaviour in the API.
2. Then add field-level patching: either `blog_save_post(patch: true, ...)` merging onto `base_revision_id`, or a dedicated `blog_patch_revision(post_id, base_revision_id, fields{}, if_match)`.

Immutable revisions are the right model; we just shouldn't have to resend 20KB to change an alt text.

### 4.7 Document ETag targeting

`target: "revision"` requires the **revision** ETag; `target: "article"` requires the **article** ETag. Mixing them returns `VERSION_CONFLICT`. This tripped us on the `in_review` call.

The error is recoverable — the response helpfully includes `current_etag` — so this is a documentation fix, not a code fix. One line in the tool description each.

### 4.8 Batch operations

**Problem.** Publishing one article is ~8 calls (save, media create, PUT, process, poll, save, validate, 3 × status). We have **33 more finished articles ready**, plus ongoing production across 10 communities. That's ~260 calls for the current backlog alone, each carrying a full article body.

**Build — in priority order:**
1. `blog_validate_batch(community_id, revisions[])` — lint many drafts before creating anything. Most valuable, least risky.
2. `blog_change_status_batch(items[])` — move many revisions through review in one call.
3. Optional: a trusted-service auto-approve path, so a service principal holding both `editor` and `approver` isn't making three sequential round trips per article purely to satisfy a state machine.

Reference spec §9 already lists "batch ops work" as a test criterion. Nothing batch-capable exists.

---

## 5. P1 — SEO Control: the indexing gap

**This is the most important section in this document.**

Reference spec §2.3 specifies a full SEO Control family, tagged `[EXISTING]`. **None of it is built.** Note that `[EXISTING]` in that doc means "carried over from Complete-Build-Spec v3.1" — document lineage, not build state. It's an easy tag to misread; nothing in §2.3 is callable.

Consequence today: **we can publish an article but we cannot influence whether anything ever finds it.** We're an SEO and AI-visibility product with no MCP control over discovery surfaces.

### 5.1 `llms.txt` — highest priority, no workaround exists

**Build:**
```
seo_get_llms_txt(community_id)                    → {content, updated_at}
seo_update_llms_txt(community_id, content, if_match) → {content, updated_at, etag}
```

**Why first.** Reference spec §6's canonical publish workflow *ends* with `seo_update_llms_txt(foxchase, updated_content)` — it is a required step in our own documented pipeline, and there is no tool and no automatic path. Sitemap and RSS at least plausibly ride the `publication_reconcile` job on publish. `llms.txt` has nothing. Every article we publish makes the file more out of date, with no way to fix it.

§1 of the reference doc already defines the format (community name, one-line description, Property Pages, Blog, Contact). We generate that content; we just need somewhere to put it.

**Acceptance:** update, then `curl https://<community>.staging.brightplace.ai/llms.txt` returns the new content.

### 5.2 Sitemap

**Confirmed by brightplace: `publication_reconcile` already updates both sitemap and RSS on publish.** Good — that is the right design, and it means we are *not* asking for manual sitemap CRUD on blog posts. Hand-managed entries would duplicate state you already maintain and drift the moment anyone forgets.

**What we still need:**

```
seo_get_sitemap(community_id) → {entries:[{url, lastmod, priority, changefreq}], updated_at}
```

Read access only, so we can verify a published article actually landed. Today we cannot confirm our own content is indexable — `/sitemap.xml` is behind Vercel protection (§11, outstanding for Tom #1) and no tool exposes it.

**Write access, scoped narrowly:** `seo_add_sitemap_entry` / `seo_remove_sitemap_entry` for URLs the blog CMS does not own — property pages, landing pages, anything outside `blog_posts`. Not for articles.

**Acceptance:** publish an article; `seo_get_sitemap` lists its URL with a correct `lastmod`. Archive it; the URL disappears (§5.11).

### 5.3 robots.txt

```
seo_get_robots_txt(community_id)
seo_update_robots_txt(community_id, content, if_match)
```

Reference spec §1 defines the required content — allow GPTBot, ChatGPT-User, ClaudeBot, PerplexityBot, Google-Extended, GoogleOther, Googlebot, Bingbot, AppleBot, plus the Sitemap line. Lower urgency if you're serving it from a static template, but we need **read access at minimum** to verify AI crawlers aren't blocked. Blocking them silently would be an invisible, total failure of the AI-citation half of the product.

**Acceptance:** `seo_get_robots_txt` returns live served content, and it allows every bot in §1.

### 5.4 Page metadata (non-blog)

```
seo_get_page_meta(community_id, path)  → {title, description, canonical, og, schemas}
seo_update_page_meta(community_id, path, {title, description, canonical})
```

Blog post metadata is handled inside the revision. This is for the **property pages** — home, floor-plans, amenities, neighbourhood, contact — which are most of each site's crawlable surface and currently have zero MCP control.

### 5.5 `seo_validate_page`

```
seo_validate_page(community_id, path)
  → {content_in_html, schemas_present, h1_count, heading_hierarchy, images_have_dimensions, canonical_set, result: PASS|FAIL}
```

Distinct from `blog_validate_post`: that validates a **stored revision**; this validates a **rendered page as served**. Reference spec §1's non-negotiable rule is that `curl [url]` must show 100% of content with JS disabled. We currently have no way to check that — and given Vercel protection, no way to check it manually either.

**This should also cover property pages,** which have never been validated by anything.

### 5.6 Redirects and slug changes

**Confirmed by brightplace: `slug` can change after publish.** That resolves the question and makes this section *more* urgent, not less.

A mutable slug with no redirect layer is actively dangerous: every slug edit silently breaks inbound internal links, external backlinks, social shares and anything already indexed. Right now there is no redirect tool of any kind, so a slug change today is a clean URL loss with no trail.

**Build — required, not optional, given slugs are mutable:**

```
redirect_create(community_id, from_path, to_path, status_code: 301|302, request_key)
redirect_list(community_id) / redirect_delete(community_id, redirect_id, if_match)
```

**The behaviour that matters most:** when a published article's slug changes, **the CMS should auto-create a 301 from the old path to the new one.** Leaving that to the caller guarantees it gets missed. If you would rather it be explicit, then reject the slug change unless a redirect is supplied in the same call — either is fine, silent breakage is not.

**Acceptance:** change a published article's slug → old path returns 301 to the new one, and `redirect_list` shows the rule without anyone having created it by hand.

**Knock-on:** redirects also serve the archive-with-replacement case (§5.11) and repair the link graph after a slug change (§5.7). Three sections depend on this one.

### 5.7 Internal link graph

**Problem.** Internal linking is core on-page SEO and there is no server-side view of it. `brief_save` accepts `internal_links[]` as *intent*, but nothing exposes the actual link graph of published content. We cannot find orphan pages, cannot detect internal links broken by an archive, and when a slug changes every inbound internal link breaks silently.

**Build:**
```
seo_find_broken_links(community_id) → [{from_path, to_path, reason}]
seo_get_link_graph(community_id)    → {nodes:[{path,title}], edges:[{from,to,anchor_text}], orphans:[path]}
```

**Minimum viable is `seo_find_broken_links` alone.** The CMS already parses every published body to render it, so it already knows every link in every article — this is surfacing something you compute anyway.

**Why:** we are about to publish 34 heavily cross-linked articles across 10 communities. Without this, link rot is invisible until a reader or a crawler finds it.

### 5.8 Canonical override

Canonical is auto-set to the community's own host and `CANONICAL_HOST` enforces a trusted hostname. Correct default — but reference §0 notes these communities have **legacy live domains** (`citilakesapartments.com` and similar). Where legacy and brightplace sites serve overlapping content, we need cross-domain canonical control or the two sites compete for the same queries.

**Build:** per-article and per-page canonical override, validated against an allow-list of owned domains.
**Also document:** what canonical the blog index and any paginated pages receive.

### 5.9 RSS feed access

Reference §4 states publishing triggers "RSS auto-include." No tool exposes the feed, and we cannot fetch it through Vercel protection. RSS remains a real syndication and AI-crawler discovery surface.

**Build:** `seo_get_rss(community_id)` returning the served feed — or at minimum, document the path and confirm it updates on publish.

### 5.10 Update and freshness semantics

**Problem.** Content refresh is a core recurring SEO activity — our pipeline has a dedicated article-update agent and a portfolio content-audit stage. When we publish a *new revision of an already-published article*, nobody has told us what happens to:

- the Article schema's `dateModified`
- the sitemap's `lastmod`
- `last_reviewed_on` — we set it, and reference §4's template shows a "Last reviewed" line in the meta bar, but we have not seen it rendered
- ISR/cache invalidation for the existing URL

**Ask:** document the update path and confirm `dateModified` reflects the republish rather than first publish. Freshness signalling is most of why we refresh at all — if it silently reports the original date, the whole refresh cycle is wasted work.

### 5.11 Archive and removal semantics

**Decided by brightplace. Three paths, not two:**

| Case | Response | Sitemap |
|---|---|---|
| Content deliberately retired | **410 Gone** | Removed on archive |
| URL never existed | **404 Not Found** | n/a |
| Content replaced by another article | **301** to the replacement | Old URL removed, new one present |

410 tells crawlers the removal is intentional and permanent — Google drops 410s from the index faster than 404s. 404 implies "might come back", which is wrong for retired content.

**The third path is the common one.** Most retirement is really replacement — a 2026 guide superseded by a 2027 one. There a 301 to the successor beats both status codes, because it carries the accumulated equity forward instead of discarding it. So archiving should accept an optional replacement target:

```
blog_change_status(target=article, lifecycle=archived, redirect_to_path?, if_match)
  → no redirect_to_path : URL returns 410, dropped from sitemap
  → redirect_to_path set : URL returns 301 to that path, redirect recorded in redirect_list (§5.6)
```

**Also confirm:** does unpublish (`published_revision_id: null`) differ from archive at the URL? We assume unpublish → 404 (treated as never-published) and archive → 410, but that is a guess.

**Acceptance:** archive without a target → 410 and gone from the sitemap. Archive with a target → 301, and the rule appears in `redirect_list`.

### 5.12 Index submission (nice to have)

Reference §1's GSC section says "brightplace submits sitemaps to GSC manually after deployment." Workable for 10 sites at launch; not for continuous publishing.

**Build:** fire IndexNow on publish, or expose `seo_request_indexing(community_id, url)`. IndexNow is a single keyed HTTP POST and measurably shortens time-to-index on Bing and Yandex. Google Indexing API is more restricted — worth checking whether our content types qualify.


---

## 6. P2 — Pipeline enablement

### 6.1 Community profiles (`profile_*`) — reference §2.10

```
profile_create(community_id, positioning, differentiators[], neighborhood_anchors[{name,time}],
               things_we_never_say[], tour_questions[], resident_feedback)
profile_get(community_id) / profile_update(community_id, ...) / profile_list()
```

**Why.** Our writing agents need each community's positioning, differentiators and — critically — `things_we_never_say` (Fair Housing and brand-safety constraints). That content currently lives only in local `context.md` files on one laptop. It is not versioned server-side, not visible to the dashboard, and not available to any future automated trigger.

`things_we_never_say` is a compliance surface. It should not live in a local file.

### 6.2 Author entity and E-E-A-T

**Decided: one named human author per community — ten in total — not an organization byline.** brightplace will not compromise on E-E-A-T here. Author pages live on each community's own subdomain, so one author record per `community_id` is sufficient.

Important framing for the build: **a bio field on its own does very little.** What Google attaches reputation to is an *entity* — a stable URL, `Person` schema, and an `@id` that every article's `author` field points at. Without that linkage you get a name in a byline with nothing behind it.

**Profile fields** — extend `profile_*` above rather than adding a separate table:

```
author_slug           varchar   -- URL segment
author_name           varchar
author_title          varchar   -- e.g. "Community Manager, Foxchase"
author_bio            text      -- 2-3 sentences
author_photo_asset_id uuid      -- reuse the existing media pipeline
author_credentials    text[]    -- optional
author_sameas         text[]    -- LinkedIn / professional profiles; feeds schema sameAs
```

**Rendering — four surfaces, in order of how much each matters:**

1. **Author page** at `/authors/<author_slug>` carrying `Person` schema with a stable `@id`. This is the piece doing the actual work; without it the rest is decoration.
2. **Article byline that links to that page**, not plain text.
3. **Author card** at the end of every article — photo, name, title, bio, link.
4. **Blog archive/index byline** on each card.

**Article schema change.** Today the CMS emits:

```json
"author": {"@type": "Organization", "name": "AIR Communities"}
```

Required:

```json
"author": {
  "@type": "Person",
  "@id": "https://<community>.brightplace.ai/authors/<author_slug>",
  "name": "...",
  "jobTitle": "...",
  "worksFor": {"@type": "Organization", "name": "AIR Communities"}
}
```

**Default `author_name` from the community profile** rather than accepting it per article. It is free text today and already inconsistent on staging — our articles say "AIR Communities", an existing post says "Foxchase Editorial". Defaulting server-side kills that at the source.

**Reviewer as well as author.** Schema supports `reviewedBy` alongside `author`, and we want both:

- a visible "Reviewed by [Name], [Title] — [date]" line on the article
- `reviewedBy` as a `Person` in the Article schema
- sourced from the existing `last_reviewed_on` field, which we already populate (we set `2026-09-01` on the Foxchase article) and which currently renders as a bare date with nobody attached — a wasted signal

This pattern is also the one that survives scrutiny: brightplace writes, a named community expert reviews. One person can credibly review twenty articles a month; claiming to have written twenty is thinner.

**Sequencing — worth flagging for planning.** This should land **before** we publish the remaining 33 articles. Retrofitting authorship afterwards means re-saving every published revision, and because revision saves are full replaces (§4.6) each one resends a ~20KB body. Doing it first costs nothing extra; doing it later costs a migration.

**Acceptance:** an article's `author.@id` resolves to a live author page carrying matching `Person` schema; the byline links there; the archive card shows the name; omitting `author_name` on save inherits it from the community profile rather than nulling.

### 6.3 Events (`events_*`) — reference §2.11

```
events_list_pending(community_id?)   — omit for all communities
events_list_all(community_id, status, limit) / events_get(id)
events_mark_processed(id) / events_mark_failed(id, error)
```

**Why.** This is the two-way comms layer the entire architecture assumes. Reference §6 opens every workflow with `events_list_pending()`. Without it there is no pipeline — every run is a human manually invoking Claude Code, exactly as today.

Event types per §2.11: `brief_approved`, `article_update_requested`, `article_published`, `content_rejected`, `new_review`, `profile_updated`, `qna_request`, `brief_request`.

**Most valuable first:** `brief_approved` and `article_update_requested`. Those two alone turn dashboard actions into agent work, and would let us close the loop on the brief → article → publish cycle that Phase 2 was supposed to deliver.

Reference §0 notes the events table is designed to carry all three scale phases without a schema change — worth building on the intended shape now rather than retrofitting at 50 communities.

---

## 7. Operational gaps

None of these are in the reference doc, and all three will bite before the backlog ships.

### 7.1 Service account for the agent pipeline

Existing staging posts were created by `service:188snp3fi7ga5idhk1mogokvhq`; ours by a human user principal. Automated runs need a service identity.

1. How do we get one provisioned, per environment?
2. **Should it hold `approver` and `publisher`?** Our account currently holds all five roles, so our agent approves its own work. Fine on staging; questionable for production governance. If community managers are meant to be the approval gate, the agent account probably should not be able to self-approve.

We would rather you set this boundary than have us discover it.

### 7.2 Rate limits

`RATE_LIMITED` appears in the error envelope's code list (reference §2.1). The actual limits are undocumented. Our current backlog is roughly 260 calls and a batch run could exceed whatever the ceiling is. Please publish the limits and state whether they are per-token, per-community or global.

### 7.3 Staging → production promotion

**The biggest unanswered operational question, and it is in neither document.** Once these 34 articles are validated on staging, how do they reach production?

- Re-run the full publish chain against a production MCP endpoint — meaning content is effectively authored twice?
- A promotion tool — `content_promote(community_id, post_id, from_env, to_env)`?
- Database-level sync you handle?

We have no preference. We do need to know **before** we publish 34 articles into staging and find they are stranded there.

---

## 8. Conventions for anything new

Please build new tools in the **idiom you already established**, not the older reference-spec idiom. The live conventions are good and we've adapted to them:

- `community_id` on every call
- `request_key` (UUID) for idempotency on creates
- `if_match` ETag on mutations, with `VERSION_CONFLICT` returning `current_etag`
- Async work returns `{job_id, status}`; caller polls `job_get`. Pending ≠ complete
- Role gating via `operator_context_get` roles (`editor` / `approver` / `publisher` / `media_manager` / `viewer`)
- Envelope: `{success, data, etag, job, page, request_id}`

**One addition we'd like:** document the **role → permitted transition matrix**. The review chain enforces roles, but nothing states which role may perform which transition. We hold all five on our operator account, so we cannot discover the boundaries by testing — we'd just succeed at everything and ship an agent that breaks for a restricted user.

---

## 9. Acceptance tests

Runnable end-to-end once §4 and §5 land:

1. Dry-run validate a body containing an H1 → fails `BODY_NO_H1`, nothing persisted.
2. Trigger any `VALIDATION_ERROR` → `details` names the field and rule.
3. Save a revision with FAQs in both body and array → warning or single render.
4. `blog_preview_post` → returns `preview_url`; opens in a clean browser; drafts still 404 without it.
5. Patch one field on an existing revision without resending `body_markdown`.
6. Publish an article → `seo_get_sitemap` lists its URL with correct `lastmod`.
7. `seo_update_llms_txt` → `curl /llms.txt` shows the new content.
8. `seo_get_robots_txt` → allows all nine bots from reference §1.
9. `seo_validate_page` on the published Foxchase article → PASS.
10. Approve a brief in the dashboard → `events_list_pending()` returns `brief_approved`; `events_mark_processed` stops it reappearing.
11. Change a published article's slug → old path 301s to the new one.
12. Archive a published article → URL returns the documented status (404 or 410) and drops out of the sitemap.
13. Republish an existing article → Article schema `dateModified` and sitemap `lastmod` both move.
14. Archive an article another article links to → `seo_find_broken_links` reports the inbound link.
15. Publish an article → `author.@id` resolves to a live author page carrying matching `Person` schema; byline links there; archive card shows the name.
16. Save a revision omitting `author_name` → inherits from the community profile rather than nulling.

---

## 10. Everything else still to build — shortlist from the reference doc

The sections above cover content, SEO and indexing. This is the **rest of the reference copy doc's tool catalogue**, so you can see the whole remaining surface in one place and sequence it. Not specified here — reference §2 already carries the signatures. Counts are tools, approximate.

**Scale:** 14 tools live · ~25 covered by §4–§7 of this doc · **~67 below.**

| Ref § | Family | Tools | What it unlocks | Reference phase |
|---|---|---|---|---|
| 2.2 | Site management | 3 | `site_list` / `site_get` / `site_update_config` — per-community domain and config state | 1 |
| 2.4 | Blog templates | 2 | `blog_get_template` / `blog_update_template` — layout, typography, CTA blocks, related posts | 3 |
| 2.6 | Social OAuth | 5 | Per-community Instagram/Facebook connection, token refresh, disconnect | 4 |
| 2.7 | Social posts | 7 | Post creation and batching off a published article, scheduling, status | 4 |
| 2.8 | GBP posts, reviews, Q&A, suggestions | ~23 | Google Business Profile content, review replies, seeded Q&A, the weekly suggestion checks | 5 |
| 2.9 | GBP live profile write | 2 | `gbp_get_profile` / `gbp_apply_suggestion` — the accept-a-suggestion-and-it-deploys loop. Needs a broader OAuth scope than posting; see reference §10.4 | 5 |
| 2.12 | Stats, per-community | 10 | Blog/social/GBP metrics, SEO visibility, leads, attribution, AI citations, traffic | 3+ |
| 2.13 | Portfolio rollup | 1 | `stats_portfolio_overview` — the portfolio Home screen. Nothing aggregates across communities today | 8 |
| 2.14 | Insight + attention feed | 7 | `insight_*` / `attention_item_*` — agent-authored narrative cards the dashboard renders | 8 |
| 2.15 | Site theme + non-blog pages | 7 | `site_*_theme`, `page_*` — homepage, floor plans, amenities, neighbourhood, contact. **Currently zero MCP surface despite being most of each site** | 9 |

**Three notes on sequencing, from our side:**

- **§2.15 is bigger than its phase number suggests.** Property pages are most of each site's crawlable surface and most of its conversion path, and no agent can touch any of it. Once blog content is flowing, this is the next real lever — arguably ahead of social and GBP.
- **§2.12 stats has a dependency nobody has resolved.** Reference §10.2 leaves GA4 as an open question. Our view: make GA4 a fourth `source` in `seo_visibility_snapshots` rather than a separate `stats_ga4` tool — one shared property filtered by hostname is already the design, and a separate tool implies separate properties.
- **§2.8 is the largest single block (~23 tools) and the one with the most external dependency.** Worth splitting: reviews and Q&A deliver value early; the suggestion engine and live profile write can follow.

**Also outstanding from the reference doc, not tools:**

- **§3 database:** `site_pages`, `portfolio_insights`, `attention_items` — three tables backing §2.13–2.15.
- **Reference §10.3 — listings, floor plans, pricing, availability.** Flagged there as undecided, and it is quietly a content problem as well as a property-page one: our published articles quote specific rents (`$1,487`, `$2,484`) that go stale with no feed behind them. Today that means manual rewrites across 34 articles. Worth resolving sooner than its phase implies.

---

## 11. Questions — answered and outstanding

### Answered by brightplace (16 Sep 2026)

| # | Question | Answer | Lands in |
|---|---|---|---|
| 1 | Does `publication_reconcile` update sitemap and RSS? | **Yes.** No manual sitemap CRUD for articles; read access still needed to verify | §5.2 |
| 2 | Featured image — exact or minimum? | **Minimum + server-side downscale.** Low-stakes | §4.4 |
| 3 | `seo_title` / `meta_description` caps | **Follow the documented best practice: 60 / 160.** Align the API to the schema; flexible if there is a stated reason | §2 |
| 5 | Author coverage model | **One named author per community, ten total.** Real people; pages on each community subdomain | §6.2 |
| 6 | Can `slug` change after publish? | **Yes** — which makes auto-301-on-change mandatory, not optional | §5.6 |
| 7 | Archived URLs — 404 or 410? | **410 archived · 404 never-existed · 301 when replaced.** Third path is the common one | §5.11 |

### Outstanding — for Tom

1. **Vercel automation bypass secret.** Is there one we can hold? Distinct from the signed `preview_url` in §4.5 and solving a different problem: a revision-scoped preview token cannot fetch `/sitemap.xml`, `/robots.txt` or `/llms.txt`. Today we cannot verify any of those, or confirm our own published article renders. This is the single ask that unblocks the most verification.
2. **Rate limits.** `RATE_LIMITED` is in the error envelope (reference §2.1) but the limits are undocumented. Our backlog is ~260 calls. Per-token, per-community or global?
3. **Unpublish vs archive at the URL.** We assume unpublish → 404, archive → 410 (§5.11). Please confirm.
4. **Anything in §10 already in flight?** So we don't double-spec it.

### Outstanding — brightplace's own calls

1. **Staging → production promotion.** Our recommendation is that Tom builds *nothing* here: the source of truth is markdown on disk, so promotion is re-running the publish chain against a production endpoint, not re-authoring. We need a production endpoint, credentials, and confirmation that `community_id` values match across environments. Confirming this removes work from the backlog rather than adding it.
2. **Should the agent account self-approve in production?** Our operator holds all five roles, so the agent approved its own article on staging. If community managers are the intended approval gate, the agent should hold `editor` only and stop at `in_review`. No default — needs a deliberate call.

---

## 12. Suggested build order

| # | Item | Section | Effort | Unblocks |
|---|---|---|---|---|
| 1 | Error `details` | 4.1 | Hours | Every future debugging session |
| 2 | `llms.txt` tools | 5.1 | Small | A required step in our own documented pipeline |
| 3 | `seo_get_sitemap` (read) | 5.2 | Small | Verifying published content is indexable — writes not needed for articles |
| 4 | Redirects + **auto-301 on slug change** | 5.6 | Medium | Slugs are mutable — without this every edit breaks a live URL |
| 5 | Validator check codes + dry-run | 4.2 | Medium | Batch-linting 33 drafts before creating posts |
| 6 | Signed `preview_url` + automation bypass | 4.5, §11 | Small | Review model, and verifying our own output |
| 7 | FAQ dedupe/warning | 4.3 | Small | Stops duplicate content shipping |
| 8 | `robots.txt` read | 5.3 | Small | Verifying AI crawlers aren't blocked |
| 9 | `profile_*` | 6.1 | Medium | Gets compliance rules off a local laptop |
| 10 | **Author entity + `Person` schema** | 6.2 | Medium | E-E-A-T — and must land *before* the 33-article backlog |
| 11 | `seo_find_broken_links` | 5.7 | Medium | Link rot across 34 cross-linked articles |
| 12 | Archive → 410 / 301-to-replacement | 5.10–5.11 | Small | Retirement and replacement without losing equity |
| 13 | Revision patching | 4.6 | Medium | Stops 20KB resends per edit |
| 14 | `events_*` | 6.3 | Large | Converts manual CLI runs into a pipeline |
| 15 | Batch ops | 4.8 | Medium | Scaling past ~10 articles per session |
| 16 | `seo_validate_page` + page meta | 5.4–5.5 | Medium | Property pages, currently unvalidated |
| 17 | Canonical override · RSS · IndexNow | 5.8–5.9, 5.12 | Small each | Duplicate content and time-to-index |

**Items 1–3 are the ones we'd most like next.** The first costs hours and pays back on every subsequent call; the next two close the gap between "we published an article" and "the article is discoverable."

**Item 10 is the one with a deadline attached.** Everything else can land after the backlog ships. Author entity cannot — publishing 33 articles under an Organization byline and converting them later means re-saving every revision.

---

*Grounded in a verified staging publish on 16 Sep 2026: post `e7052535-da91-4a74-a766-d071d3c3b55e`, revision `cb78ef0c-f2ac-4063-a0ce-f82839ca214d`, validation 13/13, `publication_reconcile` succeeded. Every behaviour described in §2, §3 and §4 was observed directly, not inferred.*
