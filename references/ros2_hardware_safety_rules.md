# ROS2 Hardware Safety Rules

## P0 安全原则

1. 任何会导致电机、机械臂、升降台、夹爪、底盘运动的代码都必须有 stop/fail-safe 路径。
2. 通信丢失、node crash、lifecycle deactivate、exception、Ctrl-C、timeout 时必须进入安全状态。
3. 真实硬件动作必须有 dry-run/fake mode。
4. 不允许 agent 在未确认的情况下执行危险硬件命令。
5. V5 只能由真实硬件验证支持，不能由代码阅读声称。

## 必须审查

```text
hardware surface
command topics/services/actions
timeout / watchdog
emergency stop
safe shutdown
current state feedback
fake backend
rate limit
position/velocity/force limit
```

## SSH 板端特别规则

- 远程执行前先确认 host、用户、workspace、ROS_DOMAIN_ID、RMW、setup 文件。
- 默认只做只读诊断命令。
- 涉及 motion command 必须询问用户确认。
- 不要把密码写入文件或命令历史。
- 不要默认 `StrictHostKeyChecking=no`，除非用户明确要求临时跳过主机校验。
