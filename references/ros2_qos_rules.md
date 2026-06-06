# ROS2 QoS Rules

## 默认建议

| 数据类型 | Reliability | Durability | History/Depth | 说明 |
|---|---|---|---|---|
| camera/image/depth/pointcloud | best_effort | volatile | keep_last 1-5 | 低延迟优先 |
| command/cmd_vel/stop | reliable | volatile | keep_last 1-3 | 命令不可轻易丢 |
| safety heartbeat | reliable | volatile | keep_last 1 | 需要 deadline/liveliness |
| robot state/status | reliable | transient_local 可选 | keep_last 1-10 | 晚订阅可拿状态 |
| map/static config | reliable | transient_local | keep_last 1 | 静态数据 |
| debug/log | best_effort | volatile | keep_last 10 | 不阻塞主链路 |

## 审查重点

1. publisher/subscriber QoS 是否兼容。
2. sensor stream 是否错误使用 reliable 大队列。
3. 控制命令是否误用 best_effort。
4. late joiner 是否需要 transient_local。
5. Deadline/liveliness 是否适合安全心跳。
6. QoS 是否集中定义，避免散落魔法数字。

## 输出格式

```text
Topic:
Expected QoS:
Actual Publisher QoS:
Actual Subscriber QoS:
Compatibility:
Risk:
Fix:
Verify: ros2 topic info -v / ros2 topic hz
```
