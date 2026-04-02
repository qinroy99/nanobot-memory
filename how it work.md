# nanobot-memory 记忆召回：完整使用指南
我给你整理了**最简单、最清晰、可直接照着用**的召回使用方法，包含**自动召回**和**手动调用**两种方式，你直接复制就能用。

---

# 一、核心原理（一句话）
nanobot-memory 会**自动把历史对话存到 SQLite**，并在**每次生成新回复前**，自动搜索与当前问题相关的记忆，插入到提示词里：
```
<relevant-memories>
  我喜欢喝咖啡
  我住在北京
</relevant-memories>
```

---

# 二、自动记忆召回（开箱即用，无需写代码）
## 启用条件
你已经完成：
1. 应用补丁
```bash
bash scripts/apply_patch.sh
```
2. 重启 nanobot

## 自动召回流程（完全自动）
1. **你说话** → 系统自动存入记忆
2. **你问新问题**
3. 系统**自动检索相关记忆**
4. 自动把相关记忆注入上下文
5. AI 参考记忆回答

**不需要任何操作，全自动生效。**

---

# 三、手动调用记忆召回（可在技能/脚本中使用）
如果你想自己控制**什么时候召回、召回什么内容**，可以直接调用模块。

## 1. 基础调用示例
```python
from nanobot_memory import MemoryStore

# 初始化记忆库
memory = MemoryStore()

# 1. 存储记忆（自动）
memory.add(
    content="我喜欢喝美式咖啡",
    role="user"
)

# 2. 关键词召回（最常用）
memories = memory.recall(
    query="咖啡",    # 搜索关键词
    limit=5          # 返回最多5条
)

# 3. 打印召回结果
for m in memories:
    print(m.content)
```

## 2. 召回并格式化（可直接给 LLM 用）
```python
from nanobot_memory import format_memories

# 召回
memories = memory.recall("咖啡")

# 生成 LLM 可识别的记忆块
memory_text = format_memories(memories)
print(memory_text)
```

输出：
```
<relevant-memories>
我喜欢喝美式咖啡
</relevant-memories>
```

---

# 四、在 Skill 里主动触发记忆召回（nanobot 技能开发）
在 `skills/nanobot-memory/` 里可以这样写：

```python
async def recall_memory(query: str):
    from nanobot_memory import MemoryStore
    memory = MemoryStore()
    memories = memory.recall(query)
    return memories
```

用途：
- 主动查询记忆
- 做记忆管理面板
- 做记忆清理/导出

---

# 五、三种召回模式
## 1. 关键词召回（默认）
适合：对话上下文、用户偏好、历史信息
```python
memory.recall(query="咖啡")
```

## 2. 按用户ID召回（多用户隔离）
```python
memory.recall(query="咖啡", user_id="tom")
```

## 3. 按时间范围召回
```python
memory.recall(query="咖啡", days=7)  # 只召回7天内的
```

---

# 六、验证记忆是否正常工作
## 快速测试脚本
```bash
python3 tests/test_memory_recall.py
```

## 查看数据库
```bash
ls -la memory.sqlite
```

你可以用 DB Browser 打开查看所有记忆。

---

# 七、最关键的区别
- **官方 memory**：必须手工写 MEMORY.md，手工 grep
- **nanobot-memory**：自动存、自动召回、自动注入上下文

---

# 总结（极简版）
1. **自动召回**：打补丁 → 重启 → 全自动生效
2. **手动召回**：`memory.recall(query="关键词")`
3. **给 LLM 使用**：`format_memories(memories)`
4. **存储**：SQLite，不占文件，不污染目录
