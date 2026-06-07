# /ros2-fix

执行 `skills/ros2-fix/SKILL.md`。

目标：按已批准 fix plan 执行最小安全修复。worker 不能自证完成；merge barrier 负责 accept/reject 和验证等级判断。fix 被接受后必须更新 fix 文档状态，并在接口/配置/launch/QoS/lifecycle 等发生变化时向最近 scan session 追加 `99_CHANGE_LOG_FROM_FIXES.md`。
