# Vercel Design System Reference
# Source: github.com/VoltAgent/awesome-design-md (MIT License)
# Use as REFERENCE for premium SaaS aesthetic, not as direct copy

## Color System
- Ink: #171717 (primary CTA, text on light)
- Canvas: #ffffff (cards, modals)
- Canvas Soft: #fafafa (page background)
- Canvas Soft 2: #f5f5f5 (inset surfaces)
- Hairline: #ebebeb (1px dividers, borders)
- Body: #4d4d4d (secondary text)
- Mute: #888888 (lowest-priority text)
- Link: #0070f3 (links, success)
- Error: #ee0000 (destructive)
- Warning: #f5a623 (caution)

## Typography
- Display: Geist 600, negative tracking (-2.4px to -0.6px)
- Body: Geist 400, 16px/24px
- Caption: 12px/16px
- Code: Geist Mono 400, 13px
- Headlines: sentence-case, period-terminated
- Display ceiling: weight 600 (never 700+)

## Spacing (4px base)
- xs: 8px (tight gaps)
- sm: 12px (inline gaps)
- md: 16px (container gutters)
- lg: 24px (card padding)
- xl: 32px (larger cards)
- 4xl: 64px (section padding)
- 5xl: 96px (feature bands)
- section: 192px (hero top/bottom)

## Border Radius
- sm: 6px (inputs, nav buttons)
- md: 8px (feature cards)
- lg: 12px (pricing cards)
- pill: 100px (marketing CTAs)
- full: 9999px (icon buttons)

## Shadows (Stacked, Never Single Heavy Drop)
- Level 1: `0 0 0 1px #00000014` inset (default card)
- Level 2: Subtle drop + inset hairline (marketing cards)
- Level 3: Soft stack + inset hairline (feature cards)
- Level 4: Float stack (pricing, callouts)
- Level 5: Modal (dialogs, dropdowns)

## Buttons
- Primary: #171717 bg, white text, pill radius, 48px height
- Secondary: white bg, #171717 text, pill radius
- Nav: sm radius (6px), 28-32px height
- Touch target minimum: 44x44px

## Layout
- Max width: 1400px
- Gutters: 24px desktop, 16px mobile
- Bands stretch edge-to-edge, content centered
- Section padding: 96px top/bottom
- Hero padding: 192px

## Responsive
- Mobile (<600px): stacked, hamburger nav
- Tablet (600-959px): 2-up grids
- Desktop (960+): full layouts
- Touch targets: 44x44px minimum on mobile

## Do's
- Reserve dark color for primary CTAs only
- Use pill radius for marketing CTAs, sm for nav
- Sentence-case headlines with period termination
- Cycle surfaces: soft → white → dark bands
- Layer stacked shadows with inset hairline

## Don'ts
- Don't use all-caps headlines
- Don't use single heavy drop-shadow
- Don't use display weight 700+
- Don't mix pill and sm radius on same screen
