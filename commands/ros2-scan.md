# /ros2-scan

执行 `skills/ros2-scan/SKILL.md`。

强制规则：默认每次创建新的 `docs/ros2-quality/<RUN_ID>-scan/`，不得写入旧 session。新的 scan 应读取最近一次 scan 作为历史参考，特别是上一轮 fix 追加的 `99_CHANGE_LOG_FROM_FIXES.md`，但只能用于对比，不能作为输出目录。
