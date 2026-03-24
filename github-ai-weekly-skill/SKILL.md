---
name: github-ai-weekly
description: 自动生成 GitHub 热门 AI 项目榜单，定时推送到钉钉
author: sangshy
version: 1.0.0
tags: [github, ai, weekly, dingtalk, trending]
---

# GitHub AI 开源项目周报

## 技能描述

自动生成近两周 GitHub 增长最快的 AI/Agent 项目榜单，支持定时推送到钉钉群。

**核心特性：**
- ✅ 双数据源保障（Trending API + GitHub API）
- ✅ 自动翻译项目描述（英→中）
- ✅ 自动生成核心亮点
- ✅ 丰富的中文报告格式
- ✅ 钉钉 Markdown 完美适配

## 触发方式

- **定时触发**：每周一 10:00 自动推送
- **手动触发**：随时调用

## 输出格式

Markdown 榜单，包含：
- 项目名称和作者
- 开发语言和总星数
- 项目详细介绍（中文翻译）
- 核心亮点（自动生成）
- 项目地址链接
- 趋势分析

## 配置说明

### 钉钉 Webhook

在 `main.py` 中替换 `DINGTALK_WEBHOOK` 为你的钉钉机器人地址。

### 筛选关键词

可在 `main.py` 中修改 `AI_KEYWORDS` 列表：
```python
AI_KEYWORDS = ["ai", "agent", "llm", "claude", "gpt", "openai", "agi", "mcp", "rag", "agentic", "framework"]
```

### 榜单数量

可在 `main.py` 中修改 `SHOW_COUNT`（默认 10 条）：
```python
SHOW_COUNT = 10
```

### 定时任务

```bash
# 每周一 10:00 推送
0 10 * * 1 cd /Users/wanggenshen/.openclaw/workspace && python3 skills/github-ai-weekly/main.py >> logs/github-ai-weekly.log 2>&1
```

## 使用方法

### 手动运行

```bash
cd /Users/wanggenshen/.openclaw/workspace
python3 skills/github-ai-weekly/main.py
```

### 查看日志

```bash
tail -f logs/github-ai-weekly.log
```

## 数据源

1. **主数据源**：trendings.herokuapp.com（GitHub Trending API）
2. **备用数据源**：GitHub 官方 Search API

## 翻译服务

使用 MyMemory 免费翻译 API（英→中），无需配置 API Key。

## 报告格式示例

```
📊 过去两周 GitHub 增长最快的 AI 开源项目盘点（03 月 10 日 -03 月 24 日）

**聚焦 Agent 基础设施爆发，生产级工具成主流**

---

### 1. author/project ⭐ 新上榜

**开发语言**：Python | **总星数**：1,234

**项目详细介绍**：（中文翻译的项目描述）

**核心亮点**：AI 智能体开发框架，可快速构建多角色、自主工作的 AI 代理系统

🔗 项目地址：https://github.com/author/project

---
```
