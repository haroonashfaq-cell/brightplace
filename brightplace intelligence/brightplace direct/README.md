# brightplace direct — Content Engine for Operators

**What it is:** An AI-powered content engine that researches keywords, writes articles, and publishes SEO-optimized content for apartment operators.

**What it is NOT:** A website builder. Templates and site deployment are handled by the developer team (Tom & Dennis). brightplace direct is purely the content production pipeline.

## What We Do

```
CONTENT ENGINE (our scope)
1. Keyword Agent → researches and suggests keywords for the operator
2. Operator approves keywords for writing
3. Brief Agent → auto-generates content brief from approved keyword
4. Writing Agent → writes the article (uses operator's brand guidelines + business context)
5. QA Agent → validates quality, accuracy, SEO, AI readiness
6. Image Agent → generates featured image
7. Publish Agent → pushes content to operator's site
8. Analytics → tracks traffic, leads, AI citations

CONTINUOUS OPTIMIZATION
- Monthly keyword refresh
- Competitor gap analysis
- Content performance reporting
- AI citation monitoring
```

## What Developer Team Does (NOT our scope)
- Template design and selection (Tom & Dennis provide 6 templates)
- Site deployment to [operator].brightplace.ai
- Property page components (rent calculator, floor plans, amenities, etc.)
- Technical infrastructure (Vercel, DNS, SSL)

## Folder Structure

```
brightplace direct/
├── README.md              ← This file
├── PRODUCT-FLOW.md        ← Complete content engine flow
└── Agents/
    ├── keyword-agent.md   ← Keyword research + suggestions for operators
    ├── brief-agent.md     ← Auto-generates content briefs from keywords
    ├── writing-agent.md   ← Writes articles with operator brand context
    ├── qa-agent.md        ← Quality assurance (6 sections)
    ├── image-agent.md     ← Featured image generation
    └── publish-agent.md   ← Pushes content to operator site
```

## Relationship to Other Systems

| System | Owner | Purpose |
|---|---|---|
| **brightplace intelligence** | Content team (us) | Content engine for brightplace.ai (our own site) |
| **brightplace direct** | Content team (us) | Content engine for operator sites (client sites) |
| **operator-pages** | Developer team | Next.js codebase that powers operator websites |
| **Developer-Team** | Developer team | Generic agents for building any site |

## How Content Flows

```
Keyword Agent suggests → Operator approves → Brief Agent generates →
Writing Agent writes → QA Agent validates → Image Agent creates →
Publish Agent pushes to site (developer team's codebase)
```

We produce the content. Developer team provides the site it goes into.
