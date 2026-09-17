## Webflow CMS Configuration

**Site ID:** 69d6907887b739e09622100f

### Collections
- **Resources:** `69fcfcef26d35b66ba874f9d` (ALL new content goes here)
- **Guides:** `69dccfeabed64ec697c4f7d2` (RESTRICTED — do not push)
- **News:** `6a32f0722779d53e287b5cc5`

### Author
- **Katie Mikles:** `69dcd70089c4135f7a4158bc` (ALWAYS set as author-2)

### Categories
- Top Apartments: `69df6fa543a7bf3d08de2528` (property-specific articles)
- Renter Advice: `69df6feb55f0f6d5f4e0d20d` (how-to guides, data articles)
- Neighborhood Guides: `69df6ef62355bc3a757acebe` (city/neighborhood content)
- Renters Corner: `6a1852a0e900a98e33e475b2` (Katie interview pieces)
- Lifestyle: `6a0223968011f8b2c9af166e`
- Property: `6a022353abefb2d114e7b04a`
- News: `6a33e903e1454372f37cf6e8`

### Field Mapping
| Markdown Field | CMS Field | Notes |
|---|---|---|
| `title` | `name` | Article title, max 256 chars |
| `slug` | `slug` | URL slug |
| `meta_description` | `meta-description` | Under 155 chars (editorial limit) |
| `seo_title` (distinct from H1) | `seo-title` | Format: [Short Title] \| brightplace, max 60 chars |
| `primary_keyword` | `focus-keyword` | Exact keyword from brief |
| First paragraph (plain text) | `post-summary` | Summary for grid display |
| Article body (HTML) | `post-body` | Rich text, exclude schema blocks |

### HTML Rules (Webflow RichText)
- **NEVER** use `<ul><li>` tags (Webflow strips them — content disappears)
- Convert all lists to `<p><strong>Label:</strong> text</p>` format
- `<ol><li>` is OK for numbered lists only
- No `<h1>` in post-body (Webflow uses `name` field for H1)
- No `<script>` tags (Webflow strips from RichText)
- Push as **DRAFT only** (user adds featured image before publishing)

## Provenance and routing

Migrated: 2026-09-16. Sources: `Agents/WORKFLOW.md` Stage 6,
`Agents/content-writing-guidelines.md` §12 and Claude project `MEMORY.md`.
These IDs are imported configuration, not a fresh API verification.
New resource, property, and neighborhood articles go to Resources. Guides remains
restricted. News ID is retained for an explicitly authorized news task; its presence
is not permission to route ordinary articles there. Never publish automatically.

Additional fields: `author-2` = Katie ID above; `category-2` = applicable category ID;
`main-image` = user-uploaded featured image. `post-summary` is plain text under 300
characters. SEO title must differ from H1 and be under 60 characters. Strip frontmatter,
schema blocks, duplicate H1, and the internal review note from CMS body. Standalone
HTML may include schemas in its head; RichText may not. Keep the original Markdown.
