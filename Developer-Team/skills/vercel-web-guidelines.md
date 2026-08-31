# Vercel Web Interface Guidelines
# Source: github.com/vercel-labs/agent-skills

## Accessibility
- Icon-only buttons require `aria-label`
- Form controls need `<label>` or `aria-label`
- Interactive elements need keyboard handlers
- Use `<button>` for actions, `<a>` for navigation (never `<div onClick>`)
- Images require `alt` (or `alt=""` if decorative)
- Hierarchical headings h1-h6 with skip link
- Heading anchors need `scroll-margin-top`

## Focus States
- Interactive elements need visible focus: `focus-visible:ring-*`
- Never use `outline-none` without focus replacement
- Prefer `:focus-visible` over `:focus`
- Sticky headers must not obscure focused elements

## Forms
- Inputs need `autocomplete` and meaningful `name`
- Use correct `type` (email, tel, url, number) and `inputmode`
- Never block paste
- Labels must be clickable
- Submit button enabled until request starts, show spinner during request
- Errors display inline next to fields, focus first error on submit
- Warn before navigation with unsaved changes

## Animation
- Honor `prefers-reduced-motion`
- Animate only `transform`/`opacity` (compositor-friendly)
- Never use `transition: all` — list properties explicitly
- Animations must be interruptible

## Typography
- Use ellipsis character not three dots
- Use curly quotes not straight
- Use `font-variant-numeric: tabular-nums` for number columns
- Apply `text-wrap: balance` on headings

## Images
- `<img>` needs explicit `width` and `height` (prevents CLS)
- Below-fold: `loading="lazy"`
- Above-fold: `priority` or `fetchpriority="high"`

## Performance
- Large lists (>50 items): virtualize
- No layout reads in render
- Add `<link rel="preconnect">` for CDN domains
- Critical fonts: `<link rel="preload" as="font">`

## Navigation & State
- URL reflects state (filters, tabs, pagination in query params)
- Links use `<a>` (supports Cmd+click, middle-click)
- Destructive actions need confirmation or undo

## Touch & Interaction
- `touch-action: manipulation` (prevents double-tap zoom)
- `overscroll-behavior: contain` in modals/drawers
- Use `autoFocus` sparingly — desktop only

## Anti-patterns (Always Flag)
- `user-scalable=no` disabling zoom
- `transition: all`
- `outline-none` without replacement
- `<div>` with click handlers instead of `<button>`
- Images without dimensions
- Form inputs without labels
- Icon buttons without `aria-label`
- Hardcoded date/number formats
