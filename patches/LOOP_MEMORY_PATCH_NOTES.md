# LOOP_MEMORY_PATCH_NOTES

当前已固化到 nanobot 安装中的核心修改点：

1. `import sqlite3`
2. `self._memos_db_path = self.workspace / ".memos-nanobot" / "memos.db"`
3. 新增方法：
   - `_strip_memory_block`
   - `_ensure_memos_db`
   - `_content_to_text`
   - `_persist_messages_to_memos`
   - `_recall_memories_block`
   - `_inject_recall_into_messages`
4. 在 `_process_message()` 中注入 recall
5. 在 `_save_turn()` 中将新增消息持久化

建议在 nanobot 升级后重新核对 `AgentLoop` 结构，再应用此 patch。
