# Task for Claude: design brightplace content-agent memory

The user wants to improve the agents used for brightplace content by adding
episodic, semantic, and procedural memory. They explicitly asked Claude to think
through and plan this architecture, with Codex implementing later and Claude
reviewing. This request is DESIGN ONLY. Do not implement or modify agent files.

Inspect the actual local repository before proposing the design. Start with
`brightplace intelligence/Agents/WORKFLOW.md`, `master-writer-agent.md`, writing
guidelines, and QA rules. Inspect representative briefs, research, QA reports,
and completed articles. Compare `AIR operator/Agents/Writing Agents/` and a
representative community's context, research, and content tracker where relevant.
Inspect `SUPER SEO Agents` only to clarify shared versus copied instructions.
Do not read .env files or credentials; do not reproduce embedded credentials if
they appear in documentation. Do not browse or claim current external facts.

Working definitions:
- Episodic: traceable experiences from article production, user corrections,
  revisions, QA failures/fixes, and measured outcomes when actually available.
- Semantic: established brand, audience, community, and source knowledge with
  provenance, scope, confidence, verification date, and expiry when appropriate.
- Procedural: versioned instructions for research, writing, QA, and publishing.

Produce a concrete Markdown design that Codex can implement, including:
1. Findings with repository paths: existing memory-like material, duplication,
   conflicts, and actual gaps. Distinguish observed facts from assumptions.
2. A minimal architecture suited to this file-based agent workflow. Explain
   storage/retrieval choices and whether a database or embeddings are needed now.
3. Record formats and realistic examples for all three memory types. Clearly
   label synthetic examples; never fabricate performance or user feedback.
4. Exact read/write points in the content workflow; who records, retrieves,
   verifies, approves, supersedes, expires, and archives memories.
5. Retrieval scope and context limits, especially brand-wide vs community vs
   article-specific knowledge, to prevent cross-community fact contamination.
6. Conflict resolution, stale prices/policies, provenance, duplicate detection,
   and keeping subjective lessons distinct from verified facts.
7. How experiences become candidate procedures, what can be recorded
   automatically, and which changes require human approval. Existing user and
   editorial instructions take precedence; one article must not silently rewrite
   global rules. Memory content must not grant tools or execution permissions.
8. A phased migration and exact proposed files/integration edits. Preserve
   existing work and avoid introducing another competing source of truth.
9. A small evaluation plan with measurable acceptance criteria and rollback.
10. Decisions genuinely needing user input, with recommended defaults for others.

Optimize for a useful first version, not a speculative autonomous platform.
Return the complete plan in your answer. Codex will save it as a reviewable design
document; no memory system is being built in this handoff.
