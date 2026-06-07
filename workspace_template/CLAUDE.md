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
2. Use project subagents from `.claude/agents/` for exploration, review, SSH, runtime diagnosis, worker lanes, merge barriers, and design synthesis.
3. `/ros2-design` must read context first, ask P0 blocking questions before final architecture, and must not use a hard numeric question limit. Questions should be grouped as P0/P1/P2.
4. Use parallel read-only subagent lanes when tasks are independent, then merge results through `PARALLEL_LANE_SUMMARY.md`, `CONFLICTS_AND_DEPENDENCIES.md`, and `MERGED_DECISION.md`.
5. `/ros2-design` must run a design consistency review after drafting.
6. After accepted fixes, update fix status docs and append public interface/config changes to the latest scan change log.
7. New `/ros2-scan` sessions should reference the latest previous scan but must never overwrite it.
8. Do not run motion, actuator, reboot, network-edit, or destructive commands without explicit user confirmation.
9. Do not claim V5 hardware verification without user-provided hardware evidence.
