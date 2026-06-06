# ROS2 Launch / Config Rules

## 目标

launch 和 config 是 ROS2 系统 contract 的运行入口，必须可读、可复现、可覆盖、可部署到板端。

## 检查重点

1. launch args 是否有默认值和说明。
2. config 文件是否被安装并实际加载。
3. namespace/remap 是否清晰。
4. lifecycle transition 是否由 launch 或 supervisor 管理。
5. composable node container 是否合理。
6. fake/real backend 是否可切换。
7. 参数名是否和代码声明一致。
8. 模型路径、设备路径、串口路径是否可通过参数覆盖。

## 常见反模式

- config 里参数改了，但代码没 declare 或 launch 没加载。
- launch 写死 `/dev/video0`、绝对模型路径、板端用户名路径。
- remap 后文档仍写原 topic，后续集成混乱。
- fake 和 real 混在同一 launch，比赛/测试难以复现。

## 推荐结构

```text
launch/
  bringup.launch.py
  fake.launch.py
  real.launch.py
config/
  default.yaml
  robot_k1.yaml
  sim.yaml
```
