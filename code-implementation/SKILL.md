---
name: code-implementation
description: >
  全栈开发 Skill，根据架构方案输出完整可运行代码。
  适用场景：新功能开发、编码实现、功能开发、代码重构、API 开发、
  前端页面开发、数据库脚本、后端接口开发。
  注意：日常修 bug 不需要走完整的研发链路，直接修复即可。
---

# 代码实现 Skill

## 工作流程

### Step 1：读取架构文档
读取 `docs/architecture.md`，理解技术栈、API 接口定义、数据库表结构、模块划分。

### Step 2：判断项目类型，加载实现指南
根据架构文档中的技术栈，读取对应的 reference 文件：
- React/Next.js → `references/web-react.md`
- Vue/Nuxt → `references/web-vue.md`
- Java/Spring Boot → `references/backend-java.md`
- Node.js/Express → `references/backend-node.md`
- Python/FastAPI → `references/backend-python.md`
- Go → `references/backend-go.md`
- Tauri 桌面应用 → `references/tauri.md`
- 微信小程序 → `references/miniprogram.md`
- CLI 工具 → `references/cli.md`

找不到完全匹配的 reference 时，选最接近的作为基础，自行补充差异。

### Step 3：制定任务清单
将功能拆解为可独立实现的任务，按类别分组（基础设施 → 业务模块 → 前端页面）。

**等待用户确认任务清单后，再开始编码。**

### Step 4：按任务逐步实现
- 每次只完成一个任务，完成后标记 [x]
- 每个文件写完后，简要说明实现了什么
- 遇到架构文档中没有明确的细节，先做合理实现，完成后统一列出"未确认项"

### Step 5：自检
对照加载的 reference 中的约束规范自检：命名、注释、异常处理、配置项。

## 约束
- 代码输出到 `src/` 目录（目录结构以架构文档为准）
- 所有配置项通过环境变量注入，提供 `.env.example`
- 严格遵守对应 reference 中的技术约束和编码规范
