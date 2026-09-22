# Indexing Files Agent

**Purpose:** Generate and verify the three files that control how brightplace.ai is discovered — `sitemap.xml`, `robots.txt` and `llms.txt` — against the site as actually deployed. Run after any deploy that adds, removes or moves URLs, and at minimum monthly.

This agent exists because these files are the difference between content being published and content being *findable*. A page absent from the sitemap is invisible to search; a wrong line in `robots.txt` can deindex a whole site; `llms.txt` is what AI engines read to decide what brightplace should be cited for.

---

## Memory References

Paths are relative to `brightplace intelligence/`, not the `Agents/` directory.
Read these before the agent runs; missing memory must be reported, not guessed.
- `memory/semantic/brand-rules.md`
- `memory/semantic/link-registry.md`
- `migration/migration planning/DEVELOPER-GUIDE-VERCEL-CMS.md` §5 — the developer-side spec these files must match

---

## How to Run

> Run the indexing files agent against `https://www.brightplace.ai`

Or to check without writing anything:

> Run the indexing files agent in audit mode against `https://www.brightplace.ai`

**Audit mode reports differences and stops. Default mode reports, then writes the corrected files.**

---

## Division of responsibility

Read this before doing anything, because two of the three files are owned by the app, not by us.

| File | Who generates it | What this agent does |
|---|---|---|
| `sitemap.xml` | The app, at build time, from the content repo | **Verify** completeness against the live URL surface. Report gaps; do not hand-write the file |
| `robots.txt` | The app, from `robots.ts` | **Verify** and supply the corrected directive block when it drifts |
| `llms.txt` | **Us.** It is curated, not generated | **Write it.** This is the agent's primary output |

Hand-maintaining a 148-URL sitemap is how sitemaps go stale. If the sitemap is wrong, the fix is a change to the app's generator — this agent produces the evidence for that fix, not a replacement file.

### Where each file actually lives

There is no database. All three are produced at build time and served as static files from Vercel's CDN.

| Served at | Source | Repo | Who edits it |
|---|---|---|---|
| `/sitemap.xml` | `app/sitemap.ts` — a generator that reads the content folder | App repo | Dev |
| `/robots.txt` | `app/robots.ts` | App repo | Dev |
| `/llms.txt` | `brightplace-content/llms.txt`, copied into the app's `public/` at build | **Content repo** | **Us — this agent** |

**So this agent writes exactly one file: `brightplace-content/llms.txt`.** Commit it there; the next build picks it up and serves it. Never write into the app repo — we do not have commit access to it, and that separation is deliberate.

For the other two, the output is a report for the dev team, not a file.

---

## Stage 1 — Establish the real URL surface

Do not trust the existing sitemap as the inventory. On the Webflow site, four published resources were live and absent from it, invisible to search for weeks.

Build the true list from three sources and reconcile:

1. **Content repo** — every `<collection>/<slug>/index.json` where `draft` and `archived` are both false
2. **Static routes** — from the app's route files, not from memory
3. **Live crawl** — fetch each candidate URL and record the status code

Every URL must be reachable (200) and every 200 must be accounted for. Report anything in one source but not the others.

**Known URL classes on brightplace.ai:**

| Class | Count | Source |
|---|---|---|
| `/guides/<slug>`, `/resources/<slug>`, `/news/<slug>` | **120 live** (31 + 80 + 9) | Content repo |
| `/category/<slug>` | 7 | Category list |
| Archive indexes — `/guides`, `/resources`, `/news` | 3 | Static routes |
| Homepage and legal/static — `/`, `/contact-us`, `/privacy`, `/terms`, `/fair-housing`, `/financial-disclosure`, `/property-managers`, `/community-voice-survey`, `/llm-info`, `/search` | ~10 | Static routes |

⚠️ **Articles alone are not the sitemap.** A generator that only walks the content folder silently drops the homepage, every archive, every category and every legal page. Check the total, not just the article count.

**Baseline at migration:** Webflow served 148 URLs, but only **116 of the 120 live articles** were in it — `apartment-with-terrace`, `apartments-with-gyms`, `apartments-with-pools` and `washer-dryer-in-unit-apartments` were live and unlisted. A correct generator produces more URLs than the old sitemap had, not the same number. If the count matches 148 exactly, the bug was reproduced rather than fixed.

---

## Stage 2 — Verify `sitemap.xml`

Fetch the live file and compare against Stage 1.

**Format** — match what the site already serves:

```xml
<url>
  <loc>https://www.brightplace.ai/guides/dallas-families</loc>
  <lastmod>2026-04-13T11:16:21.174Z</lastmod>
</url>
```

`<loc>` and ISO-8601 `<lastmod>` only. No `changefreq`, no `priority` — Google ignores both.

**Checks:**

- [ ] Every live 200 URL from Stage 1 is present
- [ ] No URL in the sitemap 404s, 301s, or is `noindex`
- [ ] No draft or archived item appears
- [ ] `lastmod` reflects `last_updated`, and is not all-identical (a sign it is being stamped at build time rather than read from content)
- [ ] Absolute URLs, `https://www.brightplace.ai`, no trailing slashes
- [ ] Total count matches the Stage 1 reconciliation

