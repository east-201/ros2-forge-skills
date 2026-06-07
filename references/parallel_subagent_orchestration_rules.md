# Parallel Subagent Orchestration Rules

## Purpose

Use subagents flexibly when tasks are independent. The goal is not to force a fixed waterfall, but to let specialized reviewers map, design, review, and verify separate ROS2 concerns in parallel while preserving merge safety.

## When to parallelize

Parallelize when the lanes can read the same context and produce separate reports without editing the same files.

Good parallel lanes:

```text
interface contract lane
QoS / executor / callback lane
launch / config / parameter lane
lifecycle / resource ownership lane
hardware / safety lane
testing / verification lane
runtime / SSH diagnostics lane
source mapping lane
```

Do not parallelize when:

```text
one lane depends on another lane's unresolved result
multiple workers would edit the same file
public interfaces may change without an approved ICR
hardware-affecting commands are involved
```

## Design workflow parallelism

During `/ros2-design`, the main agent may dispatch multiple read-only subagents in parallel after context is collected:

```text
design-requirement-questioner -> P0/P1/P2 questions and assumptions
explorer-source-mapper -> existing package/source/launch/config context
contract-architect -> candidate interface/parameter/lifecycle contract
ros2-interface-reviewer -> interface connectivity risks
ros2-qos-executor-reviewer -> timing, callback, QoS, backpressure risks
ros2-launch-config-reviewer -> launch/config/namespace/remap feasibility
ros2-hardware-safety-reviewer -> only if hardware or board access is involved
ros2-test-verifier -> acceptance test and evidence plan
ssh-board-operator -> only read-only SSH environment inspection when requested or needed
```

The main agent then merges the lane outputs into one design. A final pass by `design-consistency-reviewer` is required before `design-ready`.

## Review workflow parallelism

During `/ros2-review`, dispatch reviewers by scope. Each reviewer writes a separate report and must cite evidence from source, scan facts, or runtime facts.

```text
ros2-interface-reviewer -> interface report
ros2-qos-executor-reviewer -> QoS/executor report
ros2-lifecycle-reviewer -> lifecycle report
ros2-launch-config-reviewer -> launch/config report
ros2-hardware-safety-reviewer -> safety report
ros2-test-verifier -> verification gap report
```

## Fix workflow parallelism

During `/ros2-fix`, parallel workers are allowed only after `/ros2-plan` created independent fix lanes.

Each lane must declare:

```text
lane id
issue ids
allowed files
forbidden files
expected diff shape
verification command
rollback plan
```

Rules:

1. One worker lane must not edit files owned by another lane.
2. Interface/config changes require ICR approval before implementation.
3. Worker lanes cannot update final fix status.
4. `merge-barrier-reviewer` accepts/rejects each lane.
5. `scan-history-curator` updates fix documentation and appends scan change logs after acceptance.

## Merge synthesis

After parallel lanes finish, the main agent must produce:

```text
PARALLEL_LANE_SUMMARY.md
CONFLICTS_AND_DEPENDENCIES.md
MERGED_DECISION.md
FOLLOW_UP_QUESTIONS_OR_ICR.md
```

If reports disagree, do not silently choose one. Record the disagreement and either ask the user or create a specific ICR.
