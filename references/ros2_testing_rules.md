# ROS2 Testing Rules

## 验证等级

参见 `verification_levels.md`。

## 推荐测试层级

1. Static：package.xml/CMake/launch/config/facts。
2. Unit：纯函数、状态机、消息转换、参数验证。
3. Component：node with fake backend。
4. Launch smoke：启动节点、检查 topic/service/action。
5. Runtime：本机或 SSH 板端运行时图。
6. Hardware：真实设备安全验证。

## 测试重点

- 参数缺失/错误时是否 fail fast。
- fake backend 是否覆盖无硬件测试。
- lifecycle transition 是否释放资源。
- action cancel/preempt 是否安全。
- QoS 是否兼容。
- launch 是否加载 config。
