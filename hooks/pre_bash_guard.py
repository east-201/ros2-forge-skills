#!/usr/bin/env python3
"""Optional command risk guard.

Usage: pre_bash_guard.py '<command string>'
"""
from __future__ import annotations
import sys, re
cmd = " ".join(sys.argv[1:])
DANGEROUS = [r"ros2\s+topic\s+pub\s+.*cmd_vel", r"sudo\s+reboot", r"sudo\s+poweroff", r"rm\s+-rf\s+/"]
for pat in DANGEROUS:
    if re.search(pat, cmd):
        print(f"DANGEROUS_COMMAND_REQUIRES_USER_CONFIRMATION: {pat}")
        raise SystemExit(2)
raise SystemExit(0)
