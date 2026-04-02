from __future__ import annotations

from typing import Any

from .store import MemoryStore


def build_recall_block(store: MemoryStore, query: str, session_key: str, limit: int = 5) -> str:
    rows = store.recall(query, session_key, limit=limit)
    if not rows:
        return ''
    lines = []
    for i, (role, content, _ts) in enumerate(rows, 1):
        excerpt = str(content).replace('\n', ' ')[:220]
        lines.append(f'{i}. [{role}] {excerpt}')
    return '\n\n<relevant-memories>\n' + '\n'.join(lines) + '\n</relevant-memories>'


def inject_recall(initial_messages: list[dict[str, Any]], store: MemoryStore, session_key: str) -> list[dict[str, Any]]:
    if not initial_messages:
        return initial_messages
    last = initial_messages[-1]
    if not isinstance(last, dict) or last.get('role') != 'user':
        return initial_messages
    content = last.get('content', '')
    if not isinstance(content, str):
        return initial_messages
    query = store.strip_runtime_prefix(content)
    if not query:
        return initial_messages
    block = build_recall_block(store, query, session_key)
    if not block:
        return initial_messages
    patched = list(initial_messages)
    patched[-1] = dict(last)
    patched[-1]['content'] = content + block
    return patched
