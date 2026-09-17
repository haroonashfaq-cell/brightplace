# brightplace Direct overview: QA report

Date: 16 September 2026
Scope: revised single-page developer reference
Verdict: **Reference package ready for review. Production release remains blocked on browser QA, approved content/CTA and integration.**

## Workflow evidence

Applied Developer-Team flow, design, developer, writing, desktop QA, mobile QA and SEO roles. Independent design and copy reviews preceded final implementation; independent desktop/mobile static review followed the build. Root rechecked structure and corrected reported CSS issues.

Property-story keyword research, rental offers, floor-plan counts and ApartmentComplex schemas do not apply to this operator-facing overview. No production build, GitHub push or deployment was requested or performed. The sample is HTML/CSS, so a Next.js build is a production integration gate, not a static-reference test.

## Desktop / content / infrastructure

| Check | Result | Evidence |
|---|---|---|
| Offer comprehension | PASS, editorial review | Hero names websites, advisor and content; rows connect each to an operator use |
| Product examples | PASS | Concrete cost, pet/transit and move-date questions, explicitly illustrative |
| Scope | PASS | One Direct overview; no directory routes or community search |
| Source discipline | PASS | No invented rent, fees, ROI, conversion statistics or live chat; exact Foxchase guide title used |
| AIR evidence | LIMITED | Actual local content example; staging evidence recorded in README. No verified public screenshot supplied |
| Brand copy | PASS | brightplace lowercase; Direct capital-D; no em dashes or banned filler in visible copy |
| Design direction | PASS, static review | Developer-Team navy/orange/paper tokens; deliverable rows, journey, proof, rollout and editorial shelves |
| Eyebrow restraint | PASS | Three labels across nine sections |
| Semantic HTML | PASS | One H1; sequential headings; header/main/nav/footer; every section has a unique ID |
| Links | PASS, local only | All in-page anchors and local handoff links resolve; no dummy # links |
| Content in source | PASS | All copy and FAQ answers are in initial HTML; native details controls |
| JavaScript dependency | PASS | No application JavaScript or client-only content |
| CTA honesty | PASS for reference | Plan-your-pilot action opens the actual agenda section; no pretend inquiry submission |
| Type/dependencies | N/A | Plain HTML/CSS; production TypeScript build not performed |
| Remote dependencies | DISCLOSED | Google Fonts optional; system fallbacks. Two press destinations still require live verification |
| Asset weight | PASS, static size | HTML and CSS together under 30KB; remote font transfer and rendered performance not measured |

## Accessibility and mobile

Static code inspected for 375, 390, 428, 768 and 1280px layouts. These are code-review targets, **not browser-tested viewports**.

| Check | Static finding | Browser status |
|---|---|---|
| Horizontal overflow | Fluid wrappers, explicit responsive grids, no obvious wide fixed content | Pending actual rendering and font loading |
| Touch targets | Navigation/links minimum44px height; native summaries padded beyond44px; labels give adequate widths | Pending geometry and hit-area measurement |
| Text size | Minimum12px, including narrow media rules | Pending rendered readability |
| Grid collapse | Primary two-column sections, proof and hub collapse by800px; narrow layout at600px | Pending all four mobile widths |
| Fixed/absolute positioning | Only skip link and summary indicators; no chat/overlay competing with page content | Pending keyboard/zoom check |
| Interaction | Native details/summary; links have actual destinations; visible focus styles | Pending keyboard, screen-reader and touch behavior |
| Spacing | 16px mobile gutters,48px section padding,8px minimum wrapped-nav row gap | Pending visual review |
| Reduced motion | Smooth scroll disabled for prefers-reduced-motion | Pending preference test |
| Dark OS preference | Explicit light color scheme for this reference | Pending browser/OS preference check |

### Contrast calculations

Ratios calculated from the actual CSS color pairs:

- Navy on paper:13.75:1.
- Body ink-soft on paper:11.07:1.
- Muted on paper:5.37:1.
- Muted on paper-deep:4.92:1.
- Navy on orange buttons:7.31:1.
- Paper on navy:13.75:1.
- Ink-soft on orange-soft story surface:8.83:1.

All these text pairs exceed4.5:1. Story notes explicitly use ink-soft rather than muted on orange-soft. Focus visibility is coded but not visually verified.

### Issues found and fixed

1. AIR proof initially described a staging publishing pipeline and linked internal documentation. Changed to an operator-readable Foxchase guide example. Technical evidence limits moved to README.
2. Four eyebrow labels exceeded the nine-section allowance. Reduced to three.
3. Tablet CSS overrode the proof grid back to two columns and left the content hub split. Both now collapse at800px.
4. Wrapped mobile navigation had a4px row gap. Increased to8px.

## SEO audit adaptation

| Group | Result |
|---|---|
| Property schemas, floor-plan offers and GeoCoordinates | N/A: B2B product overview |
| Article schema | N/A: article cards link to future article pages; this page is not an article |
| FAQ schema | Not required for the reference; semantic HTML answers provided |
| Title and description | PASS:40-character title,142-character description |
| Heading hierarchy and accessible diagram | PASS, source inspection |
| Initial HTML content | PASS |
| Reference index policy | PASS: intentional noindex,nofollow |
| Canonical, OG/Twitter, share image | Production dependency: approved route/assets needed |
| robots, sitemap and llms serving | Production integration dependency; do not list this private reference as live |
| Draft content | Non-linked planned cards in sample; production must hide pending records |
| External news destinations | Pending live verification |

## Cross-page and release status

The actual `operator-pages` application and existing shared components were not edited. There are no new directory pages in the current package. All developer-reference document links must travel with the package. Older exploration remains in the superseded folder and is excluded from the ZIP.

Browser inventory returned no available browser, so no rendered screenshots, Lighthouse score, mobile simulation, screen-reader test or native interaction pass is claimed. Required before launch: browser QA, real proof assets, approved CTA/destination, actual product/integration availability review, article migrations, production Next.js build and coordinated Direct announcement.
