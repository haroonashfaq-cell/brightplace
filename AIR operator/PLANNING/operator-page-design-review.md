# brightplace Direct: operator overview design direction

Design-agent review, 16 September 2026. Proposed content and interaction direction for the developer reference, not approved launch copy.

## Design read

An apartment operator should understand what Direct includes, what renters do with it, and how that connects to their leasing team before encountering the broader industry thesis.

Control dials: DESIGN_VARIANCE 7 / MOTION_INTENSITY 2 / VISUAL_DENSITY 3. Warm editorial design with a plainly explained product. Content stays readable without JavaScript. One page only.

## Section-by-section plan

### 1. Hero: explain the offer immediately

Suggested heading: **Help renters choose. Connect them directly to your team.**

Suggested description: **brightplace Direct brings community websites, a renter advisor and helpful content together, so renters can understand cost, availability and fit before they contact you.**

Supporting factual line: Community experiences on brightplace.ai, built around your community information.

Primary action: **See how it works**, linking to the product walkthrough. Header navigation: What you get, Renter experience, AIR pilot. Avoid adding a second primary action before the offer is understood.

Visual: a real, approved AIR community screenshot with a short caption naming what the renter can do. If a usable screenshot is unavailable, show a typographic flow explicitly labeled **Illustrative renter journey**. Do not invent product UI or imply that an illustration is a screenshot.

The existing headline about the relationship starting before the lead is a thesis. Move that idea below the explanation of the product.

### 2. What you get: three deliverables, three practical uses

Heading: **One experience, from the first question to the next step.**

Use editorial rows with a deliverable, a renter use, and an operator implication. Do not put three equally sized promotional cards side by side.

| Included | What a renter can do | Why an operator would care |
|---|---|---|
| Data-connected community websites | Explore community details, availability and cost information. | Give renters a place to understand the community before contacting leasing. |
| A renter advisor | Ask about affordability, everyday needs and tradeoffs. | Make community information useful in the context of a renter's questions. |
| Helpful community content | Find explanations of the questions that come before an inquiry. | Publish useful answers associated with the operator's communities. |

Do not promise fewer leasing calls, more qualified leads or organic ranking improvements without evidence.

### 3. Walkthrough: show the experience with one question

Heading: **“What would living here actually cost?”**

Use a connected, numbered sequence. The reader should be able to follow it without clicking:

1. **A renter has a question.** They want to understand the monthly cost before deciding whether to inquire.
2. **Your community helps them explore.** They review available community information and ask the advisor about costs and affordability.
3. **They choose their next step.** When they want to continue, they can use the community's contact path to reach the leasing team.

Place the operator takeaway below the entire sequence: **Your community becomes a place to make a decision, with a direct path to your team.**

If interactive examples are added, use native buttons for Cost / Fit / Availability with a visible active state and matching explanatory text. Label these as illustrative examples. Do not add a pretend chat input, fake live response, invented rent, qualification recommendation or availability claim. The core journey remains visible with scripts disabled.

### 4. Operator rationale: explain the business relevance

Heading: **Be useful before the inquiry arrives.**

Keep this compact. Renters make decisions while comparing cost, needs and availability. Direct gives those questions a community-specific home and a route to the operator's team.

Use a two-column editorial comparison titled **Discovery** and **Decision**, not unsupported claims that all ILS platforms or websites lack a feature. Explain how helpful content invites exploration and the site plus advisor supports understanding. The value is the connected experience; do not state that Direct replaces every existing vendor or integration.

### 5. AIR pilot: evidence, not ornament

Heading: **See the approach in the AIR pilot.**

Use an actual captured page, a named community, a descriptive caption, and two or three annotations identifying observable features. Link to a confirmed publicly accessible pilot URL only when available. Do not describe a protected staging page as a public experience.

An AIR wordmark on an abstract building illustration does not explain the product. No invented testimonial, conversion statistic, launch count or outcome. Distinguish pilot functionality from launch-wide availability in developer notes.

### 6. Practical questions: remove purchase uncertainty

Heading: **What this means for your team.**

Address these in a short FAQ, publishing only approved answers:

- What is included? Community sites, renter advisor and content, as defined above.
- Where does it live? Community experiences on brightplace.ai.
- How do renters reach our team? Explain the actual community contact path, after verification.
- What information do we provide? Describe the agreed onboarding inputs after confirmation.

Do not invent pricing, guaranteed rollout times, data rights, integration availability or staffing reductions. Track unresolved answers in the developer handoff, not a long list of product-page disclaimers.

### 7. Insights and news: support the case after explaining the offer

Heading: **The thinking behind Direct.**

Feature Apartment Leads Have Disconnected as one larger editorial story with the other two thought-leadership titles as smaller text rows. Press belongs in a separate compact list. Avoid six equivalent cards competing with the product explanation.

Pending announcements and unpublished articles should not have working-looking empty links. Keep their content records in the handoff; render only approved public links in production. This section must not outrank What you get or AIR proof.

### 8. Closing action: give the operator an understandable next step

Heading: **See what Direct could look like for your communities.**

Suggested CTA: **Request a Direct walkthrough**. Production destination and follow-up expectations need business approval. The sample can demonstrate a clearly labeled local inquiry interaction, but must not imply submission to a real sales system or silently send data.

## Brand, layout and accessibility

- Colors: paper `#FAF6EF`, paper-deep `#F3ECDE`, navy `#1A2744`, ink `#0F1830`, secondary `#2B3655`, muted `#5C6580`, borders `#E3DDCF`, orange `#F5A623`, teal-deep `#008A9E`. Use navy text on orange buttons. Verify each actual text/background pair; do not assume every palette combination meets contrast requirements.
- Type: Urbanist 600 headings, Lato 400/700 body. Libre Baskerville italic only when it adds editorial meaning. Body 16 or 17px, line-height around 1.6. Headings follow the available 28/36/48/64px scale. Keep desktop hero heading compact.
- Spacing: use 4/8/12/16/24/32/48/64/96/128px tokens. Generous section spacing, restrained component padding. Use at least four layout families: hero, editorial rows, connected sequence, proof feature, FAQ, story shelf.
- Surfaces: paper hero, inset product explanation, paper journey, one navy rationale or closing band. Avoid excessive cards inside cards, gradients, badges and floating decorations.
- Desktop: generous centered content width, asymmetric hero and proof. Tablet: reduce hero text size and use fewer columns. Mobile: one-column reading order, 16 or 24px gutters, full-width proof image, vertical journey, no horizontal page overflow.
- Motion: minimal hover/focus transitions. No scroll-dependent content reveal or decorative continuous animation. Honor reduced-motion preferences.
- Accessibility: one H1, logical headings, visible focus, skip link, 44px minimum action targets, meaningful image alternatives, native details/summary for FAQs, keyboard-operable demo controls. Keep all essential explanations rendered in HTML.
- Copy: lowercase brightplace, capital-D Direct; no em dashes; avoid “signal” externally. No unverified ROI, metrics, pricing, rollout duration or competitor absolutes.

## Review test

After ten seconds, an operator should be able to say: **“This gives my communities websites, an advisor and content that help renters understand their options and reach my leasing team.”**

After scrolling, they should be able to point to one concrete renter journey, actual pilot evidence, and a clear next step. If they can only repeat a slogan about owning relationships, the page still needs work.
