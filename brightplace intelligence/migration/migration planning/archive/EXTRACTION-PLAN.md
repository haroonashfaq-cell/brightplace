# Webflow Content Extraction — Execution Plan

**Version 3 · 2026-09-17** · plan only, nothing extracted yet

Deliver every Resource and every Guide as three flat files — markdown, HTML, image.

**In scope:** Resources content · Guides content · featured images
**Deferred:** HTML design templates · per-item rendered `page.html` · sitemap/robots/llms.txt ·
GA4 and Search Console tags. These come after the content is assembled.

---

## 1. Target structure

Flat per collection, named by slug:

```
brightplace intelligence/migration/extract/
├── resources/
│   ├── how-to-rent-an-apartment.md
│   ├── how-to-rent-an-apartment.html
│   ├── how-to-rent-an-apartment.jpg
│   ├── what-is-a-guarantor-on-a-lease.md
│   ├── what-is-a-guarantor-on-a-lease.html
│   └── …
├── guides/
│   ├── atlanta-active-renters.md
│   ├── atlanta-active-renters.html
│   ├── atlanta-active-renters.jpg
│   └── …
└── reports/
    ├── coverage.md            what came from where, and what is missing
    └── divergence.md          local .md vs published CMS body
```

**On the image extension.** The example said `.png`, but Webflow's actual featured images are
`.jpg` and `.webp` — e.g. the Atlanta guide's is
`69e2216182ba55b65fbcda5e_atlanta-CI1rrwUO.jpg`. Files keep their **real** extension so they are
not corrupt-on-open. Slug stays the filename: `atlanta-active-renters.jpg`.

---

## 2. What already exists locally — measured, not assumed

Checked against the 76 live Resource and 31 live Guide URLs in the sitemap.

### Resources (76 live)

| Asset | Source | Have | Missing |
|---|---|---|---|
| `.md` | `brightplace intelligence/Complete Articles/` | **71** | 5 |
| `.html` | `brightplace intelligence/Webflow CMS Data/` | **64** | 12 |
| image | — | **0** | **76** |

### Guides (31 live)

| Asset | Source | Have | Missing |
|---|---|---|---|
| `.md` | `brightplace intelligence/Guide Articles/Complete Articles/` | **30** | 1 |
| `.html` | `brightplace intelligence/Guide Articles/Webflow CMS Data/` | **3** | 28 |
| image | — | **0** | **31** |

The single guide missing markdown is **`austin-north-central-renters`**.

**This is much better than the earlier estimate.** A previous pass reported "0 of 31 guides
present" because it only looked at the top-level `Webflow CMS Data/`. The guide markdown lives in
the **nested** `Guide Articles/Complete Articles/` folder — 34 files, 30 of which match live
slugs.

So the MCP pull is scoped to the gap, not the whole corpus:

| Needs pulling from Webflow | Count |
|---|---|
| Resource `.md` | 5 |
| Resource `.html` | 12 |
| Guide `.md` | 1 |
| Guide `.html` | 28 |
| **All images** | **107** |

---

## 3. The risk in using local files

Local `.md` files are the **writing-stage source**. The Webflow CMS holds what was **actually
published** — and articles can be edited in Webflow after the markdown was written. The two can
disagree.

This is not hypothetical: an earlier comparison found the local export disagreeing with the CMS on
several files.

**So the CMS is authoritative for `.html`.** Local HTML is used only where the CMS pull is not
needed, and every reused local file is checked against the CMS body. `reports/divergence.md`
lists every mismatch for a per-item decision. Local `.md` is kept as the readable version, with
divergences flagged rather than silently resolved.

If a divergence check shows widespread drift, the fallback is to pull all 107 bodies from MCP and
regenerate markdown from them. Decide that after Phase 2, on evidence.

---

## 4. Images

Featured images come from the CMS `main-image` field, **not** from scraping live pages — a page
scrape returns site chrome (logo, social icons, favicons) mixed with content images, which is how
you end up with 107 copies of the TikTok icon.

Confirmed by sampling:
- Guide `atlanta-active-renters` → has a featured image, served in responsive variants
  (`-p-500`, `-p-1080`, `-p-1600`). **Take the original, not a variant.**
- Resource `113-university-place` → no featured image at all; the test CMS fetch likewise returned
  `main-image: null`.

**Expect many Resources to have no image.** Those simply get no image file, and the coverage
report records it. That is a real finding about the content, not an extraction failure.

---

## 5. Extraction method

