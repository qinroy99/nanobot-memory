# nanobot-memory: Complete Guide to Memory Recall

中文版说明见目录

A clear, copy-paste-ready guide for **automatic & manual memory recall** for nanobot-memory. Works out of the box.

---

## Core Principle (One Sentence)
nanobot-memory **automatically saves conversation history to SQLite**, and **retrieves relevant memories** before generating each new response, then injects them into the LLM prompt like this:

```xml
<relevant-memories>
  I like drinking coffee
  I live in Beijing
</relevant-memories>
```

---

## Automatic Memory Recall (Zero Code, Out of the Box)
### Prerequisites
You have already:
1. Applied the patch
   ```bash
   bash scripts/apply_patch.sh
   ```
2. Restarted nanobot

### Fully Automatic Flow
1. You send a message → automatically stored in memory
2. You ask a new question
3. System retrieves relevant memories automatically
4. Relevant memories are injected into context automatically
5. AI answers with memory context

**No action required — fully automatic.**

---

## Manual Memory Recall (For Skills / Scripts)
Control **when to recall** and **what to recall** by calling the module directly.

### 1. Basic Usage Example
```python
from nanobot_memory import MemoryStore

# Initialize memory store
memory = MemoryStore()

# 1. Add a memory (automatic in real usage)
memory.add(
    content="I like drinking americano",
    role="user"
)

# 2. Keyword recall (most common)
memories = memory.recall(
    query="coffee",  # search keyword
    limit=5          # max 5 results
)

# 3. Print results
for m in memories:
    print(m.content)
```

### 2. Recall + Format for LLM
```python
from nanobot_memory import format_memories

# Retrieve memories
memories = memory.recall("coffee")

# Format into LLM-ready memory block
memory_text = format_memories(memories)
print(memory_text)
```

Output:
```xml
<relevant-memories>
I like drinking americano
</relevant-memories>
```

---

## Trigger Memory Recall in a Skill (Nanobot Skill Development)
Inside `skills/nanobot-memory/`:

```python
async def recall_memory(query: str):
    from nanobot_memory import MemoryStore
    memory = MemoryStore()
    memories = memory.recall(query)
    return memories
```

Use cases:
- Actively query memories
- Build a memory management panel
- Clean or export memories

---

## Three Recall Modes
### 1. Keyword Recall (Default)
Best for: conversation context, user preferences, history
```python
memory.recall(query="coffee")
```

### 2. User-isolated Recall (Multi-user)
```python
memory.recall(query="coffee", user_id="tom")
```

### 3. Time-range Recall
```python
memory.recall(query="coffee", days=7)  # last 7 days only
```

---

## Verify Memory Functionality
### Quick test script
```bash
python3 tests/test_memory_recall.py
```

### Inspect database
```bash
ls -la memory.sqlite
```

You can open `memory.sqlite` with any DB Browser for SQLite to view all records.

---

## Key Difference
- **Official built-in `memory`**: manual file-based (`MEMORY.md`), manual `grep` search
- **nanobot-memory**: auto-save, auto-recall, auto-inject into context

---

## Summary (Ultra-Concise)
- **Automatic recall**: apply patch → restart → works fully automatically
- **Manual recall**: `memory.recall(query="keyword")`
- **For LLM usage**: `format_memories(memories)`
- **Storage**: SQLite, clean, no file clutter

---
