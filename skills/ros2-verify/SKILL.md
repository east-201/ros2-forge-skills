---
name: ros2-verify
description: Run V1-V5 ROS2 verification and bringup checks locally or through SSH while preserving safety boundaries.
---

# ROS2 Verify

## 目标

对修复或当前工作区执行 V1-V5 验证，生成证据。验证可以本机执行，也可以通过 SSH 板端执行 runtime dry-run。

## 必读 references

- `subagent_dispatch_matrix.md`
- `verification_levels.md`
- `ros2_change_traceability_rules.md`
- `ros2_testing_rules.md`
- `ros2_runtime_diagnose_rules.md`
- 需要 SSH 时读 `ros2_ssh_board_access_rules.md`

## 流程

1. 创建新的 `docs/ros2-quality/<RUN_ID>-verify/`。
2. 明确目标验证等级。
3. V1：静态检查 / colcon build。
4. V2：单元测试 / 组件测试。
5. V3：launch smoke / local runtime graph。
6. V4：SSH 板端 dry-run / 真实接口不驱动危险硬件。
7. V5：真实硬件验证，必须由用户确认或提供证据。
8. 如果验证目标来自 fix session，验证完成后回写 fix 文档中的验证等级和剩余风险。

## 输出文件

```text
60_VERIFICATION_SUMMARY.md
61_V1_BUILD_STATIC.md
62_V2_UNIT_COMPONENT.md
63_V3_LAUNCH_SMOKE.md
64_V4_BOARD_DRY_RUN.md
65_V5_HARDWARE_EVIDENCE.md
66_FAILURES_AND_NEXT_STEPS.md
SESSION_INDEX.md
SESSION_META.json
```

## 禁止

- 不要为了验证而自动执行危险 motion command。
- SSH 只看到节点存在，不等于 V5。

## Fix verification 回写

如果本次验证对应某个 fix session，调用 `scan-history-curator` 或手动更新：

```text
55_FIX_STATUS_REGISTER.md
56_CHANGE_IMPACT_SUMMARY.md
```

不要只生成新的 verify 目录而忘记把 active fix session 中的问题状态改成 fixed/partial/needs-follow-up。