**The constraint:** one Resource item is ~14KB of CMS payload. Pulling 107 through the assistant's
context would be ~1.5MB and would truncate.

**The mechanism:** oversized MCP responses are auto-persisted to a JSON file on disk, with only a
short preview returned inline. Verified — a 65KB response persisted exactly this way.

```
 1.  MCP list_collection_items, batches of 25, offset stepping
        ↓  response exceeds inline threshold
 2.  auto-persisted to disk at full fidelity
        ↓
 3.  local script reads the JSON
        ↓
 4.  writes <slug>.md / <slug>.html, and downloads <slug>.<ext>
        ↓
 5.  coverage script diffs output against the live sitemap
```

4 batch calls for Resources (86 staged), 2 for Guides (31). Nothing truncated, context stays flat.

| Collection | ID | Staged | Live |
|---|---|---|---|
| Resources | `69fcfcef26d35b66ba874f9d` | 86 | 76 |
| Guides | `69dccfeabed64ec697c4f7d2` | 31 | 31 |
| Categories | `69df6e40b18552d426ddd816` | 7 | — |
| Authors | `69dcd5b9150dec1c53e3e8de` | 3 | — |

Staged exceeds live because **drafts are mixed in** — a test fetch returned an item with
`isDraft: true, lastPublished: null`. Filtering is mandatory.

---

## 6. Phases

### Phase 0 — Skeleton and lookups
- Create `extract/resources/`, `extract/guides/`, `extract/reports/`.
- Pull Categories (7) and Authors (3); build the ID → name lookup, since `author-2` and
  `category-2` come back as raw IDs.
- **Gate:** all 10 IDs resolve to names.

### Phase 1 — Guides (the real gap)
Guides first, because 28 of 31 HTML files are missing — this is where the work actually is.
1. Pull all 31 guide items from MCP in 2 batches.
2. Write `<slug>.html` from `post-body` for all 31.
3. Copy the 30 local `.md` files across; generate the 1 missing
   (`austin-north-central-renters`) from its CMS body.
4. Download each `main-image` original → `<slug>.<ext>`.
- **Gate:** 31 `.html`, 31 `.md`, and every guide with a non-null `main-image` has its image file.

### Phase 2 — Resources
1. Pull all 86 Resource items from MCP in 4 batches; filter drafts and archived.
2. Copy the 71 local `.md`; generate the 5 missing from CMS bodies.
3. Write the 12 missing `.html` from CMS; **verify the 64 local ones against the CMS body**.
4. Download available `main-image` originals.
- **Gate:** 76 `.md`, 76 `.html`, images for every item that has one.

### Phase 3 — Reports
- `coverage.md` — per item: `.md` source (local/CMS), `.html` source, image present y/n, draft y/n.
  Must reach **107/107** on `.md` and `.html`.
- `divergence.md` — every local file that disagrees with the CMS, with a recommendation per item.
- **Gate:** coverage 100%; every divergence listed and triaged.

---

## 7. Volume

| | `.md` | `.html` | images | total |
|---|---|---|---|---|
| Resources | 76 | 76 | ≤76 | ~200 |
| Guides | 31 | 31 | ≤31 | ~90 |
| Reports | — | — | — | 2 |
| **Total** | **107** | **107** | **≤107** | **~292** |

---

## 8. Deferred — do not lose track of these

| Item | When it becomes urgent |
|---|---|
| HTML design templates (Guides, Resources) | Before the developer builds layouts |
| Per-item rendered `page.html` | **Before Webflow is cancelled** — the only record of how pages rendered |
| sitemap.xml · robots.txt · llms.txt | Before cutover. Note `/llms.txt` already exists (4,144 bytes) — capture, don't rewrite |
| GA4 (`G-DK6QHHS88K`) + Search Console | **Before DNS moves**, or analytics goes dark and GSC loses verification |
| Image binaries beyond featured images | Before Webflow cancellation, or in-body images 404 |

---

## 9. Confirm before execution

1. **Drafts** — Resources has ~10 drafts among its 86. Skip them (recommended — they are not live
   pages), or extract with a `draft` marker?
2. **Frontmatter in `.md`** — add YAML frontmatter (title, slug, URL, SEO title, meta description,
   category, author, dates) to each markdown file, or keep the files exactly as they are locally?
   **Recommendation: add it** — otherwise the URL and SEO fields exist nowhere in the handoff.
3. **Local vs CMS on divergence** — default to CMS (what is actually published), flagging the
   difference? **Recommendation: yes.**
