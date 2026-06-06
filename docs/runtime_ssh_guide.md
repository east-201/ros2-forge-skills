# Runtime SSH Guide

## Basic probe

```bash
python3 .claude/tools/ros2_ssh_probe.py --ssh user@host
```

## ROS2 snapshot

```bash
python3 .claude/tools/ros2_runtime_snapshot.py \
  --ssh user@host \
  --setup "source /opt/ros/humble/setup.bash && source ~/ros2_ws/install/setup.bash" \
  --out docs/ros2-quality/<RUN_ID>-runtime/raw/runtime_snapshot.json
```

## Safe defaults

Only read runtime state by default. Do not publish movement commands, call hardware actions, or edit board system configuration without explicit user confirmation.


## Password/passphrase SSH note

Runtime tools default to non-interactive BatchMode so an agent does not hang on password prompts. For a one-off manual terminal run where you want to type the password/passphrase yourself, add `--allow-password-prompt`. Prefer SSH keys for repeated agent use.
