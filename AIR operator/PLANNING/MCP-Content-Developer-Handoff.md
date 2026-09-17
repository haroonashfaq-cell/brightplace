# AIR Operator MCP — comparison and developer handoff

Date: 16 September 2026
Status: proposed implementation backlog; product decisions below remain open.

## 1. Conclusion

Keep the revision-based CMS described in **MCP Content Specs v1.2**. Update the older reference to describe it. Do not rebuild the old CRUD/status model simply to match that reference.

The immediate work is to make publishing reviewable, errors actionable, updates predictable, and production output verifiable. SEO controls, profiles and event automation follow. Several statements in Content Specs need correction before they become implementation requirements.

### Evidence and scope

- **R:** [AIR-Operator-MCP-Reference copy.md](AIR-Operator-MCP-Reference%20copy.md), version 1.0. Design intent, not an inventory of deployed functionality.
- **C:** [MCP-Content-Specs.md](MCP-Content-Specs.md), version 1.2. Reports a successful staging publish, 14 callable tools and specific observed issues on 16 September 2026.
- This review compares the documents. It does **not** independently reproduce MCP failures, inspect backend code or verify production deployment. “Reported” below means reported in C. Tool absence could reflect deployment, environment or permissions; confirm against the intended service identity.
- Preserve both source documents. Use this handoff to reconcile them and create developer tickets. No developer message has been sent.

## 2. What differs between the documents

| Area | Reference design | Content Specs reports | Action |
|---|---|---|---|
| Blog writes | Create/update/delete tools; flat status | Save creates immutable revisions; review status, lifecycle and published pointer are separate | Document actual state machine and examples; retire obsolete agent examples |
| Content ownership | Agents supply HTML and JSON-LD | CMS renders markdown and four schema types | CMS owns rendering/schema; agents supply validated content fields |
| Briefs | Five CRUD tools | `brief_save`, `brief_get`, `brief_list` | Document supported save/delete/status operations; do not assume name substitution preserves behavior |
| Media | Single upload tool | Create → HTTP PUT → process → readiness polling | Document upload, failure/retry, dimensions and ready-image publish gate |
| Preview | Signed browser preview | HTML response only | Add exact-revision browser review with defined access behavior |
| Updates | Generic update fields | Full replacement; omitted optional fields cleared | Document immediately; add merge-to-new-revision operation |
| SEO | Tools specified | SEO tools reported unavailable; sitemap/RSS updates confirmed by brightplace | Separate automatic serving from missing controls and missing verification |
| Communities | Identity says 10; table and several sections say 5 | Ten staging communities | One environment-aware community registry; update all examples and rollout counts |
| Archive | Anonymous 404 | Product decision: 410 retired, 301 replaced | Explicitly supersede R §4/§9 and correct C acceptance tests |
| Profiles/events | Specified in initial workflow | Reported missing | Phase separately; preserve manual invocation until a runner is deployed |
| Analytics | Shared GA4 tag required; ingestion design open | Suggests using visibility snapshots | Keep tag installation and analytics ingestion as separate deliverables |

## 3. Corrections needed in Content Specs before implementation

### C01 — Character limits are internally inconsistent

**Sources:** R §1 semantic template, R §3 SQL; C §2/§11.

R itself specifies `<60` title and `<155` description in its template, which explains 59/154 exactly, while its SQL permits 60/160. Do not present the API behavior as an unexplained off-by-one defect. Record **60/160 as the new product decision** and align schema, validation, agent instructions and boundary tests. Define how characters are counted; do not silently trim.

### C02 — Archive test contradicts the accepted decision

**Sources:** C §5.11, §9 test 12, §11.

C §9 still accepts “404 or 410.” Replace it with: retired → 410; replacement → 301; never existed → 404. Unpublish remains undecided. Define whether restoring an archived article removes its redirect/tombstone and how cached routes are invalidated.

### C03 — Author and reviewer requirements do not have a complete data model

**Sources:** C §6.2/§11.

The proposed fields describe an author, but the reviewer requirement supplies only `last_reviewed_on`. A date cannot identify who reviewed a revision. Add an explicit reviewer identity and reviewed revision/date, and define how changing an author profile affects already-published articles. A new content revision must not automatically inherit a claim that someone reviewed its changed text.

