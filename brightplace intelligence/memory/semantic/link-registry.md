# Link Registry

Migrated: 2026-09-16. Sources: `Agents/WORKFLOW.md` URL tables; `Agents/qa-agent.md` §§5–6; `Agents/master-writer-agent.md`; Claude project `MEMORY.md`.

## Domain and host rules

Updated 2026-09-24, verified against live HTTP.

- **`app.brightplace.ai` is merged into the main site.** It is no longer a separate
  destination: `app.brightplace.ai/<path>` returns 308 to `www.brightplace.ai/<path>`,
  path preserved.
- **Never write `app.brightplace.ai` in a link.** This is a QA failure, not a style
  preference. Every one costs a needless redirect hop.
- **Canonical host in every `href` is `https://www.brightplace.ai`.** Bare apex
  `https://brightplace.ai` also 308s to www, so it costs a hop too. Write
  "brightplace.ai" in link *text* where the brand reads better; the href stays `www`.
- Internal links may instead be **site-relative** (`/resources/<slug>`), which avoids
  the host question entirely. This is what the migration docs recommend, and it is the
  preferred form for links inside `<slug>.html` bodies.
- CTA targets, one domain now:
  - search action → `https://www.brightplace.ai/search` (200, in the sitemap;
    `robots.txt` disallows `/search/` with a trailing slash, which does not block `/search`)
  - brand mention → `https://www.brightplace.ai`
- The old "never `brightplace.ai` and `app.brightplace.ai` in the same line" rule is
  **retired**. There is only one domain.

## Sitemap

Updated 2026-09-24, fetched live.

- `https://www.brightplace.ai/sitemap.xml` is a **sitemap index**, not a flat
  `<urlset>`. It returns 4 child entries, not article URLs. Fetching it and grepping
  for `<loc>` gives 4 results, not 155.
- **Editorial URLs are in `https://www.brightplace.ai/sitemaps/content.xml`** — 155
  URLs. This is the file to fetch for internal-link verification.
- Property pages are in `/sitemaps/property-1.xml` through `-3.xml` (~22,774 URLs).
- `robots.txt` points at the index and names 13 AI crawlers explicitly.

### Added since the 2026-09-17 migration snapshot

Seven URLs, all live and now sitemapped. The four resources are valid internal
link targets and were previously missing from the sitemap:

- `/resources/apartment-with-terrace`
- `/resources/apartments-with-gyms`
- `/resources/apartments-with-pools`
- `/resources/washer-dryer-in-unit-apartments`
- `/author/katie-mikles`
- `/author/haroon-ashfaq`
- `/author/tom-sharp`

Nothing was removed. The collection totals are unchanged: 80 resources, 31 guides,
9 news, 7 categories.

## Verification and path rules
- Fetch `https://www.brightplace.ai/sitemaps/content.xml` before each production batch.
  Not `/sitemap.xml` — that is the index and contains no article URLs.
- Use the exact sitemap URL; never substitute `/resources/` for `/guides/` or vice versa.
- New Resources article URLs/schemas use `/resources/`; never `/knowledgebase/`.
- All URLs use HTTPS. Internal links use the live sitemap's host and path.
- These lists record historical observations, not current HTTP checks. A blocked
  request is not proof that a domain is dead. Verify replacements before using them.
- Consult `episodic/link-failures.md` for newer discoveries; fresh verified evidence
  overrides historical observations, but permanent policy changes need approval.
- Do not publish unresolved `[INTERNAL LINK: ...]` placeholders; find a valid target
  or flag the link as blocked. Never invent a URL.

## Slugs that do not hold what their name suggests

- **`/resources/apartments-with-no-credit-check`** is live (200, in the sitemap) but
  serves **"How to Rent an Apartment with Bad Credit"**, not a no-credit-check article.
  Link to it for bad-credit topics only. A no-credit-check draft was prepared as an
  overwrite of this same Webflow item (`6a42d7dc3123ff16d5f95e7a`) and never published;
  it was removed on 2026-09-24 at the user's instruction. The topic is unclaimed — if
  it gets written, it needs its own slug, not this one.

## Known Non-Existent Internal URLs (NEVER link to)
- `/resources/studio-apartments`
- `/resources/pet-friendly-houses-for-rent`
- `/resources/1-bedroom-apartments-near-me`
- `/guides/studio-apartments`

## Known Broken External URLs (use replacement)

