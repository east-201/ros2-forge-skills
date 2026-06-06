# Changelog

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
