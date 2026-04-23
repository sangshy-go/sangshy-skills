# Web 前端 E2E 测试指南

## 测试工具组合
| 测试类型 | 工具 |
|---------|------|
| 单元测试 | Jest / Vitest（与项目框架一致） |
| 组件测试 | Testing Library |
| E2E/UI 测试 | Playwright MCP 或 Playwright |

## 单元测试规范
- 测试文件与源文件同目录：`button.tsx` → `button.test.tsx`
- 命名：`describe('ComponentName')` + `it('should 行为描述')`
- 只测公共 API，不测实现细节
- Mock 外部依赖（API 调用、路由）

## E2E 测试流程（Playwright）
1. `mkdir -p docs/test-screenshots` 创建截图目录
2. 每步操作后截图，保存到 `docs/test-screenshots/TC-编号-step[n].png`
3. 浏览器自动化操作：导航、填写、点击、断言
4. 实际结果与期望不符时，记录差异并截图

## 常见 E2E 测试场景
- 表单提交（正常流程 + 校验错误）
- 登录/登出流程
- 页面导航和路由
- 列表分页/筛选
- 错误页面和空状态
