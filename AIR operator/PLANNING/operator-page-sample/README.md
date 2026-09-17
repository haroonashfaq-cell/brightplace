# brightplace Direct overview: developer reference

## Open the sample

Open **index.html** in a browser and keep the other files in this folder beside it. No build or credentials are required. Google Fonts supplies Urbanist and Lato when online; system fallbacks apply offline.

This is one operator-facing page. It explains what Direct includes, how renters use it, why the operator would care and what a pilot discussion should cover. No operator directory or community-search flow is included.

## Start here

- [Section-by-section implementation plan](../operator-page-implementation-plan.md)
- [Independent design review](../operator-page-design-review.md)
- [QA report](../operator-page-qa-report.md)
- [Source strategy](../operator-page-content-strategy.md)

## What changed

The earlier page led with the abstract idea that intent starts before a lead. This version starts with three tangible deliverables and puts an operator benefit beside each. A clearly labeled renter-question walkthrough demonstrates cost, fit and availability. The AIR section illustrates an actual community guide, then rollout and FAQ sections address the operator's practical questions.

The Developer-Team flow/design/developer/writing/desktop QA/mobile QA/SEO guidance was applied to this B2B sample. Property-story word counts, floor-plan schemas, directory data and production deployment commands are outside this reference's scope.

## Sources and limits

The current operator-page-content-strategy.md defines the intended integrated Direct offer. Older August files describe a content-only product and are not the authority for current page scope.

The AIR evidence comes from MCP-Content-Specs.md sections 1–3. It reports one Foxchase article publishing flow completed on staging on 16 September 2026. This does not establish improved leasing outcomes, publicly live advisor/availability integration or production-wide adoption. The public-facing sample therefore uses the article as a content example, not a conversion case study.

The exact guide title comes from `AIR operator/Foxchase/foxchase-intelligence/fox-chase-apartments/09-fox-chase-apartments-final-enriched.md`: **What Renters Should Know About Foxchase Apartments in Alexandria, VA**. Topics described in the sample correspond to its headings. No rent, fees, occupancy, review counts or other time-sensitive property figures are repeated.

No actual product screenshots or approved AIR logo were supplied. The text treatment/typographic journey are illustrations, not captured UI. Replace with approved real product evidence when available. Do not generate a fake dashboard or property photo as proof.

New copy and onboarding responsibilities remain proposed. Before launch, product must approve feature availability, integration scope, data rights, service scope, pricing/timing wording and final acquisition CTA. Do not infer these from the sample.

## Content hub

The three thought-leadership titles come from the strategy. Full originals still need approved on-domain migration. The Direct announcement is gated to launch; the RET announcement needs an exact URL. Non-linked planned items reserve layout slots and should be hidden in production until approved.

The financial-intelligence and connect URLs are taken from the strategy. Automated retrieval could not confirm them during the original build; verify them before publication. No article bodies, testimonials, results or case-study claims have been invented.

## Implementation

The HTML is a portable design/interaction reference. Port the sections into the actual site's Next.js server-component system and existing CMS. The current operator-pages application is unchanged. Server-render all page copy and published links; use client code only for enhancement.

This unpublished sample is non-indexable. Production canonical, social metadata, sitemap inclusion and a real sales/booking destination remain launch dependencies. A sample action must never claim that an inquiry was submitted when no submission exists.

The earlier multi-page exploration is preserved separately in `../operator-page-sample-superseded/` and excluded from the current developer ZIP.

## Review status

See the QA report for checks actually run. No connected browser is available in this environment, so rendered desktop/mobile, keyboard behavior and full accessibility sign-off remain pending. Static code checks are not a substitute for those checks, or for the production Next.js build.
