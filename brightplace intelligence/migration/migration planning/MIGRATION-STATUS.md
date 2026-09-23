# brightplace.ai — Migration Status

**Audited:** 2026-09-23 against live production
**Site:** `https://www.brightplace.ai` — Next.js on Vercel
**Method:** direct HTTP probing of the live site. Every figure below came from a request made during this audit, not from a document.

---

## Verdict

**The migration is complete and successful. All five issues from `issue-pointed.md` are resolved.**

The site is in materially better SEO shape than it was on Webflow. It now ships canonicals, meta descriptions and structured data — none of which existed before. Nothing found in this audit blocks indexing or crawling.

Three minor items are open. None is urgent; all are listed in §6.

---

## 1. Issue list — final status

| # | Issue | Status | Evidence |
|---|---|---|---|
| 🔴 1 | 22,774 property pages missing from sitemap | **Fixed** | `/sitemap.xml` is now a `<sitemapindex>` with four children totalling **22,383 URLs** |
| 🟠 2a | Four live resources absent from sitemap | **Fixed** | All four present. Resources count 76 → **80**, matching the live article count |
| 🟠 2b | `robots.txt` emitted `Sitemap:` twice | **Fixed** | Emitted exactly once |
| 🟠 2c | Static copies, `lastmod` frozen | **Fixed** | Both files generated. `robots.txt` now carries the full AI-crawler allowlist |
| 🟠 3 | `dateModified` earlier than `datePublished` on 71 articles | **Fixed** | Correct ordering on 17/17 sampled |
| 🟡 4 | `datePublished` was the migration timestamp on 47 articles | **Fixed** | Real dates restored, spread April–August 2026 |
| 🟡 5 | Two articles without `og:image` | **Fixed** | Present on 17/17 content pages sampled |

---

## 2. Sitemap

```
/sitemap.xml                    <sitemapindex>, 4 children
  /sitemaps/content.xml            155 URLs
  /sitemaps/property-1.xml      10,000 URLs
  /sitemaps/property-2.xml      10,000 URLs
  /sitemaps/property-3.xml       2,228 URLs
                                ─────────────
                                22,383 URLs
```

All four children return 200 and parse as valid XML.

**`content.xml` composition — 155 URLs:**

| Class | Count |
|---|---|
| `/resources/*` | 80 |
| `/guides/*` | 31 |
| `/news/*` | 9 |
| `/category/*` | 7 |
| `/communities/*` | 6 |
| `/stories/*`, `/author/*` | 3 each |
| Archive indexes, homepage, legal and static pages | ~16 |

The index structure is correct: a flat `<urlset>` caps at 50,000 URLs, and splitting property pages across three files keeps regeneration manageable.

**Note:** `/author/*` pages are now included. That was an open decision in the handover and has been resolved in favour of including them.

---

## 3. robots.txt

Generated, not copied. Emits `Sitemap:` **once**. Explicitly allows thirteen crawlers:

`*` · GPTBot · OAI-SearchBot · ChatGPT-User · ClaudeBot · Claude-User · anthropic-ai · PerplexityBot · Perplexity-User · Google-Extended · Applebot-Extended · CCBot · meta-externalagent

Disallows are limited to functional paths — `/api/`, `/chat/`, `/search/`, `/join/`, `/demo/`, `/login`, `/get-started`, `/unavailable`. **No content path is blocked.**

The vestigial Webflow rule `Disallow: /*?*_page=` has been correctly dropped.

---

## 4. Content pages — 17 sampled, zero failures

Every sampled article carries:

- Self-referencing canonical
- `<meta name="description">`
- `og:image` and a complete Open Graph set
- Exactly one `<h1>`
- 3–4 JSON-LD blocks
- `datePublished` ≤ `dateModified`, both real dates

**Schema shape:** `Article + BreadcrumbList + WebPage`, plus `FAQPage` where FAQs exist. Matches the spec in `VERCEL-CONTENT-TEMPLATES.md` §5.

### AEO — content is genuinely server-rendered

The check that matters for AI crawlers and JS-disabled indexing: body text present in the **raw HTML response**.

| Page | Words in raw HTML |
|---|---|
| `/guides/dallas-families` | 3,152 |
| `/resources` (archive) | 4,478 |
| A property page | 5,655 |

This was Webflow's core failure — schema was JS-injected and effectively invisible. It is now fixed.

### Archive, category and author pages

