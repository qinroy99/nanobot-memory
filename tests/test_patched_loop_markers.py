from pathlib import Path

LOOP = Path('/root/.local/share/uv/tools/nanobot-ai/lib/python3.11/site-packages/nanobot/agent/loop.py')
text = LOOP.read_text(encoding='utf-8')
markers = [
    'import sqlite3',
    'self._memos_db_path = self.workspace / ".memos-nanobot" / "memos.db"',
    'def _persist_messages_to_memos',
    'def _inject_recall_into_messages',
    'initial_messages = self._inject_recall_into_messages(initial_messages, key)',
    'self._persist_messages_to_memos(session.key, added_entries)',
]
missing = [m for m in markers if m not in text]
if missing:
    raise SystemExit('missing markers: ' + ', '.join(missing))
print('ok')
