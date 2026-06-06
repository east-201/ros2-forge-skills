#!/usr/bin/env python3
"""Summarize QoS-related lines from a runtime snapshot."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

KEYS = ["Reliability", "Durability", "History", "Depth", "Lifespan", "Deadline", "Liveliness"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("snapshot")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    snap = json.loads(Path(args.snapshot).read_text(encoding="utf-8"))
    rows = []
    for topic, res in snap.get("topic_info", {}).items():
        text = (res.get("stdout") or "") + "\n" + (res.get("stderr") or "")
        row = {"topic": topic}
        for k in KEYS:
            m = re.search(rf"{k}:\s*([^\n]+)", text, re.IGNORECASE)
            if m:
                row[k.lower()] = m.group(1).strip()
        rows.append(row)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"out": str(out), "rows": len(rows)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
