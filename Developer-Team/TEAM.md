# brightplace Developer Team — Agent Architecture

## Mission
Build production-grade, SEO-first websites for any client. Every page must be server-rendered HTML that AI crawlers and search engines can read without executing JavaScript. Premium design. Zero AI slop.

## USP (Non-Negotiable)
**Server-Side Rendering ONLY.** No client-side rendering that blocks crawlers.
- All content MUST be in the HTML source
- `'use client'` ONLY for interactive enhancements (animations, toggles, forms)
- Text, data, pricing, FAQs = server-rendered
- Animations, hover effects, accordions = client-side progressive enhancement
- AI crawlers (GPTBot, ClaudeBot, PerplexityBot) see ALL content without JS

## Tech Stack
- **Framework:** Next.js 15+ App Router (Server Components by default)
- **Language:** TypeScript (strict)
- **Animation:** Framer Motion (`motion/react`)
- **Styling:** CSS custom properties + inline styles
- **Deployment:** Vercel (SSG + ISR)
- **Data:** JSON files → Supabase at scale

## Skills Library
All agents reference skills in `Developer Agents/skills/`:
- `vercel-web-guidelines.md` — accessibility, forms, performance, anti-patterns
- `taste-core-skill.md` — anti-AI-slop rules, 40+ banned patterns, pre-flight checks
- `image-to-code-skill.md` — design-first workflow, analysis-before-coding
- `vercel-design-system.md` — premium SaaS aesthetic reference (colors, type, spacing, shadows)

## Agent Roster (8 agents)

### 1. Flow Agent (`flow-agent.md`)
**Role:** Production orchestrator
**When:** Every page change
**Pipeline:** Research → Design → Build → Desktop QA → Mobile QA → SEO Audit → Cross-Page QA → Deploy

### 2. Design Agent (`design-agent.md`)
**Role:** UI/UX architect
**Skills used:** taste-core-skill, vercel-design-system, image-to-code-skill
**Enforces:** Three dials (variance/motion/density), anti-slop checklist, pre-flight checks

### 3. Developer Agent (`developer-agent.md`)
**Role:** Frontend engineer
**Skills used:** vercel-web-guidelines, taste-core-skill
**Enforces:** Server-first rendering, SSR content, client progressive enhancement only

### 4. Operator Writing Agent (`operator-writing-agent.md`)
**Role:** Content writer for property stories
**Enforces:** AEO/SEO rules, entity density, BLUF format, date-stamped data

### 5. Story Page Agent (`story-page-agent.md`)
**Role:** Content strategist
**Enforces:** Keyword research, content gaps, cross-linking strategy

### 6. QA Agent (`qa-agent.md`)
**Role:** Desktop quality assurance
**Skills used:** vercel-web-guidelines
**Enforces:** 18 checks across 6 sections

### 7. Mobile QA Agent (`mobile-qa-agent.md`)
**Role:** Mobile quality assurance
**Enforces:** 7 checks at 4 viewports (375/390/428/768px)

### 8. SEO Audit Agent (`seo-audit-agent.md`)
**Role:** SEO and data consistency
**Enforces:** 23 checks — schemas, meta tags, crawlability, data consistency, accessibility

## How To Use This Team

### For a new client site:
1. **Flow Agent** orchestrates the entire build
2. **Design Agent** creates the visual spec using skills
3. **Developer Agent** builds server-rendered components
4. **QA Agent** validates desktop quality
5. **Mobile QA Agent** validates mobile
6. **SEO Audit Agent** validates search readiness
7. **Flow Agent** approves deployment

### For new content:
1. **Story Page Agent** identifies keywords and content gaps
2. **Operator Writing Agent** writes the article
3. **SEO Audit Agent** validates schemas and meta
4. **Flow Agent** approves deployment

### For design improvements:
1. **Design Agent** audits current design against taste-core-skill
2. **Image-to-Code Skill** converts reference screenshots to code
3. **Developer Agent** implements changes
4. Full QA pipeline runs

## Rules For ALL Agents

1. **Server-rendered content is LAW.** If a crawler can't see it, it doesn't exist.
2. **Zero em-dashes.** The #1 AI tell. Use periods, commas, or line breaks.
3. **brightplace always lowercase.** Even at sentence start.
4. **No banned phrases.** (See writing agent for full list)
5. **44px minimum touch targets.** On every interactive element.
6. **12px minimum text.** On every screen size.
7. **One H1 per page.** Sequential heading levels.
8. **Every image needs alt text.** Including `role="img"` divs.
9. **All URLs HTTPS.** No http links anywhere.
10. **npm run build must pass.** Before every deployment.
