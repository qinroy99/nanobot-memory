# Architecture

## 目标

把 MemOS/OpenClaw 风格的“持久记忆 + recall 注入 + 后续可扩展的任务切分/技能演化”迁移为 nanobot 原生可用方案。

## 分层

### 1. Storage Layer
- SQLite 本地库
- 存储 user / assistant / tool 文本
- 去除 runtime metadata 与 `<relevant-memories>` 注入块

### 2. Recall Layer
- 基于关键词的轻量召回
- 优先当前 session，再回退跨 session
- 注入到最后一条 user message 后

### 3. Patch Layer
- 在 `AgentLoop._process_message` 后半段注入 recall
- 在 `AgentLoop._save_turn` 尾部做落盘

### 4. Future Layer
- 任务切分
- 去重/压缩
- 长期摘要
- skill evolver

## 为什么拆成项目

因为直接改 site-packages 虽然最快，但不利于：
- 迁移
- 回滚
- 复用
- 版本对比
- 二次开发
