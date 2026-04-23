---
name: testing
description: >
  测试验证 Skill，基于需求文档和代码设计测试用例，并执行自动化测试。
  适用场景：测试用例设计、接口测试、UI 自动化测试、回归测试、性能测试用例、边界值测试、跑测试。
---

# 测试验证 Skill

## 工作流程

### Step 1：读取测试输入
- `docs/prd.md`：功能需求和验收标准
- `docs/architecture.md`：接口定义
- `docs/review-report.md`：已知问题和修复情况
- `src/`：实现逻辑

### Step 2：判断项目类型，加载测试策略
根据架构文档中的技术栈，读取对应的 reference：
- Web 前端项目 → `references/web-e2e.md`
- 纯后端 API 项目 → `references/api-testing.md`

无匹配测试策略时，自行设计合理的测试方案并说明执行方式（如 CLI 用 `go test`/`pytest`，小程序用微信开发者工具内置测试等）。

无前端页面的项目跳过 UI 自动化测试。

### Step 3：设计测试用例
设计全面的测试用例（功能 / 边界 / 安全 / 性能），等用户确认后再执行。

用例格式：
| 用例编号 | 测试类型 | 前置条件 | 测试步骤 | 期望结果 | 执行方式 |

将用例设计保存到 `docs/test-case-design.md`。

### Step 4：执行测试
按 reference 中的工具和流程执行测试，记录结果。

### Step 5：输出测试报告

```markdown
# 测试报告
- 测试时间：YYYY-MM-DD HH:mm
- 总结：共执行 XX 个用例，通过 XX，失败 XX，阻塞 XX

## 测试结果汇总
| 用例编号 | 测试类型 | 测试内容 | 期望 | 实际 | 状态 | 截图 |

## 失败用例详情
### TC-XXX：[用例名称]
- 期望结果：...
- 实际结果：...
- 复现步骤：...
- 初步分析：...

## 覆盖率统计
- 功能测试覆盖率：XX/XX 个功能点
- 接口覆盖率：XX/XX 个接口
```

## 约束
- 产出保存到 `docs/test-report.md`
- 截图保存到 `docs/test-screenshots/`（仅 Web/App 项目，按需创建）
- 不要只测"能跑通"，要找 bug——假设代码有 bug，你的任务是找出来