| Broken URL | Replacement |
|---|---|
| `consumerfinance.gov/consumer-tools/renting/` | `consumerfinance.gov/housing/housing-insecurity/help-for-renters/` |
| `consumerfinance.gov/housing/renting/` | `consumerfinance.gov/housing/housing-insecurity/help-for-renters/` |
| `consumer.ftc.gov/articles/renting-home` | `consumerfinance.gov/housing/housing-insecurity/help-for-renters/` |
| `ftc.gov/news-events/topics/consumer-protection` | `consumerfinance.gov/housing/housing-insecurity/help-for-renters/` |
| `consumer.ftc.gov/articles/what-know-about-homeowners-renters-insurance` | `consumerfinance.gov/housing/housing-insecurity/help-for-renters/` |
| `azag.gov/consumer/landlord-tenant` | `azag.gov/civil-rights/fair-housing` |
| `dhcd.virginia.gov/landlord-tenant` | `dhcd.virginia.gov/landlord-tenant-resources` |
| `hud.gov/program_offices/comm_planning/affordablehousing/` | `hud.gov/topics/rental_assistance` |
| `sandiego.gov/park-and-recreation/parks/regional/mission-bay` | `sandiego.gov/parks-and-recreation` |
| `sandiego.gov/treasurer/short-term-residential-occupancy-tax` | `sandiego.gov/treasurer/short-term-residential-occupancy` |
| `mecknc.gov/CodeEnforcement/Pages/default.aspx` | `mecknc.gov/luesa/codeenforcement/` |
| `ridetransit.org` | `charlottenc.gov/cats/home/` |
| `hcr.ny.gov/tenant-protection` | `hcr.ny.gov/` |
| `hcr.ny.gov/system/files/documents/2020/11/fact-sheet-07-09-2020.pdf` | `hcr.ny.gov/` |
| `nyc.gov/site/dca/about/about-dca.page` | `nyc.gov/site/dca/` |
| Any `nyc.gov/site/hpd/...` deep link | `nyc.gov/hpd` (deep links return 403) |
| `greenvillerec.com/swamp-rabbit-trail/` | `greenvillerec.com/` |
| `sjcfl.us/Parks/TreatyPark` | `sjcfl.us/Beaches` |
| `redstone.army.mil` | Remove link, keep text (domain dead) |
| `tdhca.texas.gov` | `texas.gov` (domain dead) |
| `texasattorneygeneral.gov/.../renters-rights` | `texas.gov` (domain dead) |
| `trec.texas.gov` | `texas.gov` (domain dead) |
| `scps.k12.fl.us` | `scps.us` (domain moved) |

## Approved External URLs (confirmed working July 2026)
- `hud.gov/topics/rental_assistance`
- `hud.gov/program_offices/fair_housing_equal_opp`
- `consumerfinance.gov/housing/housing-insecurity/help-for-renters/`
- `consumerfinance.gov/consumer-tools/credit-reports-and-scores/`
- `floodsmart.gov`
- `annualcreditreport.com`
- `rentguidelinesboard.cityofnewyork.us/`

## Historically used internal URLs (verify exact sitemap path)
- `/guides/how-to-rent-an-apartment` (resolved conflicting legacy Resources entry using the source sitemap rule)
- `/resources/pet-deposit-vs-pet-fee`
- `/resources/renters-insurance-with-roommates`
- `/resources/short-term-lease-agreement`
- `/resources/move-in-specials-apartments`
- `/resources/apartments-with-no-credit-check`
- `/resources/homes-for-rent-no-deposit`
- `/resources/what-does-income-restricted-mean`
- `/resources/prorated-rent`
- `/resources/cheap-one-bedroom-apartments`
- `/resources/affordable-places-to-live-in-florida`
- `/resources/one-bedroom-apartment-nyc`
- `/resources/sublet-apartments-nyc`
- `/resources/cat-friendly-apartments`
- `/resources/apartments-with-dog-parks`
- `/resources/questions-to-ask-when-touring-an-apartment`
- `/resources/rent-affordability-18-an-hour`
- `/resources/month-to-month-vs-12-month-lease`

## Pages Under /guides/ (NOT /resources/)
your-true-monthly-cost, how-to-rent-an-apartment, brooklyn-neighborhood-guide, denver-city-orientation, phoenix-renters-orientation, austin-young-professionals, dallas-families, houston-city-orientation, charlotte-affordable-neighborhoods, nashville-corporate-relocation-neighborhoods, relocating-to-austin, miami-city-orientation, chicago-pet-owners, huntsville-renters-orientation, knoxville-young-professionals, philadelphia-city-orientation, tampa-renters-orientation, kansas-city-young-professionals, dog-friendly-neighborhoods-san-diego

## Additional historical guide targets
- `/guides/atlanta-active-renters`
- `/guides/columbia-usc-student`
- `/guides/dc-empty-nesters`
- `/guides/fort-collins-outdoor-renters`
- `/guides/greensboro-renters-orientation`
- `/guides/lexington-student-neighborhoods-uk`
- `/guides/minneapolis-city-orientation`
- `/guides/raleigh-durham-young-professionals`
- `/guides/salt-lake-city-renters-orientation`
- `/guides/ut-austin-student-housing`