Use `Article.author` for actual authorship. Put `reviewedBy` on the linked **WebPage** node, its documented Schema.org domain, and keep the visible reviewer aligned with it. Google supports both Person and Organization authors; a named person per community is a brightplace requirement, not a Google requirement or guaranteed ranking improvement. Sources: [Schema.org reviewedBy](https://schema.org/reviewedBy), [Google Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article).

### C04 — “Only authors must land before the backlog” is too broad

**Sources:** C §4.4, §7, §11, final paragraph of §12.

The document also reports 33 missing hero images, unresolved production access/promotion and undecided production approval permissions. List these as release dependencies. Browser review and production output checks must be available before relying on the proposed manager approval workflow. Revision patching and batch operations can be deferred with a correct full-payload client.

### C05 — Missing SEO tools do not establish that pages are undiscoverable

**Sources:** C §1, §5 opening, §5.2/§5.9/§11.

C confirms automatic sitemap/RSS updates but cannot inspect the protected endpoints. Describe this as **missing verification and control**, not proven failure of discovery. `llms.txt` remains a requested product feature; neither document establishes it as a prerequisite for search indexing or AI citations. A successful sitemap read proves inclusion in a sitemap, not inclusion in a search engine index.

### C06 — Fix tool counts, request estimates and event coverage

**Sources:** C §2/§3/§4.8/§6.3/§8/§10; R §2.11.

- `job_retry` appears in C §2 but not the 14-tool baseline. Mark availability unverified until tool discovery confirms it.
- The illustrated chain requires at least **10 MCP calls plus one HTTP upload** with one media poll and one job poll; more polls or ETag reads increase it. For 33 articles that is at least 330 MCP calls plus 33 uploads for that exact chain, not ~260 total. Not every request carries the article body.
- R lists ten event types; C omits `social_regenerate` and `review_reply_rejected`. Label C's list a first-phase subset or include all ten.
- “`community_id` on every call” needs exceptions for authorized portfolio/global operations, including `events_list_pending()` and `profile_list()`.
- Replace approximate tool totals with a generated inventory. R §2.8 lists 25 signatures across its four groups, while C estimates ~23.

### C07 — GA4 and canonical proposals assume facts not established

**Sources:** C §5.8/§10; R §0/§3/§10.

A separate GA4 tool does not imply separate GA4 properties. Adding `source=ga4` alone does not add sessions/engaged-sessions fields to the shown snapshot schema. Let the developer propose a metric model with hostname, date range and aggregation rules.

R mentions legacy domains to prohibit using them as community IDs/hosts; it does not establish that duplicate articles exist there. Confirm ownership and actual duplication before requiring cross-domain canonical overrides. Keep canonical overrides constrained and environment-aware.

### C08 — Tighten technical explanations without changing useful product requirements

- R §1 incorrectly says Googlebot cannot execute JavaScript. Keep server-rendered content as a product requirement, but correct the explanation. [Google JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics).
- C §5.11 should retain the chosen 410 behavior without promising faster removal than 404 or saying 404 means “might come back.” Google documents both statuses for removed pages. [Google crawling error guidance](https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors).
- Ordinary apartment articles do not qualify for Google's Indexing API, which supports JobPosting or BroadcastEvent embedded in VideoObject. Exclude it from this article backlog. [Google Indexing API](https://developers.google.cn/search/apis/indexing-api/v3/quickstart).
- C §6.3 overstates events: events provide work to consume; a scheduled worker/webhook runner is also needed for automatic execution. R §6 explicitly starts with manual invocation.

## 4. Developer tickets and acceptance criteria

Priorities here differ from C: **release gate** means needed before the intended production backlog/review workflow; **next** means valuable with a documented workaround; **later** means automation or expansion.

| ID / priority | Work and evidence | Acceptance criteria |
|---|---|---|
| DEV-01 / immediate | Publish implementation contract. R §2–§6 vs C §2–§3/§8 | Generate `MCP-CONTRACT.md` from callable tool schemas, with environment/version, required fields, limits, examples, roles, article/revision ETags and replacement semantics. Include brief/media operations and job failures. Confirm `job_retry` availability. Mark unavailable tools separately. |
| DEV-02 / next | Actionable errors and dry-run validation. C §4.1–§4.2 | Choose one H1 rule code, preferably `BODY_NO_H1`; save and dry-run report the same field/rule. Dry-run creates no records. Publish applies the same publish-relevant rules. Errors retain request IDs. |
| DEV-03 / release gate | Reviewable revision preview and protected-environment verification. C §4.5/§11 | Clean browser opens precisely the requested revision until expiry; expired/wrong-revision token fails; tokenless draft is unavailable. Document separate automation access for protected sitemap/robots/feed routes. Do not expose a deployment-wide bypass secret in public content or ordinary preview URLs. |
| DEV-04 / release gate | FAQ ownership. C §4.3 | Prefer `faqs[]` as the rendered FAQ/schema source; client removes only the known duplicate FAQ block from markdown. A duplicate produces a stable validator finding and blocks our publish workflow until resolved. Preview contains each FAQ once; schema matches visible answers. This strengthens C's warning-only acceptance. |
| DEV-05 / next | Safe partial updates. C §4.6–§4.7 | Patch creates a new immutable revision. Omitted fields inherit, explicit null follows field rules, original stays unchanged. Stale ETag causes no write. Test changing alt text preserves body, SEO fields and FAQs. Document which resource supplies each ETag. |
| DEV-06 / release gate for slug changes and retirement | Redirects, archive and cache reconciliation. C §5.6/§5.10–§5.11 | Publishing a changed slug creates an old→new 301; merely saving an unpublished revision does not move the live URL. Canonical/sitemap/RSS use new URL. Reject collisions, loops and invalid replacements. Archive returns 410 or replacement 301 and removes old discovery entries. Confirm unpublish and restore behavior. |
| DEV-07 / release gate | Verify served publication, not just preview. C §5.2–§5.5/§5.9–§5.10 | After reconcile succeeds, production page is anonymously accessible, renders expected revision in HTML, and uses production canonical/schema URLs. Sitemap/RSS contain only appropriate published URLs. Refresh preserves original publication date and updates modification time for content changes. Verify cache invalidation within a documented interval. Staging/preview indexing policy is separate from production. |
| DEV-08 / next | SEO control tools. C §5.1–§5.5 | Reads reflect actually served robots/sitemap/RSS/llms content. Writes enforce scope, roles and ETags. Blog sitemap entries remain CMS-owned. Page metadata changes render on the target page. `seo_validate_page` reports rendered-page failures and distinguishes fetch/access failure from valid content. |
| DEV-09 / release gate under current product decision | Community profiles and truthful author/reviewer entities. C §6.1–§6.2 | Brightplace supplies ten approved identities/bios and review assignments. Author page, byline and Article author agree; WebPage reviewer agrees with recorded review. Define default inheritance and historical identity behavior. No invented author or automatic claim of human review. |
| DEV-10 / release gate | Production identity and promotion runbook. C §7/§11 | Document endpoints, community mapping, roles, rate limits/backoff and approved promotion approach. If replaying source files, upload media into destination, map destination IDs, track payload/revision hashes and resume idempotently. Re-running creates no duplicate posts. Verify one production article before the remaining backlog. |
| DEV-11 / later | Durable events and runner. R §2.11/§6; C §6.3 | Brief approval yields a scoped event. Define claim/lease or another single-consumer guarantee, retries and deduplication. A failed worker can resume safely; processed events stop reappearing. Mark completion only after required async work succeeds. Document manual vs scheduled invocation. |
| DEV-12 / later | Batch operations and link checks. C §4.8/§5.7 | Batch responses report per-item result, preserve role/state checks and support safe retries after partial failure. Broken-link reporting distinguishes intentional redirects from missing pages and reports inbound links to retired pages. Auto-approval requires a separate explicit product decision. |

## 5. Work owned by brightplace, not backend development

1. Generate and review the remaining 33 hero images reported missing in C; supply alt text. Developer documents minimum dimensions, aspect-ratio/crop policy and failed-media handling.
2. Update agent adapters to use `blog_save_post`, full revision payloads until patching exists, correct ETags, no body H1, and a single FAQ source.
3. Supply author/reviewer identities and community profile content. Decide who is permitted to approve and publish in production. If the agent stops at `in_review`, identify the manager/publisher responsible for the remaining steps and any required media role.
4. Confirm file replay versus a promotion tool. A replay runner is still work even if no backend promotion feature is built; environment-specific IDs/assets must be handled.
5. Reconcile agent workflow instructions with the implementation contract before the bulk run. Never blindly retry publication mutations after a timeout; inspect state and use the documented idempotency mechanism.

## 6. Questions the developer/product owners must resolve

- **Developer:** Which features are implemented but unavailable to our staging identity? Provide tool inventory and transition/role matrix.
- **Developer:** How can reviewers and automation access protected staging routes? What is the production endpoint and publication reconciliation timeout/failure behavior?
- **Developer + product:** Does a slug belong to the article or revision, and when does its change become public? What do unpublish and restore return?
- **Product:** Who actually authors and reviews each community's content, and can the production service identity self-approve? Named people must reflect actual responsibility.
- **Product + developer:** Confirm environment policy: public production discovery; protected staging/preview; no staging URLs copied into production canonicals, feeds or schema.
- **Developer:** Which §10 expansion features are already in flight? Keep social/GBP/stats/design work outside this initial content release estimate.

## 7. Suggested message to the developer

> We compared MCP Content Specs v1.2 with the consolidated MCP reference. Please keep the implemented revision-based CMS and publish its actual contract; the reference's CRUD examples are stale. For the production content release, we need exact-revision browser review, verification of served pages/sitemap/RSS, resolved FAQ duplication, production roles/access and promotion steps, plus the agreed author/reviewer model. Redirect/archive behavior must be defined before changing published URLs. Please review DEV-01 through DEV-10, identify what already exists, and provide dependencies and estimates. Dry-run validation, patching, events and batching should preserve the existing revision and approval model. We will provide images, profile content and the production approval decision. This comparison is based on the documented staging run; please confirm implementation state before estimating.

