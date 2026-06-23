---
name: renters-corner
description: "Use this skill whenever turning a renter interview transcript into a published-ready Renter's Corner article for brightplace, or when reviewing, editing, or formatting interview-format content where a real renter answers questions and Katie provides expert synthesis. Triggers include: any mention of 'Renter's Corner', 'renter interview', 'interview transcript', 'PoE content', 'proof of experience', 'Katie interview', turning a transcript into a blog/article, or producing conversational Q&A content for SEO/AEO. This skill governs the transcript-to-node transformation, the Proof-of-Experience reality gate, the Fair Housing reframe pattern, and the SEO/AEO node structure. For the full banned-word list, Fair Housing checklist, Webflow embed components, and CMS publishing workflow, defer to the guide-publishing and neighborhood-guide skills, which remain authoritative."
---

# brightplace Renter's Corner Production

This skill turns a real renter interview transcript into a brand-compliant, SEO/AEO-optimized Renter's Corner article. The output is a draft for human sign-off, never an auto-publish.

Renter's Corner content emulates the *structure and density* of a high-signal forum thread (atomic Q&A nodes, first-person experience, answer-first), then adds a named expert on top. The renter's verbatim words are the proof-of-experience that earns AI citations. Katie's synthesis is the authority layer. Both are required.

## Authoritative dependencies (read first, every time)

Before producing anything, read these in order:

1. `guide-publishing/SKILL.md` — banned words, banned sources, SEO/GEO/AEO readiness, Webflow CMS formatting, FAQPage requirement, publishing workflow. **Authoritative for all shared rules.**
2. `neighborhood-guide/SKILL.md` — full Fair Housing checklist, editorial voice, sourcing rules.
3. `/mnt/skills/public/docx/SKILL.md` — required before building the `.docx`.
4. The transcript itself, in full (including any truncated middle sections).

Do not restate or re-derive rules that live in those files. This skill encodes only the transformation and the gates specific to interview content.

## Content brief as input (when present)

When a content brief from the agent pipeline is supplied alongside the transcript, the brief and the transcript are the two halves of one article. The brief is the demand side: queries, phrasing, proof points, tables, citability rules. The transcript is the supply side: the lived experience that answers them. They meet at the H2. Read the brief in full before building nodes. Inputs are now two, not one.

### Surface routing (decide first)
- A brief tagged for `/knowledgebase/` is a synthesized how-to and needs no transcript. Write it per the brief on `/knowledgebase/`. This is not a Renter's Corner job.
- A Renter's Corner piece lives on `/resources/` and is transcript-driven. A brief's keyword graduates to Renter's Corner only when a real transcript covers it.
- Never target the same primary keyword on both surfaces. Route each keyword to exactly one. Prefer Renter's Corner when a matching transcript exists, because the proof-of-experience version out-cites the synthesized one. Default to `/knowledgebase/` otherwise. Promote to Renter's Corner only on a matching transcript plus an explicit tag.

### Brief-to-transcript match (gate before building)
For each brief query, classify against the transcript:
1. **Demand and the transcript covers it** — the strongest node. Build these first. Demand plus proof.
2. **Demand but the transcript is silent** — Katie answers expert-only with no quote, or flag the query for the next interview. Never invent a quote to fill a keyword.
3. **Transcript is rich but no demand** — keep as supporting color or cut. Do not build a node around a query nobody runs.

If the transcript does not cover the brief's core topic at all (for example, a pet brief paired with a no-pets interview), **stop**. There is no supply side. Request a matching transcript rather than fabricating experience. This is Gate 1 applied to the brief.

### Field mapping (brief -> Renter's Corner node skill)
- Primary keyword -> single H1, reframed to cohort + intent (drop "how to," "guide," and ranking words per voice rules)
- Secondary keywords + PAA questions -> H2 node phrasing and FAQ questions (the brief's exact query strings beat the keyword universe)
- Search intent + SERP/competitor gap -> which transcript questions to promote to nodes, and the lead angle
- Entities to mention -> topical-coverage checklist across the nodes
- Proof points, cost tables, definitions -> the answer-first leads and the comparison table, date-stamped exactly as the brief specifies
- Citability rules (first-paragraph, structured-data, definition, proof-point) -> apply to node leads and the table
- E-E-A-T / information-gain gaps -> where Katie's synthesis adds the expert layer competitors lack
- Date-stamp and last-reviewed notes -> carry through unchanged
- Schema (Article, FAQPage, HowTo, Speakable) -> implement as specified
- Recommended word count -> node count and depth
- Internal link suggestions -> internal-links step (existing pages only)

### Override hierarchy (when a brief routes to Renter's Corner)
The brief's research fields are inputs. The Renter's Corner format, voice, expert (Katie), quote/PoE gate, single light CTA, and Fair Housing reframe override any conflicting brief field:
- The brief's how-to section structure yields to the interview-node structure.
- The brief's multiple fixed CTAs yield to one light brightplace mention near the close (keep the brief's CTA copy rules: lowercase, no urgency, no superlatives).
- The brief's "brightplace as first-hand data observer" framing yields to the renter's lived experience as the experience signal; Katie carries the analysis.
- The brief's `/knowledgebase/` slug becomes a `/resources/` slug.

