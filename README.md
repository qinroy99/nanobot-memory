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
