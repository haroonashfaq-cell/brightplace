# PART 1: Rendering & AI Crawler Requirements

How to build these sites so Google AND every AI search engine can read them.

---

## The Problem We're Solving

AI search engines (ChatGPT, Claude, Perplexity, Google AI Overviews) are now the primary way renters discover apartments. These AI crawlers do NOT execute JavaScript. They fetch raw HTML and read it — exactly like running `curl` on a URL.

If the site uses client-side rendering (React SPA, Angular SPA, or even Next.js with `'use client'` everywhere), the AI crawlers see an empty page. The content is invisible. We lose 100% of AI search traffic.

Our architecture must guarantee that every piece of content is in the raw HTML source — no JavaScript execution required.

---

## How Every Major AI Crawler Works (2026)

| Crawler | Who Operates It | Executes JavaScript? | What It Reads |
|---------|----------------|---------------------|---------------|
| **GPTBot** | OpenAI (ChatGPT, SearchGPT) | No | Raw HTML + JSON-LD schemas |
| **ClaudeBot** | Anthropic (Claude) | No | Raw HTML + JSON-LD schemas |
| **PerplexityBot** | Perplexity AI | No | Raw HTML + JSON-LD schemas |
| **Google-Extended** | Google (AI Overviews) | No | Raw HTML + JSON-LD schemas |
| **Googlebot** | Google (traditional search) | Yes (limited, delayed) | HTML first, JS second — prefers HTML |
| **Bingbot** | Microsoft (Copilot) | Limited | Raw HTML preferred |
| **AppleBot** | Apple (Siri, Spotlight) | No | Raw HTML + meta tags |

**Key insight:** Every AI crawler behaves like `curl`. If `curl https://your-site.com/page` doesn't show the content, no AI engine will ever surface it.

---

## Recommended Architecture

```
Framework:     Next.js 15+ with App Router
Language:      TypeScript (strict mode)
Rendering:     Static Site Generation (SSG) for property pages
               Incremental Static Regeneration (ISR) for blog pages
Styling:       CSS custom properties (no Tailwind, no CSS modules)
Animation:     Framer Motion 11+ (progressive enhancement only)
Deployment:    Vercel (CDN edge serving)
```

### Why SSG (Static Site Generation)

| Approach | AI Crawlers See Content? | Speed | Hosting Cost | Complexity |
|----------|------------------------|-------|-------------|------------|
| **SSG (our choice)** | Yes — pre-built HTML files | Fastest (CDN edge) | Near zero | Low |
| SSR (Server-Side Rendering) | Yes — rendered per request | Fast | Medium (server required) | Medium |
| ISR (for blog) | Yes — static + auto-regeneration | Fast | Low | Medium |
| CSR (Client-Side Rendering) | **No — empty page** | Slow (JS must load + execute) | Low | Low |
| SPA (Single Page App) | **No — empty page** | Slow | Low | Medium |

SSG builds every page into a plain `.html` file at deploy time. Vercel serves these from its global CDN. No server runtime. No JavaScript required to see content. Fastest possible Time to First Byte.

---

## The Two-Layer Rendering Model

### Layer 1: Static HTML (Server Components — DEFAULT)

Everything the user and AI crawlers need to READ is in plain HTML:

- Property names, addresses, phone numbers
- Floor plan names, pricing, square footage
- Amenity lists and descriptions
- FAQ questions and answers
- Neighborhood information and distances
- Blog article text
- All meta tags (title, description, canonical, Open Graph, Twitter Card)
- All JSON-LD structured data schemas

**Rule:** Server Components are the default. Never add `'use client'` unless the component absolutely needs `useState`, `useEffect`, or Framer Motion.

### Layer 2: Progressive Enhancement (Client Components — OPT-IN ONLY)

Interactive features that enhance the human experience but are NOT required to consume content:

- Scroll-triggered fade-in animations (Framer Motion)
- FAQ accordion expand/collapse
- Image gallery lightbox
- Rent calculator (interactive pricing tool)
- AI chat assistant widget
- Parallax scrolling effects
- Mobile menu toggle

**Rule:** If you disable JavaScript in the browser, the page must still display 100% of the content. Interactions stop working, animations disappear, but all text, pricing, images, and data remain visible.

### How to Verify

```bash
# This must show all content — if it doesn't, something is client-rendered
curl https://foxchaseofalexandriaapts.com/blog/foxchase-apartments | grep "88 wooded acres"

# Count JSON-LD schemas — must return 3 for property pages
curl -s https://site.com/page | grep -c "application/ld+json"

# Check that robots.txt allows AI crawlers
curl https://foxchaseofalexandriaapts.com/robots.txt
```

---

## AI Crawler Access Configuration

### robots.txt (MUST be at site root)

```
# AI Search Engines — ALLOW ALL
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

# Traditional Search Engines
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: AppleBot
Allow: /

# Sitemap
Sitemap: https://[domain]/sitemap.xml
```

**Why this matters:** 90%+ of apartment community websites block AI crawlers. By explicitly allowing them, our content gets indexed and cited in AI search results while competitors are invisible.

### llms.txt (MUST be at site root)

A plain-text file that gives AI models a structured summary of the site without requiring them to crawl every page. Format:

