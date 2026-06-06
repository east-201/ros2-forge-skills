#!/usr/bin/env python3
"""Optional helper to append a summary line to SESSION_INDEX.md."""
from __future__ import annotations
import argparse
from pathlib import Path
from datetime import datetime
ap = argparse.ArgumentParser()
ap.add_argument('--session', required=True)
ap.add_argument('--summary', required=True)
args = ap.parse_args()
p = Path(args.session) / 'SESSION_INDEX.md'
p.parent.mkdir(parents=True, exist_ok=True)
with p.open('a', encoding='utf-8') as f:
    f.write(f"\n- {datetime.now().isoformat(timespec='seconds')}: {args.summary}\n")
