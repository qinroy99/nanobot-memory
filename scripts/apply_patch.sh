#!/usr/bin/env bash
set -euo pipefail

TARGET="/root/.local/share/uv/tools/nanobot-ai/lib/python3.11/site-packages/nanobot/agent/loop.py"
BACKUP_DIR="$(cd "$(dirname "$0")/.." && pwd)/patches/backups"
mkdir -p "$BACKUP_DIR"
TS="$(date +%Y%m%d-%H%M%S)"
cp -f "$TARGET" "$BACKUP_DIR/loop.py.$TS.bak"
echo "Backup created: $BACKUP_DIR/loop.py.$TS.bak"
echo "Note: current host already has the memory patch applied."
echo "If you need re-application on another host/version, compare against:"
echo "  patches/LOOP_MEMORY_PATCH_NOTES.md"
echo "  src/nanobot_memory/"
