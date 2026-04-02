from __future__ import annotations

from pathlib import Path

LOOP = Path('/root/.local/share/uv/tools/nanobot-ai/lib/python3.11/site-packages/nanobot/agent/loop.py')
OUT = Path(__file__).resolve().parents[1] / 'patches' / 'current-loop.py.snapshot'
OUT.write_text(LOOP.read_text(encoding='utf-8'), encoding='utf-8')
print(str(OUT))
