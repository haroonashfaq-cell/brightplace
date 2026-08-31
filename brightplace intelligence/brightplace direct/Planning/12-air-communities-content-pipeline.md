# 12 — AIR Communities Content Pipeline: How Data Travels

## The Real Problem

Right now articles are **React components hardcoded in TypeScript**. Look at `stories.tsx`:

```tsx
content: HarpersPointArticle,  // This is a function that returns JSX
```

This means to publish an article, you need to:
1. Write a React component
2. Import it in TypeScript
3. Add it to the stories array
4. Build the project
5. Git push

**This is NOT a CMS. This is code. And code can't be written through an API.**

---

## The Fix: Separate Content from Code

### Current Architecture (Broken for Scale)

```
Content lives as → React components in .tsx files → requires code deploy to publish
```

### Required Architecture (Works for Scale)

```
Content lives as → JSON/Markdown files or database rows → read at build time → no code changes needed
```

---

## What Tom & Dennis Need to Build

### Change 1: Articles as Markdown Files (Not React Components)

**Instead of this (current):**
```
src/data/stories.tsx (hardcoded React components)
```

**Build this:**
```
content/
  air-communities/
    oak-trail-cherry-creek-guide.md        ← markdown file
    oak-trail-cherry-creek-guide.json      ← metadata file
    lakeview-gateway-park-guide.md
    lakeview-gateway-park-guide.json
    one-canal-boston-guide.md               ← NEW — we create this
    one-canal-boston-guide.json
```

**The .md file contains:**
```markdown
Oak Trail at Cherry Creek South is a 384-unit apartment community...

## What is all-in pricing at Oak Trail?

All-in pricing means every listed price includes base rent plus...

[CTA: See all Oak Trail amenities](/air-communities/oak-trail#amenities)

## How much does it cost to live at Oak Trail?

| Floor Plan | Beds/Bath | Sq Ft | Price |
|---|---|---|---|
| Design 1A | 1bd/1ba | 678 | $1,512/mo |
...
```

**The .json file contains:**
```json
{
  "title": "Oak Trail at Cherry Creek South: Pricing and Guide",
  "slug": "oak-trail-cherry-creek-guide",
  "metaTitle": "Oak Trail Cherry Creek South: Pricing | brightplace",
  "metaDescription": "Oak Trail at Cherry Creek South offers 7 floor plans...",
  "operator": "air-communities",
  "property": "oak-trail",
  "primaryKeyword": "Oak Trail at Cherry Creek South",
  "secondaryKeywords": ["cherry creek apartments", "apartments near cherry creek state park"],
  "author": "brightplace Research",
  "datePublished": "2026-08-28",
  "dateModified": "2026-08-28",
  "readTime": "7 min",
  "thumbnail": "/images/air-communities/story-cherry-creek.jpg",
  "featuredImage": "/images/air-communities/oak-trail-hero.jpg",
  "faqs": [
    {
      "question": "What is all-in pricing at Oak Trail?",
      "answer": "Every listed price includes base rent plus required monthly fees..."
    }
  ]
}
```

**Why this works:** We can create .md and .json files through the GitHub API without touching any code. The Next.js app reads these files at build time and renders them as pages.

### Change 2: Dynamic Page That Reads Markdown

Tom & Dennis build ONE page component that reads any markdown file:

```
src/app/[operator]/[slug]/page.tsx
```

This page:
1. Checks if `slug` matches a property JSON → renders property page
2. Checks if `slug` matches an article JSON in `content/[operator]/` → renders article page
3. Converts markdown to HTML at build time
4. Auto-generates JSON-LD from the metadata JSON
5. Uses the StoryLayout component for rendering

**Key:** The page component NEVER changes. Only the content files change.

### Change 3: Auto-Discovery of Content Files

```typescript
// In the data layer
function getAllArticles(operator: string): Article[] {
  const dir = path.join(process.cwd(), 'content', operator)
  const jsonFiles = fs.readdirSync(dir).filter(f => f.endsWith('.json'))
  return jsonFiles.map(f => {
    const meta = JSON.parse(fs.readFileSync(path.join(dir, f)))
    const mdPath = path.join(dir, f.replace('.json', '.md'))
    const content = fs.readFileSync(mdPath, 'utf-8')
    return { ...meta, content }
  })
}
```

New article? Drop a .md + .json file. Next build picks it up automatically. No code changes.

### Change 4: GitHub API as the "CMS"

We don't need a custom CMS API. We use GitHub's API directly:

```
Claude Code generates article
  → Creates .md file content
  → Creates .json metadata
  → Calls GitHub API: PUT /repos/{owner}/{repo}/contents/content/{operator}/{slug}.md
  → Calls GitHub API: PUT /repos/{owner}/{repo}/contents/content/{operator}/{slug}.json
  → Vercel detects git change → auto-rebuilds → article is live
```

**This is the simplest possible architecture.** No custom backend. No database. No CMS. Just files in a git repo.

