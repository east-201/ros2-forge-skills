# ROS2 Lifecycle / Resource Rules

## 适合 lifecycle 的节点

- camera/audio/serial/lidar 等硬件资源节点。
- AI model / large memory / runtime backend 节点。
- manager / task executor / mission controller。
- 需要 predictable startup/shutdown 的节点。

## 必须定义

```text
on_configure: 参数读取、资源准备、模型加载可选
on_activate: publisher activate、开始采集/订阅/worker
on_deactivate: 停止采集/worker、停止输出命令
on_cleanup: 释放资源、关闭设备
on_shutdown: safe stop + cleanup
on_error: safe stop + report
```

## 常见错误

- on_deactivate 不停止 worker thread。
- on_cleanup 不释放相机/串口/模型句柄。
- inactive 状态仍发布控制命令。
- launch 启动后 lifecycle 没 transition 到 active。

## 审查输出

```text
Node:
Lifecycle expected?: yes/no
Current behavior:
Resource ownership:
State transition risks:
Fix:
Verify: ros2 lifecycle get/set + launch smoke
```
