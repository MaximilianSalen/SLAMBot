"""Claude Code Stop hook: audit Markdown files that changed.

When Claude is about to end its turn, this compares every .md file in the repo
with the state at the last audit (.claude/doc-audit-state.json, gitignored). If
any changed, it blocks the stop once and tells Claude to run the doc-auditor
agent. Edits Claude makes while fixing the findings count as audited.

    python3 .claude/hooks/doc_audit_gate.py --mark-audited

records the current docs as audited, after an audit Claude already ran.
"""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
STATE = ROOT / ".claude" / "doc-audit-state.json"
SKIP_DIRS = {".git", ".venv", "build", "data"}


def markdown_files() -> list[str]:
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "*.md"],
            cwd=ROOT, capture_output=True, check=True,
        ).stdout.decode()
        return sorted({p for p in out.split("\0") if p})
    except (OSError, subprocess.CalledProcessError):  # e.g. no git in the container
        files = []
        for dirpath, dirnames, filenames in os.walk(ROOT):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            files += [os.path.relpath(Path(dirpath, f), ROOT) for f in filenames if f.endswith(".md")]
        return sorted(files)


def main() -> None:
    hook_input = {} if "--mark-audited" in sys.argv else json.load(sys.stdin)
    current = {
        p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
        for p in markdown_files()
        if (ROOT / p).is_file()
    }
    try:
        audited = json.loads(STATE.read_text())
    except (OSError, ValueError):
        audited = {}
    STATE.write_text(json.dumps(current, indent=1, sort_keys=True) + "\n")

    changed = sorted(p for p in current if current[p] != audited.get(p))
    removed = sorted(p for p in audited if p not in current)
    if "--mark-audited" in sys.argv or hook_input.get("stop_hook_active") or not (changed or removed):
        return

    reason = "Markdown files changed since the last doc audit."
    if changed:
        reason += f" Changed: {', '.join(changed)}."
    if removed:
        reason += f" Removed (check for dangling references): {', '.join(removed)}."
    reason += " Run the doc-auditor agent on them, fix what it finds, then finish."
    print(json.dumps({"decision": "block", "reason": reason}))


if __name__ == "__main__":
    main()
