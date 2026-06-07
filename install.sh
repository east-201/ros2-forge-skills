#!/usr/bin/env bash
set -euo pipefail

OVERWRITE=0
TARGET=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --overwrite) OVERWRITE=1; shift ;;
    -h|--help) echo "Usage: ./install.sh [--overwrite] /path/to/ros2_ws"; exit 0 ;;
    *) TARGET="$1"; shift ;;
  esac
done

if [[ -z "$TARGET" ]]; then
  echo "ERROR: target workspace required"
  echo "Usage: ./install.sh [--overwrite] /path/to/ros2_ws"
  exit 2
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$(mkdir -p "$TARGET" && cd "$TARGET" && pwd)"
CLAUDE_DIR="$TARGET_DIR/.claude"
mkdir -p "$CLAUDE_DIR" "$TARGET_DIR/docs/ros2-quality" "$TARGET_DIR/docs/ros2-design"

copy_dir() {
  local name="$1"
  local src="$ROOT_DIR/$name"
  local dst="$CLAUDE_DIR/$name"
  if [[ ! -d "$src" ]]; then return 0; fi
  if [[ -e "$dst" && "$OVERWRITE" != "1" ]]; then
    echo "SKIP existing $dst; use --overwrite to replace"
    return 0
  fi
  rm -rf "$dst"
  cp -a "$src" "$dst"
  echo "installed .claude/$name"
}

for d in commands skills agents references subagent_templates tools hooks evals workspace_template docs; do
  copy_dir "$d"
done

find "$CLAUDE_DIR/tools" -type f -name "*.py" -exec chmod +x {} + 2>/dev/null || true
find "$CLAUDE_DIR/hooks" -type f -name "*.py" -exec chmod +x {} + 2>/dev/null || true

cat > "$CLAUDE_DIR/ROS2_FORGE_INSTALLED.md" <<EOF
# ROS2 Forge Skills Installed

Installed from: $ROOT_DIR
Installed to: $TARGET_DIR

Start Claude Code in this workspace and run:

\`\`\`text
/ros2
\`\`\`
EOF

echo "OK: ROS2 Forge Skills v4.4 installed into $TARGET_DIR/.claude"
