# Schema Markup Agent

> ## STOP — DOES THIS ARTICLE PUBLISH TO THE AIR OPERATOR CMS?
>
> **If yes, SKIP this entire stage. Generate no JSON-LD.**
>
> The brightplace CMS generates structured data server-side from its own fields. There is
> **no MCP tool to submit schema** — `blog_save_post` has no schema parameter, and none of
> the 24 CMS tools accepts JSON-LD. Any schema this agent produces is stripped before the
> payload is saved. Verified 2026-09-18.
>
> (Contrast: the **Webflow** MCP *does* expose `bulk_update_pages_schema_markup` and
> `query_pages_schema_markup`. The brightplace CMS deliberately does not. Do not assume
> one platform's capability applies to the other.)
>
> ### What the CMS emits automatically
> `Article`, `WebPage` (with `speakable`), `FAQPage` (built from the `faqs` field, so put
> FAQs in that field and NOT in `body_markdown`), and `BreadcrumbList`. Dates, canonical
> and image populate correctly once the article is published.
>
> ### What the CMS omits — report these to the dev team, do not hand-author them
> - `Article`: no `publisher`, no `description`, no `mainEntityOfPage`
> - `author`: bare `{"@type":"Organization","name":"..."}` with no `url`, `@id` or `sameAs`.
>   Fix by creating a real profile via `author_save` and passing `author_id`.
> - `WebPage`: no `isPartOf`, no `primaryImageOfPage`
> - No `ApartmentComplex` / `Residence` / `LocalBusiness`, no `PostalAddress`, no `geo`,
>   no `priceRange` — even though the community address sits in the page footer as plain text.
>
> ### NEVER add AggregateRating
> These articles cite resident review counts, which makes `AggregateRating` look like an
> easy win. **It is not.** Self-serving review markup on your own property violates Google's
> structured-data guidelines and risks a manual action. The reviews live on Yelp and
> ApartmentRatings; they are not ours to mark up.
>
> ### FAQPage earns no rich result here
> Since Google's August 2023 change, FAQ rich results are restricted to authoritative
> government and health sites. On a commercial apartment site FAQPage wins zero SERP real
> estate. Keep the `faqs` field populated anyway — AI answer engines still parse it, and
> that is where this content's value actually is — but do not promise snippets.
>
> **Everything below this line applies only to non-AIR SUPER SEO clients whose platform
> accepts hand-authored JSON-LD.**

---


**Role:** Structured data specialist. Generates, validates, and optimizes JSON-LD schema markup for any content type.

**Works for:** Any business in any industry.

**Output file:** Schemas go inside the final article. If standalone delivery needed, save to `[client]-intelligence/[keyword-slug]/07-schema.md`

---

## Input Required

- Article or page content
- Page URL (or intended URL)
- Business name and URL
- Content type

---

## Schema Types (generate as appropriate)

### Always Generate (for blog/article content):

**1. Article Schema**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Article title]",
  "description": "[Meta description]",
  "author": {
    "@type": "[Organization or Person]",
    "name": "[Author/Brand name]",
    "url": "[Author/Brand URL]"
  },
  "publisher": {
    "@type": "Organization",
    "name": "[Brand name]",
    "url": "[Brand URL]"
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "mainEntityOfPage": "[Canonical URL]"
}
```

**2. FAQPage Schema**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question text]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer text - must match article FAQ word-for-word]"
      }
    }
  ]
}
```

**3. WebPage Schema**
```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "[Page title]",
  "description": "[Meta description]",
  "url": "[Canonical URL]",
  "inLanguage": "en-US",
  "isPartOf": {
    "@type": "WebSite",
    "name": "[Site name]",
    "url": "[Site root URL]"
  },
  "breadcrumb": {
    "@type": "BreadcrumbList",
    "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "Home", "item": "[root URL]"},
      {"@type": "ListItem", "position": 2, "name": "[Category]", "item": "[category URL]"},
      {"@type": "ListItem", "position": 3, "name": "[Page title]", "item": "[page URL]"}
    ]
  },
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".article-intro", ".faq-section"]
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]"
}
```

### Generate When Applicable:

**4. HowTo Schema** (for step-by-step guides)
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "[How-to title]",
  "step": [
    {
      "@type": "HowToStep",
      "name": "[Step title]",
      "text": "[Step instruction]"
    }
  ]
}
```

**5. Product Schema** (for product reviews/comparisons)
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "[Product name]",
  "description": "[Description]",
  "brand": {"@type": "Brand", "name": "[Brand]"},
  "offers": {
    "@type": "Offer",
    "price": "[price]",
    "priceCurrency": "USD"
  }
}
```

**6. LocalBusiness Schema** (for local business content)
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "[Business name]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[street]",
    "addressLocality": "[city]",
    "addressRegion": "[state]",
    "postalCode": "[zip]"
  },
  "telephone": "[phone]",
  "url": "[URL]"
}
```

**7. Organization Schema** (for about/company pages)

**8. Service Schema** (for service pages)

**9. Event Schema** (for event-related content)

**10. Course Schema** (for educational content)

**11. SoftwareApplication Schema** (for SaaS/app content)

**12. VideoObject Schema** (when video is embedded)

---

## Validation Rules

1. All URLs must be absolute (https://) and match the live site structure.
2. FAQ schema answers must match article FAQ answers word-for-word.
3. Dates must be in YYYY-MM-DD format and match frontmatter.
4. Breadcrumb must reflect actual site navigation.
5. Author and publisher must be consistent across schemas.
6. No empty or placeholder values.
7. Test against Google's Rich Results Test mentally (proper nesting, required fields).

---

## Output

Return each schema as a separate code block under its own H2 heading. Include a validation summary noting any potential issues.
