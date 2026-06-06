# CLAUDE.md - ROS2 Workspace Agent Guide

This workspace uses **ROS2 Forge Skills**. Prefer slash commands instead of ad-hoc edits:

- `/ros2` for dispatch
- `/ros2-design` before new ROS2 packages or major features
- `/ros2-contract` to freeze interface/config/QoS/lifecycle contracts
- `/ros2-scan` before reviewing existing code
- `/ros2-review` before fixes
- `/ros2-plan` before code edits
- `/ros2-fix` for approved patch lanes
- `/ros2-verify` for evidence-based validation
- `/ros2-runtime` for local/SSH runtime diagnosis
- `/ros2-ssh` for board/remote-host SSH diagnosis

Rules:

1. Never overwrite old `docs/ros2-quality/<RUN_ID>-*` or `docs/ros2-design/<RUN_ID>-*` sessions.
2. Use project subagents from `.claude/agents/` for exploration, review, SSH, runtime diagnosis, worker lanes, and merge barriers.
3. Do not run motion, actuator, reboot, network-edit, or destructive commands without explicit user confirmation.
4. Do not claim V5 hardware verification without user-provided hardware evidence.
