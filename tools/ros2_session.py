#!/usr/bin/env python3
"""Create and manage ROS2 Forge RUN_ID sessions.

Default behavior is intentionally non-destructive: `new` always creates a fresh
RUN_ID directory and updates CURRENT.md as a pointer. It never reuses old output
folders unless caller explicitly uses `current`.

For `scan` sessions, the new session also receives a read-only reference to the
latest previous scan so the agent can compare changes without overwriting old
reports.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

VALID_KINDS = {"design", "contract", "scan", "review", "plan", "fix", "verify", "runtime"}


def normalize_kind(kind: str) -> str:
    if kind not in VALID_KINDS:
        raise SystemExit(f"invalid kind {kind}; valid: {sorted(VALID_KINDS)}")
    return kind


def now_run_id() -> str:
    return datetime.now().strftime("%Y-%m-%d-%H%M%S")


def quality_root(workspace: Path) -> Path:
    return workspace / "docs" / "ros2-quality"


def design_root(workspace: Path) -> Path:
    return workspace / "docs" / "ros2-design"


def session_root(workspace: Path, kind: str) -> Path:
    return design_root(workspace) if kind in {"design", "contract"} else quality_root(workspace)


def write_current(workspace: Path, kind: str, session_dir: Path, run_id: str) -> None:
    root = session_root(workspace, kind)
    root.mkdir(parents=True, exist_ok=True)
    (root / "CURRENT.md").write_text(
        f"# Current ROS2 Forge Session\n\n"
        f"kind: {kind}\n\n"
        f"run_id: {run_id}\n\n"
        f"path: {session_dir.as_posix()}\n\n"
        f"updated_at: {datetime.now().isoformat(timespec='seconds')}\n",
        encoding="utf-8",
    )


def latest_previous_scan(workspace: Path, current: Path) -> Path | None:
    root = quality_root(workspace)
    if not root.exists():
        return None
    scans = sorted(
        [p for p in root.iterdir() if p.is_dir() and p.name.endswith("-scan") and p.resolve() != current.resolve()],
        key=lambda p: p.name,
    )
    return scans[-1] if scans else None


def seed_previous_scan_reference(workspace: Path, session_dir: Path) -> None:
    prev = latest_previous_scan(workspace, session_dir)
    out = session_dir / "09_PREVIOUS_SCAN_REFERENCE.md"
    if prev is None:
        out.write_text("# Previous Scan Reference\n\nNo previous scan session found.\n", encoding="utf-8")
        return
    change_log = prev / "99_CHANGE_LOG_FROM_FIXES.md"
    out.write_text(
        f"# Previous Scan Reference\n\n"
        f"- previous_scan: `{prev}`\n"
        f"- previous_change_log: `{change_log if change_log.exists() else 'not found'}`\n\n"
        f"Use the previous scan as comparison context only. Do not write new scan outputs into the previous scan directory.\n",
        encoding="utf-8",
    )


def create_session(workspace: Path, kind: str, prefix: str | None = None) -> Path:
    kind = normalize_kind(kind)
    root = session_root(workspace, kind)
    root.mkdir(parents=True, exist_ok=True)
    for attempt in range(100):
        rid = prefix or now_run_id()
        if attempt:
            rid = f"{rid}-{attempt:02d}"
        path = root / f"{rid}-{kind}"
        try:
            path.mkdir(parents=False, exist_ok=False)
            (path / "raw").mkdir(exist_ok=True)
            (path / "facts").mkdir(exist_ok=True)
            meta = {
                "project": "ROS2 Forge Skills",
                "run_id": rid,
                "kind": kind,
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "workspace_root": str(workspace.resolve()),
                "source": "new",
                "session_dir": str(path),
            }
            (path / "SESSION_META.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
            (path / "SESSION_INDEX.md").write_text(
                f"# Session Index\n\n- project: ROS2 Forge Skills\n- kind: {kind}\n- run_id: {rid}\n- path: `{path}`\n\n",
                encoding="utf-8",
            )
            write_current(workspace, kind, path, rid)
            if kind == "scan":
                seed_previous_scan_reference(workspace, path)
            return path
        except FileExistsError:
            continue
    raise SystemExit("failed to create unique session directory")


def read_current(workspace: Path, kind: str) -> Path:
    kind = normalize_kind(kind)
    current = session_root(workspace, kind) / "CURRENT.md"
    if not current.exists():
        raise SystemExit(f"No CURRENT.md for kind={kind}. Create a new session first.")
    path_line = None
    for line in current.read_text(encoding="utf-8").splitlines():
        if line.startswith("path:"):
            path_line = line.split(":", 1)[1].strip()
            break
    if not path_line:
        raise SystemExit(f"CURRENT.md has no path: {current}")
    path = Path(path_line)
    if not path.is_absolute():
        path = workspace / path
    if not path.exists():
        raise SystemExit(f"Current session path does not exist: {path}")
    return path


def list_sessions(workspace: Path, kind: str | None = None) -> list[Path]:
    roots = [session_root(workspace, normalize_kind(kind))] if kind else [quality_root(workspace), design_root(workspace)]
    out: list[Path] = []
    for root in roots:
        if root.exists():
            out.extend(sorted([p for p in root.iterdir() if p.is_dir() and "-" in p.name], key=lambda p: p.name))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["new", "current", "list"])
    ap.add_argument("kind", nargs="?")
    ap.add_argument("--workspace", default=".")
    ap.add_argument("--prefix", help="optional run_id prefix; normally omit")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    ws = Path(args.workspace).resolve()
    kind = normalize_kind(args.kind or "scan") if args.command in {"new", "current"} else (normalize_kind(args.kind) if args.kind else None)

    if args.command == "new":
        path = create_session(ws, kind, args.prefix)
        data = {"path": str(path), "kind": kind}
        print(json.dumps(data, ensure_ascii=False) if args.json else path)
    elif args.command == "current":
        path = read_current(ws, kind)
        data = {"path": str(path), "kind": kind}
        print(json.dumps(data, ensure_ascii=False) if args.json else path)
    elif args.command == "list":
        paths = list_sessions(ws, kind)
        print(json.dumps([str(p) for p in paths], indent=2, ensure_ascii=False) if args.json else "\n".join(map(str, paths)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
