# Claude / Codex collaboration

The user prefers Claude to plan and Codex to execute implementation tasks.
For an automatic joint task, run from the repository root:

```sh
python3 automation/agent-team/team.py "The user's task, with relevant context"
```

Read `automation/agent-team/README.md` for behavior and limitations. The runner
coordinates Claude planning, Codex implementation, and Claude review/fix rounds.
Include constraints and context from the current conversation in the task.
Do not start it for simple questions or read-only explanations.

For a direct consultation, either assistant can call
`python3 automation/agent-team/team.py --ask claude "question"` or
`python3 automation/agent-team/team.py --ask codex "question"`.
Replies are read-only. Pass the relevant context explicitly.

If `BRIGHTPLACE_TEAM_CHILD=1`, you are already inside this workflow: perform only
your assigned role. Never invoke the runner or another AI CLI from a child run.
Preserve unrelated uncommitted changes. Report blocked permissions and missing
information accurately. Do not claim a task is approved unless the review says so.
