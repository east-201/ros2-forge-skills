#!/usr/bin/env python3
"""Manage previous scan references and append-only change logs for ROS2 Forge."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

QUALITY_ROOT = Path("docs/ros2-quality")


def find_scan_sessions(workspace: Path) -> list[Path]:
    root = workspace / QUALITY_ROOT
    if not root.exists():
        return []
    return sorted([p for p in root.iterdir() if p.is_dir() and p.name.endswith("-scan")], key=lambda p: p.name)


def latest_scan(workspace: Path, exclude: Path | None = None) -> Path | None:
    scans = find_scan_sessions(workspace)
    if exclude is not None:
        ex = exclude.resolve()
        scans = [p for p in scans if p.resolve() != ex]
    return scans[-1] if scans else None


def print_latest(args: argparse.Namespace) -> int:
    ws = Path(args.workspace).resolve()
    p = latest_scan(ws)
    data = {"latest_scan": str(p) if p else None}
    print(json.dumps(data, indent=2, ensure_ascii=False) if args.json else (str(p) if p else ""))
    return 0


def append_change(args: argparse.Namespace) -> int:
    ws = Path(args.workspace).resolve()
    scan = Path(args.scan_session).resolve() if args.scan_session else latest_scan(ws)
    if not scan:
        raise SystemExit("No scan session found. Run /ros2-scan first or pass --scan-session.")
    scan.mkdir(parents=True, exist_ok=True)
    log = scan / "99_CHANGE_LOG_FROM_FIXES.md"
    fix_session = args.fix_session or "unknown"
    block = f"""

## Change from fix session {fix_session}

- accepted_at: {datetime.now().isoformat(timespec='seconds')}
- fix_set_id: {args.fix_set_id or 'unknown'}
- status: {args.status}
- verification_level: {args.verification_level}
- summary: {args.summary}
- changed_files: {args.changed_files or 'none recorded'}
- changed_interfaces: {args.changed_interfaces or 'none recorded'}
- changed_params: {args.changed_params or 'none recorded'}
- changed_launch_config: {args.changed_launch_config or 'none recorded'}
- changed_qos_lifecycle: {args.changed_qos_lifecycle or 'none recorded'}
- migration_notes: {args.migration_notes or 'none'}
- follow_up_scan_focus: {args.follow_up_scan_focus or 'compare implementation against this change note'}
"""
    if not log.exists():
        log.write_text(
            "# Change Log From Accepted Fixes\n\n"
            "This file is append-only. It records accepted fixes that changed public ROS2 interfaces, parameters, launch/config, QoS/lifecycle, package exports, or hardware behavior after this scan baseline was created.\n",
            encoding="utf-8",
        )
    with log.open("a", encoding="utf-8") as f:
        f.write(block)
    print(json.dumps({"appended_to": str(log)}, ensure_ascii=False) if args.json else f"appended to {log}")
    return 0


def seed_previous(args: argparse.Namespace) -> int:
    ws = Path(args.workspace).resolve()
    scan = Path(args.scan_session).resolve()
    scan.mkdir(parents=True, exist_ok=True)
    prev = latest_scan(ws, exclude=scan)
    out = scan / "09_PREVIOUS_SCAN_REFERENCE.md"
    if prev is None:
        out.write_text("# Previous Scan Reference\n\nNo previous scan session found.\n", encoding="utf-8")
        data = {"previous_scan": None, "written": str(out)}
    else:
        change_log = prev / "99_CHANGE_LOG_FROM_FIXES.md"
        out.write_text(
            f"# Previous Scan Reference\n\n"
            f"- previous_scan: `{prev}`\n"
            f"- previous_change_log: `{change_log if change_log.exists() else 'not found'}`\n\n"
            f"Use this as comparison input only. Do not write new outputs to the previous scan directory.\n",
            encoding="utf-8",
        )
        data = {"previous_scan": str(prev), "previous_change_log": str(change_log) if change_log.exists() else None, "written": str(out)}
    print(json.dumps(data, indent=2, ensure_ascii=False) if args.json else out)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("latest")
    p.add_argument("--workspace", default=".")
    p.add_argument("--kind", default="scan", help="kept for command readability; only scan is supported")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=print_latest)

    p = sub.add_parser("append-change")
    p.add_argument("--workspace", default=".")
    p.add_argument("--scan-session")
    p.add_argument("--fix-session")
    p.add_argument("--fix-set-id")
    p.add_argument("--status", default="accepted")
    p.add_argument("--verification-level", default="unknown")
    p.add_argument("--summary", required=True)
    p.add_argument("--changed-files")
    p.add_argument("--changed-interfaces")
    p.add_argument("--changed-params")
    p.add_argument("--changed-launch-config")
    p.add_argument("--changed-qos-lifecycle")
    p.add_argument("--migration-notes")
    p.add_argument("--follow-up-scan-focus")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=append_change)

    p = sub.add_parser("seed-previous")
    p.add_argument("--workspace", default=".")
    p.add_argument("--scan-session", required=True)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=seed_previous)

    args = ap.parse_args()
    if getattr(args, "kind", "scan") != "scan":
        raise SystemExit("ros2_scan_history currently supports scan sessions only")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
