"""Mechanical checks for the Markdown docs, run in CI.

    python3 scripts/check_docs.py

Checks every tracked .md file for emoji, and that relative links and #anchors
point to files and headings that exist. Checks the main docs against a line
budget, so they stay short. Contradictions and wording are left to the
doc-auditor agent (.claude/agents/doc-auditor.md).
"""

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LINE_BUDGETS = {"CLAUDE.md": 60, "README.md": 200, "docs/ROADMAP.md": 500}
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✅]")
FENCE = re.compile(r"^\s*(```|~~~)")


def tracked_markdown() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "--", "*.md"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout
    return out.split()


def prose_lines(text: str):
    """Yields (line number, line) outside fenced code blocks."""
    in_fence = False
    for number, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence:
            yield number, line


def anchors(path: Path) -> set[str]:
    """GitHub-style anchors of the file's headings."""
    result = set()
    for _, line in prose_lines(path.read_text()):
        if heading := re.match(r"#{1,6}\s+(.*)", line):
            slug = re.sub(r"[^\w\- ]", "", heading.group(1).strip().lower()).replace(" ", "-")
            result.add(slug)
    return result


def check(rel_path: str) -> list[str]:
    path = REPO_ROOT / rel_path
    text = path.read_text()
    problems = []
    if (budget := LINE_BUDGETS.get(rel_path)) and (count := len(text.splitlines())) > budget:
        problems.append(f"{rel_path}: {count} lines, budget is {budget}")
    for number, line in prose_lines(text):
        if EMOJI.search(line):
            problems.append(f"{rel_path}:{number}: emoji")
        for target in LINK.findall(re.sub(r"`[^`]*`", "", line)):
            if re.match(r"[a-z]+:", target):  # http:, https:, mailto:
                continue
            file_part, _, anchor = target.partition("#")
            linked = (path.parent / file_part).resolve() if file_part else path
            if not linked.exists():
                problems.append(f"{rel_path}:{number}: broken link {target}")
            elif anchor and linked.suffix == ".md" and anchor not in anchors(linked):
                problems.append(f"{rel_path}:{number}: no heading for #{anchor} in {file_part or rel_path}")
    return problems


def main() -> None:
    problems = [p for rel_path in tracked_markdown() for p in check(rel_path)]
    print("\n".join(problems) or "Docs OK")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
