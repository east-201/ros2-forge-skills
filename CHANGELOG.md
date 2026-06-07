# Changelog

## v4.4.0

- Removed the hard numeric limit for `/ros2-design` questions.
- Design intake now asks as many useful questions as needed, grouped as `P0 blocking`, `P1 quality`, and `P2 future/backlog`.
- Added `parallel_subagent_orchestration_rules.md` for flexible parallel subagent lanes.
- Added `parallel-subagent-coordinator` project subagent and matching template.
- Updated `/ros2-design` so context reading, requirement intake, interface/QoS/launch/lifecycle/safety/testing/SSH analysis, and final synthesis can use parallel read-only lanes.
- Added synthesis outputs: `PARALLEL_LANE_SUMMARY.md`, `CONFLICTS_AND_DEPENDENCIES.md`, and `MERGED_DECISION.md`.

# Changelog

## v4.3.0

- Added mandatory `/ros2-design` intake gate: brainstorm first, ask blocking questions, and avoid final architecture until enough information is available.
- Added design post-review through `design-consistency-reviewer` for requirement coverage, interface connectivity, function responsibility closure, launch/config alignment, QoS/lifecycle feasibility, and verification coverage.
- Added `design-requirement-questioner`, `design-consistency-reviewer`, and `scan-history-curator` project subagents.
- Added `ros2_design_intake_rules.md` and `ros2_change_traceability_rules.md`.
- Added fix documentation sync: accepted fixes must update fix status docs and change impact summary.
- Added scan history append flow: interface/config/launch/QoS/lifecycle/package/hardware changes append to the latest scan session's `99_CHANGE_LOG_FROM_FIXES.md`.
- Added previous scan reference flow: new scan sessions create `09_PREVIOUS_SCAN_REFERENCE.md` and should compare against the latest previous scan.
- Added `ros2_scan_history.py` helper.

## v4.2.0

- Renamed project to **ROS2 Forge Skills**.
- Simplified slash commands to `/ros2`, `/ros2-design`, `/ros2-contract`, `/ros2-scan`, `/ros2-review`, `/ros2-plan`, `/ros2-fix`, `/ros2-verify`, `/ros2-runtime`, `/ros2-ssh`.
- Simplified skill folders to `skills/ros2-*`.
- Standardized output roots as `docs/ros2-quality` and `docs/ros2-design`.
- Renamed session tool to `ros2_session.py` while keeping legacy kind aliases for migration.
- Added bilingual README with click-through language switch.
- Kept project-level Claude Code subagents under `.claude/agents/`.

## v4.1.0

- Added real project-level subagents under `agents/`.
- Added Skill frontmatter and explicit subagent dispatch matrix.
- Hardened SSH diagnostics with non-interactive defaults.
