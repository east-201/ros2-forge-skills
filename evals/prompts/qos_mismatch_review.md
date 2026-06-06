# Eval: QoS mismatch review

Prompt: 审查一个 camera image publisher 使用 reliable depth=10，而 subscriber 使用 sensor_data_qos 的包。

Expected: 必须指出 sensor stream QoS contract、publisher/subscriber mismatch 风险、验证命令 `ros2 topic info -v`。
