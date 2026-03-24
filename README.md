# Sangshy Skills 🚀

> 记录和提供有用的 Skill，你不会错过

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills Collection](https://img.shields.io/badge/collection-skills-blue)](.)

---

## 📖 仓库简介

**Sangshy Skills** 是一个精选技能（Skill）集合仓库，致力于收集和提供实用、高效的 AI 助手技能。

### 🎯 仓库目标

- ✅ **精选实用** - 只收录真正有用的技能
- ✅ **开箱即用** - 每个技能都有完整的使用文档
- ✅ **持续更新** - 不断添加新的优质技能
- ✅ **易于管理** - 清晰的文件结构和版本管理

### 💡 什么是 Skill？

Skill 是 AI 助手的扩展能力模块，每个 Skill 都是一个独立的功能单元，可以：

- 🤖 自动化执行特定任务
- 📊 获取和处理数据
- 📤 推送信息到指定平台
- 🔧 扩展 AI 助手的能力边界

---

## 📦 当前收录的 Skills

### 1️⃣ GitHub AI 开源项目周报 📊

**目录**: [`github-ai-weekly-skill/`](./github-ai-weekly-skill/)

**功能描述**:
- 🔍 自动抓取 GitHub 近一周增长最快的 AI/Agent 开源项目
- 🤖 智能筛选 AI 相关项目（12+ 关键词）
- 📝 自动生成中文榜单（项目介绍 + 核心亮点 + 趋势分析）
- 📤 定时推送到钉钉群（支持其他平台扩展）
- 🔄 双数据源保障（GitHub API + Trending API，自动重试 3 次）

**核心特性**:
| 特性 | 说明 |
|------|------|
| **智能筛选** | 12+ AI 关键词自动过滤（ai, agent, llm, claude, gpt...） |
| **双数据源** | GitHub API + Trending API，自动降级保障 |
| **自动重试** | 每个数据源重试 3 次，网络波动不影响 |
| **中文翻译** | MyMemory 免费翻译 API，英→中自动翻译 |
| **亮点生成** | 根据项目描述自动生成中文核心亮点 |
| **格式统一** | 严格统一的 Markdown 格式，适配钉钉渲染 |
| **可配置** | 关键词、数量、Webhook 均可自定义 |

**输出示例**:
```markdown
# GitHub 热门 AI 开源项目推荐

**【统计周期】3.10 - 3.17**

---

### **1. langgenius/dify**（新上榜）

**【开发语言】** TypeScript  |  **【总星数】** 134,211

**【项目介绍】** 用于代理工作流程开发的生产就绪平台。

**【核心亮点】** AI 工作流开发平台，可视化编排 Agent 流程...

**【项目地址】** https://github.com/langgenius/dify
```

**使用方式**:
```bash
# 克隆仓库
git clone https://github.com/sangshy-go/sangshy-skills.git

# 进入技能目录
cd sangshy-skills/github-ai-weekly-skill

# 安装依赖
pip install -r requirements.txt

# 配置 Webhook（编辑 main.py）
# 运行
python3 main.py

# 定时任务（每周一 10:00）
0 10 * * 1 python3 main.py >> logs/github-ai-weekly.log 2>&1
```

**详细文档**: [查看完整 README](./github-ai-weekly-skill/README.md)

---

## 🗂️ 目录结构

```
sangshy-skills/
├── README.md                          # 本文件（总览）
├── github-ai-weekly-skill/            # GitHub AI 周报技能
│   ├── README.md                      # 技能使用文档
│   ├── main.py                        # 主程序
│   ├── SKILL.md                       # 技能描述
│   ├── requirements.txt               # Python 依赖
│   └── .gitignore                     # Git 忽略配置
└── ...                                # 更多技能（持续更新）
```

---

## 🚀 快速开始

### 前置要求

- Python 3.8+
- Git
- 网络连接

### 使用步骤

1. **克隆仓库**
```bash
git clone https://github.com/sangshy-go/sangshy-skills.git
cd sangshy-skills
```

2. **选择技能**
查看当前可用的技能列表（见上方"当前收录的 Skills"）

3. **安装依赖**
```bash
cd <技能目录>
pip install -r requirements.txt
```

4. **配置参数**
编辑 `main.py` 文件，按说明配置必要参数（如 Webhook、API Key 等）

5. **运行技能**
```bash
python3 main.py
```

6. **设置定时任务（可选）**
```bash
crontab -e
# 添加定时任务
```

---

## 📋 技能提交指南

如果你想贡献新的 Skill，请遵循以下规范：

### 文件结构要求

```
<skill-name>/
├── README.md          # 必需：详细使用文档
├── main.py            # 必需：主程序
├── SKILL.md           # 推荐：技能描述
├── requirements.txt   # 推荐：依赖列表
└── .gitignore         # 推荐：Git 忽略配置
```

### README 内容要求

- ✅ 功能描述（解决什么问题）
- ✅ 核心特性（功能亮点）
- ✅ 使用方式（安装、配置、运行）
- ✅ 输出示例（效果展示）
- ✅ 配置说明（参数解释）
- ✅ 故障排查（常见问题）

### 提交步骤

1. 在仓库根目录创建新的技能目录
2. 按照规范编写代码和文档
3. 更新主 README（本文件）的技能列表
4. 提交 Pull Request

---

## 🔄 更新日志

### v1.0.0 - 2026-03-24

- 🎉 仓库初始化
- 📊 新增 GitHub AI 开源项目周报技能
  - 自动抓取 GitHub 热门 AI 项目
  - 双数据源 + 自动重试
  - 中文翻译 + 亮点生成
  - 定时推送（每周一 10:00）

---

## 🤝 贡献指南

欢迎贡献新的 Skills！

### 贡献方式

1. **提交新技能** - 创建实用的 AI 助手技能
2. **改进现有技能** - 修复 bug、优化性能、添加功能
3. **完善文档** - 改进使用说明、添加示例
4. **反馈问题** - 提交 Issue 报告问题或建议

### 贡献流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 📞 联系方式

- **GitHub**: [@sangshy-go](https://github.com/sangshy-go)
- **Issues**: [提交 Issue](https://github.com/sangshy-go/sangshy-skills/issues)

---

## ⭐ 支持项目

如果你觉得这个仓库有用，请给一个 ⭐ Star！

**Sangshy Skills - 记录和提供有用的 Skill，你不会错过** 🚀

---

*Last Updated: 2026-03-24*
