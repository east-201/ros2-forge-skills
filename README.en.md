# ROS2 Forge Skills

English | [中文](README.md)

**ROS2 Forge Skills** is an agentic engineering skill suite for Claude Code and similar agent workflows. It helps design, scan, review, fix, verify, and diagnose ROS2 packages.

It is not limited to robot projects, and it is not intended to be a huge ROS2 encyclopedia. Instead, it provides a practical ROS2 package engineering workflow: turn requirements into contracts, extract as-built facts, perform contract-based review, execute safe subagent-guided fixes, and preserve verification evidence.

```text
Requirement / idea
  -> /ros2-design architecture brainstorming
  -> /ros2-contract design contract
  -> /ros2-scan as-built fact extraction
  -> /ros2-review contract-based review
  -> /ros2-plan fix planning
  -> /ros2-fix subagent-safe patch execution
  -> /ros2-verify V1-V5 verification evidence
  -> /ros2-runtime local/SSH runtime diagnosis
  -> RUN_ID historical record
```

## Use cases

- Design a new ROS2 package before writing code.
- Define nodes, topics, services, actions, parameters, launch files, QoS, lifecycle, and tests.
- Extract facts from an existing workspace.
- Review interface mismatches, launch/config drift, QoS incompatibility, callback blocking, lifecycle gaps, and safety risks.
- Generate an executable fix plan before allowing code edits.
- Diagnose a ROS2 system locally or over SSH on a board/remote host.
- Keep every scan/review/fix/verification run in a separate non-overwritten RUN_ID directory.

## Commands

All commands start with `/ros2` and use short functional names:

```text
/ros2           # dispatcher
/ros2-design    # package/feature architecture brainstorming
/ros2-contract  # interface, parameter, launch, QoS, lifecycle contract
/ros2-scan      # as-built facts; creates a fresh RUN_ID by default
/ros2-review    # contract-based review
/ros2-plan      # executable fix plan, ICR, worker lanes
/ros2-fix       # safe P0/P1/P2 patch execution
/ros2-verify    # V1-V5 verification
/ros2-runtime   # local/SSH runtime diagnosis
/ros2-ssh       # SSH board/remote-host read-only diagnostics
```

## Skill bundle

```text
skills/ros2-design/     # architecture brainstorming
skills/ros2-contract/   # design contracts
skills/ros2-scan/       # as-built facts
skills/ros2-review/     # contract-based review
skills/ros2-plan/       # fix planning
skills/ros2-fix/        # worker-lane patch execution
skills/ros2-verify/     # V1-V5 verification
skills/ros2-runtime/    # local/SSH runtime diagnosis
```

## Modular references

To avoid bloated prompts, ROS2 knowledge is split into focused references under `references/`:

```text
ros2_workspace_build_rules.md
ros2_interface_contract_rules.md
ros2_qos_rules.md
ros2_executor_callback_rules.md
ros2_lifecycle_rules.md
ros2_launch_config_rules.md
ros2_tf_time_rules.md
ros2_hardware_safety_rules.md
ros2_perception_audio_camera_rules.md
ros2_testing_rules.md
ros2_runtime_diagnose_rules.md
ros2_ssh_board_access_rules.md
parallel_subagent_orchestration_rules.md
```

## Subagents

Project-level subagents are installed into `.claude/agents/` rather than being kept as passive templates. Important roles include:

```text
explorer-source-mapper          # read-only source/config exploration
contract-architect              # contract generation
ros2-interface-reviewer         # topic/service/action/param/TF review
ros2-qos-executor-reviewer      # QoS/callback/executor/backpressure review
ros2-lifecycle-reviewer         # lifecycle/resource ownership review
ros2-launch-config-reviewer     # launch/config/remap/install review
ros2-hardware-safety-reviewer   # hardware safety, stop, watchdog, dry-run review
worker-lane-patch-executor      # edits only one approved worker lane
merge-barrier-reviewer          # accepts/rejects worker changes
ros2-test-verifier              # classifies V1-V5 evidence
runtime-diagnoser               # analyzes runtime snapshots
ssh-board-operator              # read-only SSH diagnostics
parallel-subagent-coordinator    # merges parallel subagent lane outputs
```

## Installation

Linux/macOS:

```bash
./install.sh --overwrite /path/to/ros2_ws
```

Windows PowerShell:

```powershell
.\install.ps1 -Target C:\path\to\ros2_ws -Overwrite
```

Then start Claude Code in the ROS2 workspace:

