# brightplace Content Memory

For content production or content-agent work in this directory, start with
`Agents/WORKFLOW.md` and `memory/procedural/workflow-reference.md`.
All `memory/...` paths in agent prompts are relative to this directory.
Read the required canonical semantic files and relevant episodic records using
that workflow's Session Start/read-write contract. Report memory access failures.
The memory system applies only here, not to AIR operator or SUPER SEO Agents.

## Publishing (changed 2026-09-24)

Webflow is retired. The site is Next.js on Vercel and builds from GitHub. Finished
articles are written to `brightplace content/<collection>/` as three files sharing one
slug — `[slug].md`, `[slug].html` (body fragment, no H1, no script) and the featured
image — and the git commit is what publishes them. There is no CMS, no API push, no MCP
call and no draft state. See `memory/semantic/cms-config.md` for the schema and
`brightplace content/README.md` for the format.

`app.brightplace.ai` is merged into the main site and must never appear in a link.
Every href uses `https://www.brightplace.ai`, or a site-relative path for internal
links. Verify internal links against `https://www.brightplace.ai/sitemaps/content.xml`,
not `/sitemap.xml` — that is now an index and carries no article URLs.
Permanent rule changes require explicit user promotion; never infer permission
from a trend, a score, or an old episode. Follow the user's chosen manual handoff:
Claude plans/reviews; Codex implements the supplied plan without launching another
planning session automatically.
