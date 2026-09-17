# Link Registry

Migrated: 2026-09-16. Sources: `Agents/WORKFLOW.md` URL tables; `Agents/qa-agent.md` §§5–6; `Agents/master-writer-agent.md`; Claude project `MEMORY.md`.

## Verification and path rules
- Fetch `https://www.brightplace.ai/sitemap.xml` before each production batch.
- Use the exact sitemap URL; never substitute `/resources/` for `/guides/` or vice versa.
- New Resources article URLs/schemas use `/resources/`; never `/knowledgebase/`.
- All URLs use HTTPS. Internal links use the live sitemap's host and path.
- These lists record historical observations, not current HTTP checks. A blocked
  request is not proof that a domain is dead. Verify replacements before using them.
- Consult `episodic/link-failures.md` for newer discoveries; fresh verified evidence
  overrides historical observations, but permanent policy changes need approval.
- Do not publish unresolved `[INTERNAL LINK: ...]` placeholders; find a valid target
  or flag the link as blocked. Never invent a URL.

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
