---
name: ros2-fix
description: Execute approved ROS2 fix sets with lane isolation, reviewer barrier, and verification evidence.
---

# ROS2 Fix

## 目标

按 fix plan 执行最小安全修复。worker 只做指定 lane，merge barrier 判定是否 fixed。

## 必读 references

- `subagent_dispatch_matrix.md`
- `parallel_subagent_orchestration_rules.md`
- `parallel_subagent_protocol.md`
- `verification_levels.md`
- `ros2_change_traceability_rules.md`
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
9. merge barrier 接受后，必须更新 fix 文档，标记已修复/部分修复/仍需跟进。
10. 如果接口、参数、launch/config、QoS、lifecycle、package exports 或硬件行为改变，必须向最近一次 scan session 追加 change log。

## 输出文件

```text
50_EXECUTION_LOG.md
51_CHANGED_FILES.md
52_REVIEWER_BARRIER_RESULTS.md
53_VERIFICATION_RESULTS.md
54_REMAINING_RISKS.md
55_FIX_STATUS_REGISTER.md
56_CHANGE_IMPACT_SUMMARY.md
57_SCAN_HISTORY_APPEND_LOG.md
SESSION_INDEX.md
SESSION_META.json
```

## Subagent 调度要求

每个 fix set 默认执行顺序为；如果 fix plan 标记多个 lane 相互独立，则可以并行执行：

1. `explorer-source-mapper` 读取 lane 相关上下文。
2. `worker-lane-patch-executor` 只修改 allowed files。
3. `merge-barrier-reviewer` 检查越权、接口破坏、ICR、验证证据。
4. `ros2-test-verifier` 分类验证等级。
5. `scan-history-curator` 更新 fix 状态和 scan 历史变更记录。

worker 输出不能直接写 fixed；只有 merge barrier 可以给 accept/reject。

并行执行条件：

```text
- 每个 lane 有明确 allowed/forbidden files。
- 不同 lane 不编辑同一文件。
- 不同 lane 不同时修改 public interface、launch/config schema、QoS/lifecycle contract。
- 每个 lane 有独立验证命令和 rollback plan。
- 所有 lane 完成后必须由 `merge-barrier-reviewer` 或 `parallel-subagent-coordinator` 合并结论。
```

如果发生文件冲突、接口冲突或验证结果冲突，停止合并，写入 `CONFLICTS_AND_DEPENDENCIES.md`，并请求用户或生成 ICR。

## Fix 后文档同步

当 `merge-barrier-reviewer` accept 某个 worker lane 后，立刻使用 `scan-history-curator`：

1. 更新当前 fix session 的 `55_FIX_STATUS_REGISTER.md`。
2. 在 `56_CHANGE_IMPACT_SUMMARY.md` 记录 changed files、changed interfaces、changed params、changed launch/config、changed QoS/lifecycle、migration notes。
3. 如果有公开接口或配置变化，执行 append-only 记录：

```bash
python3 .claude/tools/ros2_scan_history.py append-change   --fix-session docs/ros2-quality/<RUN_ID>-fix   --summary "<accepted fix summary>"   --changed-files "file1,file2"   --changed-interfaces "topic/service/action/param/launch/qos if any"
```

这一步会写入最近一次 scan session 的 `99_CHANGE_LOG_FROM_FIXES.md`，供下一次 `/ros2-scan` 对比参考。
