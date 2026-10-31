# SLAMBot

A project to learn visual SLAM by building it, following Gao & Zhang's book.
The plan, decisions and conventions are in `docs/ROADMAP.md`. Build, test and
tool commands are in `README.md`.

## Who writes what
- Core algorithms (tasks marked *(us)* in the roadmap) are written by the
  people learning. Don't implement them unless asked. Write the header, the
  Catch2 tests (including numerical Jacobian and synthetic-data checks) and a
  stub marked `TODO(human)` instead.
- *(pair)* tasks: propose the design and discuss it before writing code;
  leave the math inside them to the people learning.
- Claude writes infrastructure: build, CI, Docker, scripts, dataset readers,
  viewer code and test scaffolding (tasks marked *(Claude)*).
- When explaining, teach: derivation, intuition, pitfalls.

## Code
- Naming follows roadmap decision D5.
- A new module goes in `slambot/<name>/`, registered with `slambot_add_module()`
  (example: `slambot/core/CMakeLists.txt`).
- Poses, time, units and quaternion order follow the roadmap's Conventions.
- Keep CI green; it treats compiler warnings as errors.
- Never commit datasets (`data/` is gitignored; EuRoC is non-commercial).

## Docs
- One home per fact: rules for Claude here, how to build and run in
  `README.md`, the plan and decisions in `docs/ROADMAP.md`. Link instead of
  repeating.
- Short and plain: no emoji, no filler, almost no bold. Only write claims you
  have checked.
- After changing any `.md` file, run the `doc-auditor` agent and
  `python3 scripts/check_docs.py`, fix what they find, then run
  `python3 .claude/hooks/doc_audit_gate.py --mark-audited`. A Stop hook (the
  same script) reminds you if docs changed since the last audit.
