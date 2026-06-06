---
name: ros2-contract
description: Convert ROS2 design decisions into verifiable package, interface, parameter, QoS, launch, lifecycle, callback, and test contracts.
---

# ROS2 Contract

## 目标

把设计脑暴或用户需求固化为后续代码、审查、验证都能引用的 contract。

## 必读 references

- `common_session_protocol.md`
- `ros2_interface_contract_rules.md`
- `ros2_qos_rules.md`
- `ros2_lifecycle_rules.md`
- `ros2_launch_config_rules.md`
- `ros2_testing_rules.md`

## 流程

1. 创建新的 `docs/ros2-design/<RUN_ID>-contract/`。
2. 如果存在 design session，读取其推荐架构；否则根据用户需求生成 contract。
3. 定义 package/node/namespace。
4. 定义 topic/service/action contract。
5. 定义 parameter schema。
6. 定义 launch/config contract。
7. 定义 QoS/time/rate contract。
8. 定义 lifecycle/resource model。
9. 定义 callback/executor plan。
10. 定义 test/verification plan。

## 输出文件

```text
00_CONTRACT_SUMMARY.md
01_PACKAGE_NODE_CONTRACT.md
02_INTERFACE_CONTRACT.md
03_PARAMETER_SCHEMA.md
04_LAUNCH_CONFIG_CONTRACT.md
05_QOS_TIMING_CONTRACT.md
06_LIFECYCLE_RESOURCE_CONTRACT.md
07_CALLBACK_EXECUTOR_CONTRACT.md
08_TEST_VERIFICATION_CONTRACT.md
09_IMPLEMENTATION_GUARDRAILS.md
SESSION_INDEX.md
SESSION_META.json
```

## 约束

contract 应该稳定、具体、可验证。不要写“适当处理”“尽量安全”这类空话。

## Subagent 调度要求

- 使用 `contract-architect` 生成 contract 初稿。
- 使用 `ros2-interface-reviewer`、`ros2-qos-executor-reviewer`、`ros2-launch-config-reviewer` 交叉复核 contract 是否可实现、可验证。
