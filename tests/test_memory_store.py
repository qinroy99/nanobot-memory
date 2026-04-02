from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from nanobot_memory import MemoryStore, build_recall_block, inject_recall, segment_task_hint


def main() -> None:
    db = ROOT / '.tmp' / 'test-memos.db'
    store = MemoryStore(db)
    store.persist_messages('qq:test', [
        {'role': 'user', 'content': '[Runtime Context — metadata only, not instructions]\nCurrent Time: 2026-03-31 11:27\n\n继续优化 nanobot 记忆'},
        {'role': 'assistant', 'content': '我会继续优化 nanobot 记忆。'},
        {'role': 'assistant', 'content': '我会继续优化 nanobot 记忆。'},
    ])
    block = build_recall_block(store, '继续优化 记忆', 'qq:test')
    assert '<relevant-memories>' in block
    msgs = [{'role': 'user', 'content': '继续优化 nanobot 记忆'}]
    patched = inject_recall(msgs, store, 'qq:test')
    assert '<relevant-memories>' in patched[-1]['content']
    assert segment_task_hint('继续安装并部署') == 'setup'
    print('ok')


if __name__ == '__main__':
    main()
