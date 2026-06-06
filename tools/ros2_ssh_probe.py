#!/usr/bin/env python3
"""Small SSH connectivity probe for ROS2 board diagnosis."""
from __future__ import annotations
import argparse, json, shlex, subprocess, time


def run(cmd, timeout):
    start = time.time()
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
        return {"cmd": cmd, "returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr, "duration_s": round(time.time() - start, 3)}
    except subprocess.TimeoutExpired as e:
        return {"cmd": cmd, "returncode": None, "stdout": e.stdout or "", "stderr": (e.stderr or "") + "\nTIMEOUT", "duration_s": round(time.time() - start, 3)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ssh", required=True, help="user@host")
    ap.add_argument("--timeout", type=float, default=8)
    ap.add_argument("--setup", default="", help="optional remote setup command before checks")
    ap.add_argument("--allow-password-prompt", action="store_true", help="allow interactive SSH password/passphrase prompt; default is BatchMode fail-fast")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    remote = "whoami; hostname; uname -m; command -v ros2 || true; printenv | grep -E 'ROS|RMW|CYCLONEDDS|FASTRTPS' || true"
    if args.setup:
        remote = f"{args.setup} >/dev/null 2>&1 || true; {remote}"
    cmd = ["ssh", "-o", "ConnectTimeout=6", "-o", "ServerAliveInterval=5", "-o", "ServerAliveCountMax=1"]
    if not args.allow_password_prompt:
        cmd += ["-o", "BatchMode=yes"]
    cmd += [args.ssh, "bash", "-lc", remote]
    res = run(cmd, args.timeout)
    status = "ok" if res["returncode"] == 0 else "failed"
    data = {"ssh": args.ssh, "status": status, "result": res}
    print(json.dumps(data, indent=2, ensure_ascii=False) if args.json else json.dumps(data, ensure_ascii=False))
    return 0 if status == "ok" else 1

if __name__ == "__main__":
    raise SystemExit(main())
