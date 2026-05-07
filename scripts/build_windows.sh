#!/usr/bin/env bash
# build_windows.sh - One-click build script for Windows (run from bash)
#
# Produces a self-contained "Arbiter.exe" inside scripts/dist/.
# The bundle embeds Python and every required library, so it can run on
# machines that do not have Python installed.
#
# Usage (from any directory):
#   bash scripts/build_windows.sh
#
# Requirements on the build machine:
#   - Python 3.10+ with pip
#   - Bash environment (e.g., GitHub Actions shell: bash)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC_DIR="$REPO_ROOT/src"
REQ_FILE="$REPO_ROOT/requirements.txt"

echo "==> Installing/upgrading PyInstaller and project dependencies..."
pip install --upgrade pip
pip install --upgrade pyinstaller
pip install -r "$REQ_FILE"

echo "==> Building Arbiter.exe with PyInstaller..."
pyinstaller \
  --name "Arbiter" \
  --windowed \
  --noconfirm \
  --clean \
  --distpath "$SCRIPT_DIR/dist" \
  --workpath "$SCRIPT_DIR/build" \
  --specpath "$SCRIPT_DIR" \
  --paths "$SRC_DIR" \
  --add-data "$SRC_DIR/ui;ui" \
  --hidden-import "webview" \
  --hidden-import "webview.platforms.winforms" \
  --hidden-import "webview.platforms.edgechromium" \
  --hidden-import "webview.platforms.mshtml" \
  --hidden-import "py4swiss" \
  --collect-all "webview" \
  "$SRC_DIR/mainGUI.py"

echo ""
echo "==> Build complete!"
echo "    Standalone executable: $SCRIPT_DIR/dist/Arbiter/Arbiter.exe"
