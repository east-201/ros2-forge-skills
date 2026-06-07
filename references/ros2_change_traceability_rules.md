# ROS2 Change Traceability Rules

## Purpose

After a fix is accepted, documentation must be synchronized. Fix reports, issue registers, and the latest scan history should show what changed and what is now resolved.

## Required after accepted fix

When `merge-barrier-reviewer` accepts a worker lane, the main agent must update the active fix session:

```text
50_EXECUTION_LOG.md
52_REVIEWER_BARRIER_RESULTS.md
53_VERIFICATION_RESULTS.md
55_FIX_STATUS_REGISTER.md
56_CHANGE_IMPACT_SUMMARY.md
```

The status register must mark each covered issue as one of:

```text
fixed-v1
fixed-v2
fixed-v3
fixed-v4
fixed-v5
partially-fixed
rejected
needs-follow-up
```

Never mark `fixed-v5` without user-provided hardware evidence.

## Interface/config change log

If the accepted fix changes any of these, append a change note to the latest scan session:

```text
topic/service/action/msg/srv/action fields
parameters or parameter defaults
launch arguments, remaps, namespaces
YAML config files
package exports, dependencies, install rules
lifecycle behavior
QoS policy
hardware safety behavior
SSH/runtime setup commands
```

Append to:

```text
docs/ros2-quality/<LATEST_SCAN_RUN_ID>-scan/99_CHANGE_LOG_FROM_FIXES.md
```

This is an intentional exception to the normal non-overwrite rule: scan history may receive append-only change notes so future scans know what changed after that baseline.

## Next scan behavior

A new `/ros2-scan` must read the latest previous scan as reference, especially:

```text
SESSION_INDEX.md
facts/*.json
99_CHANGE_LOG_FROM_FIXES.md
```

The new scan must still create a fresh RUN_ID directory. It may use the previous scan for comparison only, never as an output target.

## Change note format

```text
## Change from fix session <RUN_ID>

- accepted_at:
- fix_set_id:
- reviewer:
- status:
- verification_level:
- changed_files:
- changed_interfaces:
- changed_params:
- changed_launch_config:
- changed_qos_lifecycle:
- migration_notes:
- follow_up_scan_focus:
```
