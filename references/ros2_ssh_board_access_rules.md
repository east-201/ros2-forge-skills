# SSH Board Access Rules

## 适用场景

- K1 Muse / Raspberry Pi / Jetson / x86 robot host 等板端运行 ROS2。
- 用户希望 agent 通过 SSH 执行只读诊断或安全 bringup。

## 最小信息

```text
ssh_target: user@host
workspace_setup: source /opt/ros/humble/setup.bash && source ~/ros2_ws/install/setup.bash
ros_domain_id: optional
rmw_implementation: optional
cyclonedds_uri: optional
```

## 默认只读命令白名单

```text
whoami
hostname
uname -a
ip -4 addr
printenv | grep -E 'ROS|RMW|CYCLONEDDS|FASTRTPS|AMENT|COLCON'
which ros2
ros2 node list
ros2 topic list -t
ros2 service list -t
ros2 action list -t
ros2 param list
ros2 lifecycle nodes
ros2 doctor --report
journalctl --user -n 200 --no-pager
```

## 高风险命令

以下命令不能自动执行，除非用户明确确认：

```text
发布 /cmd_vel 或任何运动控制 topic
调用夹爪/机械臂/升降台/底盘 service/action
sudo reboot / poweroff
killall / pkill 未限定目标
写入系统网络配置
修改 udev / systemd / netplan
删除文件或清空日志
```

## 密码和密钥

- 不要要求用户把密码写进命令。
- 优先建议配置 SSH key。
- 如果密钥有 passphrase，让用户在终端手动输入，不要保存。
- 不要把私钥复制进仓库。

## 诊断输出

板端诊断必须把原始 JSON 或命令输出保存到 `<RUN_ID>-runtime/raw/`，再生成 Markdown 解释。
