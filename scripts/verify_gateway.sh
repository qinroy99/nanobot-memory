#!/usr/bin/env bash
set -euo pipefail

cd /root/.nanobot/workspace

timeout 20s ~/.local/bin/nanobot gateway \
  --config /root/.nanobot/config.json \
  --workspace /root/.nanobot/workspace \
  --port 8765
