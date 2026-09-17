#!/usr/bin/env python3
"""Read-only checks for the brightplace Markdown memory integration.

This validates files, references, and evidence integrity. It does not prove an
LLM will follow prompts, verify external SEO claims, or publish a test article.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "semantic/brand-rules.md", "semantic/cms-config.md", "semantic/link-registry.md",
    "semantic/keyword-strategy.md", "semantic/ranking-rules.md", "semantic/content-standards.md",
    "episodic/qa-patterns.md", "episodic/content-log.md", "episodic/corrections.md",
    "episodic/link-failures.md", "episodic/reddit-patterns.md", "episodic/candidate-rules.md",
    "episodic/trend-intelligence.md", "procedural/workflow-reference.md",
}


def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print("PASS:", message)


def main():
    memory = ROOT / "memory"
    actual = {str(p.relative_to(memory)) for p in memory.rglob("*.md")}
    check(actual == EXPECTED, "Exactly 14 planned memory files exist")
    agents = {p.name: p.read_text() for p in (ROOT / "Agents").glob("*.md")}
    for p in list((ROOT / "Agents").glob("*.md")) + list(memory.rglob("*.md")):
        text = p.read_text()
        for ref in re.findall(r'`(?:memory/)?((?:semantic|episodic|procedural)/[a-z-]+\.md)`', text):
            check((memory / ref).is_file(), f"{p.name}: reference {ref}")
    joined = "\n".join(agents.values())
    check(not re.search(r"em dash|25\.7%|83%", joined, re.I),
          "Migrated brand rule and trend statistics are absent from agent prompts")
    for name in ["WORKFLOW.md", "seo-writing-agent.md", "qa-agent.md",
                 "content-writing-guidelines.md", "master-writer-agent.md",
                 "brief-check-agent.md", "content-brief-agent.md", "reddit-research-agent.md"]:
        check("## Memory References" in agents[name], f"{name}: memory entry point")
    qa = agents["qa-agent.md"]
    check(all(f"## SECTION {section}:" in qa for section in [1, 2, "2B", "2C", "2D", 3, 4, 5, 6]),
          "All QA sections retained, including new trend check")
    check("### 2f. Active Trend Alignment" in agents["brief-check-agent.md"], "Brief trend gate exists")
    check("## POST-QA MEMORY WRITE" in qa, "QA memory writes are wired")
    check("### Trends Applied" in agents["master-writer-agent.md"] and
          "### Trend Status Changes" in agents["master-writer-agent.md"], "Teaching reports trend usage and changes")
    check("Edit `brightplace intelligence/Agents/" not in agents["master-writer-agent.md"],
          "Teaching no longer instructs direct permanent agent edits")
    workflow = agents["WORKFLOW.md"]
    check(all(f"## Stage {x}:" in workflow for x in [0, 1, 2, "2.5", 3, 4, 5, "5.5", 6, 7]),
          "All ten workflow stage labels preserved")
    trends = (memory / "episodic/trend-intelligence.md").read_text()
    check(all(f"### TREND-{n:03}:" in trends for n in range(1, 7)), "All six legacy trends preserved")
    for section in re.split(r"^### TREND-", trends, flags=re.M)[1:]:
        match = re.search(r"\*\*Status:\*\* (\w+)", section)
        check(match is not None, "Trend has explicit status")
        if match.group(1) == "ACTIVE":
            check(bool(re.search(r"\*\*Last verified:\*\* \d{4}-\d{2}-\d{2}", section)) and
                  "https://" in section, "Active trend has a real verification date and source URL")
    patterns = (memory / "episodic/qa-patterns.md").read_text()
    for section in re.split(r"^## QA-", patterns, flags=re.M)[1:]:
        refs = re.findall(r"`(QA Reports/[^`]+)`", section)
        count = int(re.search(r"\*\*Occurrence count:\*\* (\d+)", section).group(1))
        check(count == len(set(refs)), "QA pattern count equals distinct evidence reports")
        check(all((ROOT / ref).is_file() for ref in refs), "QA pattern evidence exists")
    first = patterns.split("## QA-002:")[0]
    for ref in re.findall(r"`(QA Reports/[^`]+)`", first):
        check("mainEntityOfPage" in (ROOT / ref).read_text(), "Schema failure evidence names the missing field")
    log = (memory / "episodic/content-log.md").read_text()
    for article in (ROOT / "Complete Articles").glob("*.md"):
        check(f"| {article.stem} |" in log, f"Content history includes {article.stem}")
    research = (memory / "episodic/reddit-patterns.md").read_text()
    check(all(f"Reddit Research/{p.name}" in research for p in (ROOT / "Reddit Research").glob("*.md")),
          "All local research reports are represented")
    candidates = (memory / "episodic/candidate-rules.md").read_text()
    check("User decision:" in candidates and "PENDING / PROMOTED / REJECTED" in candidates,
          "Candidate format retains user decision provenance and promotion states")
    print("\nMemory integration validation passed. External claims and live agent behavior were not tested.")


if __name__ == "__main__":
    main()
