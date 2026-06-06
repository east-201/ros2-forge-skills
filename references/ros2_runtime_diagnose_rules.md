# ROS2 Runtime Rules

## 目标

把运行中的 ROS2 系统当成事实来源，和源码 specs/contract 对比。

## 本机诊断命令

```bash
ros2 node list
ros2 topic list -t
ros2 topic info -v /topic
ros2 topic hz /topic
ros2 service list -t
ros2 action list -t
ros2 param list
ros2 lifecycle nodes
ros2 doctor --report
```

## SSH 板端诊断

优先使用：

```bash
python3 .claude/tools/ros2_runtime_snapshot.py --ssh user@host --setup "source /opt/ros/humble/setup.bash && source ~/ws/install/setup.bash"
```

## 诊断顺序

1. SSH 是否通。
2. ROS 环境是否 source。
3. `ros2` 命令是否存在。
4. Domain/RMW/CycloneDDS/FastDDS 环境是否符合预期。
5. 节点是否存在。
6. topic/service/action 是否存在。
7. QoS 是否兼容。
8. rate 是否正常。
9. lifecycle 是否 active。
10. param 是否与 config 一致。
11. logs 是否有 error/exception。

## 输出报告

```text
40_RUNTIME_GRAPH_SNAPSHOT.md
41_TOPIC_QOS_AND_RATE_REPORT.md
42_LIFECYCLE_STATE_REPORT.md
43_PARAM_RUNTIME_DIFF.md
44_TF_RUNTIME_REPORT.md
45_LOG_AND_ERROR_SUMMARY.md
46_RUNTIME_TO_SOURCE_MISMATCH.md
47_SSH_BOARD_ACCESS_REPORT.md
SESSION_INDEX.md
```
