# Workspace Template Rules

After installation into a ROS2 workspace, agents should find commands, skills, references, tools, and subagents under `.claude/`.

Recommended project layout:

```text
<ros2_ws>/
├── src/
├── docs/
│   ├── ros2-quality/
│   ├── ros2-design/
│   └── architecture/
└── .claude/
    ├── commands/
    ├── skills/
    ├── agents/
    ├── references/
    ├── tools/
    └── hooks/
```

- `docs/ros2-quality/` stores scan/review/plan/fix/verify/runtime evidence.
- `docs/ros2-design/` stores architecture brainstorming and contracts.
- `docs/architecture/` may store ADRs.
