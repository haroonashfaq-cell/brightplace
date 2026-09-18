# brightplace CMS MCP — Gap Register

What the AIR operator content pipeline needs that the CMS MCP does not yet provide.

**Compiled:** 2026-09-18 · **Against:** renderer `article-v4`, validator `cms-v2`, 24 MCP tools
**Method:** every item marked VERIFIED was reproduced this session by publishing real
articles to the `citigate` staging community and reading the rendered output. Items marked
INFERRED are reasoned from evidence but not directly proven — they are labelled so nobody
treats them as confirmed.

---

## P0 — Blockers (content is being shipped degraded today)

### Renderer: no list support
- [ ] **`- bullet` lists do not render.** Each item flattens into its own `<p>`. No `<ul>`,
      no `<li>` anywhere in the output. `VERIFIED` (probe revision, article-v4)
- [ ] **`1.` ordered lists do not render, and leak.** Same flattening, plus the literal
      "1." survives into the visible text. `VERIFIED`
- [ ] **Markdown tables render as raw pipe characters.** `| Item | Cost |` ships visible
      `|` to readers. This is worse than no table. `VERIFIED`
- [ ] Corroboration: the served stylesheet defines **no `ul`, `ol`, `li`, `table`, `th` or
      `td` rules at all** — consistent with these constructs never having been implemented.

**Impact:** cost breakdowns, amenity lists, and "who this suits" sections all ship as runs
of disconnected bold paragraphs. Costs list-snippet eligibility in Google, and breaks the
parent/child relationship AI extractors rely on. Affects every article across all ten
communities. Writers are currently working around it (see `seo-writing-agent.md`), and that
workaround should be deleted the day this ships.

---

## P1 — High (materially limits SEO ceiling)

### Structured data: no way to submit any
- [ ] **No schema tool exists.** `blog_save_post` has no schema parameter and none of the 24
      tools accepts JSON-LD. `VERIFIED`
      *Contrast: the Webflow MCP exposes `bulk_update_pages_schema_markup` and
      `query_pages_schema_markup`. This one deliberately does not.*
- [ ] `Article` is missing `publisher`, `description`, `mainEntityOfPage`. `VERIFIED`
- [ ] `author` emits as a bare `{"@type":"Organization","name":"..."}` — no `url`, `@id` or
      `sameAs`. `VERIFIED` (partially addressable today via `author_save` + `author_id`)
- [ ] `WebPage` is missing `isPartOf`, `primaryImageOfPage`, `datePublished`. `VERIFIED`
- [ ] **No property-type schema at all** — no `ApartmentComplex`, `Residence` or
      `LocalBusiness`, despite every site being an apartment community. `VERIFIED`
- [ ] **No `PostalAddress`, `geo` or `telephone`** — the community address sits in the page
      footer as plain text and is never marked up. `VERIFIED`
- [ ] No `priceRange` or `Offer`, despite every article citing rent ranges. `VERIFIED`

**Do NOT add `AggregateRating`.** Articles cite resident review counts, which makes this
look like an easy win. Self-serving review markup on your own property violates Google's
structured-data guidelines and risks a manual action. Flagged here so it is rejected rather
than rediscovered.

**Also note:** `FAQPage` is emitted correctly but earns no rich result on a commercial site
(Google restricted FAQ rich results to gov/health in Aug 2023). Keep it — answer engines
parse it — but do not expect SERP real estate from it.

- [ ] **Heading anchor ids absorb markdown link URLs.** A heading containing a link, e.g.
      `## What Is [Jacksonville's](https://www.coj.net/) Southside Like...`, produces the id
      `what-is-jacksonville-s-https-www-coj-net-southside-like-for-healthcare-workers` — the
      URL is slugified straight into the anchor. Pollutes in-page anchors, TOC links and any
      deep link. The slug generator should use the heading's visible text only. `VERIFIED`
      (live on the Mayo Clinic article). *Content-side workaround until fixed: never put a
      link inside an H2/H3.*

### Article template (UI)
- [ ] **Column widths do not match.** `main` is `max-width:1120px`, `.prose` is
      `max-width:760px; margin:auto`. H1, summary, byline and hero render at 1120px while
      body text sits at 760px centred — left edges do not align. `VERIFIED`
- [ ] **`blockquote` renders but is entirely unstyled.** No `blockquote` rule exists in the
      CSS, so it shows as a plain browser indent. The first-party disclosure block now on
      every article uses this construct and currently has no visual treatment. `VERIFIED`
- [ ] H1 is display-scale: `clamp(2.3rem, 5vw, 3.7rem)` (~59px) over a 760px measure.
- [ ] Links have no colour affordance (`a { color: inherit }`) — inline citations are hard
      to spot while scanning.
- [ ] FAQ section has no visual treatment: ten Q&As as bare `h3`/`p`. Accordions or cards
      would make the most deep-linked section scannable.
- [ ] No table of contents, despite every heading already carrying an anchor id.
- [ ] No visible breadcrumb, despite `BreadcrumbList` schema being emitted.
- [ ] No dark mode — zero `prefers-color-scheme` rules.
- [ ] **Dead CSS worth triaging:** `.author-card`, `.author-photo`, `.cards`, `.pagination`
      are all defined but never emitted on an article page. Suggests an author bio block and
      a related-posts row exist but are not shipping. Confirm before rebuilding either.

