# ROS2 TF / Time Rules

## 检查重点

1. frame 命名是否稳定：`map/odom/base_link/camera_link/...`。
2. 静态 TF 是否使用 static transform publisher 或 static broadcaster。
3. 消息 header.stamp 是否来自 node clock。
4. `use_sim_time` 是否与 `/clock` 匹配。
5. TF lookup 是否有 timeout 和错误处理。
6. 视觉/深度数据坐标系是否明确。

## 常见反模式

- 用 `now()` 伪造传感器原始时间。
- 缺少 camera optical frame。
- launch 里 frame_id 和代码默认值不一致。
- TF lookup 在 callback 中无限等待。
