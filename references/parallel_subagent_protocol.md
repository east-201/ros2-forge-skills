# Parallel Subagent Protocol

## 角色

- Explorer：只读，建立事实地图。
- Contract Architect：读需求和事实，提出 contract。
- Worker Lane：只改允许文件，只做一个 fix set。
- Reviewer Barrier：检查越权、接口破坏、验证证据。
- Verifier：运行验证，不擅自改代码。

## 并行规则

1. 同文件默认不能并行修改。
2. 公共接口、msg/srv/action、launch、config、CMake/package.xml 默认需要 ICR。
3. worker 不能修改 final status。
4. reviewer 才能标记 fixed。
5. reviewer 不能声称 V5，除非有硬件证据。

## Worker 必须收到

```text
Allowed files
Forbidden files
Expected diff shape
Must not change
Verification command
Rollback plan
```
