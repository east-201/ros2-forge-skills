#!/usr/bin/env python3
"""Lightweight ROS2 as-built facts extractor.

This tool is intentionally conservative. It creates machine-readable hints for
agent review; it does not prove correctness. It scans package.xml, CMake, launch,
config, msg/srv/action and common rclcpp/rclpy interface patterns.
"""
from __future__ import annotations
import argparse, json, re, xml.etree.ElementTree as ET
from pathlib import Path

IGNORE = {"build", "install", "log", ".git", ".venv", "__pycache__"}

TOPIC_PATTERNS = [
    re.compile(r"create_publisher\s*<[^>]+>\s*\(\s*\"([^\"]+)\""),
    re.compile(r"create_subscription\s*<[^>]+>\s*\(\s*\"([^\"]+)\""),
    re.compile(r"create_service\s*<[^>]+>\s*\(\s*\"([^\"]+)\""),
    re.compile(r"create_client\s*<[^>]+>\s*\(\s*\"([^\"]+)\""),
    re.compile(r"create_wall_timer\s*\("),
    re.compile(r"create_publisher\s*\(\s*[^,]+,\s*['\"]([^'\"]+)['\"]"),
    re.compile(r"create_subscription\s*\(\s*[^,]+,\s*['\"]([^'\"]+)['\"]"),
    re.compile(r"create_service\s*\(\s*[^,]+,\s*['\"]([^'\"]+)['\"]"),
    re.compile(r"create_client\s*\(\s*[^,]+,\s*['\"]([^'\"]+)['\"]"),
]


def iter_files(root: Path):
    for p in root.rglob("*"):
        if any(part in IGNORE for part in p.parts):
            continue
        if p.is_file():
            yield p


def parse_package_xml(path: Path):
    try:
        tree = ET.parse(path)
        r = tree.getroot()
        def texts(tag): return [e.text.strip() for e in r.findall(tag) if e.text]
        return {
            "path": str(path),
            "name": (r.findtext("name") or "").strip(),
            "version": (r.findtext("version") or "").strip(),
            "buildtool_depend": texts("buildtool_depend"),
            "depend": texts("depend"),
            "build_depend": texts("build_depend"),
            "exec_depend": texts("exec_depend"),
            "test_depend": texts("test_depend"),
            "member_of_group": texts("member_of_group"),
        }
    except Exception as e:
        return {"path": str(path), "error": str(e)}


def scan_code(path: Path):
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    hits = []
    for m in re.finditer(r"declare_parameter\s*\(\s*['\"]([^'\"]+)['\"]", text):
        hits.append({"kind": "param_decl", "name": m.group(1), "path": str(path), "pos": m.start()})
    for m in re.finditer(r"get_parameter\s*\(\s*['\"]([^'\"]+)['\"]", text):
        hits.append({"kind": "param_get", "name": m.group(1), "path": str(path), "pos": m.start()})
    for kw in ["create_publisher", "create_subscription", "create_service", "create_client", "create_wall_timer"]:
        if kw in text:
            hits.append({"kind": "ros_api", "name": kw, "path": str(path)})
    for m in re.finditer(r"['\"](/[^'\"]+)['\"]", text):
        s = m.group(1)
        if len(s) < 128 and not s.startswith("//"):
            hits.append({"kind": "absolute_ros_name_candidate", "name": s, "path": str(path), "pos": m.start()})
    for bad in ["sleep(", "std::this_thread::sleep", "spin_until_future_complete", "system(", "popen("]:
        if bad in text:
            hits.append({"kind": "risk_pattern", "name": bad, "path": str(path)})
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    packages = [parse_package_xml(p) for p in root.rglob("package.xml") if not any(part in IGNORE for part in p.parts)]
    launch_files = [str(p.relative_to(root)) for p in iter_files(root) if p.suffix in {".launch.py", ".xml", ".yaml", ".yml"} and ("launch" in p.parts or "config" in p.parts)]
    interfaces = {
        "msg": [str(p.relative_to(root)) for p in root.rglob("*.msg") if not any(part in IGNORE for part in p.parts)],
        "srv": [str(p.relative_to(root)) for p in root.rglob("*.srv") if not any(part in IGNORE for part in p.parts)],
        "action": [str(p.relative_to(root)) for p in root.rglob("*.action") if not any(part in IGNORE for part in p.parts)],
    }
    code_hits = []
    for p in iter_files(root):
        if p.suffix in {".cpp", ".hpp", ".h", ".cc", ".py"}:
            code_hits.extend(scan_code(p))

    data = {
        "workspace_root": str(root),
        "packages": packages,
        "launch_config_files": launch_files,
        "interfaces": interfaces,
        "code_hits": code_hits,
    }
    for name, val in [
        ("packages.json", packages),
        ("launch_config_files.json", launch_files),
        ("interfaces.json", interfaces),
        ("code_hits.json", code_hits),
        ("ros2_facts.json", data),
    ]:
        (out / name).write_text(json.dumps(val, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"out": str(out), "packages": len(packages), "code_hits": len(code_hits)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
