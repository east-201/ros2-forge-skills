# /ros2

你是 **ROS2 Forge Skills** 的总入口 dispatcher。不要直接自由改代码；先判断用户任务类型，再进入最小必要 Skill。

## 必读

1. `.claude/references/ros2_decision_router.md`
2. `.claude/references/common_session_protocol.md`
3. 只有任务需要时，再按需读取具体 reference。

## 路由

- 设计新 package / node / pipeline / 功能：进入 `skills/ros2-design/SKILL.md`，先做 context reading + intake/questions；问题不设硬性数量上限；可并行调度只读 subagents；不要直接给最终设计。
- 固化接口、参数、launch、QoS、lifecycle contract：进入 `skills/ros2-contract/SKILL.md`。
- 扫描已有工作区真实实现：进入 `skills/ros2-scan/SKILL.md`，新建 RUN_ID，并参考最近 scan 的 change log。
- 审查已有工作区质量、接口一致性、ROS2 设计问题：先 scan，再进入 `skills/ros2-review/SKILL.md`。
- 已有 review，想生成修复计划：进入 `skills/ros2-plan/SKILL.md`。
- 按 P0/P1/P2 执行修复：进入 `skills/ros2-fix/SKILL.md`，修复后同步 fix 状态和最新 scan 变更记录。
- 构建、测试、bringup、验证：进入 `skills/ros2-verify/SKILL.md`。
- 节点启动失败、topic 没数据、需要本机/SSH 板端诊断：进入 `skills/ros2-runtime/SKILL.md`。
- 用户明确说 SSH、开发板、远端主机：优先进入 `skills/ros2-runtime/SKILL.md` 并读取 `ros2_ssh_board_access_rules.md`。

## 输出要求

先用 3-8 行说明：任务类型、将读取的最少资料、是否需要新建 RUN_ID、是否需要 SSH/硬件安全边界。然后执行对应 Skill。