```
# [Community Name] Apartments
> [One-line description with key differentiators]

## Property Pages
- [Page Name](/url): [Key details — location, floor plans, price range, top amenities]

## Blog
- [Article Title](/blog/slug): [One-line summary]

## About
[Brief description of what the site offers]

## Contact
Website: [url]
Phone: [number]
```

AI models check for `llms.txt` before deep-crawling. This file gives them everything they need in one request.

### X-Robots-Tag Header (Vercel config)

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

---

## JSON-LD Structured Data Requirements

Every page must inject schemas into the `<head>` via `<script type="application/ld+json">`. AI crawlers and Google parse these directly.

### Property Pages (3 schemas)

**1. ApartmentComplex**
```json
{
  "@context": "https://schema.org",
  "@type": "ApartmentComplex",
  "name": "Foxchase Apartments",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "766 N Howard Street",
    "addressLocality": "Alexandria",
    "addressRegion": "VA",
    "postalCode": "22304"
  },
  "telephone": "434-337-5919",
  "amenityFeature": [
    { "@type": "LocationFeatureSpecification", "name": "Resort-Style Pool", "value": true },
    { "@type": "LocationFeatureSpecification", "name": "24-Hour Fitness Center", "value": true }
  ],
  "priceRange": "$1,467 - $2,521/mo",
  "numberOfAvailableAccommodation": 7
}
```

**2. FAQPage**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Does Foxchase allow pets?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, Foxchase is a pet-friendly community with an on-site dog park..."
      }
    }
  ]
}
```
This triggers Google's FAQ rich results AND gets pulled into AI-generated answers.

**3. BreadcrumbList**
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://foxchaseofalexandriaapts.com" },
    { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://foxchaseofalexandriaapts.com/blog" },
    { "@type": "ListItem", "position": 3, "name": "Article Title", "item": "https://foxchaseofalexandriaapts.com/blog/slug" }
  ]
}
```

### Blog Pages (3 schemas)

1. **Article** — headline, author, datePublished, dateModified, publisher
2. **FAQPage** — all FAQ pairs from the article
3. **WebPage** — page-level metadata with breadcrumbs

---

## Semantic HTML Requirements

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>SEO Title (different from H1, under 60 chars)</title>
  <meta name="description" content="Under 155 characters...">
  <link rel="canonical" href="https://exact-page-url">
  <meta property="og:title" content="...">
  <meta property="og:description" content="...">
  <meta property="og:image" content="https://cdn-url/image.webp">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{ schemas here }</script>
</head>
<body>
  <header><!-- Navigation --></header>
  <main>
    <article>
      <h1>Display Title (only ONE h1 per page)</h1>
      <section id="pricing">
        <h2>What Does It Cost to Live at Foxchase?</h2>
      </section>
      <section id="amenities">
        <h2>What Amenities Does Foxchase Offer?</h2>
      </section>
      <section id="faq">
        <h2>Frequently Asked Questions</h2>
        <h3>Does Foxchase allow pets?</h3>
      </section>
    </article>
  </main>
  <footer><!-- Contact, legal --></footer>
</body>
</html>
```

### Rules
- One `<h1>` per page — the display title
- `<title>` tag uses the SEO title (must differ from H1)
- Heading hierarchy never skips levels (no h1 then h3)
- Every `<section>` has an `id` attribute for anchor navigation
- H2 headings in question format match People Also Ask queries
- All images have `width` and `height` attributes (prevents layout shift)
- External links get `target="_blank" rel="noopener"`
- Internal links do NOT get `target="_blank"`

---

## Performance Requirements (Google Ranking Factor)

| Metric | Target | Why |
|--------|--------|-----|
| Time to First Byte (TTFB) | Under 200ms | Vercel CDN edge handles this with static files |
| Largest Contentful Paint (LCP) | Under 2.5s | Optimize hero/featured images (WebP, compressed) |
| Cumulative Layout Shift (CLS) | Under 0.1 | Set width/height on ALL images, no late-loading content |
| First Input Delay (FID) | Under 100ms | Minimal JavaScript on content pages |
| Total page weight | Under 500KB | Light pages rank better and load faster on mobile |
| First Load JS bundle | Under 160KB | Keep client-side JS minimal |

### Image Requirements
- Format: WebP (we provide all images in WebP)
- Hero/featured images: `loading="eager"` (load immediately)
- All other images: `loading="lazy"` (load on scroll)
- Always set explicit `width` and `height` attributes
- Serve via CDN with `Cache-Control: public, max-age=31536000, immutable`

---

## What We Do NOT Want

| Approach | Problem |
|----------|---------|
| React SPA / Create React App | Content invisible to all AI crawlers — empty `<div id="root">` |
| Client-side API fetching (`useEffect` + `fetch`) | Content loads after JS executes — AI crawlers see nothing |
| `'use client'` on content components | Defeats server rendering — content not in initial HTML |
| WordPress with page builders | Bloated, slow, usually blocks AI bots, limited schema control |
| iframes for content sections | Crawlers don't follow iframes — content is invisible |
| Content behind authentication/login | Crawlers can't authenticate — content is invisible |
| Lazy-loading text content | Crawlers don't scroll — only above-fold HTML is guaranteed |
| JavaScript-dependent routing (hash routes) | `/#/page` URLs are invisible to crawlers |
| `<meta name="robots" content="noindex">` on blog pages | Explicitly tells crawlers to ignore the page |
| Blocking AI bots in robots.txt | Competitors do this — we gain advantage by NOT doing it |

---

