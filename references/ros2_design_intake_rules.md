# ROS2 Design Intake Rules

## Purpose

A design session must not jump directly into architecture. It first performs requirement intake, context reading, and brainstorming so the final ROS2 package/node/pipeline design is grounded in the user's real constraints.

## Mandatory intake gate

Before producing a final design, the agent must classify the available information:

```text
Known requirements:
Known constraints:
Context already confirmed from source/docs/latest scan:
Unknown but important decisions:
Assumptions the agent is about to make:
Questions that block a reliable design:
Questions that improve design quality:
Questions that can be deferred to implementation/backlog:
```

If any blocking decision is missing, ask the user focused questions first and stop before writing the final architecture. A provisional option sketch is allowed only when it is clearly labeled as provisional.

## No hard question limit

Do not enforce a numeric limit such as "6-12 questions". Ask as many questions as the design actually needs.

However, questions must remain useful and structured:

1. Do not ask questions already answered in the prompt, docs, source tree, or latest scan facts.
2. Group questions by engineering concern so the user can answer them in order.
3. Mark each question as `P0 blocking`, `P1 quality`, or `P2 future/backlog`.
4. When there are many questions, split them into rounds. Ask all P0 questions first; keep P1/P2 available in the design intake file.
5. If the user wants fast progress, proceed with explicitly stated assumptions and mark the design as `provisional-only` until assumptions are confirmed.

## Question categories

Ask useful questions, grouped by ROS2 engineering concern:

1. Goal and success criteria: what the package must do, demo/MVP boundary, failure conditions.
2. Package role: driver, bridge, perception, manager, action server, lifecycle wrapper, tool, testkit.
3. Upstream/downstream interfaces: publishers, subscribers, services, actions, TF frames, external processes.
4. Runtime environment: ROS2 distro, language, board/host, OS, RMW, network, SSH target, compute budget.
5. Timing and QoS: sensor rate, control loop rate, latency tolerance, drop/queue policy, reliability needs.
6. Lifecycle/resource model: startup/shutdown, active/inactive behavior, model/device ownership, cleanup.
7. Launch/config: namespace, remaps, YAML files, fake/real backend, dry-run, environment variables.
8. Hardware and safety: actuators, stop/watchdog, timeout, forbidden commands, safe defaults.
9. Testing and verification: fake inputs, bag replay, launch tests, hardware evidence level.
10. Compatibility and migration: existing packages, message types, API stability, future extension.

## Context-first questioning

Before asking the user, inspect available context when it exists:

```text
docs/ros2-quality/CURRENT.md
latest docs/ros2-quality/*-scan/SESSION_INDEX.md
latest docs/ros2-quality/*-scan/facts/*.json
README.md / docs/
package.xml / CMakeLists.txt / setup.py / setup.cfg
launch/ config/ msg/ srv/ action/
```

The design intake must record what context was used and which questions remain unresolved.

## Design readiness states

A design session must maintain a clear state:

```text
intake-needed       # not enough context read yet
questions-sent      # user must answer P0 questions
provisional-only    # may sketch options, but assumptions are unconfirmed
design-draft        # enough information for a draft design
design-review-failed
design-ready        # post-design review passed
superseded          # replaced by a later design session
```

Do not label a design `design-ready` until the post-design consistency review passes.

## Output files

Design sessions should include:

```text
00A_CONTEXT_USED_FOR_DESIGN.md
00_DESIGN_INTAKE.md
01_QUESTIONS_TO_USER.md
02_REQUIREMENT_TRACEABILITY.md
02A_NON_GOALS.md
03_DESIGN_OPTIONS.md
03A_OPTION_SCORE_MATRIX.md
04_RECOMMENDED_ARCHITECTURE.md
05_INTERFACE_DRAFT.md
06_LAUNCH_CONFIG_DRAFT.md
07_RISK_AND_ASSUMPTIONS.md
08A_ACCEPTANCE_TESTS.md
08_DESIGN_REVIEW.md
09_REQUIREMENT_COVERAGE_MATRIX.md
10_INTERFACE_CONFIG_CONNECTIVITY_CHECK.md
11_IMPLEMENTATION_HANDOFF_PROMPT.md
12_DESIGN_STATE.md
13_ADR_CANDIDATES.md
SESSION_INDEX.md
SESSION_META.json
```

A final design should not be considered accepted until the post-design review passes.
