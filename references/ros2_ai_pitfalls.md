# ROS2 AI Agent Pitfalls

1. 把 ROS1 写法混进 ROS2。
2. 忽略 package.xml/CMake install，导致源码能跑、安装后不能跑。
3. 改 topic 名但忘记 launch remap/config/docs。
4. 以为 MultiThreadedExecutor 自动解决阻塞。
5. 在 callback 中做重推理和阻塞等待。
6. 只看源码，不看 launch 实际命名空间。
7. fixed 后直接声称硬件验证通过。
8. 随手重构接口，破坏其他包。
9. 把设备路径、模型路径、用户名路径写死。
10. SSH 远程执行危险命令前不询问。

每个 Skill 都要主动防这些坑。
