---
name: ros2-review
description: Perform contract-based ROS2 review from scan facts, design contracts, and source evidence.
---

# ROS2 Review

## 目标

基于 scan as-built facts 和可用 design contract，审查 ROS2 工程质量、安全性、接口一致性和可验证性。

## 必读 references

- `subagent_dispatch_matrix.md`
- `common_session_protocol.md`
- `ros2_interface_contract_rules.md`
- `ros2_qos_rules.md`
- `ros2_executor_callback_rules.md`
- `ros2_lifecycle_rules.md`
- `ros2_launch_config_rules.md`
- `ros2_hardware_safety_rules.md`
- `ros2_testing_rules.md`

## 流程

1. 创建新的 `docs/ros2-quality/<RUN_ID>-review/`。
2. 找到最新或用户指定的 `<RUN_ID>-scan/`。
3. 读取 facts 和 as-built Markdown。
4. 若存在 design contract，逐项对比。
5. 使用专业 reviewer subagents 分领域审查。
6. 每个 issue 必须有 evidence、risk、fix direction、verification。

## Issue 格式

```text
ID:
Priority: P0/P1/P2/P3
Category:
Contract/Expected:
Actual:
Evidence:
Risk:
Fix direction:
Verification:
ICR required?: yes/no
```

## 输出文件

```text
20_REVIEW_SUMMARY.md
21_CONTRACT_VIOLATIONS.md
22_ROS2_INTERFACE_REVIEW.md
23_QOS_AND_EXECUTOR_REVIEW.md
24_LIFECYCLE_RESOURCE_REVIEW.md
25_LAUNCH_CONFIG_REVIEW.md
26_HARDWARE_SAFETY_REVIEW.md
27_TESTING_GAPS.md
28_FALSE_POSITIVE_CANDIDATES.md
29_ISSUE_REGISTER.md
SESSION_INDEX.md
SESSION_META.json
```

## 禁止

- 不要只写“建议优化”。必须给 evidence。
- 不要把无法验证的推测写成事实。
- 不要直接修代码。

## Subagent 调度要求

至少按领域使用这些 reviewer，并把每个 reviewer 的结论写入对应报告：

- `ros2-interface-reviewer` -> `22_ROS2_INTERFACE_REVIEW.md`
- `ros2-qos-executor-reviewer` -> `23_QOS_AND_EXECUTOR_REVIEW.md`
- `ros2-lifecycle-reviewer` -> `24_LIFECYCLE_RESOURCE_REVIEW.md`
- `ros2-launch-config-reviewer` -> `25_LAUNCH_CONFIG_REVIEW.md`
- `ros2-hardware-safety-reviewer` -> `26_HARDWARE_SAFETY_REVIEW.md`
- `ros2-test-verifier` -> `27_TESTING_GAPS.md`

如果项目很小，仍要说明哪些 reviewer 被跳过以及原因。
