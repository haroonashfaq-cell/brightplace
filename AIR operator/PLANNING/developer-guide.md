# PART 2: Developer Guide — How to Build the Sites

How the existing property pages work and how to add the 5 AIR communities.

---

## Tech Stack

- **Next.js 15+** with App Router
- **TypeScript** (strict mode)
- **Framer Motion 11+** for animations
- **CSS custom properties** for styling (no Tailwind, no CSS modules)
- **Static export** deployed on **Vercel**

## How Property Pages Work

**Step 1: All property data lives in a TypeScript file**

`src/data/operators.ts` defines a typed interface (`PropertyData`) with every field a property page needs: name, address, floor plans, amenities, FAQs, pricing, images, meta tags, neighborhood info, etc.

Each community's data is a separate file under `src/data/operators/[operator-name]/`.

**Step 2: Pages are generated at build time**

`src/app/[operator]/[slug]/page.tsx` uses `generateStaticParams()` to list every operator + property combination. Next.js builds a separate HTML file for each one.

**Step 3: Components compose the page**

Each property page is built from 10 reusable components:
1. `Header` — navigation + branding
2. `Hero` — hero image, headline, promo banner
3. `RentCalculator` — all-in pricing breakdown
4. `FloorPlans` — interactive floor plan gallery
5. `Amenities` — community + apartment features
6. `Neighborhood` — nearby attractions with distances
7. `Gallery` — image lightbox
8. `FAQ` — accordion with structured data
9. `TourCTA` — call-to-action for scheduling
10. `Footer` — links, legal, contact

Plus `AIAssistant` (chat widget) and `StoryLayout` (for guide/article pages).

**Step 4: Build outputs pure HTML**

`npm run build` generates an `out/` directory with static HTML files. Vercel serves these from its CDN edge network. No Node.js server needed at runtime.

## File Structure

```
operator-pages/
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Root layout (fonts, global CSS)
│   │   ├── page.tsx                # Homepage
│   │   └── [operator]/
│   │       ├── page.tsx            # Operator landing
│   │       └── [slug]/page.tsx     # Property page (SSG via generateStaticParams)
│   ├── components/                 # 13 reusable React components
│   ├── data/                       # Static operator data (TypeScript)
│   └── lib/                        # Utilities, animation presets
├── public/
│   ├── robots.txt                  # AI crawler permissions
│   ├── llms.txt                    # LLM-readable site summary
│   ├── sitemap.xml                 # All pages listed
│   └── images/                     # Per-operator image folders
├── out/                            # Static export output (built HTML)
├── next.config.ts                  # output: 'export'
└── vercel.json                     # Headers, routing
```

## To Add a New Community (e.g., Foxchase)

1. Create `src/data/operators/air-communities/foxchase.ts` with all property data following the `PropertyData` interface
2. Add property images to `public/images/air-communities/`
3. Register the property in the operator's index so `generateStaticParams()` picks it up
4. Run `npm run build` — verify the HTML file appears in `out/`
5. Push to GitHub — Vercel auto-deploys

---

