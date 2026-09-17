# brightplace Direct: operator page implementation plan

Date: 16 September 2026
Status: developer reference and proposed plan, not launch approval

## 1. Product structure

Build a reusable relationship: **brightplace Direct features operators; each operator owns a collection of communities; each community opens its own published experience.**

The [content strategy](operator-page-content-strategy.md) describes the operator-facing offer. The [interactive reference](operator-page-sample/index.html) adds the operator/community hierarchy requested by Matiullah. These are two related page types, not one long mixed-audience page.

| Page | Audience and purpose | Proposed production route | Reference |
|---|---|---|---|
| Direct overview | Operators considering brightplace; explain offer, demonstrate AIR, host editorial and press shelves | `/direct` | `operator-page-sample/index.html` |
| Operator collection | Renters exploring an operator's communities; useful also as operator proof | `/operators/[operatorSlug]` | `operator-page-sample/air-communities.html` |
| Community site | Renters evaluating a specific community; cost, fit, availability, advisor, next steps | Approved community hostname, e.g. a configured brightplace subdomain | Existing community system; not rebuilt in this sample |
| Thought leadership | Operator-first original/republished articles | `/insights/[slug]` | Cards only; source text/migration pending |
| Press | Published company announcements | Existing `/news/[slug]` | Existing links where supplied |

Route choices are proposals to reconcile with the actual brightplace site. Do not deploy the reference folder as the production information architecture.

## 2. What to build on each page

### Direct overview

1. Brand and navigation: approach, operators, perspectives, approved primary CTA.
2. Hero: intent begins before a lead; plain explanation of Direct. Proposed copy is in the reference.
3. Problem: discovery outside operator surfaces, unanswered renter questions, underused community knowledge. Product owner approves final hierarchy.
4. Product: data-connected community sites, renter advisor, continuous content engine. Do not imply every integration is live before verification.
5. Differentiation: relationship ownership versus listing distribution; decision support versus disconnected website tools. No unsourced competitor performance claims.
6. Featured operators: reusable card, AIR first. Link to the operator's actual collection. No fake testimonials, ROI or portfolio totals.
7. Thought leadership shelf: the three named strategy articles, with the anchor first after publication. Cards link to full on-domain pages, not invented previews.
8. Press shelf: published Direct announcement first when released, followed by approved existing news items.
9. Final acquisition CTA: destination and wording require product sign-off. Prototype uses internal exploration so it functions without collecting personal information.

### Operator collection

1. Breadcrumb back to Direct/operators.
2. Approved operator identity and introductory copy.
3. Count of **published communities in this collection**, not the operator's worldwide portfolio.
4. Directory: search community/city, state filter, sort, result count, empty state and reset.
5. Community cards: approved photo or honest fallback, name, city/state, short sourced summary and ordinary community link.
6. Optional renter guidance/FAQ grounded in actual product behavior.
7. Shared footer with operator-facing route back to Direct.

Show all published community records belonging to the operator. The ten seeded AIR communities are only the current reference collection. Never infer that an operator's entire portfolio is live from its corporate property count.

## 3. Data model and ownership

| Record | Minimum fields | Owner |
|---|---|---|
| Operator | `id`, unique `slug`, approved `name`, description, logo/alt, publication status, featured order | brightplace content team; developer enforces publication |
| Community | existing canonical `community_id`, `operator_id`, name, city, state, approved summary, image/alt, environment-aware published URL, publication status, source/verified timestamp | Approved community/profile system |
| Editorial article | id, slug, title, summary, category, body, author/reviewer, publication state/date, canonical, source URL, migration status | brightplace editorial |
| Press item | title, approved URL, publication state/date, shelf order | brightplace communications |
| Direct page config | hero/problem/product copy, approved CTA label/destination, featured operator IDs, shelf selections, announcement launch gate | brightplace product/content |

Use a required community→operator foreign key for the current one-operator model. If co-management or operator transfers are needed later, model them explicitly instead of duplicating communities. Query by `operator_id` and public status on the server. Derive visible counts from the same result set as the directory.

Reuse canonical IDs from MCP. AIR reference records: `foxchase`, `citi-lakes`, `sorrel`, `verdant-peachtree-creek`, `villages-at-raleigh-beach`, `3400-avenue-of-the-arts`, `citigate`, `indigo-west`, `one-boynton`, `one-canal`.

Sample records: [communities.json](operator-page-sample/communities.json). `publicationStatus: reference` and null brightplace URLs are deliberate; these are not claims of production readiness.

Existing `operator-pages/src/data/operators.ts` already groups operator metadata and community JSON. It can inform the component/data boundary, but its example inventory differs from the AIR pilot. Avoid merging the old inventory or portfolio totals automatically. Select the actual production host/repository before integrating.

## 4. Components and rendering contract

Suggested components: `DirectHero`, `ProblemGrid`, `DirectCapabilities`, `FeaturedOperatorCard`, `ContentShelf`, `PressShelf`, `OperatorHeader`, `CommunityDirectory`, `CommunityCard`, `SharedFooter`.