```bash
claude
/ros2
```

## Output directories

Quality, review, fix, verification, and runtime outputs are written to:

```text
docs/ros2-quality/
```

Design and contract outputs are written to:

```text
docs/ros2-design/
```

Each run creates a fresh RUN_ID directory by default and does not overwrite previous reports:

```text
docs/ros2-quality/2026-06-07-143210-scan/
docs/ros2-quality/2026-06-07-143411-review/
docs/ros2-quality/2026-06-07-143902-plan/
docs/ros2-quality/2026-06-07-144010-fix/
docs/ros2-quality/2026-06-07-144522-runtime/
docs/ros2-design/2026-06-07-145000-design/
docs/ros2-design/2026-06-07-145210-contract/
```

`CURRENT.md` is only a pointer to the latest session. Old sessions are not overwritten. Reusing a previous session is allowed only when the user explicitly asks to resume/update the current session.


## v4.4: Unlimited design questions and parallel subagent lanes

`/ros2-design` no longer uses a hard numeric question limit. The agent should ask as many questions as needed for design correctness and classify them as:

```text
P0 blocking  # unanswered questions may make the architecture wrong
P1 quality   # design can proceed, but assumptions and risks must be recorded
P2 future    # not needed for this iteration; keep as backlog or ADR candidates
```

When many questions exist, the first round should prioritize P0 questions. P1/P2 questions are kept in the intake document instead of being dropped due to a question count limit.

Parallel subagent orchestration is also supported. Design, review, verification, and runtime diagnosis can split independent work into interface, QoS/executor, launch/config, lifecycle, safety, testing, SSH/runtime, and source-mapping lanes. The main agent or `parallel-subagent-coordinator` then merges the results into:

```text
PARALLEL_LANE_SUMMARY.md
CONFLICTS_AND_DEPENDENCIES.md
MERGED_DECISION.md
```

## v4.3: Ask before design, review after design

`/ros2-design` now starts with requirement intake and brainstorming instead of jumping directly into architecture:

```text
known requirements / known constraints / blocking questions / deferrable questions / assumptions / design readiness
```

If critical information is missing, such as upstream/downstream interfaces, node responsibilities, launch/config, QoS, lifecycle, hardware safety, SSH/board environment, or verification method, the agent should ask questions first. After drafting, `design-consistency-reviewer` checks requirement coverage, interface connectivity, parameter and launch/config alignment, module/function closure, and whether the verification plan can prove the design.

## v4.3: Sync fix docs and scan history after accepted fixes

After `merge-barrier-reviewer` accepts a fix, `/ros2-fix` must update the active fix session:

```text
55_FIX_STATUS_REGISTER.md
56_CHANGE_IMPACT_SUMMARY.md
57_SCAN_HISTORY_APPEND_LOG.md
```

If the fix changes topics/services/actions, parameters, launch/config, QoS, lifecycle, package exports, or hardware behavior, it appends an entry to the latest scan session:

```text
docs/ros2-quality/<LATEST_SCAN_RUN_ID>-scan/99_CHANGE_LOG_FROM_FIXES.md
```

The next `/ros2-scan` reads the latest previous scan and this change log as reference, but still creates a fresh RUN_ID directory and never overwrites the previous scan.

## SSH runtime diagnosis

Test SSH first:

```bash
python3 .claude/tools/ros2_ssh_probe.py --ssh user@192.168.1.10
```

Generate a remote ROS2 runtime snapshot:

```bash
python3 .claude/tools/ros2_runtime_snapshot.py \
  --ssh user@192.168.1.10 \
  --setup "source /opt/ros/humble/setup.bash && source ~/ros2_ws/install/setup.bash" \
  --out docs/ros2-quality/<RUN_ID>-runtime/raw/runtime_snapshot.json
```

SSH tools use non-interactive BatchMode by default to prevent agents from hanging on password prompts. For a one-off manual terminal run where you want to type a password or key passphrase, add:

```bash
--allow-password-prompt
```

For repeated agent use, SSH keys are recommended.

## Repository layout

```text
commands/                  slash command entry points
skills/                    Claude Skills; each skill keeps only workflow logic
agents/                    Claude Code project-level subagents
references/                modular ROS2 knowledge base
subagent_templates/        human-readable subagent prompt sources
tools/                     session, facts, runtime, SSH, QoS utilities
hooks/                     optional safety hooks
evals/                     skill evaluation prompts
workspace_template/        recommended workspace template
docs/                      output schemas and guides
```