# Categories & Authors Extraction — Coverage Report

**Completed 2026-09-17**

## Categories — 7 / 7

| Asset | Count |
|---|---|
| `.md` | 7 / 7 |
| `.html` | 7 / 7 (placeholder — see below) |
| Icon image | **4 / 7** |

### Categories have no rich-text body

The Webflow Categories collection has **no rich-text field**. Its only fields are `name`, `slug`,
`description` (PlainText), `icon`, `color`, `seo-title`, `meta-description`.

**`description` is null for all 7 categories**, and `color` is null for all 7. So there is no body
content to extract. The `.html` files are placeholders recording this explicitly, rather than
being silently empty — the `.md` files carry the real payload (SEO title, meta description, icon).

**For the rebuild:** `/category/<slug>` pages currently have no editorial intro at all. They are
pure listing pages whose only unique text is the SEO title and meta description. Three of the
seven don't even have those.

### Article counts per category

| Category | Slug | Articles | SEO fields | Icon |
|---|---|---|---|---|
| Property | `property` | **41** | ❌ none | ❌ |
| Neighborhood Guides | `neighborhood-guides` | 30 | ✅ | ✅ |
| Lifestyle | `lifestyle` | 19 | ❌ none | ❌ |
| Renter Advice | `renter-advice` | 15 | ✅ | ✅ |
| News | `news` | 10 | ❌ none | ❌ |
| Renters Corner | `renter-corner` | 6 | ✅ | ✅ |
| Top Apartments | `top-apartments` | 5 | ✅ | ✅ |

**Worth flagging:** `property` is the largest category at 41 articles and has **no SEO title, no
meta description and no icon**. `lifestyle` (19 articles) is in the same state. Those two
`/category/` pages are indexable with no unique metadata.

Note the slug/name mismatch on Renters Corner: name is "Renters Corner", slug is `renter-corner`
(singular). The live URL is `/category/renter-corner`.

## Authors — 3 / 3

| Asset | Count |
|---|---|
| `.md` | 3 / 3 |
| `.html` | 3 / 3 (bio rich text) |
| Picture | **1 / 3** |

| Author | Slug | Articles | Picture | Socials |
|---|---|---|---|---|
| Katie Mikles | `katie-mikles` | **123** | ✅ | Instagram + LinkedIn |
| Haroon Ashfaq | `haroon-ashfaq` | 1 | ❌ | none |
| Tom Sharp | `tom-sharp` | 1 | ❌ | none |

Katie Mikles authors **123 of 127** articles. Haroon and Tom have one each.

### Two data quirks carried into the output

1. **The field slug is `facebook-profile-link` but its label is "Instagram Profile Link"**, and
   Katie's value is `https://www.instagram.com/katiemikles`. Mapping by slug would wire an
   Instagram URL into a Facebook link. The extracted `.md` maps it as `instagram` and carries a
   `note:` line recording the mismatch.
2. **Katie's LinkedIn URL is typo'd in the live data**: `https://www.linkedign.com/in/katiemikles`
   — "linkedign", not "linkedin". It is preserved verbatim in the extract rather than silently
   corrected, but it should be fixed in whichever system ends up owning this record.

### Bio content note

All three bios open with an `<h1>` ("About Katie", "About Haroon", "About Tom"). If the author
template also renders the author name as a page `<h1>`, the rebuilt page will have two H1s.
Worth checking against the current template.

## Metadata

`reports/categories-metadata.json` · `reports/authors-metadata.json`
