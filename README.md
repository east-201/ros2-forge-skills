# ROS2 Forge Skills

[English](README.en.md) | 中文

**ROS2 Forge Skills** 是一套面向 Claude Code / Agent 工作流的 ROS2 专项技能库，用于设计、扫描、审查、修复、验证和运行时诊断各种 ROS2 package。

它不局限于机器人项目，也不只是一个 ROS2 知识大全。它更像一个面向 ROS2 package 的工程锻造流程：先把需求变成 contract，再提取真实实现 facts，再做 contract-based review，最后通过 subagent 安全修复并留下验证证据。

```text
需求/想法
  -> /ros2-design 设计脑暴
  -> /ros2-contract 设计契约
  -> /ros2-scan as-built 事实扫描
  -> /ros2-review contract-based 审查
  -> /ros2-plan 修复计划
  -> /ros2-fix subagent 安全修复
  -> /ros2-verify V1-V5 验证证据
  -> /ros2-runtime 本机/SSH 运行时诊断
  -> RUN_ID 历史留档
```

## 适用场景

- 新建 ROS2 package 前，需要先设计节点、topic/service/action、参数、launch、QoS、lifecycle。
- 已有工作区比较乱，需要生成真实实现 spec/facts。
- 想检查接口是否没对齐、launch/config 是否没生效、QoS 是否不兼容、callback 是否阻塞。
- 想让 agent 根据审查报告生成可执行修复计划，而不是直接乱改代码。
- 想通过 SSH 查看开发板/远端主机上的 ROS2 runtime 状态。
- 想保留每次审查、修复、验证的历史记录，不覆盖旧报告。

## 命令设计

所有命令都以 `/ros2` 开头，名字尽量短：

```text
/ros2           # 总入口，自动路由
/ros2-design    # 新包/新功能设计脑暴
/ros2-contract  # 生成接口、参数、launch、QoS、生命周期契约
/ros2-scan      # 扫描当前工作区 as-built facts，默认新 RUN_ID
/ros2-review    # 基于 facts/contract 审查
/ros2-plan      # 生成可执行 fix plan、ICR、worker lanes
/ros2-fix       # 按 P0/P1/P2 安全修复
/ros2-verify    # V1-V5 验证
/ros2-runtime   # 本机/SSH 运行时诊断
/ros2-ssh       # SSH 板端/远端主机只读诊断入口
```

## Skill Bundle

```text
skills/ros2-design/     # 设计脑暴
skills/ros2-contract/   # 设计契约
skills/ros2-scan/       # as-built facts
skills/ros2-review/     # contract-based review
skills/ros2-plan/       # fix planwriting
skills/ros2-fix/        # worker lane patch execution
skills/ros2-verify/     # V1-V5 verification
skills/ros2-runtime/    # local/SSH runtime diagnosis
```

## 模块化知识库

为了避免冗杂，具体 ROS2 知识拆在 `references/` 中，Skill 只按需读取：

```text
ros2_workspace_build_rules.md
ros2_interface_contract_rules.md
ros2_qos_rules.md
ros2_executor_callback_rules.md
ros2_lifecycle_rules.md
ros2_launch_config_rules.md
ros2_tf_time_rules.md
ros2_hardware_safety_rules.md
ros2_perception_audio_camera_rules.md
ros2_testing_rules.md
ros2_runtime_diagnose_rules.md
ros2_ssh_board_access_rules.md
```

## Subagent 机制

安装后会把项目级 subagent 放到 `.claude/agents/`，而不是只放普通模板。关键角色包括：

```text
explorer-source-mapper          # 只读扫描源码和配置
contract-architect              # 设计契约生成
ros2-interface-reviewer         # topic/service/action/param/TF 审查
ros2-qos-executor-reviewer      # QoS/callback/executor/backpressure 审查
ros2-lifecycle-reviewer         # lifecycle 和资源释放审查
ros2-launch-config-reviewer     # launch/config/remap/install 审查
ros2-hardware-safety-reviewer   # 硬件安全、stop、watchdog、dry-run 审查
worker-lane-patch-executor      # 只执行一个批准的 worker lane
merge-barrier-reviewer          # 修复后 accept/reject，worker 不能自证 fixed
ros2-test-verifier              # V1-V5 验证证据分类
runtime-diagnoser               # runtime snapshot 分析
ssh-board-operator              # SSH 只读板端诊断
```

## 安装

Linux/macOS：

```bash
./install.sh --overwrite /path/to/ros2_ws
```

Windows PowerShell：

```powershell
.\install.ps1 -Target C:\path\to\ros2_ws -Overwrite
```

安装后进入 ROS2 工作区：

```bash
claude
/ros2
```

## 输出目录规则

所有质量、审查、修复、验证、运行时诊断结果放在：

```text
docs/ros2-quality/
```

设计和 contract 放在：

```text
docs/ros2-design/
```

每次运行默认创建新的 RUN_ID 目录，**不会覆盖旧报告**：

```text
docs/ros2-quality/2026-06-07-143210-scan/
docs/ros2-quality/2026-06-07-143411-review/
docs/ros2-quality/2026-06-07-143902-plan/
docs/ros2-quality/2026-06-07-144010-fix/
docs/ros2-quality/2026-06-07-144522-runtime/
docs/ros2-design/2026-06-07-145000-design/
docs/ros2-design/2026-06-07-145210-contract/
```

`CURRENT.md` 只记录最新 session 指针，不覆盖旧 session。只有用户明确说“继续当前 session / resume / update current”时，才允许复用旧目录。

## SSH 运行时诊断

先测试 SSH：

```bash
python3 .claude/tools/ros2_ssh_probe.py --ssh user@192.168.1.10
```

生成远端 ROS2 runtime snapshot：

```bash
python3 .claude/tools/ros2_runtime_snapshot.py \
  --ssh user@192.168.1.10 \
  --setup "source /opt/ros/humble/setup.bash && source ~/ros2_ws/install/setup.bash" \
  --out docs/ros2-quality/<RUN_ID>-runtime/raw/runtime_snapshot.json
```

默认 SSH 工具使用非交互 BatchMode，避免 agent 卡在密码输入。如果你手动在终端运行且需要输入密码或密钥 passphrase，可以加：

```bash
--allow-password-prompt
```

长期建议配置 SSH key。

## 目录结构

```text
commands/                  slash command 入口
skills/                    Claude Skills，每个 Skill 只保留任务流程
agents/                    Claude Code 项目级 subagents
references/                模块化知识库，按需读取
subagent_templates/        subagent 模板源文件
tools/                     session、facts、runtime、SSH、QoS 等工具
hooks/                     可选防误改 hook
evals/                     skill 自测样例
workspace_template/        推荐工作区模板
docs/                      输出 schema 和使用说明
```

## 安全边界

- 默认不执行会导致底盘、机械臂、升降台、夹爪、电机、继电器动作的命令。
- 默认不执行 reboot/poweroff、网络配置修改、删除文件、写入密钥或密码。
- 没有真实硬件证据，不得声称 V5。
- worker 不能自证 fixed，必须经过 merge barrier。

## 使用效果

他竟然真的能让mimov2.5pro变聪明!