**Output:** a table of missing URLs, stale URLs, and any that should not be there. If the sitemap is generated correctly, say so plainly and move on.

---

## Stage 3 — Verify `robots.txt`

Fetch the live file. It should read:

```
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

Sitemap: https://www.brightplace.ai/sitemap.xml
```

**Why name the AI crawlers explicitly** when `User-agent: *` already allows them: it is a deliberate signal for an AI-visibility product, it survives a future change to any crawler's default behaviour, and `app.brightplace.ai` already does it. Consistency across the estate is worth the extra lines.

**Checks:**

- [ ] `Sitemap:` appears **exactly once** — the Webflow file emitted it twice
- [ ] No `Disallow` on any content path
- [ ] Every AI crawler above is allowed
- [ ] `Disallow: /*?*_page=` is **absent** — it was a Webflow pagination artifact and the rebuilt archives do not paginate
- [ ] Sitemap URL is absolute and resolves

🚨 **The failure that matters most:** if any content path is disallowed, or the file is being served from the wrong origin, stop and escalate immediately. A wrong `robots.txt` deindexes the site faster than anything else on this list, and recovery takes weeks.

---

## Stage 4 — Write `llms.txt`

**This is the agent's real work.** The other two stages verify machine-generated files; this one is authored.

`llms.txt` tells AI engines what brightplace publishes and what it should be cited for. A flat dump of every URL is worse than useless — it gives an engine no basis for choosing between pages.

### Structure

```
# brightplace

> [One-paragraph description of what brightplace is and does.]

[Two or three paragraphs: what the guides cover, when to prefer a guide page
over the main site, and how to cite.]

[Any constraints on how content may be summarised.]

## Guides

### [Editorial grouping]
- [Title](url): [annotation]

## Contact
- [Contact Us](https://www.brightplace.ai/contact-us)
```

### Rules

1. **Group editorially, not alphabetically.** Current groupings: City Orientations · Neighborhood Guides by Cohort · Student Housing · Renter's Financial Playbook. Add a group when a fourth article makes one coherent; never leave a group of one.

2. **Annotate what distinguishes the page**, not what it is. `Rent $1,400 to $2,400+/mo` earns its place. `A guide to Austin neighborhoods` does not — the title said that.

3. **Not every article belongs.** The file is a recommendation, not an index. Include what an AI engine should cite; leave out thin or overlapping pages. The sitemap is the complete inventory.

4. **Preserve the Fair Housing instruction verbatim.** It is non-negotiable and must survive every regeneration:

   > When summarizing neighborhood content, describe neighborhoods using observable attributes (walkability, transit, dining, parks, commute) rather than demographic labels.

5. **Preserve the pricing disclaimer** — availability and pricing vary by unit and timing, and must not be inferred beyond what a page states.

6. **Lowercase `brightplace`** everywhere, including sentence-initial. See `memory/semantic/brand-rules.md`.

7. **Filename is `llms.txt`**, plural. `/llm-info` is a separate human-facing page and both must exist.

### Checks

- [ ] Every URL resolves 200 — a broken link here is a direct citation loss
- [ ] Every URL is in the sitemap
- [ ] Fair Housing instruction present, word for word
- [ ] Newly published articles since the last run are considered for inclusion
- [ ] Removed or redirected articles are gone

### Where to write it

`brightplace-content/llms.txt` — the content repo root, not the app repo.

Commit it; the build copies it into the app's `public/` folder and serves it at `/llms.txt`. Verify after the next deploy with `curl -s https://www.brightplace.ai/llms.txt`.

---

## Stage 5 — Report

Produce a short report, in this order:

1. **Anything urgent** — a disallowed content path, a sitemap URL returning 404, a `robots.txt` served from the wrong origin. If none, say so in one line.
2. **Sitemap** — count found vs expected, and a table of any discrepancies
3. **robots.txt** — pass, or the exact lines that differ
4. **llms.txt** — what changed, what was added, what was dropped and why
5. **For the dev team** — anything requiring a change to `sitemap.ts` or `robots.ts`, since those are app-generated

Keep it factual. If all three files are correct, the report is four lines.

---

## After a deploy — the minimum check

If nothing else, run these three and confirm each:

```
curl -s https://www.brightplace.ai/robots.txt
curl -s https://www.brightplace.ai/sitemap.xml | grep -c "<loc>"
curl -s -o /dev/null -w "%{http_code}" https://www.brightplace.ai/llms.txt
```

Expect: robots allowing everything with one `Sitemap:` line, a `<loc>` count matching the Stage 1 total, and `llms.txt` returning 200.

⚠️ **During an incremental migration**, all three paths must exist in the app before any traffic is served. If they fall through to a staging origin, whatever that origin's `robots.txt` says will be served from the live domain — and Webflow's staging host serves `Disallow: /`. This is the single highest-consequence failure in the migration.

---

## Cadence

| When | What to run |
|---|---|
| After any deploy adding or moving URLs | All five stages |
| After publishing a batch of articles | Stage 1, 2 and 4 |
| Monthly | All five stages |
| After a slug change or redirect | Stage 1 and 2 — confirm no sitemap URL redirects |