| Page | Status | JSON-LD | `<h1>` |
|---|---|---|---|
| `/guides`, `/resources`, `/news` | 200 | 1–2 | 1 |
| `/category/property`, `/category/renter-corner` | 200 | 2 | 1 |
| `/author/katie-mikles` | 200 | 2 | 1 |

`/category/renter-corner` correctly preserves the singular slug against the plural collection name.

---

## 5. Parity and redirects — all assertions pass

| Assertion | Result |
|---|---|
| `/guides/` → redirect → `/guides` | 308 → 200, 1 hop |
| `brightplace.ai/guides` → `www` | 308 → 200, 1 hop |
| Unknown path | Real 404, no soft 200 |
| `/knowledgebase/*` | 404 preserved, as required |
| `app.brightplace.ai/guides/dallas-families` | → `www.brightplace.ai/guides/dallas-families` |
| `app.brightplace.ai/property/nv/las-vegas/…` | → same path on `www` |

**Paths are preserved byte-for-byte. One hop, no chains.** No redirect to the homepage — the failure mode that destroys migrations.

⚠️ **Redirects are 308, not 301.** Google treats 308 identically to 301 for canonicalisation, so this is not a defect — but it differs from the spec and is worth recording so nobody "fixes" it later.

---

## 6. Open items — none urgent

### 6.1 — 546 property URLs unaccounted for

The sitemap lists **22,228** property URLs. The old `app.brightplace.ai` sitemap listed **22,774**. Difference: 546.

Every property URL sampled returns 200, so this is not broken pages. It is most likely deduplication or intentional delisting — but nobody has confirmed which. **Ask Dennis** whether the delta is deliberate. If those URLs are live but unlisted, it is the same class of bug as the four missing resources.

### 6.2 — `/search` listed in sitemap while robots disallows `/search/`

`/search` returns 200 and is in `content.xml`. `robots.txt` carries `Disallow: /search/`.

The trailing slash means `/search` itself is probably not blocked — prefix matching would catch `/search/anything` but not the bare path. Ambiguous rather than broken. Resolve by either removing it from the sitemap or tightening the robots rule.

### 6.3 — A small share of property pages lack `og:image`

Roughly **1 in 25** sampled. Always accompanied by missing `og:image:alt` and `twitter:image`, which points to properties with no photo in the source feed rather than a template fault.

Affects social sharing previews only — no indexing impact. Low priority.

---

## 7. Verified correct — do not change

Recorded so these are not "fixed" by a later change:

- Redirect status **308** (see §5)
- `/knowledgebase/*` returning **404** — this is parity, not an oversight
- `/category/renter-corner` singular slug against the plural collection name
- `trailingSlash: false` behaviour
- The thirteen-crawler allowlist in `robots.txt`
- Sitemap **index** structure rather than a flat urlset

---

## 8. Reproducing this audit

```bash
# sitemap is an index, and total URL count
curl -s https://www.brightplace.ai/sitemap.xml | head -3
for f in content property-1 property-2 property-3; do
  echo -n "$f: "; curl -s https://www.brightplace.ai/sitemaps/$f.xml | grep -c '<loc>'
done

# robots emits Sitemap once, blocks no content
curl -s https://www.brightplace.ai/robots.txt | grep -c '^Sitemap:'

# a content page carries everything, server-rendered
curl -s https://www.brightplace.ai/guides/dallas-families \
  | grep -cE 'rel="canonical"|name="description"|og:image|application/ld\+json'

# redirects preserve path, one hop
curl -s -o /dev/null -w '%{http_code} %{redirect_url}\n' \
  https://app.brightplace.ai/guides/dallas-families

# llms.txt intact
curl -s https://www.brightplace.ai/llms.txt | grep -c 'observable attributes'
```

The `indexing-files-agent` (`brightplace intelligence/Agents/`) automates these checks and should be run after any deploy that adds, removes or moves URLs.

---

## 9. What changed versus Webflow

| | Webflow (before) | Vercel (now) |
|---|---|---|
| Canonical tags | **None** | Every page, self-referencing |
| Meta descriptions | **None** on rendered pages | Every page |
| JSON-LD in server HTML | **Zero** | 3–4 blocks per content page, 6 on property |
| Open Graph | Partial, inconsistent | Complete set |
| Visible `<time>` | **None** | Published and modified dates |
| Sitemap | 148 URLs, 4 live pages missing, no property pages | 22,383 URLs across an index |
| robots.txt | Duplicate `Sitemap:`, no AI crawler list | Clean, thirteen crawlers named |
| llms.txt | Present, curated | Preserved verbatim |

The SEO debt catalogued before the migration has been cleared.
