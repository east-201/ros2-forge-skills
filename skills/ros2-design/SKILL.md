---
name: ros2-design
description: Brainstorm ROS2 package, node, pipeline, or feature architecture before implementation.
---

# ROS2 Design

## 目标

在写代码前帮助用户设计 ROS2 package 或功能。不要直接实现代码。输出可比较的设计方案、推荐架构和后续 handoff prompt。

## 必读 references

- `common_session_protocol.md`
- `ros2_decision_router.md`
- `ros2_interface_contract_rules.md`
- `ros2_qos_rules.md`
- `ros2_executor_callback_rules.md`
- 涉及硬件时读 `ros2_hardware_safety_rules.md`
- 涉及相机/音频/AI 时读 `ros2_perception_audio_camera_rules.md`
- 涉及 SSH/板端 bringup 时读 `ros2_ssh_board_access_rules.md`

## 流程

1. 创建新的 `docs/ros2-design/<RUN_ID>-design/`。
2. 重写用户需求，区分确定信息、假设、待确认问题。
3. 识别 package 类型：driver / bridge / perception / manager / action server / lifecycle wrapper / testkit / tools。
4. 输出三套方案：MVP、工程稳健版、扩展展示版。
5. 对比接口复杂度、实时性、调试难度、硬件风险、后续扩展。
6. 给出推荐方案。
7. 输出实现前必须确认的 contract 草案。

## 输出文件

```text
00_REQUIREMENT_REWRITE.md
01_DESIGN_OPTIONS.md
02_RECOMMENDED_ARCHITECTURE.md
03_INTERFACE_DRAFT.md
04_RISK_AND_ASSUMPTIONS.md
05_IMPLEMENTATION_HANDOFF_PROMPT.md
SESSION_INDEX.md
SESSION_META.json
```

## 设计强制项

- 是否需要 lifecycle。
- 是否需要 fake/dry-run backend。
- 是否需要 action 而不是 service。
- sensor/control/status/debug topic 分层。
- callback 是否可能阻塞。
- 低算力板上是否需要降频、丢帧、线程限制。
- SSH/板端 bringup 是否需要 runtime skill 支持。

## Subagent 调度要求

- 使用 `contract-architect` 辅助把需求拆成候选 contract。
- 涉及硬件时使用 `ros2-hardware-safety-reviewer` 做设计期安全审查。
- 涉及相机/音频/AI pipeline 时使用 `ros2-qos-executor-reviewer` 评估实时性和 backpressure。
