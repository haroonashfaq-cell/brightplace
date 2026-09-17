# brightplace Direct overview: section-by-section plan

Date: 16 September 2026
Scope: one operator-facing overview page, not an operator/community directory.
Status: developer reference. Proposed copy and experience, not launch approval.

## 1. The page must answer an operator's question

**What do I get, and how does it help my communities?**

The previous sample led with an industry thesis. This version leads with the actual offer: community websites, a renter advisor and ongoing content that help renters understand a community and reach its leasing team. Every section must add a concrete answer, rather than repeat a slogan.

Ten-second comprehension test: a new reader should be able to explain the three deliverables, name a renter task they support, and identify the operator's next step. No page can establish improved lead quality or ROI without evidence; this sample explains the mechanism rather than promising those outcomes.

## 2. Developer-Team workflow applied

Sources: `Developer-Team/TEAM.md`, `WORKFLOW.md`, `flow-agent.md`, `design-agent.md`, `developer-agent.md`, `operator-writing-agent.md`, `qa-agent.md`, `mobile-qa-agent.md`, `seo-audit-agent.md`, and the four design/web skills in `Developer-Team/skills/`.

Flow: source review → independent design and content review → developer implementation → desktop/static QA → mobile QA → SEO review → cross-page check → developer handoff.

The page strategy supplied by Matiullah controls product scope. Older August documents define Direct as content-only and are historical context, not current offer authority. Property-story requirements such as 2,000 words, rent tables, ApartmentComplex schema and floor-plan counts do not apply to this B2B overview.

This delivery is a portable HTML/CSS reference. The production developer should port its sections into the existing Next.js server-component system. A production `npm run build`, preview deployment and browser QA are release requirements, not claims made by running a static-file check. No GitHub push or deployment is part of this task.

## 3. Section decisions

### Hero: “What is Direct?”

Show the definition immediately: community websites, renter advisor and helpful content. Explain the intended benefit in everyday terms: renters can understand costs, availability and fit before contacting leasing.

Use one clear action to explore the experience. The visual should explain how these parts connect, not imitate an unavailable dashboard. Do not put “intent,” “upstream,” or “owned demand” in the lead explanation.

**Reader should leave knowing:** this is a connected renter experience for my communities, not an ad package or another generic slogan.

### What you get: “What am I actually buying?”

Use editorial rows, each naming a deliverable, a renter task and an operator use:

| Deliverable | Renter use | Operator value to explain |
|---|---|---|
| Community website | Understand the community and explore approved cost/availability information | Give people a useful destination before they contact leasing |
| Renter advisor | Ask questions in the context of their needs | Make community information easier to use in a decision |
| Continuous content | Find answers while researching a move | Build a body of helpful, community-specific information associated with the operator |

These are proposed offer components from the strategy. Do not state that every integration is connected today or that all existing vendors can be replaced.

### Renter walkthrough: “What does this look like in practice?”

Walk through a recognizable question such as “What would living here actually cost?” Then show the path: discover useful content → explore community information → ask a question → choose a next step with the community team.

Label illustrative examples as illustrative. Do not generate a pretend live advisor answer, invented rent, availability or qualification decision. Keep the explanation visible in HTML without interaction; accordions may reveal additional examples.

**Reader should leave knowing:** how the site, advisor and content work together, and where my leasing team enters the process.

### Operator rationale: “Why add this to my current marketing?”

Explain the connection between discovery and the decision. A renter needs useful answers before an inquiry can become a meaningful conversation. Direct brings those answers and the next step together around the community.

Keep the relationship intent explicit: the renter should reach the operator's team. Do not turn that intent into unverified contractual data-ownership promises. Do not assert that every ILS or website competitor lacks a feature.

### AIR pilot: “What evidence is there?”

Name the concrete Foxchase content example. The MCP Content Specs report a first staging article publish on 16 September 2026, with CMS review/publish and rendered content checked. That supports a content-workflow example; it does not prove production-wide advisor functionality, live availability, traffic growth or conversion lift.

Use an approved real capture when supplied. Until then, present a clearly labeled pilot example with its actual article title and the reader task it supports. Do not make a decorative AIR logo stand in for evidence. Do not link protected staging as if it were a public case study.

### Rollout and responsibilities: “What would my team have to do?”

Propose a practical discussion: select starting communities, confirm approved community information/contact paths, review content and agree publication responsibility. Show the split between operator knowledge/approval and brightplace setup/content work.

These are a proposed onboarding agenda. Product must confirm scope, supported data connections, effort, timing and commercial terms before the page promises them.

### FAQs: “What might stop me?”

