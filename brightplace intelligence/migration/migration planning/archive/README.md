# Archive

Superseded or one-time material. Not needed to build the site — kept for traceability.

| File | Why it's here |
|---|---|
| `migration-plan-v1.md` | Superseded by `migration-plan-v2.md`. Assumed a separate Next.js repo and an untouched `app.brightplace.ai`. Kept for the reasoning trail. |
| `EXTRACTION-PLAN.md` | The plan for the Webflow extraction, which is complete. Results are in `extract/`. |
| `build-pages.py`, `build-listings.py` | Generated the 127 `.page.html` and 3 `_listing.page.html` files in `extract/`. |
| `extract-guides.py`, `html2md.py` | Pulled content from the Webflow Data API and converted bodies to markdown. |
| `HTML sample.html` | Rendered Webflow **guide** page, captured from the live site. |
| `Resources-HTML template.html` | Rendered Webflow **resource** page. |
| `Resources Archive Page Sample HTML.html` | Rendered Webflow **archive** page. |

## About the three rendered samples

These are the **only records of how brightplace.ai looked on Webflow**.

The 127 `.page.html` files in `extract/` were generated from the blank templates, so they show content in the *new* structure with generic styling — not the Webflow design. If a visual reference for the old site is ever needed, it is these three files and nothing else.

They are also the source the design tokens in `TEMPLATE-blog-page.html` were sampled from.

## Internal only

`migration-plan-v1.md` and `EXTRACTION-PLAN.md` are internal planning records — see `DOC-INDEX.md`. Do not send them to the dev team.

The extraction scripts stay runnable in case anything needs re-pulling before the Webflow account is cancelled. After cancellation they are historical only.
