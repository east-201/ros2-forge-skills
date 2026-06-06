# ROS2 Perception / Audio / Camera Rules

## 视觉/深度相机

- 图像流应避免 reliable 大队列造成 backpressure。
- 处理节点应丢旧帧，优先处理新帧。
- depth/color 对齐策略必须明确。
- encoding、frame_id、camera_info 必须与输出 topic 对齐。
- 模型推理应与 callback 解耦。
- 低算力板上要限制频率、分辨率、线程数。

## 音频

- 音频 chunk size、采样率、通道数、格式必须 contract 化。
- ALSA device/card 不应硬编码为易变 index；优先使用 stable name 或配置。
- wakeword/listen 状态机必须明确窗口、超时、二次唤醒。

## AI 推理

- backend、model path、thread count、provider、input size 应参数化。
- 推理错误不能阻塞安全链路。
- 应有 fake/dry-run 模式和 replay 模式。
