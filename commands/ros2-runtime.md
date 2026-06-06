# /ros2-runtime

执行 `skills/ros2-runtime/SKILL.md`。

目标：诊断本机或 SSH 板端 ROS2 运行状态，生成 `docs/ros2-quality/<RUN_ID>-runtime/` 报告。支持 node/topic/service/action/param/lifecycle/TF/log/QoS 检查。

SSH 示例：

```bash
python3 .claude/tools/ros2_runtime_snapshot.py \
  --ssh user@192.168.1.10 \
  --setup "source /opt/ros/humble/setup.bash && source ~/ros2_ws/install/setup.bash" \
  --out docs/ros2-quality/<RUN_ID>-runtime/raw/runtime_snapshot.json
```
