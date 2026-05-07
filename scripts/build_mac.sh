#!/usr/bin/env bash
# build_mac.sh - One-click build script for macOS
#
# Produces a self-contained "Arbiter.app" bundle inside scripts/dist/.
# The bundle embeds Python and every required library, so it can run on
# machines that do not have Python installed.
#
# Usage (from any directory):
#   bash scripts/build_mac.sh
#
# Requirements on the build machine:
#   - Python 3.10+ with pip

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC_DIR="$REPO_ROOT/src"
REQ_FILE="$REPO_ROOT/requirements.txt"

echo "==> Installing/upgrading PyInstaller and project dependencies..."
pip install --upgrade pip
pip install --upgrade pyinstaller
pip install -r "$REQ_FILE"

echo "==> Building Arbiter.app with PyInstaller..."
pyinstaller \
  --name "Arbiter" \
  --windowed \
  --noconfirm \
  --clean \
  --distpath "$SCRIPT_DIR/dist" \
  --workpath "$SCRIPT_DIR/build" \
  --specpath "$SCRIPT_DIR" \
  --paths "$SRC_DIR" \
  --add-data "$SRC_DIR/ui:ui" \
  --hidden-import "webview" \
  --hidden-import "webview.platforms.cocoa" \
  --hidden-import "py4swiss" \
  --collect-all "webview" \
  "$SRC_DIR/mainGUI.py"

echo ""
echo "==> Build complete!"
echo "    Standalone app: $SCRIPT_DIR/dist/Arbiter.app"
