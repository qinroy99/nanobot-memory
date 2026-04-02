# nanobot-memory
nanobot 可拆分、可复用的**本地持久记忆增强套件**，提供 SQLite 自动记忆存储、召回、上下文注入能力，支持三种灵活部署方式，不依赖手工维护文件记忆。

## 项目定位
为 nanobot 打造的增强型记忆方案，区别于官方内置文件记忆，实现**自动捕获对话、持久化存储、智能召回注入**，让机器人具备原生连续记忆能力。

## 目录结构
```
├── src/nanobot_memory/  # 可复用 Python 核心模块（存储、召回、去重、任务切分）
├── patches/             # nanobot 原生代码补丁与提取文件
├── skills/nanobot-memory/ # 独立记忆技能（启用/检查/维护入口）
├── scripts/             # 安装、打补丁、验证自动化脚本
├── tests/               # 模块基础验证脚本
├── docs/                # 架构设计与使用说明
```

## 核心组成（三种使用形态）
### 1. 原生 Patch 版
- 深度集成：将**记忆召回 + 持久化**直接嵌入 nanobot `AgentLoop`
- 无侵入修改：通过补丁方式无缝对接原生运行流程
- 全自动生效：对话无需额外配置，自动启用增强记忆

### 2. 独立模块版
- 纯 Python 模块：`nanobot_memory`
- 核心能力：SQLite 存储、关键词召回、记忆去重、对话切分
- 灵活复用：可独立集成到其他 nanobot 扩展/技能中

### 3. Skill 版
- 独立技能：`nanobot-memory`
- 使用方式：在工作区直接启用，可视化管理记忆
- 提供检查、维护、重置记忆的便捷操作

## 快速使用
### 1. 仅验证核心模块功能
```bash
python3 tests/test_memory_store.py
```

### 2. 查看补丁文件
```bash
ls patches
```

### 3. 应用补丁到本地 nanobot
```bash
bash scripts/apply_patch.sh
```

### 4. 启动并验证增强记忆
```bash
bash scripts/verify_gateway.sh
```

## 运行状态
✅ 已在 **nanobot 0.1.4.post6** 环境完成实测
✅ 基础启动、记忆存储、自动召回全流程验证通过

## 与官方内置 memory 对比
### 官方 memory（内置标准技能）
- 存储：`MEMORY.md` + `HISTORY.md` 文件
- 检索：`grep`/`read_file` 手工查询
- 特点：显式、手工维护、易审计
- 适用：项目背景、用户偏好、固定事实

### nanobot-memory（本套件）
- 存储：**SQLite 数据库**
- 机制：自动捕获对话 → 持久化 → 生成回复前**自动召回**
- 注入：自动添加 `<relevant-memories>` 到上下文
- 特点：全自动、无感知、跨轮次记忆
- 适用：对话连续性、自动上下文增强、长期对话记忆

## 一句话总结
- **官方 memory**：文件型、显式、手工可控的基础记忆
- **nanobot-memory**：SQLite + 自动召回的增强智能记忆


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