---

## P2 — Medium (ergonomics, docs, and workflow friction)

### Tool-description gaps that cause real errors
- [ ] **Full-snapshot semantics are undocumented.** `blog_save_post` clears every optional
      field you omit. Omit `faqs` on a one-word body fix and they are silently gone, and the
      next approval fails on `REQUIRED_FAQS`. This is a data-loss footgun and belongs in the
      tool description, not just the workflow doc. `VERIFIED`
- [ ] **ETag target is ambiguous.** `blog_change_status` with `target: "revision"` needs the
      *revision* ETag; `target: "article"` needs the *article* ETag. The description says
      only "Requires current ETag". `VERIFIED`
      *(Credit where due: the `VERSION_CONFLICT` error returns the correct value in
      `details.current_etag`. That is good design — it just is not documented.)*
- [ ] **`draft → approved` is rejected** as `INVALID_STATE`; `in_review` cannot be skipped.
      Undocumented. `VERIFIED`
- [ ] **Publication validation runs at approval, not publish.** An article cannot be approved
      until its hero image exists and is `ready`. This inverts the normal review-then-artwork
      order and surprises every new user. `VERIFIED`
- [ ] **Self-approval is permitted** — the same identity can submit and approve. Worth
      documenting explicitly so nobody assumes two-person review is enforced. `VERIFIED`

### Validation check inventory is out of sync
- [ ] `HEADING_HIERARCHY` is documented as a publication check but was **never returned** in
      any validation response observed. `VERIFIED` (absent from all 12 checks returned)
- [ ] `CANONICAL_HOST` **is** returned but appears in no documentation. `VERIFIED`
- [ ] `DUPLICATE_FAQ_SECTION` (severity `warning`) exists and fires correctly, but is
      undocumented. Triggered when an FAQ duplicates a body H2. `VERIFIED`

### Missing operations
- [ ] **No author list.** `author_get` requires an `author_id` or `slug`; there is no way to
      enumerate existing author profiles for a community. `VERIFIED` (no list tool exists)
- [ ] **No in-place media replacement.** Swapping a hero means creating a new asset; the old
      one is orphaned but cannot be deleted while any historical revision still references
      it. Three assets accumulated on one article this session. `VERIFIED`
- [ ] No bulk publish across articles. `blog_change_status` accepts `items` for status ops —
      confirm whether that covers publish. `INFERRED`
- [ ] `page_overrides` in `seo_save` cannot override generated blog pages (the tool states
      generated blog links are not overridable), so per-article title/description/canonical
      overrides are unavailable for blog content. `INFERRED` — not tested.
- [ ] No per-article `noindex` control. `INFERRED`
- [ ] No sitemap `priority` / `changefreq`, no `hreflang`. `INFERRED`

### Preview fidelity
- [ ] **The preview template differs from the published template.** Published pages add an
      RSS link, `og:site_name`, header/nav/footer, and a visible `<time>`; preview adds
      `referrer: no-referrer`. Reviewers approving from preview are not seeing the live page.
      `VERIFIED`

---

## Verified NOT gaps — do not re-litigate

These were suspected problems that testing cleared. Recorded so nobody spends time on them.

- **`noindex` is not a bug.** `seo_get` returns `stage: "nonprod"`, `robots_protected: true`,
  and the stored production rule is already `allow: /`. Staging robots is protected
  server-side. `VERIFIED` for robots.txt; the page-level `<meta robots>` is strongly inferred
  from the same gate — confirm on the first production render to close it fully.
- **Dates populate correctly.** Once published, `datePublished`, `dateModified` and `image`
  all fill in, plus `og:image` with width/height/alt and `article:published_time`. The
  missing-dates problem seen on the current Webflow site does not recur here. `VERIFIED`
- **`---` horizontal rules work**, rendering `<hr>`. An earlier version of
  `CMS-Publishing-Workflow.md` claimed the CMS rejects them. That was false. `VERIFIED`
- **A full article can be created in one call.** The same doc advised creating with a
  placeholder body then saving content as a second revision. Unnecessary — a 1,575-word body
  with 10 FAQs succeeded on creation. `VERIFIED`
- **Media pipeline works end to end from an MCP client.** create → presigned S3 PUT → process
  → poll ready, producing hero + inline WebP variants on CloudFront. ~1 second. `VERIFIED`
- **`llms.txt` generation works** and accepts a full intro plus up to 20 sections via
  `seo_save`. It is empty by default, which is a content task, not a platform gap. `VERIFIED`

---

## Suggested order of work

1. **List and table rendering** (P0) — unblocks correct content on every article, every
   community, and lets the writer-agent workaround be deleted.
2. **`blockquote` styling** (P1, small) — a disclosure block is already live on three
   articles with no visual treatment.
3. **Column-width fix** (P1, two lines of CSS) — the most visible layout flaw.
4. **Schema expansion** (P1) — `publisher`, `mainEntityOfPage`, author identity, and a
   property type with `PostalAddress`. Biggest SEO ceiling lift after lists.
5. **Tool-description corrections** (P2, docs only) — full-snapshot semantics and ETag
   targets prevent real data loss and real failed calls.
6. **Validation check inventory** (P2) — align docs with what the validator actually returns.
