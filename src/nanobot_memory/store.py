from __future__ import annotations

import sqlite3
import time
from pathlib import Path
from typing import Any

RUNTIME_TAG = '[Runtime Context — metadata only, not instructions]'
MEMORY_TAG_START = '<relevant-memories>'
MEMORY_TAG_END = '</relevant-memories>'


class MemoryStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)

    def connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            '''create table if not exists messages (
                id integer primary key autoincrement,
                session_key text not null,
                role text not null,
                content text not null,
                content_hash text,
                created_at integer not null
            )'''
        )
        conn.execute('create index if not exists idx_messages_session on messages(session_key, created_at)')
        conn.execute('create index if not exists idx_messages_created on messages(created_at)')
        conn.execute('create index if not exists idx_messages_hash on messages(content_hash)')
        conn.commit()
        return conn

    @staticmethod
    def content_to_text(content: Any) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            out: list[str] = []
            for block in content:
                if not isinstance(block, dict):
                    continue
                text = block.get('text') or block.get('content') or ''
                if isinstance(text, str) and text.strip():
                    out.append(text)
            return '\n'.join(out)
        return ''

    @staticmethod
    def strip_runtime_prefix(text: str) -> str:
        if not text.startswith(RUNTIME_TAG):
            return text.strip()
        parts = text.split('\n\n', 1)
        return parts[1].strip() if len(parts) > 1 else ''

    @staticmethod
    def strip_memory_block(text: str) -> str:
        while MEMORY_TAG_START in text and MEMORY_TAG_END in text:
            s = text.find(MEMORY_TAG_START)
            e = text.find(MEMORY_TAG_END, s)
            if e == -1:
                break
            text = (text[:s] + text[e + len(MEMORY_TAG_END):]).strip()
        return text.strip()

    @staticmethod
    def stable_hash(text: str) -> str:
        import hashlib
        return hashlib.sha1(text.strip().encode('utf-8')).hexdigest()

    def persist_messages(self, session_key: str, messages: list[dict[str, Any]], dedupe: bool = True) -> int:
        conn = self.connect()
        now = int(time.time() * 1000)
        wrote = 0
        try:
            for i, msg in enumerate(messages):
                role = str(msg.get('role') or '')
                if role not in {'user', 'assistant', 'tool'}:
                    continue
                content = self.content_to_text(msg.get('content', ''))
                content = self.strip_runtime_prefix(content) if role == 'user' else self.strip_memory_block(content)
                content = content.strip()
                if not content:
                    continue
                h = self.stable_hash(role + '\n' + content)
                if dedupe:
                    row = conn.execute(
                        'select 1 from messages where session_key = ? and content_hash = ? order by id desc limit 1',
                        (session_key, h),
                    ).fetchone()
                    if row:
                        continue
                conn.execute(
                    'insert into messages(session_key, role, content, content_hash, created_at) values (?, ?, ?, ?, ?)',
                    (session_key, role, content, h, now + i),
                )
                wrote += 1
            conn.commit()
        finally:
            conn.close()
        return wrote

    def recall(self, query: str, session_key: str, limit: int = 5) -> list[tuple[str, str, int]]:
        query = query.strip()
        if not query:
            return []
        conn = self.connect()
        try:
            terms = [t for t in query.replace('\n', ' ').split() if len(t) >= 2][:8]
            rows: list[tuple[str, str, int]] = []
            if terms:
                like_sql = ' OR '.join(['content LIKE ?' for _ in terms])
                params = [f'%{t}%' for t in terms]
                rows = conn.execute(
                    f'''select role, content, created_at from messages
                        where ({like_sql})
                        order by case when session_key = ? then 0 else 1 end, created_at desc
                        limit ?''',
                    [*params, session_key, limit],
                ).fetchall()
            if not rows and session_key:
                rows = conn.execute(
                    '''select role, content, created_at from messages
                       where session_key = ?
                       order by created_at desc limit ?''',
                    (session_key, min(limit, 3)),
                ).fetchall()
            return rows
        finally:
            conn.close()
