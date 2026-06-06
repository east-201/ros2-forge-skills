# ROS2 Executor / Callback Rules

## 关键原则

1. Callback 中避免长时间阻塞、sleep、同步等待 action/service、重 IO。
2. AI 推理、图像处理、音频处理、串口阻塞读写，应放 worker thread 或异步队列。
3. MultiThreadedExecutor 不等于自动安全并行；必须设计 callback group。
4. 安全 stop、heartbeat、watchdog 不能被低优先级感知 callback 饿死。
5. timer 周期必须与实际耗时匹配，否则积压。

## 必须审查

```text
node
executor type
callback groups
subscriptions
services/actions
timers
blocking operations
shared state locks
safe stop path
```

## 常见反模式

- 单线程 executor 内图像 callback 做重推理，导致 service/action 无响应。
- callback 里调用 `spin_until_future_complete` 等待自身 executor 的 future。
- 用 mutex 包住大段推理/IO，导致状态查询阻塞。
- timer 周期 20ms，但 callback 实际 200ms。

## 修复方向

- Reentrant/MutuallyExclusive callback group 分离。
- worker queue + bounded queue + drop old frame。
- 关键控制/safety node 独立 executor 或独立 process。
- 使用状态机/lifecycle 明确资源启停。
