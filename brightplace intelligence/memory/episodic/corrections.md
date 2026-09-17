# Corrections

Imported: 2026-09-16. These are documented historical corrections, not newly
received feedback. Use stable IDs; record date precision honestly, scope, source,
and affected files. Append revisions; do not overwrite original observations.

## COR-001: Exact sitemap paths
- **Date:** August 2026 (day unknown)
- **Context/source:** HTML comment in `Agents/qa-agent.md` §5.1.
- **Correction:** Verify exact sitemap URL; never swap Guides and Resources paths.
- **Scope:** Internal links across brightplace content.
- **Files affected:** `Agents/qa-agent.md`, `memory/semantic/link-registry.md`.

## COR-002: Research fallback
- **Date:** August 2026 (day unknown)
- **Context/source:** HTML comment in `Agents/reddit-research-agent.md` Step 1b.
- **Correction:** Add Quora/Facebook research when Reddit yields insufficient evidence.
- **Evidence limitation:** Comment reports six consecutive articles; identities absent.
- **Scope:** Renter research, not permission to cite forums in articles.
- **Files affected:** `Agents/reddit-research-agent.md`.

## COR-003: CMS routing and HTML
- **Date:** Unknown; observed in project memory at migration 2026-09-16.
- **Context/source:** Claude project `MEMORY.md`, Webflow and critical rules.
- **Correction:** New neighborhood articles use Resources; Guides restricted;
  send drafts and use the supported RichText format.
- **Scope:** brightplace Webflow content only.
- **Files affected:** `memory/semantic/cms-config.md`, `Agents/WORKFLOW.md`.

## New correction format
ID; actual date; context/source; correction text; scope; files affected; user/QA
provenance. Record QA corrections as QA observations, not as user approval of policy.
