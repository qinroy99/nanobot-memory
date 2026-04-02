# nanobot-memory-kit

为 nanobot 提供可拆分、可复用的本地持久记忆增强套件。

## 目录

- `src/nanobot_memory/`：可复用 Python 模块
- `patches/`：对 nanobot 原生代码的补丁与提取代码
- `skills/nanobot-memory/`：独立 skill
- `scripts/`：安装、应用补丁、验证脚本
- `tests/`：基础验证脚本
- `docs/`：设计说明

## 组成

1. **原生 patch 版**
   - 将 recall + persistence 集成到 nanobot `AgentLoop`
2. **模块版**
   - 以 `nanobot_memory` 模块提供 SQLite 存储、召回、去重、任务切分能力
3. **skill 版**
   - 用于说明如何在工作区中启用、检查、维护这套记忆增强能力

## 快速使用

### 1) 仅验证模块

```bash
python3 tests/test_memory_store.py
```

### 2) 生成并查看补丁来源文件

```bash
ls patches
```

### 3) 将 patch 应用到当前 nanobot 安装

```bash
bash scripts/apply_patch.sh
```

### 4) 启动验证

```bash
bash scripts/verify_gateway.sh
```

## 当前状态

本项目已基于当前机器上的 nanobot 0.1.4.post6 实测通过基础启动验证。
