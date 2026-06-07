---
name: ros2-design
description: Brainstorm ROS2 package, node, pipeline, or feature architecture with context-first requirement intake, unlimited useful questions, flexible parallel subagents, and post-design readiness review.
---

# ROS2 Design

## 目标

在写代码前帮助用户设计 ROS2 package、node、pipeline 或 feature。核心原则是：**先读上下文、再问问题、再并行脑暴、最后复查设计是否 ready**。不要直接实现代码。

## 必读 references

- `common_session_protocol.md`
- `ros2_design_intake_rules.md`
- `parallel_subagent_orchestration_rules.md`
- `subagent_dispatch_matrix.md`
- `ros2_decision_router.md`
- `ros2_interface_contract_rules.md`
- `ros2_qos_rules.md`
- `ros2_executor_callback_rules.md`
- `ros2_launch_config_rules.md`
- 涉及硬件时读 `ros2_hardware_safety_rules.md`
- 涉及相机/音频/AI 时读 `ros2_perception_audio_camera_rules.md`
- 涉及 SSH/板端 bringup 时读 `ros2_ssh_board_access_rules.md`

## 强制流程

1. 创建新的 `docs/ros2-design/<RUN_ID>-design/`。
2. 先读取已有上下文：最近 scan、README、package.xml、launch、config、msg/srv/action、已有 docs。
3. 生成 `00A_CONTEXT_USED_FOR_DESIGN.md`，记录已读上下文、已确认事实、仍未知的问题。
4. 使用 `design-requirement-questioner` 做需求 intake。
5. 生成 `00_DESIGN_INTAKE.md` 和 `01_QUESTIONS_TO_USER.md`。
6. 问题不设硬性数量上限。只要问题会影响设计正确性，就可以问；但必须按 `P0 blocking / P1 quality / P2 future` 分组。
7. 如果存在 P0 blocking questions，先向用户提问，**不要输出最终架构**。可以给极简 provisional sketch，但必须标记 `provisional-only`。
8. 如果信息足够，重写用户需求，区分确定信息、假设、待确认问题和非目标。
9. 灵活调度 subagents。能并行的只读任务应并行：接口、QoS/executor、launch/config、lifecycle、安全、测试、SSH/runtime 可分 lane 同时分析。
10. 进入 brainstorming：输出 MVP、工程稳健版、扩展展示版三套方案，也可以根据项目复杂度增加更多候选方案。
11. 用评分矩阵对比实现成本、接口稳定性、运行时安全、低算力适配、调试难度、测试便利性、后续扩展和与现有 scan/contract 的兼容性。
12. 给出推荐方案、非目标、contract 草案、acceptance tests 和 implementation handoff。
13. 使用 `design-consistency-reviewer` 做最终设计复查。
14. 只有复查通过，才把 `12_DESIGN_STATE.md` 标为 `design-ready`；否则标为 `questions-sent`、`provisional-only` 或 `design-review-failed`。

## 输出文件

```text
00A_CONTEXT_USED_FOR_DESIGN.md
00_DESIGN_INTAKE.md
01_QUESTIONS_TO_USER.md
02_REQUIREMENT_TRACEABILITY.md
02A_NON_GOALS.md
03_DESIGN_OPTIONS.md
03A_OPTION_SCORE_MATRIX.md
04_RECOMMENDED_ARCHITECTURE.md
05_INTERFACE_DRAFT.md
06_LAUNCH_CONFIG_DRAFT.md
07_RISK_AND_ASSUMPTIONS.md
08A_ACCEPTANCE_TESTS.md
08_DESIGN_REVIEW.md
09_REQUIREMENT_COVERAGE_MATRIX.md
10_INTERFACE_CONFIG_CONNECTIVITY_CHECK.md
11_IMPLEMENTATION_HANDOFF_PROMPT.md
12_DESIGN_STATE.md
13_ADR_CANDIDATES.md
PARALLEL_LANE_SUMMARY.md
CONFLICTS_AND_DEPENDENCIES.md
MERGED_DECISION.md
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
- launch/config/parameter 是否能一一对应。
- 函数/模块职责是否闭合，接口是否能连接到真实实现。
- SSH/板端 bringup 是否需要 runtime skill 支持。
- 每个关键需求是否有 acceptance test。
- 每个重要设计选择是否需要 ADR candidate。

## 问题策略

不要设置问题数量上限。问题的限制不是数量，而是价值：

```text
P0 blocking：不回答会导致架构方向可能错误，必须先问。
P1 quality：不回答也能设计，但需要写明假设和风险。
P2 future：不影响本轮实现，写入 backlog 或 ADR candidate。
```

如果问题很多，允许多轮提问：第一轮只问 P0；后续根据用户回答继续问 P1/P2。不要为了“少问”而隐藏关键不确定性。

## 设计复查 gate

设计后必须检查并给出 pass/fail：

```text
Gate 1 Requirement coverage
Gate 2 Interface connectivity
Gate 3 Launch/config/parameter consistency
Gate 4 Function/module responsibility closure
Gate 5 Runtime feasibility and callback/QoS safety
Gate 6 Safety/failure model
Gate 7 Verification and acceptance tests
Gate 8 Implementation handoff readiness
```

任何 fail 都必须说明：Evidence、Required change、Blocking level、Owner。

## Subagent 调度要求

最小必需：

- 使用 `design-requirement-questioner` 提出 P0/P1/P2 questions。
- 使用 `design-consistency-reviewer` 做最终设计复查。

按需并行：

- 使用 `explorer-source-mapper` 读取已有项目结构和最近 scan。
- 使用 `contract-architect` 辅助把需求拆成候选 contract。
- 使用 `ros2-interface-reviewer` 检查 topic/service/action/param/TF 连接。
- 使用 `ros2-qos-executor-reviewer` 评估实时性、callback、QoS、backpressure。
- 使用 `ros2-launch-config-reviewer` 检查 launch/config/remap/namespace 可行性。
- 使用 `ros2-lifecycle-reviewer` 检查 lifecycle/resource ownership。
- 涉及硬件时使用 `ros2-hardware-safety-reviewer` 做设计期安全审查。
- 涉及验证时使用 `ros2-test-verifier` 生成 acceptance tests。
- 涉及板端或远程环境时使用 `ssh-board-operator` 做只读环境确认，使用 `runtime-diagnoser` 解释运行时事实。
- 需要合并多个并行 lane 时使用 `parallel-subagent-coordinator` 或由主 agent 生成 `PARALLEL_LANE_SUMMARY.md`、`CONFLICTS_AND_DEPENDENCIES.md`、`MERGED_DECISION.md`。
