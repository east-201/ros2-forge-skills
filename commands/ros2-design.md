# /ros2-design

执行 `skills/ros2-design/SKILL.md`。

目标：先读已有上下文，再做 brainstorming 和需求澄清；问题不设硬性数量上限，按 `P0 blocking / P1 quality / P2 future` 分组。只有信息足够或用户允许带假设前进时，才输出 ROS2 package / node / pipeline / feature 设计方案。

设计阶段可以灵活并行调用 subagent：接口、QoS/executor、launch/config、lifecycle、安全、测试、SSH/runtime 等可以分 lane 并行分析，最后合并成一个设计决策。设计后必须复查用户要求、接口连接、函数职责、launch/config、QoS/lifecycle 和验证计划是否闭合。
