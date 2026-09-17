# QA Agent — brightplace direct

Validate every article before publishing. 6 sections, all must PASS. Adapted from brightplace intelligence QA but generic for any operator.

## Inputs
- Written article
- Operator brand guidelines
- Property data (for accuracy verification)

## 6 Sections

### Section 1: Brand Compliance
- [ ] Operator name casing correct everywhere
- [ ] Zero em-dashes in body
- [ ] No banned phrases (deep dive, navigate, landscape, unlock, leverage, vibrant, bustling, etc.)
- [ ] No banned sources cited (Zillow, Apartments.com, Reddit, Yelp, Walk Score, etc.)
- [ ] Fair Housing: neighborhoods described by infrastructure only
- [ ] No ranking language in title (Top X, Best, #1, Ultimate Guide)
- [ ] Operator's specific brand rules followed (from _brand.json)

### Section 2: SEO Structure
- [ ] First sentence contains primary keyword
- [ ] Keyword density 7-12 instances (0.5-1.0%)
- [ ] Meta description under 155 chars with primary keyword
- [ ] SEO title under 60 chars and DIFFERENT from H1
- [ ] One H1, sequential headings (H1 → H2 → H3)
- [ ] H2s in question format
- [ ] Each H2 opens with answer (BLUF)
- [ ] Featured snippet paragraph 49-55 words
- [ ] Date stamps on all dollar figures
- [ ] 10+ FAQ pairs, 40-60 words each
- [ ] 3 schemas present (Article, FAQPage, BreadcrumbList)

### Section 3: Content Accuracy
- [ ] Floor plan counts match property JSON data
- [ ] Prices match property JSON data
- [ ] Addresses match property JSON data
- [ ] Amenity names match property JSON data
- [ ] Pet policy details match property JSON data
- [ ] No outdated information (check date stamps)

### Section 4: Link Audit
- [ ] All internal links point to valid operator pages
- [ ] No placeholder `href="#"` links
- [ ] All external links use HTTPS
- [ ] No banned source links in body
- [ ] 3 CTAs present linking to operator property pages
- [ ] 7+ internal links total

### Section 5: Infrastructure
- [ ] No `http://` links (all HTTPS)
- [ ] Frontmatter complete (title, meta_title, meta_description, slug, operator, property, keyword, dates)
- [ ] Slug URL-safe (lowercase, hyphens, no special chars)

### Section 6: AI Readiness
- [ ] FAQ answers are self-contained (make sense without the question context)
- [ ] Entity density meets brief targets (property name 8+, city 5+, landmarks 3-5x)
- [ ] Content would be useful if extracted as a standalone answer
- [ ] Key data (prices, sqft, amenity counts) stated explicitly, not implied

## Output
```
# QA REPORT: [Article Title]
Operator: [name]
Sections: 6
Passed: [n]/6
Failed: [n]/6
Verdict: PUBLISH / BLOCK

[Failures with line, issue, and fix]
```