---

## The Complete Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONTENT CREATION                             │
│                                                                  │
│  1. Keyword Agent (Semrush) → finds "one canal apartments boston"│
│  2. Brief Agent (Claude) → generates article structure           │
│  3. Writing Agent (Claude) → writes full article in markdown     │
│  4. QA Agent (Claude) → validates content                        │
│  5. Image Agent → generates featured image prompt                │
│                                                                  │
│  OUTPUT: article.md + article.json + image                       │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     PUBLISHING                                   │
│                                                                  │
│  Option A (Now — Claude Code):                                   │
│    Claude writes files directly to local repo → git push         │
│                                                                  │
│  Option B (Soon — GitHub API):                                   │
│    Claude calls GitHub API → creates files in repo               │
│    → Vercel webhook detects change → auto-rebuilds               │
│                                                                  │
│  Option C (Future — Custom API):                                 │
│    POST /api/publish with article JSON                           │
│    → Backend writes to repo via GitHub API                       │
│    → OR writes to Supabase → ISR rebuilds page                   │
│                                                                  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     RENDERING (Build Time)                        │
│                                                                  │
│  Next.js reads content/air-communities/*.json                    │
│    → Discovers all articles                                      │
│    → For each article:                                           │
│      → Reads .md file                                            │
│      → Converts markdown to HTML (with tables, images, CTAs)     │
│      → Generates JSON-LD schemas from .json metadata             │
│      → Renders using StoryLayout component                       │
│      → Outputs static HTML page                                  │
│                                                                  │
│  Static HTML contains:                                           │
│    → Full article text (AI crawlers see everything)              │
│    → JSON-LD: Article + FAQPage + BreadcrumbList                │
│    → Meta tags: title, description, OG, Twitter, canonical       │
│    → Internal links to property pages                            │
│    → Featured image with alt text                                │
│                                                                  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     LIVE PAGE                                    │
│                                                                  │
│  URL: operator-pages.vercel.app/air-communities/one-canal-guide  │
│                                                                  │
│  Features:                                                       │
│    → Parallax hero with property image                           │
│    → Article header card (title, author, date, read time)        │
│    → Table of contents sidebar (auto-generated from H2s)         │
│    → Article body with:                                          │
│      → Tables (markdown tables → HTML tables)                    │
│      → FAQ cards (from metadata JSON)                            │
│      → CTA inline cards (links to property page sections)        │
│      → Data cards (pricing breakdowns)                           │
│      → Images with captions                                      │
│    → Author box at bottom                                        │
│    → Property CTA card                                           │
│    → AI chat assistant                                           │
│                                                                  │
│  SEO:                                                            │
│    → All content in HTML source (no JS needed to read)           │
│    → 3 JSON-LD schemas                                           │
│    → Sitemap updated                                             │
│    → llms.txt updated                                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Markdown Format Spec (What Our Agents Output)

### Article Markdown (.md)

```markdown
Oak Trail at Cherry Creek South is a 384-unit apartment community at 2234 S Trenton Way
in Denver, Colorado. Seven floor plans from $1,512 per month (as of Q3 2026) with all-in
pricing, two resort-style pools, and a 24-hour fitness center.

## What is all-in pricing at Oak Trail?

All-in pricing means every listed price includes base rent plus required monthly fees like
water, sewer, trash, pest control, valet trash, and package lockers. No surprise line items
at lease signing.

[cta link="/air-communities/oak-trail#pricing" title="Build your all-in price" subtitle="Interactive rent calculator with add-ons"]

## What floor plans does Oak Trail offer?

Oak Trail has seven floor plans across one, two, and three-bedroom layouts.

| Floor Plan | Beds/Bath | Sq Ft | Price/mo |
|---|---|---|---|
| Design 1A | 1bd/1ba | 678 | $1,512 |
| Design 1B | 1bd/1ba | 753 | $1,575 |
| Design 2A20 | 2bd/2ba | 1,048 | $1,715 |

[image src="/images/air-communities/hero-pool.jpg" alt="Resort pool at Oak Trail" caption="One of two resort-style pools"]

## How far is Oak Trail from Cherry Creek State Park?

Cherry Creek State Park is approximately 10 minutes from Oak Trail.

[cta link="/air-communities/oak-trail#neighborhood" title="Explore the neighborhood" subtitle="Cherry Creek State Park, shopping, commute times"]
```

### Custom Markdown Extensions Tom & Dennis Need to Support

| Syntax | Renders As |
|---|---|
| `## Question?` | H2 heading with border-top separator |
| `| col | col |` | Styled data table (not markdown default) |
| `[cta link="..." title="..." subtitle="..."]` | Inline CTA card with orange arrow |
| `[image src="..." alt="..." caption="..."]` | Image block with caption below |
| `**Bold label:** text` | Bold-label bullet point |
| Standard markdown | Paragraphs, links, bold, italic |

### Metadata JSON (.json)

Already defined above. The key fields the renderer needs:

| Field | Used For |
|---|---|
| `title` | H1 on page + Article schema |
| `metaTitle` | `<title>` tag + OG title |
| `metaDescription` | Meta description + OG description |
| `slug` | URL path |
| `operator` | Breadcrumb + URL |
| `property` | Links to property page |
| `faqs[]` | FAQ section at bottom + FAQPage schema |
| `datePublished` | Display + Article schema |
| `author` | Author box + Article schema |
| `thumbnail` | Story card image on operator page |
| `featuredImage` | Hero image on article page |

---

## What Tom & Dennis Need to Deliver

### Deliverable 1: Content Directory Structure
```
content/
  air-communities/
    (empty — we populate it)
  towne-properties/
    (empty — we populate it)
```

### Deliverable 2: Markdown Renderer
A Next.js utility that:
- Reads .md file
- Converts to HTML
- Handles custom extensions: `[cta]`, `[image]`, tables
- Wraps in StoryLayout component

### Deliverable 3: Dynamic Article Page
```
src/app/[operator]/[slug]/page.tsx
```
That:
- Checks content directory for matching article
- If found: render article using markdown renderer
- If not: check property data (existing behavior)
- Auto-generates all JSON-LD from metadata JSON
- Auto-adds to sitemap via generateStaticParams

### Deliverable 4: Auto-Discovery
```typescript
generateStaticParams() returns all:
  - Property pages (from data/operators/)
  - Article pages (from content/[operator]/)
```

No hardcoded lists. Drop a file, it becomes a page.

### Deliverable 5: GitHub API Publish Script
A simple script or API route:
```
POST /api/publish
Body: { operator, slug, markdown, metadata, image_url }

→ Creates content/{operator}/{slug}.md via GitHub API
→ Creates content/{operator}/{slug}.json via GitHub API
→ Uploads image if provided
→ Vercel auto-rebuilds
→ Returns { success: true, url: "..." }
```

---

## What We (Content Team) Deliver

### Per Community

| What | Format | Example |
|---|---|---|
| Property data | JSON file | `data/operators/air-communities/one-canal.json` |
| Property images | PNG/JPG files | `public/images/air-communities/one-canal-hero.jpg` |
| Article content | Markdown file | `content/air-communities/one-canal-guide.md` |
| Article metadata | JSON file | `content/air-communities/one-canal-guide.json` |

### Quality Guarantees (What Our Agents Ensure)

| Check | Agent |
|---|---|
| Keyword optimized (density, entities, H2 questions) | Writing Agent |
| All prices match property data | QA Agent |
| All links valid | QA Agent |
| Meta title < 60 chars, description < 155 chars | QA Agent |
| FAQs self-contained (for AI citation) | QA Agent |
| Zero em-dashes, zero banned phrases | QA Agent |
| Fair Housing compliant | QA Agent |
| Featured image prompt (no people, no text) | Image Agent |
| Markdown syntax valid | QA Agent |

---

## Timeline for AIR Communities (5 Communities)

### Week 1: Setup

| Day | Content Team | Dev Team |
|---|---|---|
| Mon | Research One Canal (floor plans, amenities, pricing) | Set up content/ directory + markdown renderer |
| Tue | Research Indigo West, One Boynton | Build dynamic article page |
| Wed | Research 3400 Ave Arts, Citigate | Build auto-discovery + JSON-LD generation |
| Thu | Create property JSONs for all 5 | Build GitHub API publish endpoint |
| Fri | Source images for all 5 | Test: drop a .md + .json, verify page renders |

### Week 2: Content Production

| Day | Content Team | Dev Team |
|---|---|---|
| Mon | Write One Canal guide + QA | Deploy 5 property pages |
| Tue | Write Indigo West guide + QA | Test publish flow end-to-end |
| Wed | Write One Boynton guide + QA | Fix any rendering issues |
| Thu | Write 3400 Ave Arts guide + QA | Update sitemap, llms.txt auto-generation |
| Fri | Write Citigate guide + QA | Final QA on all pages |

### Week 3: Publish + Monitor

| Day | Content Team | Dev Team |
|---|---|---|
| Mon | Publish all 5 articles | Verify all live URLs |
| Tue | Submit sitemap to Google Search Console | Monitor build times |
| Wed | Write 2nd article per community (start) | Performance optimization |
| Thu-Fri | Continue writing | Support |

---

## Summary

**The connection is simple: Markdown files in a git repo.**

- We write markdown + JSON metadata
- Dev team builds a renderer that turns them into pages
- GitHub API (or git push) is the "CMS"
- Vercel auto-rebuilds on every change
- No custom backend needed for Phase 1
- Scales to 10,000 articles (just more files in the directory)

**Everything our agents output (tables, FAQs, CTAs, images, schemas) maps to a markdown extension that the renderer handles.** The content team never touches code. The dev team never touches content. Clean separation.
