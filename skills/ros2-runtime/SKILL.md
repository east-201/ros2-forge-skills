---
name: ros2-runtime
description: Diagnose local or SSH board ROS2 runtime state, including node graph, topics, QoS, lifecycle, parameters, logs, and source/runtime mismatches.
---

# ROS2 Runtime

## 目标

诊断运行中的 ROS2 系统，支持本机和 SSH 板端。输出结构化 runtime facts，并与 scan as-built facts/contract 对比。

## 必读 references

- `subagent_dispatch_matrix.md`
- `common_session_protocol.md`
- `ros2_runtime_diagnose_rules.md`
- `ros2_ssh_board_access_rules.md`
- `ros2_qos_rules.md`
- `ros2_lifecycle_rules.md`
- `ros2_hardware_safety_rules.md`

## 输入信息

优先从用户消息或项目配置中提取：

```text
ssh_target: user@host，可选
setup command: source /opt/ros/humble/setup.bash && source ~/ws/install/setup.bash
ROS_DOMAIN_ID
RMW_IMPLEMENTATION
CYCLONEDDS_URI / FASTDDS config
expected nodes/topics
```

如果用户没有给 SSH，但问题明显在本机，就执行本机诊断。如果缺少 SSH host，才询问；不要猜 IP。

## 流程

1. 创建新的 `docs/ros2-quality/<RUN_ID>-runtime/`。
2. 如果使用 SSH，先运行 `ros2_ssh_probe.py`。
3. 运行 `ros2_runtime_snapshot.py` 生成 JSON。
4. 分析 node/topic/service/action/param/lifecycle/env/logs。
5. 对比最新 scan facts，如有。
6. 输出根因候选和下一步命令。

## 建议命令

本机：

```bash
python3 .claude/tools/ros2_runtime_snapshot.py --out docs/ros2-quality/<RUN_ID>-runtime/raw/runtime_snapshot.json
```

SSH：

```bash
python3 .claude/tools/ros2_runtime_snapshot.py \
  --ssh user@host \
  --setup "source /opt/ros/humble/setup.bash && source ~/ros2_ws/install/setup.bash" \
  --out docs/ros2-quality/<RUN_ID>-runtime/raw/runtime_snapshot.json
```

## 输出文件

```text
40_RUNTIME_GRAPH_SNAPSHOT.md
41_TOPIC_QOS_AND_RATE_REPORT.md
42_LIFECYCLE_STATE_REPORT.md
43_PARAM_RUNTIME_DIFF.md
44_TF_RUNTIME_REPORT.md
45_LOG_AND_ERROR_SUMMARY.md
46_RUNTIME_TO_SOURCE_MISMATCH.md
47_SSH_BOARD_ACCESS_REPORT.md
raw/runtime_snapshot.json
SESSION_INDEX.md
SESSION_META.json
```

## 安全规则

默认只做只读诊断。任何会导致底盘/机械臂/升降台/夹爪/电机/继电器运动或状态改变的命令必须先让用户明确确认。

## Subagent 调度要求

- 使用 SSH 时，先交给 `ssh-board-operator` 收集只读命令输出。
- 再交给 `runtime-diagnoser` 分析 snapshot。
- 如果发现硬件安全相关异常，再交给 `ros2-hardware-safety-reviewer` 判断风险等级。