Where brief and Renter's Corner voice agree (banned words, em dashes, Fair Housing, lowercase brand, date-stamps), they reinforce. Apply both.

## Hard gates (pass/fail, block the build)

### Gate 1 — Proof-of-Experience reality check
The governing test is "could an outsider have written this." Fabricated content fails it by definition.

- Inspect the transcript for markers of a synthetic/sample source: `Persona:`, "sample," "benchmark," "calibration," "illustrative," or an obviously constructed character. If present, the output is a **template/demonstration**: keep the structure, but flag in internal notes that quotes are illustrative and that publication requires a real interview with real attribution. Never present a constructed persona as a real customer testimonial.
- If the transcript is a real interview, proceed with real attribution.
- **Never invent quotes, names, prices, or specificity not present in the transcript.** Renter quotes are verbatim, edited only to remove filler, crosstalk, and false starts. Do not paraphrase a quote and present it inside quotation marks.

**Attribution form: verbatim record vs summary.** First determine what the source actually is.
- **A verbatim transcript** (word-for-word, the renter's own sentences) supports **direct quotes**: quotation marks plus "the renter said," lightly cleaned. This is the strongest form and what makes a piece feel alive.
- **An auto-generated summary or paraphrase** (third-person notes from Gemini, Otter, Fireflies, or a notetaker, e.g. "Kali discussed her search and expressed frustration with hidden fees") contains **no verbatim words**. Render the renter's contributions as **indirect reported speech**: "Kali said the hidden fees were her biggest frustration." Never wrap invented words in quotation marks and never attach a direct-quote verb to fabricated text. Quotation marks assert that these are the exact words spoken; only use them when you actually have the words.
- The test in one line: **reported speech attributes the substance; a direct quote attributes the words.** Match the form to what the source proves.
- When the source is summary-only, flag in internal notes that lifting two or three real pull-quotes from the recording will strengthen the piece, and that those spots can then flip to direct quotes. This is an upgrade, never a reason to invent quotes in the meantime. Reported speech with attribution still carries the experience signal that earns the citation.

**Consent gate (before publishing a named real renter).** A real, named renter's account requires the renter's written consent to publish, plus the standard Katie editorial sign-off. Offer first-name-only or a pseudonym if the renter prefers. A genuine, consented account is also what keeps the piece on the right side of FTC testimonial rules; an unconsented or altered one does not.

### Gate 2 — Fair Housing reframe (the highest-frequency edit)
Cultural fit is what renters talk about and exactly what the Fair Housing Act protects. Every interview will surface this. The transcript will almost always contain protected-class framing that **must not** reach published content.

Remove and rewrite any framing that describes an area by who lives there (race, ethnicity, national origin, religion, familial status, sexual orientation), by resident group ("popular with [group]," "[group] community"), or by religious-institution density (churches, mosques, temples).

Rewrite to **amenity-only, renter-led** language: the specific stores, foods, services, and infrastructure the renter named.

**Reframe pattern (before -> after):**

> Source (transcript): renter wants to live "near other [national-origin] families," close to "a temple," in a "[group] community."
>
> Published (compliant): "I cook almost every night, so I need to be near grocery stores that carry the spices, lentils, and fresh produce I use." Katie points the renter to areas with easy access to the specific grocers and cuisines named, never to areas defined by who lives there.

Rule citation for internal notes: neighborhood-guide skill, no demographic-composition framing, no religious-density references, no neighborhood identity by resident group.

### Gate 3 — Compliance scan
Run the scan in the Compliance Scan section below over the final text. Any em dash, banned word, capitalized "Brightplace," banned source, or surviving Fair Housing term blocks the build until fixed. ("cell signal" -> "cell reception": the literal token "signal" is banned.)

## The node (the core unit)

Every renter question becomes one self-contained node. Build each as four parts, in this order:

1. **H2 = the renter's real question, rephrased to match search syntax.** Use how a renter actually types ("Can you rent in Houston with no US credit history?"), not a topic label ("Credit considerations"). Pull phrasing from the keyword universe / People Also Ask where possible.
2. **Answer-first lead, 40-60 words.** Open with the direct answer or the key number in the first sentence. AI Overview and snippet extractors lift the opening sentence and skip long wind-ups. Date-stamp every dollar figure: "(as of Q_ 20__)".
3. **Renter verbatim quote.** The proof-of-experience. Lightly cleaned, never invented, in quotation marks.
4. **Katie synthesis, 2-3 sentences.** The expert framing the renter cannot give themselves. Practical, specific, never promotional.

The default expert is Katie. If the transcript names a different interviewer, map the expert role to Katie unless told otherwise, and note the mapping in internal notes.

## Production workflow

1. **Read** the dependency skills and the full transcript (Gate 1).
2. **Extract:** cohort, city, the renter's questions in the order they surfaced, verbatim quotes, and any real numbers. Determine the primary keyword (from the keyword universe or as stated) and secondary long-tails for H2 phrasing.
3. **Fair Housing pass on the source** (Gate 2). Mark every reframe before writing.
4. **Build the nodes.** One per real question. Answer-first, quote, Katie synthesis. Date-stamp figures.
5. **Add structural elements:**
   - Single **H1** carrying the primary keyword (only one H1; sections are H2, subsections H3).
   - **"Who this guide is for"** statement in the first paragraph.
   - **Metadata card** at top: Market, Audience, Read time, Last updated.
   - One **comparison/summary table** built to stand alone as a featured snippet.
   - A short **checklist list** where the interview contains one (e.g., touring checklist).
   - **FAQ section, 6-8 Q&A pairs**, drawn from the article and matched to real queries, for FAQPage schema. (Highest-probability format for AI Overview and Featured Snippet citation.)
   - **Internal links** to existing published guides only (e.g., True Monthly Cost, How to Rent). Never link to guides that do not exist yet.
6. **Compliance scan** (Gate 3). Paste the actual scan output into the chat so the gate is visible.
7. **Build the deliverable** (see Deliverables).
8. **Append internal production notes** (not published): source reality status, expert mapping, every Fair Housing and compliance edit traced to a named rule, date-stamp note, and the SEO/AEO elements included. QA at brightplace is rule-based, not judgment-based, so every change must cite its rule.
9. **Stop at draft.** Output is for Katie's sign-off. Do not push to Webflow, send, or publish without explicit human approval.

## Deliverables

**Default: `.docx` draft.** Build per the docx skill. Arial body, single H1 / H2 / H3 hierarchy, brightplace orange `#F5A623` for the Katie label and accents, teal `#00BCD4` for table headers and metadata labels, dark `#1A1A1A` headings. Renter quotes set as an indented block with a teal left rule. Internal notes appended below a divider in muted gray.

**On request: Webflow-ready HTML body.** Use the embed components defined in `guide-publishing/SKILL.md` (teal info box, amber action box, property card, teal-header table, metadata cards), each wrapped in `<div data-rt-embed-type='true'>` with SF Pro Display declared, separated by `<p>\u200d</p>` spacers. Watch the ~35K-character post-body limit; verify field content after any CMS push.

Place each renter quote in a teal info box and each "promise me / hard rule" moment (scams, flood check) in an amber action box.

## Compliance Scan

Run after the text is final, before declaring the gate passed. Works on extracted `.docx` text or the source markdown.

```python
import re, html, sys

# Pull text: for .docx, run the docx skill's unpack then read word/document.xml;
# for markdown, read the file directly. `txt` should be the plain visible text.
txt = html.unescape(re.sub(r'<[^>]+>', '', open(sys.argv[1], encoding='utf-8').read()))
low = txt.lower()

blockers = {
    'em dash (U+2014)':            '\u2014' in txt,
    '"Brightplace" capitalized':   ('Brightplace' in txt or 'BRIGHTPLACE' in txt),
    'banned word: signal':         'signal' in low,
    'banned word: navigate':       'navigate' in low,
    'banned word: landscape':      'landscape' in low,
    'banned word: deep dive':      'deep dive' in low,
    'banned word: unlock':         'unlock' in low,
    'banned word: leverage':       'leverage' in low,
    'banned: whether you\'re':     "whether you're" in low,
    'banned: hidden gem':          'hidden gem' in low,
    'banned: most underrated':     'most underrated' in low,
    'FH: demographic/national-origin framing':
        any(p in low for p in ['indian families', 'south asian community', 'popular with', 'large community of']),
    'FH: religious-density framing':
        any(p in low for p in ['temple', 'mosque', 'church density', 'synagogue']),
    'banned source: ILS/forum/review platform':
        any(s in low for s in ['apartments.com','zillow','trulia','zumper','apartment list','rentcafe',
                               'hotpads','realtor.com','reddit','city-data','biggerpockets','niche',
                               'areavibes','yelp','google reviews','apartmentratings','walk score',
                               'bike score','transit score','greatschools','nmhc']),
}
hits = [k for k, v in blockers.items() if v]
print('SCAN:', 'PASS — no blockers' if not hits else 'FAIL — ' + '; '.join(hits))
```

Note: this is a literal-token scan and the banned-source list is not exhaustive. The `guide-publishing` skill holds the full list. A flagged term inside the internal-notes section (which is not published) is acceptable, but prefer not to enumerate banned words verbatim there so the scan stays clean.

## Quality bar

- Each node stands alone. A retriever should be able to lift one H2 block and have it answer the query without the rest of the page.
- The renter sounds like a person, not a brand. If a quote could have been written by marketing, it is the wrong quote or it has been over-edited.
- Tradeoffs stated plainly. Trust comes from honest downsides, not enthusiasm.
- brightplace appears lightly, ideally once near the close, framed as the tool for the problem the renter described, never as a pitch.
- Voice: authority without arrogance, curators not salespeople.
