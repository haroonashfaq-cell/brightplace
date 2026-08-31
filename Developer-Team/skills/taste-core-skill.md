# Taste Skill — Core Design Rules
# Source: github.com/Leonxlnx/taste-skill (MIT License)

## Purpose
Bias-correction layer for AI-generated frontend. Prevents generic "AI slop" design.

## Three Control Dials (Set Before Building)

| Dial | Range | Meaning |
|---|---|---|
| DESIGN_VARIANCE | 1-10 | Symmetrical (1) → Asymmetric (10) |
| MOTION_INTENSITY | 1-10 | Static (1) → Cinematic (10) |
| VISUAL_DENSITY | 1-10 | Art gallery (1) → Packed (10) |

**brightplace baseline: 7 / 5 / 3** (editorial, moderate motion, airy)

## The 40+ AI Design Tells (BANNED)

### Typography
- NEVER default to Inter, Roboto, Arial, Open Sans
- NEVER use serif "just because creative" without justification
- NEVER use AI-purple gradients or neon glows without intent

### Layout
- NEVER do centered hero on non-manifesto briefs
- NEVER use three equal feature cards (use asymmetric grid, bento, or zig-zag)
- NEVER use eyebrows above every section (max 1 per 3 sections)
- NEVER do 3+ consecutive image+text zigzag sections
- NEVER use split-header pattern (big headline left, small explainer right) as default

### Content
- NEVER use filler verbs: "Elevate", "Seamless", "Unleash", "Empower"
- NEVER use fake-precise numbers without real data (92%, 4.1x)
- NEVER use generic names ("John Doe", "Acme Co")

### Visuals
- NEVER use div-based fake product screenshots
- NEVER hand-roll SVG icons (use Phosphor, Radix, Tabler)
- NEVER use stock photos without intent

### Critical
- **ZERO em-dashes (—) anywhere.** This is the #1 AI tell. Use periods, commas, or line breaks.

## Mandatory Pre-Flight Checks

Before shipping ANY page:
- [ ] Zero em-dashes in entire output
- [ ] Button contrast WCAG AA (4.5:1)
- [ ] CTA buttons one-line at desktop
- [ ] No duplicate CTA intent on same page
- [ ] Hero fits initial viewport (headline ≤ 2 lines)
- [ ] Hero top padding max pt-24
- [ ] Navigation one line at desktop (max 80px height)
- [ ] Eyebrow count ≤ ceil(sectionCount / 3)
- [ ] Reduced motion honored for motion > intensity 3
- [ ] Dark mode tested
- [ ] Mobile collapse explicit
- [ ] Section layout uses ≥ 4 different families across 8 sections
- [ ] No AI hallucinations in copy
- [ ] No filler verbs

## Motion Rules
- Use `motion/react` (not `framer-motion` import)
- Use `useMotionValue`/`useTransform` for continuous values
- NEVER use `window.addEventListener('scroll', ...)`
- NEVER store scroll position in React state
- Animations must be interruptible
