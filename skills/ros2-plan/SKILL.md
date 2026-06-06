---
name: ros2-plan
description: Triage review issues and write executable fix sets, ICR decisions, worker lanes, and verification plans without editing code.
---

# ROS2 Plan

## 目标

复核 review issues，合并根因，生成 worker 可执行的修复计划。不要直接改代码。

## 必读 references

- `subagent_dispatch_matrix.md`
- `common_session_protocol.md`
- `parallel_subagent_protocol.md`
- `verification_levels.md`
- `ros2_hardware_safety_rules.md`

## 流程

1. 创建新的 `docs/ros2-quality/<RUN_ID>-plan/`。
2. 读取最新或用户指定 review session。
3. 复核 issue，剔除 false positive。
4. 按根因合并 fix set。
5. 标记 P0/P1/P2/P3。
6. 标记 ICR：接口、launch、config、package、硬件行为变化必须 ICR。
7. 生成 worker lane。
8. 生成 reviewer checklist 和 verification plan。

## Fix Set 格式

```text
Fix Set ID:
Priority:
Root cause:
Issues covered:
Allowed files:
Forbidden files:
Expected diff shape:
Must not change:
ICR required?:
Implementation steps:
Verification commands:
Rollback plan:
Reviewer checklist:
```

## 输出文件

```text
30_FIX_PLAN_SUMMARY.md
31_ISSUE_TRIAGE.md
32_FIX_SETS_P0.md
33_FIX_SETS_P1.md
34_FIX_SETS_P2.md
35_ICR_REGISTER.md
36_WORKER_LANES.md
37_REVIEWER_BARRIER_CHECKLIST.md
38_VERIFICATION_PLAN.md
SESSION_INDEX.md
SESSION_META.json
```

## Subagent 调度要求

- 先用 `explorer-source-mapper` 复核 issue evidence 和相关文件。
- 对接口、QoS、lifecycle、launch/config、硬件安全问题，分别调用对应 reviewer 做 false-positive 检查。
- 输出的每个 worker lane 必须能直接交给 `worker-lane-patch-executor`。
