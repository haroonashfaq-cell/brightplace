#!/usr/bin/env python3
"""Local Claude planner -> Codex executor -> Claude reviewer workflow."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
from datetime import datetime, timezone
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
RUNS = Path(__file__).resolve().parent / "runs"
RULES = """You are in a bounded Claude/Codex collaboration run.
Do not invoke team.py, delegate to another agent, or launch another AI CLI.
The user's task defines scope. Preserve unrelated existing work, including
uncommitted edits. Do not read credentials or .env files. Do not commit, push,
publish, deploy, message others, or change external systems in this workflow.
If required permissions or information are missing, report blocked explicitly.
Follow applicable project instructions and use actual files as evidence.
"""


def schema(fields):
    return {"type": "object", "properties": fields,
            "required": list(fields), "additionalProperties": False}


TEXT = {"type": "string"}
LIST = {"type": "array", "items": TEXT}
PLAN = schema({"status": {"enum": ["ready", "blocked"], "type": "string"},
               "summary": TEXT, "steps": LIST, "acceptance_criteria": LIST,
               "files_to_inspect": LIST, "blockers": LIST})
REVIEW = schema({"verdict": {"enum": ["approved", "changes_requested", "blocked"], "type": "string"},
                 "summary": TEXT, "required_fixes": LIST, "evidence": LIST})


def validate(data, definition):
    if not isinstance(data, dict) or set(data) != set(definition["properties"]):
        raise ValueError("Agent returned missing or unexpected fields")
    for key, spec in definition["properties"].items():
        value = data[key]
        if spec.get("type") == "string" and not isinstance(value, str):
            raise ValueError(f"Invalid text field: {key}")
        if spec.get("type") == "array" and (not isinstance(value, list) or
                any(not isinstance(x, str) for x in value)):
            raise ValueError(f"Invalid list field: {key}")
        if "enum" in spec and value not in spec["enum"]:
            raise ValueError(f"Invalid verdict: {value}")
    return data


def save(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")


def invoke(command, prompt, run, label, timeout):
    (run / f"{label}.prompt.txt").write_text(prompt)
    env = os.environ.copy()
    env["BRIGHTPLACE_TEAM_CHILD"] = "1"
    # Claude refuses nested interactive sessions; this is an independent print run.
    env.pop("CLAUDECODE", None)
    print(f"{label} …", flush=True)
    with (run / f"{label}.stdout.log").open("w") as out, \
            (run / f"{label}.stderr.log").open("w") as err:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=out,
                                   stderr=err, cwd=ROOT, env=env, start_new_session=True)
        try:
            process.communicate(prompt.encode(), timeout=timeout)
        except (subprocess.TimeoutExpired, KeyboardInterrupt):
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            raise
    if process.returncode:
        raise RuntimeError(f"{label} exited {process.returncode}; see {run / (label + '.stderr.log')}")
    return (run / f"{label}.stdout.log").read_text()


def claude(prompt, definition, run, label, args):
    command = ["claude", "--print", "--output-format", "json",
               "--json-schema", json.dumps(definition),
               "--tools", "Read,Glob,Grep", "--allowedTools", "Read,Glob,Grep",
               "--permission-mode", "dontAsk", "--strict-mcp-config",
               "--mcp-config", '{"mcpServers":{}}', "--disable-slash-commands",
               "--no-session-persistence", "--append-system-prompt", RULES]
    if args.claude_model:
        command += ["--model", args.claude_model]
    envelope = json.loads(invoke(command, prompt, run, label, args.timeout))
    if envelope.get("is_error"):
        raise RuntimeError(f"Claude reported an error; see {label}.stdout.log")
    data = validate(envelope.get("structured_output"), definition)
    save(run / f"{label}.json", data)
    return data


def codex(prompt, run, label, args, read_only=False):
    result_path = run / f"{label}.md"
    command = ["codex", "-a", "never", "exec", "--sandbox", "read-only" if read_only else "workspace-write",
               "--cd", str(ROOT), "--color", "never", "--ephemeral",
               "--output-last-message", str(result_path)]
    if args.codex_model:
        command += ["--model", args.codex_model]
    command += ["-"]
    invoke(command, RULES + "\n" + prompt, run, label, args.timeout)
    if not result_path.exists() or not result_path.read_text().strip():
        raise RuntimeError("Codex did not produce an execution report")
    return result_path.read_text()


def workflow(task, run, args):
    save(run / "status.json", {"status": "planning"})
    plan = claude("Act as planner. Inspect relevant files, then give Codex a concrete plan. "
                  "You may read files but cannot implement changes. Include verifiable acceptance "
                  "criteria. Do not invent requirements.\nUSER TASK:\n" + task, PLAN, run, "01-plan", args)
    if plan["status"] == "blocked" or plan["blockers"]:
        save(run / "status.json", {"status": "blocked", "details": plan})
        return 2
    feedback = "None; first implementation pass."
    for attempt in range(1, args.rounds + 1):
        save(run / "status.json", {"status": "executing", "round": attempt})
        report = codex(f"Execute the task using Claude's plan. Implement and run appropriate checks. "
                       f"Report changed paths, test results, and any blockers.\nUSER TASK:\n{task}\n"
                       f"CLAUDE PLAN:\n{json.dumps(plan)}\nREVIEW FEEDBACK:\n{feedback}",
                       run, f"02-execute-{attempt}", args)
        save(run / "status.json", {"status": "reviewing", "round": attempt})
        review = claude(f"Review Codex's implementation against the original task and plan. "
                        f"Inspect the actual changed files and evidence, not just its claims. "
                        f"You cannot run tests yourself; distinguish reported tests from inspected evidence. "
                        f"Approve only if the task is met; otherwise give concrete required fixes or blockers.\n"
                        f"USER TASK:\n{task}\nPLAN:\n{json.dumps(plan)}\nCODEX REPORT:\n{report}",
                        REVIEW, run, f"03-review-{attempt}", args)
        if review["verdict"] in ("approved", "blocked"):
            save(run / "status.json", {"status": review["verdict"], "round": attempt, "details": review})
            return 0 if review["verdict"] == "approved" else 2
        feedback = json.dumps(review)
    save(run / "status.json", {"status": "needs_attention", "round": args.rounds, "details": review})
    return 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", nargs="?", help="Task for Claude to plan and Codex to execute")
    parser.add_argument("--task-file", type=Path)
    parser.add_argument("--rounds", type=int, default=3, help="Maximum execution/review rounds (1-5)")
    parser.add_argument("--timeout", type=int, default=1200, help="Seconds per agent call")
    parser.add_argument("--claude-model", help="Optional; default is Claude's configured model")
    parser.add_argument("--codex-model", help="Optional; default is Codex's configured model")
    parser.add_argument("--doctor", action="store_true", help="Check CLI installation and authentication")
    parser.add_argument("--ask", choices=["claude", "codex"], help="Send one question and return a read-only reply")
    args = parser.parse_args()
    if os.environ.get("BRIGHTPLACE_TEAM_CHILD"):
        parser.error("Recursive team runs are disabled")
    if not 1 <= args.rounds <= 5 or args.timeout < 1:
        parser.error("Use 1-5 rounds and a positive timeout")
    for name in ("claude", "codex"):
        if not shutil.which(name):
            parser.error(f"{name} is missing from PATH")
    if args.doctor:
        failed = False
        for command in (["codex", "login", "status"], ["claude", "auth", "status"]):
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=30)
            ok = result.returncode == 0
            if command[0] == "claude" and ok:
                ok = json.loads(result.stdout).get("loggedIn") is True
            print(f"{command[0]}: {'authenticated' if ok else 'authentication unavailable; check in your terminal'}")
            failed |= not ok
        return int(failed)
    if bool(args.task) == bool(args.task_file):
        parser.error("Provide either a task or --task-file")
    task = args.task_file.read_text() if args.task_file else args.task
    if not task.strip():
        parser.error("Task cannot be empty")
    RUNS.mkdir(parents=True, exist_ok=True)
    with (RUNS / ".lock").open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            parser.error("Another team run is already active in this workspace")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run = RUNS / f"{stamp}-{uuid4().hex[:8]}"
        run.mkdir()
        (run / "task.txt").write_text(task)
        print(f"Task history: {run}", flush=True)
        try:
            if args.ask:
                save(run / "status.json", {"status": "asking", "recipient": args.ask})
                if args.ask == "claude":
                    answer = claude("Answer the other assistant's question. Inspect files if useful. "
                                    "Do not implement changes.\nQUESTION:\n" + task,
                                    schema({"answer": TEXT}), run, "reply", args)["answer"]
                else:
                    answer = codex("Answer the other assistant's question. Do not change files.\n"
                                   + task, run, "reply", args, read_only=True)
                (run / "reply.md").write_text(answer)
                print(answer)
                save(run / "status.json", {"status": "answered", "recipient": args.ask})
                code = 0
            else:
                code = workflow(task, run, args)
        except (Exception, KeyboardInterrupt) as error:
            save(run / "status.json", {"status": "interrupted" if isinstance(error, KeyboardInterrupt)
                                      else "failed", "error": str(error)})
            print(f"Stopped: {error}. History: {run}", file=sys.stderr)
            return 1
        print((run / "status.json").read_text())
        return code


if __name__ == "__main__":
    sys.exit(main())