- Render all published copy, cards and destination links in initial server HTML. JavaScript enhances search/sort only. Never hide essential text pending an entrance animation.
- Production should use the existing Next.js/App Router system where appropriate; sample HTML/CSS is a visual/interaction reference, not a request for a separate production static stack.
- Derive HTML and structured data from the same published records. One H1 per page; meaningful H2 sections; unique metadata; canonical uses the configured production host.
- Community cards navigate normally, including opening in a new tab. The sample dialog demonstrates context only and must not replace production link navigation.
- For larger collections, add server-backed filtering/pagination with shareable query parameters and explicit page/total counts. Preserve the search query when returning from a community.
- If records or destination URLs are missing, omit the unpublished card or present an intentional non-linked state. Never construct an unverified hostname from a slug.
- Images need approved sources, meaningful alt text, dimensions and responsive variants. Use a location fallback if missing. Do not attach unrelated photos to a community.
- Scope CSS and use project tokens. Keep reduced-motion support, keyboard access and mobile layout. Do not introduce unnecessary dependencies.
- Publishing/unpublishing an operator or community must invalidate its collection, count and featured-card caches together. A draft community must not leak through directory queries.

## 5. Content hub migration

| Item | Action before linking |
|---|---|
| Apartment Leads Have Disconnected | Obtain original text and author approval; migrate as anchor thought-leadership page |
| More Leads, Fewer Answers | Obtain and migrate original; preserve renter-experience framing |
| Building for Agents, Not Users | Obtain and migrate original; cross-link published connect announcement |
| Direct announcement | Publish only with the coordinated Direct launch; promote to first press slot |
| RET Ventures announcement | Supply exact existing news URL and approved title |
| Financial intelligence / connect releases | Confirm supplied URLs resolve to their intended published articles |

Follow the strategy's on-domain canonical intent. Confirm what Substack permits for the existing posts and add approved source/back-links without promising a canonical control that has not been verified. Decide distribution/newsletter policy separately. Do not fabricate full articles from their titles or summaries.

Production shelves query published records only. “Coming soon” cards in this reference illustrate reserved slots and should be hidden in production unless product deliberately approves that treatment.

## 6. Analytics and conversion handoff

Use the existing approved analytics setup. Proposed events: `direct_operator_opened`, `operator_community_opened`, `operator_filter_used`, `direct_content_opened`, `direct_cta_clicked`. Include stable operator/community/content IDs where applicable. Do not put free-form renter search text or contact details into analytics properties.

If the final CTA becomes a demo request, implement the real destination/CRM integration, validation, accessible success/error states and a tested delivery path. The sample intentionally has no pretend submission success.

No rankings, ROI, conversion improvements, performance metrics or instant-launch promises should appear without approved evidence. The current reference has none.

## 7. Build sequence

1. **Confirm routing and sources.** Choose production repository/host, approve page distinction, community URL mapping and CTA; obtain brand assets.
2. **Create data relationships.** Operator→community query, published status, authoritative profile/URL source; import reviewed AIR records.
3. **Build the two templates.** Match the reference's section structure; connect all cards, counts and shelves to data.
4. **Integrate editorial and press.** Migrate approved originals, verify URLs/canonicals, apply launch gate and hide unpublished cards.
5. **Connect analytics and CTA.** Use approved instrumentation and an actual submission/navigation path.
6. **Review and release.** Content/brand review, responsive and accessibility checks, destination verification and coordinated Direct announcement. Publish to production only after approval.

Developers should estimate these work packages after repository/API discovery. The sample does not assume that MCP already exposes operator or page-config CRUD; confirm existing CMS control before adding tools.

## 8. Acceptance checklist

- [ ] Direct → AIR → published community navigation works in both directions with correct breadcrumbs.
- [ ] AIR query contains every published AIR community and no other operator's communities. Counts match the query.
- [ ] Adding a published community record automatically adds its card and updates the count; removing publication removes it from all discovery surfaces.
- [ ] Search/filter/sort/reset work alone and in combination; zero results has recovery; mobile fields do not overflow.
- [ ] No-JavaScript view includes copy, directory and working destination links. Published pages have a single H1 and correct canonical.
- [ ] Keyboard navigation, focus indicators, labels and result announcements work; any modal traps focus, closes with Escape and restores focus.
- [ ] No invented property photo, portfolio count, testimonial, live rent, availability or performance claim appears.
- [ ] Three migrated thought-leadership articles contain approved original content and correct metadata/canonical links.
- [ ] Unpublished announcement/article/community records are excluded from production and sitemap output.
- [ ] Final CTA reaches the approved destination; if a form, delivery and errors are tested.
- [ ] Staging stays protected/non-indexable; production has approved index settings and no reference banners or sample notes.
- [ ] Direct overview and announcement launch together. Product approves final pain-point order, value proposition and CTA.

## 9. Open decisions and validation status

Product still owes final copy hierarchy, final CTA, announcement timing, article source text, RET URL and approved assets. Developer must confirm the production repository, data/API ownership and live community destinations.

The sample preserves the source strategy's lowercase brightplace, capital-D Direct, no em dashes and no external-copy “signal.” Neighborhood copy uses location context rather than demographic claims.

The reference files have static/data/interaction checks; actual browser visual and focus review is pending because no connected browser was available. Do not treat that as completed production QA.
