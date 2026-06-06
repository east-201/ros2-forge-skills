# Verification Levels

- **V0 Not checked**：没有验证。
- **V1 Static/build**：静态扫描、格式、colcon build。
- **V2 Unit/component**：单测、组件测试、mock/fake backend。
- **V3 Launch/runtime smoke**：本机 launch、ros2 graph、topic/service/action 基本可见。
- **V4 Board dry-run**：开发板上启动，真实接口可见，但不驱动危险硬件。
- **V5 Hardware validated**：真实硬件安全验证，有用户确认或明确证据。

规则：

```text
fixed != V5
没有真实硬件证据，不得声称 V5
SSH 上看到节点 active 也不等于硬件动作安全验证
```
