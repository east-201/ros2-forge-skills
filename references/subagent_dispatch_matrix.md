# Subagent Dispatch Matrix

## Goal

Make subagent usage explicit instead of treating `subagent_templates/` as passive documentation. Claude Code discovers project subagents from `.claude/agents/`; templates remain as human-readable source prompts.

## Flexible dispatch principle

Use subagents when they add value. Do not force every subagent on every task. Dispatch by scope, risk, and independence. When several read-only analyses are independent, run them in parallel and merge their outputs.

Read also: `parallel_subagent_orchestration_rules.md`.

## Mandatory and optional dispatch points

| Workflow step | Primary subagent | Purpose | May edit? | Parallelizable? |
|---|---|---|---|---|
| Inventory/source mapping | explorer-source-mapper | Build package/node/interface/launch/config/hardware map | No | Yes |
| Design intake | design-requirement-questioner | Ask P0/P1/P2 questions before final ROS2 design | No | Yes |
| Parallel design merge | parallel-subagent-coordinator | Merge independent design/review lanes into one decision | No | Coordinator |
| Design contract | contract-architect | Convert requirements/facts into verifiable ROS2 contract | No | Yes |
| Design review | design-consistency-reviewer | Check requirement coverage and interface/config connectivity | No | Final gate |
| Interface review | ros2-interface-reviewer | Topic/service/action/param/TF contract review | No | Yes |
| QoS/executor review | ros2-qos-executor-reviewer | QoS, callback, executor, blocking, backpressure | No | Yes |
| Lifecycle review | ros2-lifecycle-reviewer | Lifecycle states and resource ownership | No | Yes |
| Launch/config review | ros2-launch-config-reviewer | Launch, config, remap, namespace, install | No | Yes |
| Hardware safety review | ros2-hardware-safety-reviewer | Stop/watchdog/dry-run/shutdown safety | No | Yes, read-only |
| Fix lane execution | worker-lane-patch-executor | Minimal patch for one approved fix set | Yes, only allowed files | Yes, only independent lanes |
| Merge barrier | merge-barrier-reviewer | Accept/reject worker changes | No by default | Final gate |
| Fix documentation sync | scan-history-curator | Update fix status and append latest scan change notes | Yes, docs only | After accepted lanes |
| Verification | ros2-test-verifier | Classify evidence V1-V5 | No | Yes |
| Runtime diagnosis | runtime-diagnoser | Interpret runtime snapshot | No | Yes |
| SSH board checks | ssh-board-operator | Read-only board diagnostics | No | Yes, read-only |

## Rules

1. A workflow that says it uses subagents must name the subagent and expected output.
2. Reviewer subagents are read-only unless the user explicitly asks for a patch and a fix plan permits edits.
3. `worker-lane-patch-executor` cannot create or modify final status files.
4. `merge-barrier-reviewer` cannot claim V5 without user-supplied hardware evidence.
5. For SSH board work, use `ssh-board-operator` for command collection and `runtime-diagnoser` for interpretation.
6. For broad design/review work, prefer independent parallel lanes followed by synthesis instead of one giant reviewer pass.

## Design gate rule

`/ros2-design` must dispatch `design-requirement-questioner` before producing a final architecture. If readiness is `blocked`, ask the user all current P0 blocking questions and stop. There is no numeric question cap. If readiness is `provisional-only`, the design must be labeled provisional and must include assumptions.

## Parallel synthesis rule

When more than one subagent lane is used, create or update:

```text
PARALLEL_LANE_SUMMARY.md
CONFLICTS_AND_DEPENDENCIES.md
MERGED_DECISION.md
```

The main agent owns synthesis. No single specialist subagent may silently override another lane.

## Fix documentation rule

After `merge-barrier-reviewer` accepts a fix lane, dispatch `scan-history-curator` to update the active fix session and append scan history notes when public interfaces, parameters, launch/config, QoS/lifecycle, package exports, or hardware behavior changed.
