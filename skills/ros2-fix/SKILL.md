---
name: ros2-fix
description: Execute approved ROS2 fix sets with lane isolation, reviewer barrier, and verification evidence.
---

# ROS2 Fix

## 目标

按 fix plan 执行最小安全修复。worker 只做指定 lane，merge barrier 判定是否 fixed。

## 必读 references

- `subagent_dispatch_matrix.md`
- `parallel_subagent_protocol.md`
- `verification_levels.md`
- `ros2_hardware_safety_rules.md`
- 与当前 fix set 对应的 ROS2 reference。

## 执行规则

1. 先读 active fix plan。
2. 不存在 fix plan 时，不要自由修复；回到 `/ros2-plan`。
3. P0 优先，尤其硬件安全、stop、watchdog、危险命令。
4. 每个 worker lane 必须限定 allowed/forbidden files。
5. 接口/launch/config/package/hardware 行为变化需要 ICR。
6. worker 不能标 final fixed。
7. merge barrier 检查后才能更新状态。
8. 没有 V5 硬件证据，不得写“硬件验证通过”。

## 输出文件

```text
50_EXECUTION_LOG.md
51_CHANGED_FILES.md
52_REVIEWER_BARRIER_RESULTS.md
53_VERIFICATION_RESULTS.md
54_REMAINING_RISKS.md
SESSION_INDEX.md
SESSION_META.json
```

## Subagent 调度要求

每个 fix set 的执行顺序固定为：

1. `explorer-source-mapper` 读取 lane 相关上下文。
2. `worker-lane-patch-executor` 只修改 allowed files。
3. `merge-barrier-reviewer` 检查越权、接口破坏、ICR、验证证据。
4. `ros2-test-verifier` 分类验证等级。

worker 输出不能直接写 fixed；只有 merge barrier 可以给 accept/reject。
