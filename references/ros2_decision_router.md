# ROS2 Decision Router

## Task classes

### design
User wants to design a new package, node, pipeline, behavior, or architecture. Use `/ros2-design`.

### contract
User has a rough design and wants stable topic/service/action/param/launch/QoS/lifecycle/test contracts. Use `/ros2-contract`.

### scan
User wants to understand an existing workspace or generate as-built facts. Use `/ros2-scan`.

### review
User wants to find interface mismatches, messy code, ROS2 design issues, launch/config drift, QoS problems, lifecycle/resource issues, or safety gaps. Use `/ros2-scan` first if current facts do not exist, then `/ros2-review`.

### plan
User has review reports and wants a repair strategy. Use `/ros2-plan`.

### fix
User wants code changes based on an approved plan. Use `/ros2-fix`.

### verify
User wants build/test/bringup/evidence. Use `/ros2-verify`.

### runtime
User says nodes do not start, topics have no data, QoS may mismatch, lifecycle is inactive, a board is abnormal, or SSH is needed. Use `/ros2-runtime` or `/ros2-ssh`.

## References by concern

- package/build: `ros2_workspace_build_rules.md`
- topic/service/action/param/TF: `ros2_interface_contract_rules.md`
- QoS: `ros2_qos_rules.md`
- callback/executor: `ros2_executor_callback_rules.md`
- lifecycle/component: `ros2_lifecycle_rules.md`
- launch/config: `ros2_launch_config_rules.md`
- TF/time: `ros2_tf_time_rules.md`
- hardware / actuators / lower controller / motion: `ros2_hardware_safety_rules.md`
- perception/audio/AI: `ros2_perception_audio_camera_rules.md`
- tests: `ros2_testing_rules.md`
- SSH/board: `ros2_ssh_board_access_rules.md`
- runtime: `ros2_runtime_diagnose_rules.md`
