#!/usr/bin/env python3
"""Conservative static scanner for ROS2 review leads."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

PATTERNS = {
    "blocking_sleep": [r"std::this_thread::sleep", r"\bsleep\s*\(", r"time\.sleep\s*\("],
    "future_wait": [r"spin_until_future_complete", r"\.wait\s*\(", r"\.get\s*\(\)"],
    "hardware_motion": [r"cmd_vel", r"servo", r"motor", r"arm", r"gripper", r"lift", r"/dev/tty", r"serial"],
    "qos_magic": [r"QoS\s*\(\s*\d+\s*\)", r"SensorDataQoS", r"KeepLast\s*\("],
    "lifecycle": [r"LifecycleNode", r"on_configure", r"on_activate", r"on_deactivate", r"on_cleanup"],
    "hardcoded_path": [r"/home/", r"/dev/video\d+", r"/dev/tty[A-Za-z]+\d*"],
    "todo_stub": [r"TODO", r"FIXME", r"stub", r"fake", r"mock"],
}

IGNORE_PARTS = {"build", "install", "log", ".git", "__pycache__"}
EXTS = {".cpp", ".hpp", ".h", ".cc", ".py", ".launch.py", ".xml", ".yaml", ".yml", ".md"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    hits = []
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix not in EXTS:
            continue
        if any(part in IGNORE_PARTS for part in p.parts):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        lines = text.splitlines()
        for category, pats in PATTERNS.items():
            for pat in pats:
                rgx = re.compile(pat, re.IGNORECASE)
                for i, line in enumerate(lines, start=1):
                    if rgx.search(line):
                        hits.append({"category": category, "pattern": pat, "path": str(p.relative_to(root)), "line": i, "snippet": line.strip()[:240]})
    out.write_text(json.dumps({"root": str(root), "hits": hits}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"out": str(out), "hits": len(hits)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
