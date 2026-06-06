# Install ROS2 Forge Skills

## Linux/macOS

```bash
cd ROS2_Forge_Skills_v4_2
./install.sh --overwrite /path/to/ros2_ws
```

## Windows PowerShell

```powershell
cd ROS2_Forge_Skills_v4_2
.\install.ps1 -Target C:\path\to\ros2_ws -Overwrite
```

## Verify installation

Inside your ROS2 workspace:

```bash
ls .claude/commands/ros2.md
ls .claude/skills/ros2-scan/SKILL.md
ls .claude/agents/ros2-interface-reviewer.md
python3 .claude/tools/ros2_session.py new scan
```

Expected output root:

```text
docs/ros2-quality/<RUN_ID>-scan/
```

Start Claude Code and run:

```text
/ros2
```
