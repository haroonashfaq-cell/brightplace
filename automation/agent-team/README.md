# Claude plans, Codex executes

From the brightplace repository root:

```sh
python3 automation/agent-team/team.py --doctor
python3 automation/agent-team/team.py "Your task here"
```

Either assistant can also ask the other a question and receive a read-only reply:

```sh
python3 automation/agent-team/team.py --ask claude "Plan the changes needed for this task"
python3 automation/agent-team/team.py --ask codex "Review whether this implementation plan is feasible"
```

These calls return a reply directly and save it as `reply.md` in the task history.

Claude reads relevant project files and produces a structured plan. Codex
implements it and runs checks. Claude inspects the result and either approves,
requests fixes, or reports a blocker. Codex automatically handles requested
fixes, with at most three implementation/review rounds by default.

Each task gets a folder under `automation/agent-team/runs/` containing the task,
prompts, plan, execution reports, reviews, logs, and `status.json`. These local
histories are ignored by Git. Exit code 0 means Claude approved (or a direct reply was received), 2 means blocked
or review rounds exhausted, and 1 means a runtime error/interruption.

## Requirements and behavior

- Python 3 on macOS/Linux, and authenticated `claude` and `codex` CLIs on PATH.
- Uses the installed CLIs and their configured authentication/models. Model calls
  consume the applicable account usage; no API key is copied into this project.
- Starts dedicated CLI sessions. It does not message existing open chats or
  automatically import their conversation history. Put needed context in the task
  or reference workspace files.
- Claude has only Read/Glob/Grep tools and no MCP servers in planner/reviewer runs.
- Codex uses its workspace-write sandbox with noninteractive approvals disabled.
  If a necessary action is blocked, it must report that instead of bypassing it.
- Both agents are instructed to preserve unrelated changes and avoid commits,
  pushes, publishing, deployment, external writes, or recursive delegation.
  These are task instructions, not an additional security sandbox around all tools.
- Runs edit this working directory. One runner at a time is enforced; do not edit
  the same files simultaneously from another session.
- Ctrl-C stops the active child process group. Each call times out after 20 minutes.
- The runner is invoked per task; it does not install a background service.

For a larger task:

```sh
python3 automation/agent-team/team.py --task-file /path/to/task.md --rounds 3
```

Optional flags: `--claude-model`, `--codex-model`, `--timeout` (seconds per call).
When authentication is unavailable, run `claude` or `codex login` in your normal
terminal and authenticate. A restricted host sandbox may be unable to read macOS
Keychain credentials even when the terminal is logged in.

CLI references: [Codex noninteractive mode](https://developers.openai.com/codex/noninteractive/)
and the installed `claude --help` / `codex exec --help`.
