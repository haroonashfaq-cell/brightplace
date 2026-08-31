# Publish Agent — brightplace direct

Push completed articles to the operator's website. Currently targets Next.js/Vercel stack. Future: plug-and-play adapters for any CMS.

## Current Stack: Next.js on Vercel

### Process
1. Convert article markdown to a Next.js page component (or JSON data file)
2. Generate JSON-LD schemas:
   - Article (headline, author, dates)
   - FAQPage (all Q&A pairs)
   - BreadcrumbList (operator → property → article)
3. Create/update the article data file in the repo
4. Update sitemap.xml with new URL
5. Update llms.txt with new article entry
6. Git commit + push (triggers Vercel auto-deploy)
7. Verify the live URL loads correctly after deploy

### File Placement
```
src/data/articles/[operator-slug]/[article-slug].json
```

### Post-Publish Checks
- [ ] Page loads at the expected URL
- [ ] JSON-LD schemas present in HTML source
- [ ] Meta tags correct (title, description, OG, canonical)
- [ ] Images load
- [ ] Internal links work
- [ ] sitemap.xml includes the new URL
- [ ] llms.txt includes the new entry

## Future Adapters

### Webflow CMS
- Convert markdown to HTML
- Push via Webflow CMS API
- Map fields: name, slug, seo-title, meta-description, post-body

### WordPress
- Convert markdown to HTML
- Push via WordPress REST API (/wp-json/wp/v2/posts)
- Set: title, slug, content, excerpt, meta fields (Yoast/RankMath)

### Contentful / Sanity
- Push as structured content via their APIs
- Map to content model fields

### Custom CMS
- POST to webhook URL with article data as JSON payload
- CMS handles rendering and publishing

## Adapter Interface (future)
```
interface PublishAdapter {
  name: string
  publish(article: ArticleData): Promise<{ url: string; success: boolean }>
  verify(url: string): Promise<{ live: boolean; schemas: boolean; meta: boolean }>
}
```

Each adapter implements this interface. The Publish Agent calls the adapter without knowing the underlying CMS.
