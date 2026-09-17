# Brand Rules — brightplace (Zero Tolerance)

> Source of truth. All agent files reference this instead of embedding rules inline.
> Last updated: 2026-09-16

## Naming

Added to canonical memory: 2026-09-16. Sources: `Agents/content-writing-guidelines.md` §1; `Agents/seo-writing-agent.md` Hard Rules; `Agents/qa-agent.md` §1; Claude project `MEMORY.md`; approved memory-system plan Key Extract #1.
- brightplace is ALWAYS lowercase. Even at the start of a sentence. Even in headings. No exceptions.
- brightplace is an "AI-powered rental search tool" — NEVER say "listing site", "listing platform", "listings", "browse listings"

## Punctuation

Added to canonical memory: 2026-09-16. Sources: `Agents/content-writing-guidelines.md` §1; `Agents/seo-writing-agent.md` Hard Rules; `Agents/qa-agent.md` §1; Claude project `MEMORY.md`; approved memory-system plan Key Extract #1.
- NEVER use em dashes. Not as `--` and not as the unicode character `—`.
- Replace with commas, periods, semicolons, colons, or parentheses.
  - Wrong: "The neighborhood is walkable -- something rare in Texas."
  - Right: "The neighborhood is walkable, something rare in Texas."

## Banned Word

Added to canonical memory: 2026-09-16. Sources: `Agents/content-writing-guidelines.md` §1; `Agents/seo-writing-agent.md` Hard Rules; `Agents/qa-agent.md` §1; Claude project `MEMORY.md`; approved memory-system plan Key Extract #1.
- NEVER use the word "signal" in any form (signal, signals, signaling, signaled).
- Alternatives: "indicator," "suggests," "points to," "reflects."

## Banned Phrases

Added to canonical memory: 2026-09-16. Sources: `Agents/content-writing-guidelines.md` §1; `Agents/seo-writing-agent.md` Hard Rules; `Agents/qa-agent.md` §1; Claude project `MEMORY.md`; approved memory-system plan Key Extract #1.
Never use any of the following:
- "deep dive" / "dive into"
- "navigate" (as metaphor)
- "landscape" (as metaphor)
- "unlock" / "leverage" (as verbs)
- "whether you're X or Y"
- "from X to Y" (as a range framing device)
- "it's worth noting that"
- "it should be mentioned"
- "interestingly" / "notably" / "arguably"
- "hidden gem" / "best-kept secret"
- "vibrant" / "bustling" / "thriving"
- "In this article, we will cover..."
- "Let's take a look at..."
- "Without further ado"
- "In today's [anything]"
- "nestled"
- "boasts"
- "plethora" / "myriad"
- "elevate"
- "tailor" / "tailored"
- "robust"
- "streamline"
- "spearhead"
- "foster"
- "paramount"
- "beacon"
- "tapestry"
- "moreover" / "furthermore"
- "in terms of"
- "at the end of the day"
- "in today's market"

## Title and Heading Rules

Added to canonical memory: 2026-09-16. Sources: `Agents/content-writing-guidelines.md` §1; `Agents/seo-writing-agent.md` Hard Rules; `Agents/qa-agent.md` §1; Claude project `MEMORY.md`; approved memory-system plan Key Extract #1.
- Never use ranking language: no "Top X", "Best", "Ultimate Guide", "#1", "Everything You Need to Know"
- Use curation framing: inform, present options, guide
- SEO title MUST differ from H1 (duplicate triggers site audit warning)
- SEO title must end with ` | brightplace` (pipe separator, not dash)

## Banned Sources (Never Cite or Link To)

Added to canonical memory: 2026-09-16. Sources: `Agents/content-writing-guidelines.md` §1; `Agents/seo-writing-agent.md` Hard Rules; `Agents/qa-agent.md` §1; Claude project `MEMORY.md`; approved memory-system plan Key Extract #1.
**ILS Platforms:** Apartments.com, Zillow, Trulia, Rent.com, Zumper, Apartment List, HotPads, RentCafe, Realtor.com, ForRent.com, Padmapper

**Review Aggregators:** ApartmentRatings, Yelp, Google Reviews (as citation source), Niche, AreaVibes, Crime Grade, Openigloo

**Score Sites:** Walk Score, Bike Score, Transit Score, GreatSchools (as primary citation)

**Forums:** Reddit, City-Data, BiggerPockets

## Fair Housing Compliance

Added to canonical memory: 2026-09-16. Sources: `Agents/content-writing-guidelines.md` §1; `Agents/seo-writing-agent.md` Hard Rules; `Agents/qa-agent.md` §1; Claude project `MEMORY.md`; approved memory-system plan Key Extract #1.
- Never describe neighborhoods by who lives there (race, ethnicity, religion, national origin, familial status, sex, disability, sexual orientation)
- Never include crime statistics, safety ratings, or safety-adjacent language ("safe area", "low crime", "avoid after dark")
- Never use "gentrification" language. Use market dynamics framing instead.
- Describe neighborhoods by lifestyle infrastructure only: walkability, dining, nightlife, transit, parks, grocery, coffee, fitness, coworking, schools (for family content), pet infrastructure (for pet content)

## QA interpretation and scoped additions

Added: 2026-09-16. Sources: `Agents/qa-agent.md` §1 and
`Agents/renters-corner-guidelines.md` brand/Fair Housing sections.
- Apply body-language checks to published content, excluding internal Research Notes,
  HTML comments, code syntax, and frontmatter delimiters (`---`). Naming also applies
  to headings, CTAs, and schema organization names.
- QA also rejects K-12 school quality rankings/ratings. Infrastructure descriptions
  may name schools without ratings or demographic steering.
- Renter's Corner additionally avoids named commercial vendors in body copy and
  the phrase "most underrated"; Research Notes may retain verification context.
- No NMHC rankings or operator-ranking references in published content.
- Rule changes require an explicit user decision recorded in candidate-rules.md.
  An anecdote, trend, or agent score cannot override these rules.
