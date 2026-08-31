# Image-to-Code Skill
# Source: github.com/Leonxlnx/taste-skill (MIT License)

## Core Workflow
**Image generation first → Deep image analysis second → Implementation third**

Never jump straight to code. Always analyze the visual reference first.

## Configuration Baseline

| Metric | Value | Meaning |
|---|---|---|
| Design Variance | 8/10 | Art-directed, not rigid |
| Visual Density | 3/10 | Airy, calm, spacious |
| Art Direction | 8/10 | Bold, not safe |
| Implementation Clarity | 9/10 | Highly buildable |
| Spacing Generosity | 9/10 | Breathable layouts |
| UI Simplicity | 9/10 | Reduce clutter aggressively |

## Key Rules

### Design Principles
- Maintain spacious, readable layouts visible on small laptops
- Avoid nested boxes (cards-within-cards)
- Minimize micro-UI clutter (pills, fake badges, system jargon)
- Keep hero sections clean with 1-3 line headlines maximum
- Visual density 3/10 while maintaining clarity at 9/10

### Analysis Before Coding
When given a design reference image, extract:
1. **Typography**: fonts, weights, sizes, line-heights, letter-spacing
2. **Spacing**: padding, margins, gaps between elements
3. **Colors**: exact hex values, gradients, opacity levels
4. **Buttons**: styles, radii, padding, hover states
5. **Layout**: grid structure, column counts, responsive behavior
6. **Components**: cards, forms, navigation patterns

### Implementation Rules
- Match the reference image pixel-for-pixel where possible
- Do NOT add features not present in the reference
- Do NOT change colors, fonts, or spacing from what was analyzed
- If a detail is missing from the reference, ask — don't invent
- Anti-drift: constantly compare your code output to the reference

### Anti-Patterns
- Never compress multiple sections into one image
- Never crop existing images instead of generating fresh ones
- Never add decorative elements not in the reference
- Never change the visual hierarchy from what was designed
