# ROS2 Workspace / Build Rules

## 检查重点

1. `package.xml`：依赖是否完整，exec/build/test 依赖是否混淆。
2. `CMakeLists.txt`：`find_package`、target、install、ament_export 是否完整。
3. Python 包：`setup.py/setup.cfg/package.xml/resource` 是否一致。
4. msg/srv/action：生成、导出、依赖是否正确。
5. launch/config/install：launch/config/rviz/scripts 是否 install。
6. overlay/underlay：是否覆盖已有包，是否 ABI/API 兼容。
7. workspace 边界：不要误改外部 underlay。

## 常见反模式

- 节点能本地运行，但 launch 安装后找不到 config。
- C++ target 链接了依赖，但 package.xml 没声明。
- Python entry point 名称和 launch executable 不一致。
- msg 包没有 `rosidl_default_runtime`。
- 用绝对路径引用模型/config，导致板端失败。

## Review 输出

每个 build/install 问题必须包含：

```text
Evidence: 文件+行/命令输出
Impact: build-time / launch-time / runtime
Fix: 最小修改
Verify: colcon build/test 或 ros2 launch smoke
```
