# Claude / Codex collaboration

Read `AGENTS.md` and `automation/agent-team/README.md`.
The user's preferred workflow is Claude planning, Codex implementation, and
Claude review. Use the team runner for automatic joint implementation tasks.
Inside a runner child (`BRIGHTPLACE_TEAM_CHILD=1`), perform only the assigned
planning or review role, return the requested schema, and do not delegate again.
