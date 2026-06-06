# /ros2-ssh

执行 `skills/ros2-runtime/SKILL.md`，并强制读取 `.claude/references/ros2_ssh_board_access_rules.md`。

目标：通过 SSH 对开发板/远端 ROS2 主机做只读诊断。默认禁止运动控制、重启、改网络、删除文件、写密钥、写密码。

常用命令：

```bash
python3 .claude/tools/ros2_ssh_probe.py --ssh user@host
python3 .claude/tools/ros2_runtime_snapshot.py --ssh user@host --setup "source /opt/ros/humble/setup.bash && source ~/ros2_ws/install/setup.bash" --out docs/ros2-quality/<RUN_ID>-runtime/raw/runtime_snapshot.json
```