Address the questions an operator is likely to ask: included components, where sites live, existing website/integration scope, who supplies information, how renters reach leasing and what a pilot would validate. Use honest bounded answers. Never invent pricing, guaranteed launch timing, all-vendor replacement, reduced staffing or a specific CRM integration.

### Content hub: “Where can I understand the thinking?”

Keep it after the product explanation and evidence. Feature Apartment Leads Have Disconnected as the anchor; use smaller supporting treatments for More Leads, Fewer Answers and Building for Agents, Not Users. Press is a separate shelf, not six equally weighted cards.

Full originals must be obtained and migrated. Publish on brightplace.ai with the intended canonical; confirm Substack controls and approved back-links. Direct announcement stays gated to the launch. RET needs its exact URL. The two supplied existing news URLs require destination verification.

### Closing: “What should I do next?”

Give the operator a concrete next step and an agenda: discuss starting communities, data readiness and the renter experience. Final acquisition CTA and destination remain open in the strategy.

If the sample offers a locally generated pilot brief, explicitly say it is a local download and does not submit an inquiry. Production should replace or connect the action only after the actual sales process is approved. No fake success messages or invented sales inbox.

## 4. Content and evidence rules

| Claim or asset | Source/status | Publication rule |
|---|---|---|
| Sites + advisor + content | User-supplied operator-page-content-strategy.md | Describe intended offer; product verifies feature availability before launch |
| Renter cost/fit/availability needs | Strategy framing | Illustrate without fake data or guarantees |
| AIR/Foxchase first publish | MCP-Content-Specs.md §1–§3 | Pilot content proof only; source reports staging |
| ROI, better conversion, fewer calls, faster launches | No measured evidence supplied | Do not claim |
| Ownership/data rights and integration scope | Strategy intent; contract/API details unconfirmed | Product/legal/engineering confirm exact wording |
| Article titles and news links | Strategy | Link only when approved and published |
| Screenshots/logos | Approved assets not supplied | Do not fabricate proof |

## 5. Developer implementation

Proposed route is `/direct`, subject to the actual brightplace site's routing. One reusable overview template with configurable hero, capability rows, walkthrough examples, proof, onboarding, FAQ, shelves and CTA.

Use server components in the production Next.js app. Keep text, FAQ answers and links in initial HTML. Client code is limited to progressive enhancement, such as generating a local brief. Use existing brand tokens and approved self-hosted fonts. Scope styles to avoid affecting existing routes.

CMS records need publication status, approved copy, linked source/evidence, media/alt text and CTA destination. Shelf entries must resolve to published articles/news. Revalidate overview when shelf publication changes. No operator/community directory data model is needed for this task.

Production metadata: unique title/description, approved canonical, appropriate WebPage/Organization semantics, social-sharing data and existing sitemap inclusion. This is not an apartment listing or article page; do not add property-specific schemas. Reference stays non-indexable until coordinated launch.

## 6. Design requirements

Use Developer-Team navy, orange, paper, peach and teal tokens. Urbanist headings, Lato body and editorial serif sparingly. No three equal feature-card layout, fake screenshots, unrelated property photography or tiny decorative labels.

Use several distinct section layouts to aid understanding: clear hero, editorial product rows, connected journey, pilot feature, responsibility split, native FAQ and restrained content shelves. Motion is minimal and must not hide content. All text at least 12px; actionable targets at least 44px; contrast verified per actual color pair.

Mobile widths: 375, 390, 428 and 768px. Single-column primary reading order at narrow widths, explicit grid collapse, no page overflow and no fixed overlays obscuring actions.

## 7. Acceptance and release gates

- [ ] Operator can name three deliverables and explain one practical use after a short read.
- [ ] Every section answers a different operator question; no directory or property-search flow.
- [ ] Walkthrough is clearly illustrative; no fake product screenshot, live response or listing data.
- [ ] AIR proof is specific and no broader than its documented evidence.
- [ ] Final copy, CTA, contact destination, integrations and commercial assertions approved.
- [ ] Content hub uses approved originals and valid links; pending announcement remains gated.
- [ ] Text and functional fallback links remain available with JavaScript disabled.
- [ ] Desktop/mobile keyboard, focus, overflow and interaction checks completed in a browser.
- [ ] Correct production metadata/canonical, no preview notes, no accidental draft indexing.
- [ ] Production Next.js build passes and existing shared-page behavior remains intact.
- [ ] Overview and Direct announcement launch together after approval.

## 8. Deliverables

- `operator-page-sample/index.html`: revised single-page sample.
- `operator-page-sample/styles.css`: brand-based responsive styling.
- `operator-page-design-review.md`: independent design rationale.
- `operator-page-qa-report.md`: actual validation results and remaining browser/release checks.
- `brightplace-direct-operator-reference.zip`: portable developer package, regenerated after review.
