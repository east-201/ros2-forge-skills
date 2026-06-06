#!/usr/bin/env python3
"""Check that ROS2 Forge sessions are unique and not ambiguous."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from collections import Counter

def scan_root(root: Path):
    return [p.name for p in root.iterdir() if p.is_dir()] if root.exists() else []

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="docs/ros2-quality")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = Path(args.root)
    dirs = scan_root(root)
    counts = Counter(dirs)
    dup = [k for k, v in counts.items() if v > 1]
    suspicious = [d for d in dirs if d.startswith("-") or d in {"scan", "review", "plan", "fix", "verify", "runtime", "specs", "reviews", "fixs"}]
    legacy_roots = [p for p in [Path("docs/ros2-quality"), Path("docs/ros2-design")] if p.exists()]
    ok = not dup and not suspicious
    data = {"ok": ok, "root": str(root), "duplicates": dup, "suspicious": suspicious, "legacy_roots_present": [str(p) for p in legacy_roots], "session_count": len(dirs)}
    print(json.dumps(data, indent=2, ensure_ascii=False) if args.json else data)
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
