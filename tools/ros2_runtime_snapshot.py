#!/usr/bin/env python3
"""Collect a JSON ROS2 runtime snapshot locally or over SSH.

Default commands are read-only. This tool is designed for agent parsing, not as a
replacement for expert bringup.
"""
from __future__ import annotations
import argparse, json, shlex, subprocess, time
from pathlib import Path

BASE_COMMANDS = {
    "identity": "whoami; hostname; uname -a",
    "network_ipv4": "ip -4 addr || true",
    "ros_env": "printenv | grep -E 'ROS|RMW|CYCLONEDDS|FASTRTPS|AMENT|COLCON' || true",
    "which_ros2": "command -v ros2 || true",
    "ros2_node_list": "ros2 node list 2>&1 || true",
    "ros2_topic_list_t": "ros2 topic list -t 2>&1 || true",
    "ros2_service_list_t": "ros2 service list -t 2>&1 || true",
    "ros2_action_list_t": "ros2 action list -t 2>&1 || true",
    "ros2_param_list": "ros2 param list 2>&1 || true",
    "ros2_lifecycle_nodes": "ros2 lifecycle nodes 2>&1 || true",
    "ros2_doctor_report": "ros2 doctor --report 2>&1 || true",
    "recent_user_journal": "journalctl --user -n 120 --no-pager 2>&1 || true",
    "recent_system_errors": "journalctl -p warning -n 120 --no-pager 2>&1 || true",
}


def run_shell(shell_cmd: str, timeout: float, ssh: str | None = None, allow_password_prompt: bool = False):
    if ssh:
        cmd = ["ssh", "-o", "ConnectTimeout=6", "-o", "ServerAliveInterval=5", "-o", "ServerAliveCountMax=1"]
        if not allow_password_prompt:
            cmd += ["-o", "BatchMode=yes"]
        cmd += [ssh, "bash", "-lc", shell_cmd]
    else:
        cmd = ["bash", "-lc", shell_cmd]
    start = time.time()
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
        return {"returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr, "duration_s": round(time.time() - start, 3), "cmd": cmd}
    except subprocess.TimeoutExpired as e:
        return {"returncode": None, "stdout": e.stdout or "", "stderr": (e.stderr or "") + "\nTIMEOUT", "duration_s": round(time.time() - start, 3), "cmd": cmd}


def wrap_setup(cmd: str, setup: str) -> str:
    if setup:
        return f"set +e; {setup}; {cmd}"
    return f"set +e; {cmd}"


def parse_topic_names(topic_list_output: str) -> list[str]:
    topics = []
    for line in topic_list_output.splitlines():
        line = line.strip()
        if not line.startswith("/"):
            continue
        topics.append(line.split()[0])
    return sorted(set(topics))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ssh", help="optional user@host")
    ap.add_argument("--allow-password-prompt", action="store_true", help="allow interactive SSH password/passphrase prompt; default is BatchMode fail-fast")
    ap.add_argument("--setup", default="", help="setup command, e.g. source /opt/ros/humble/setup.bash && source ~/ws/install/setup.bash")
    ap.add_argument("--timeout", type=float, default=12)
    ap.add_argument("--topic-info-limit", type=int, default=40)
    ap.add_argument("--topic-hz", action="append", default=[], help="topic to sample hz for; can repeat")
    ap.add_argument("--topic-hz-window", type=float, default=3.0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    snapshot = {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "mode": "ssh" if args.ssh else "local",
        "ssh": args.ssh,
        "setup": args.setup,
        "commands": {},
        "topic_info": {},
        "topic_hz": {},
    }

    for name, cmd in BASE_COMMANDS.items():
        snapshot["commands"][name] = run_shell(wrap_setup(cmd, args.setup), args.timeout, args.ssh, args.allow_password_prompt)

    topic_out = snapshot["commands"].get("ros2_topic_list_t", {}).get("stdout", "")
    topics = parse_topic_names(topic_out)[: args.topic_info_limit]
    for topic in topics:
        safe = shlex.quote(topic)
        cmd = f"ros2 topic info -v {safe} 2>&1 || true"
        snapshot["topic_info"][topic] = run_shell(wrap_setup(cmd, args.setup), args.timeout, args.ssh, args.allow_password_prompt)

    for topic in args.topic_hz:
        safe = shlex.quote(topic)
        # timeout wraps ros2 topic hz so snapshot doesn't hang.
        cmd = f"timeout {args.topic_hz_window} ros2 topic hz {safe} 2>&1 || true"
        snapshot["topic_hz"][topic] = run_shell(wrap_setup(cmd, args.setup), args.timeout + args.topic_hz_window, args.ssh, args.allow_password_prompt)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"out": str(out), "mode": snapshot["mode"], "topics_inspected": len(snapshot["topic_info"])}, ensure_ascii=False))

if __name__ == "__main__":
    main()
