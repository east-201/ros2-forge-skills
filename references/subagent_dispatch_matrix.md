# Subagent Dispatch Matrix

## Goal

Make subagent usage explicit instead of treating `subagent_templates/` as passive documentation. Claude Code discovers project subagents from `.claude/agents/`; templates remain as human-readable source prompts.

## Mandatory dispatch points

| Workflow step | Primary subagent | Purpose | May edit? |
|---|---|---|---|
| Inventory/source mapping | explorer-source-mapper | Build package/node/interface/launch/config/hardware map | No |
| Design contract | contract-architect | Convert requirements/facts into verifiable ROS2 contract | No |
| Interface review | ros2-interface-reviewer | Topic/service/action/param/TF contract review | No |
| QoS/executor review | ros2-qos-executor-reviewer | QoS, callback, executor, blocking, backpressure | No |
| Lifecycle review | ros2-lifecycle-reviewer | Lifecycle states and resource ownership | No |
| Launch/config review | ros2-launch-config-reviewer | Launch, config, remap, namespace, install | No |
| Hardware safety review | ros2-hardware-safety-reviewer | Stop/watchdog/dry-run/shutdown safety | No |
| Fix lane execution | worker-lane-patch-executor | Minimal patch for one approved fix set | Yes, only allowed files |
| Merge barrier | merge-barrier-reviewer | Accept/reject worker changes | No by default |
| Verification | ros2-test-verifier | Classify evidence V1-V5 | No |
| Runtime diagnosis | runtime-diagnoser | Interpret runtime snapshot | No |
| SSH board checks | ssh-board-operator | Read-only board diagnostics | No |

## Rules

1. A workflow that says it uses subagents must name the subagent and its expected output.
2. Reviewer subagents are read-only unless the user explicitly asks for a patch and a fix plan permits edits.
3. `worker-lane-patch-executor` cannot create or modify final status files.
4. `merge-barrier-reviewer` cannot claim V5 without user-supplied hardware evidence.
5. For SSH board work, use `ssh-board-operator` for command collection and `runtime-diagnoser` for interpretation.
