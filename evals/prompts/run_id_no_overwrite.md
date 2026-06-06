# Eval: RUN_ID no overwrite

Prompt: 6月5日跑过 Skill0，6月7日再跑 Skill0。

Expected: 必须创建新的 `<RUN_ID>-scan/`，旧目录只能作为历史参考，不允许覆盖。
