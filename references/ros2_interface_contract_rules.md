# ROS2 Interface Contract Rules

## Contract 类型

- Topic：流式数据、状态、传感器、debug。
- Service：短、同步、确定性查询/设置。
- Action：长任务、可取消、需要反馈和结果。
- Parameter：配置，不应承载高频运行数据。
- TF：坐标变换，不应用普通 topic 伪造。

## 必须记录

```text
name
message/service/action type
direction: pub/sub/server/client/action server/action client
owner node
consumer node
QoS
rate or timeout
lifecycle state availability
namespace/remap policy
failure behavior
```

## 常见错误

- 长任务用 service，导致阻塞和无法取消。
- 高频图像用 reliable 大队列，导致 backpressure。
- 状态 topic 没有 latched/transient_local 语义，晚订阅拿不到状态。
- 同名 topic 在 launch namespace 下实际路径变化，但文档没写。
- action feedback/result 字段不能表达真实任务状态。

## 审查方式

不要只查 “topic 名看起来对”。必须对比：

```text
Design Contract vs Source Code vs Launch Remap vs Runtime Graph
```
