# GitHub AI 开源项目周报 📊

> 自动生成 GitHub 热门 AI/Agent 开源项目榜单，定时推送到钉钉群

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📖 项目简介

**GitHub AI 开源项目周报** 是一个自动化技能，用于：

- 🔍 **自动抓取** GitHub 近一周增长最快的 AI/Agent 开源项目
- 🤖 **智能筛选** AI 相关项目（支持自定义关键词）
- 📝 **自动生成** 中文榜单（项目介绍 + 核心亮点 + 趋势分析）
- 📤 **定时推送** 到钉钉群（支持其他平台扩展）
- 🔄 **双数据源** 保障（GitHub API + Trending API，自动重试）

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| **智能筛选** | 12+ AI 关键词自动过滤（ai, agent, llm, claude, gpt...） |
| **双数据源** | GitHub API + Trending API，自动降级保障 |
| **自动重试** | 每个数据源重试 3 次，网络波动不影响 |
| **中文翻译** | MyMemory 免费翻译 API，英→中自动翻译 |
| **亮点生成** | 根据项目描述自动生成中文核心亮点 |
| **格式统一** | 严格统一的 Markdown 格式，适配钉钉渲染 |
| **可配置** | 关键词、数量、Webhook 均可自定义 |

## 📋 输出示例

```markdown
# GitHub 热门 AI 开源项目推荐

**【统计周期】3.10 - 3.17**

---

### **1. langgenius/dify**（新上榜）

**【开发语言】** TypeScript  |  **【总星数】** 134,211

**【项目介绍】** 用于代理工作流程开发的生产就绪平台。

**【核心亮点】** AI 工作流开发平台，可视化编排 Agent 流程...

**【项目地址】** https://github.com/langgenius/dify

---

### 【行业趋势解读】

1. Agent 基础设施成核心赛道...
2. Claude 生态持续爆发...
3. 生产级工具成主流...
4. AI 从聊天工具向自主工作系统演进...

💡 本榜单由 AI 自动生成，定时推送，关注 GitHub AI 开源前沿动态。
```

## 🚀 快速开始

### 前置要求

- Python 3.8+
- 钉钉群机器人 Webhook（或其他推送平台）
- 网络连接（访问 GitHub API）

### 安装依赖

```bash
pip install requests
```

### 配置参数

编辑 `main.py` 文件，修改配置区：

```python
# -------------------------- 🔧 配置区 --------------------------
# 钉钉机器人 WebHook（替换为你自己的）
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"

# 筛选关键词（只保留 AI/Agent 相关项目）
AI_KEYWORDS = ["ai", "agent", "llm", "claude", "gpt", "openai", 
               "agi", "mcp", "rag", "agentic", "framework", "dify", "ragflow"]

# 榜单展示数量（默认 5 条）
SHOW_COUNT = 5

# 翻译配置：MyMemory 免费翻译 API
TRANSLATION_API = "https://api.mymemory.translated.net/get"
# ----------------------------------------------------------------
```

### 手动运行

```bash
python3 main.py
```

### 定时任务（推荐）

使用 crontab 设置每周一 10:00 自动推送：

```bash
crontab -e
```

添加以下内容：

```bash
# 每周一 10:00 推送 GitHub AI 周报
0 10 * * 1 cd /path/to/github-ai-weekly && python3 main.py >> logs/github-ai-weekly.log 2>&1
```

## 📁 项目结构

```
github-ai-weekly/
├── main.py              # 主程序
├── README.md            # 使用文档
├── SKILL.md             # OpenClaw 技能描述
├── logs/                # 运行日志目录
│   └── github-ai-weekly.log
└── requirements.txt     # Python 依赖（可选）
```

## 🔧 高级配置

### 自定义筛选关键词

在 `AI_KEYWORDS` 列表中添加或删除关键词：

```python
AI_KEYWORDS = [
    "ai", "agent", "llm", "claude", "gpt", "openai", 
    "agi", "mcp", "rag", "agentic", "framework", "dify", "ragflow",
    "你的关键词"  # 添加自定义关键词
]
```

### 修改展示数量

```python
SHOW_COUNT = 10  # 改为 10 条
```

### 切换翻译服务

当前使用 MyMemory 免费 API，如需切换可修改 `translate_text()` 函数。

### 扩展推送平台

当前支持钉钉，可扩展其他平台：

- 飞书：使用飞书机器人 Webhook
- 企业微信：使用企业微信机器人
- Slack：使用 Slack Incoming Webhook
- Telegram：使用 Telegram Bot API

## 📊 数据源说明

| 数据源 | 优先级 | 说明 |
|--------|--------|------|
| **trendings.herokuapp.com** | 主数据源 | GitHub Trending 第三方 API |
| **GitHub API** | 备用数据源 | 官方 Search API（stars:>1000） |

**重试机制**：每个数据源自动重试 3 次，间隔 2 秒。

## 📝 日志查看

运行日志保存在 `logs/github-ai-weekly.log`：

```bash
# 实时查看日志
tail -f logs/github-ai-weekly.log

# 查看最近 50 行
tail -n 50 logs/github-ai-weekly.log
```

## 🛠️ 故障排查

### 问题 1：获取不到项目

**原因**：网络问题或 API 限制

**解决**：
1. 检查网络连接
2. 查看日志确认 API 响应
3. 增加重试次数或延长超时时间

### 问题 2：推送失败

**原因**：Webhook 配置错误

**解决**：
1. 检查 Webhook 是否正确配置
2. 确认钉钉机器人已启用
3. 查看日志中的错误信息

### 问题 3：翻译失败

**原因**：MyMemory API 限制

**解决**：
1. MyMemory 免费 API 有调用限制
2. 代码已自动兜底返回原文
3. 可切换其他翻译服务

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

如有问题，请提交 Issue 或联系作者。

---

**Made with ❤️ for AI Enthusiasts**
