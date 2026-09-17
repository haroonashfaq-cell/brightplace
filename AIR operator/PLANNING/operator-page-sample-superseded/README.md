# brightplace Direct: operator page reference

## Open the sample

Open **index.html** in a browser. No installation, build, network assets or API credentials are required. Keep the files in this folder together when sharing.

Optional local server, from this folder:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Then visit `http://localhost:8765/`. This is a design reference, not a deployed product or launch announcement.

### Files

| File | Purpose |
|---|---|
| `index.html` | Operator-facing Direct offer, featured operator and content hub |
| `air-communities.html` | AIR operator collection with all ten pilot community cards |
| `styles.css` | Shared responsive design, typography, focus states and layout |
| `directory.js` | Search, state filtering, sort, empty state and community detail dialog |
| `communities.json` | Example records with stable IDs, operator relationship and source references |
| `../operator-page-implementation-plan.md` | Production routes, content model, build sequence and acceptance criteria |

## What the sample demonstrates

```text
brightplace Direct
  ├─ The offer for operators
  ├─ Featured operators
  │    └─ AIR Communities
  │         └─ All published communities belonging to AIR
  │              └─ Individual community site
  ├─ Thought leadership
  └─ Press
```

The prototype seeds ten AIR pilot communities. This is **not AIR's total portfolio**. Production must derive each operator's collection from its published community records rather than hard-code the ten cards. New approved operators use the same template.

The strategy describes an operator-facing sales page; the user's request also describes operators containing communities. This sample connects those two needs while giving them separate pages and audiences. Proposed production paths are in the implementation plan; they are not existing public routes.

## Try these interactions

1. From Direct, select **Explore AIR communities**.
2. Search `Orlando`: two communities remain.
3. Reset, then choose `Florida`: five communities remain.
4. Combine search `Boston` with `Florida`: the empty state appears; Clear filters restores all ten.
5. Sort by community or city. Reset restores the original collection order.
6. Open a community: its name, location, description and source website appear in the dialog.
7. Close with the Close button or Escape. Focus returns to the card that opened it.
8. Disable JavaScript: all ten cards remain readable, with direct website links. Filtering/dialog enhancement is unavailable.

Community website navigation is real outbound navigation to the URLs in local source material. The dialog is a reference convenience. In production, **Explore community should be an ordinary link to the approved published brightplace community URL**. Do not make a modal the only crawlable route to community content.

## Content status and source discipline

- The offer and editorial section order come from [operator-page-content-strategy.md](../operator-page-content-strategy.md).
- All new marketing prose is **proposed copy**, not approved launch copy. Pain-point hierarchy and the final acquisition CTA remain open in the strategy.
- The sample uses a working internal exploration CTA instead of inventing a sales inbox, booking destination or functioning lead form.
- Thought leadership cards preserve the three supplied titles. Full source articles were not supplied, so there are no invented articles or dead “Read more” links. Cards remain coming-soon until migration.
- Direct announcement is pending. RET announcement lacks an exact URL in the source. Both remain non-linked reference cards; production should hide unpublished records.
- The financial-intelligence and connect news URLs are copied from the strategy. Automated web verification could not retrieve those pages during this task; the developer must confirm their URLs before launch.
- Community names, locations and short descriptions come from the local `AIR operator/*/context.md` records and the MCP reference. The source path for each record is in `communities.json`. Atlanta is also established in the MCP reference's community table.
- No rent, fees, availability, performance statistics, testimonials or conversion results are invented. The sample excludes the older app's unverified portfolio totals.
- The AIR wordmark is a text treatment for the reference, not an official supplied logo. Community cards use location typography rather than unrelated property photos. Replace only with approved identity/photo assets.
- No community is labeled live on brightplace. `brightplaceUrl` is deliberately null until publication is verified.

## Design and behavior

The sample uses an editorial layout: warm paper, deep green, restrained orange, serif headings and simple sans-serif body text. These are proposed tokens and should be reconciled with the production brightplace brand. It does not add a second styling library to the existing Next.js app.

Layouts adapt at 900px and 640px. Cards use three, two and one columns. There are no remote fonts, decorative property photos, trackers or external JavaScript dependencies. All copy and cards exist in HTML before JavaScript executes. Focus outlines, field labels, a skip link, result announcements and a native modal dialog are included.

Both pages include `noindex,nofollow` because they are unpublished references. Launch production pages with their approved indexing/canonical settings only after the Direct announcement gate is satisfied. Preview environments keep their own protection and indexing policy.

## Known limits

This package is a sample, not the CMS implementation. JSON is a data-contract example; the checked-in HTML is a static snapshot, not dynamically fetched from the JSON. Production renders HTML from the authoritative data source. The implementation plan covers synchronization and relationships.

No analytics, advisor, pricing feed, CRM submission, content migration or publishing integration is wired up here. No live claims are made for those systems. The existing `operator-pages` application is unchanged.

Automated checks validate static structure, links, data consistency and directory behavior. A connected browser was unavailable during this task, so rendered visual review on desktop/mobile and actual browser focus/keyboard testing remain required before sign-off.
