#!/usr/bin/env python3
"""Optional hook placeholder for guarding dangerous edits.

Claude Code hook APIs vary by environment. Keep this script as a simple callable
checker: pass file paths as args; it exits non-zero for obviously risky files.
"""
from __future__ import annotations
import sys
RISKY = (".msg", ".srv", ".action", "CMakeLists.txt", "package.xml")

def main():
    risky = [a for a in sys.argv[1:] if a.endswith(RISKY) or a.endswith("launch.py")]
    if risky:
        print("RISKY_EDIT_REQUIRES_ICR:", " ".join(risky))
        return 2
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
