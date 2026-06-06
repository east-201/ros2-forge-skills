# Common Session Protocol

## Non-overwrite rule

Every workflow creates a fresh RUN_ID directory by default. Old sessions are historical evidence and must not be reused as output targets unless the user explicitly says resume/update current.

## Output roots

```text
docs/ros2-quality/<RUN_ID>-scan/
docs/ros2-quality/<RUN_ID>-review/
docs/ros2-quality/<RUN_ID>-plan/
docs/ros2-quality/<RUN_ID>-fix/
docs/ros2-quality/<RUN_ID>-verify/
docs/ros2-quality/<RUN_ID>-runtime/
docs/ros2-design/<RUN_ID>-design/
docs/ros2-design/<RUN_ID>-contract/
```

## Session tool

```bash
python3 .claude/tools/ros2_session.py new scan
python3 .claude/tools/ros2_session.py new review
python3 .claude/tools/ros2_session.py new plan
python3 .claude/tools/ros2_session.py new fix
python3 .claude/tools/ros2_session.py new verify
python3 .claude/tools/ros2_session.py new runtime
python3 .claude/tools/ros2_session.py new design
python3 .claude/tools/ros2_session.py new contract
```

Use `current <kind>` only when the user explicitly asks to continue the current session.

## Required metadata

Every session directory must contain:

```text
SESSION_INDEX.md
SESSION_META.json
raw/
facts/
```
