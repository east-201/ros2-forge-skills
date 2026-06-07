---
name: ros2-scan
description: Extract as-built facts from an existing ROS2 workspace into Markdown and JSON without overwriting previous RUN_ID sessions.
---

# ROS2 Scan

## 目标

从现有 ROS2 工作区提取真实实现 facts，生成 Markdown 和 JSON。默认每次新建 `docs/ros2-quality/<RUN_ID>-scan/`，不得覆盖旧 session。

## 必读 references

- `subagent_dispatch_matrix.md`
- `common_session_protocol.md`
- `ros2_change_traceability_rules.md`
- `ros2_workspace_build_rules.md`
- `ros2_interface_contract_rules.md`
- `ros2_launch_config_rules.md`
- `ros2_ai_pitfalls.md`

## RUN_ID 规则

默认执行，并读取最近一次 scan 作为参考但不作为输出目标：

```bash
python3 .claude/tools/ros2_session.py new scan
python3 .claude/tools/ros2_scan_history.py latest --kind scan
```

只有用户明确要求 resume 时才执行：

```bash
python3 .claude/tools/ros2_session.py current scan
```

## 建议工具

```bash
python3 .claude/tools/extract_ros2_facts.py --root . --out docs/ros2-quality/<RUN_ID>-scan/facts
python3 .claude/tools/ros2_quality_static_scan.py --root . --out docs/ros2-quality/<RUN_ID>-scan/raw/static_scan.json
```

## 输出文件

```text
00_WORKSPACE_OVERVIEW.md
01_PACKAGE_INVENTORY.md
02_NODE_AND_PROCESS_INVENTORY.md
03_INTERFACE_AS_BUILT.md
04_PARAMETER_AS_BUILT.md
05_LAUNCH_CONFIG_AS_BUILT.md
06_QOS_AS_BUILT.md
07_LIFECYCLE_AS_BUILT.md
08_CALLBACK_EXECUTOR_AS_BUILT.md
09_PREVIOUS_SCAN_REFERENCE.md
10_SCAN_DELTA_FROM_PREVIOUS.md
11_HARDWARE_SURFACE.md
12_TEST_AND_BUILD_BASELINE.md
13_UNKNOWN_REGISTER.md
99_CHANGE_LOG_FROM_FIXES.md
facts/*.json
raw/*.json
SESSION_INDEX.md
SESSION_META.json
```

## 重点

facts 是后续 review/plan/fix 的基础。如果无法确认，写入 `13_UNKNOWN_REGISTER.md`，不要猜。

## Previous scan 参考规则

新的 scan 仍然必须创建新 RUN_ID，但应读取最近一次 `<RUN_ID>-scan/` 作为历史参考：

```bash
python3 .claude/tools/ros2_scan_history.py latest --kind scan
```

如果上一轮 fix 在旧 scan 中追加了 `99_CHANGE_LOG_FROM_FIXES.md`，本次 scan 必须重点复查其中列出的 interface/config/launch/QoS/lifecycle/package 变更，并输出 `10_SCAN_DELTA_FROM_PREVIOUS.md`。

禁止把新 scan 输出写入旧 scan 目录。
