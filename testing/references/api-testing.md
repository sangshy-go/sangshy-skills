# API 接口测试指南

## 测试工具组合
| 语言 | 单元测试 | 集成测试 | HTTP 客户端 |
|------|---------|---------|-----------|
| Java | JUnit 5 + Mockito | Spring Boot Test | MockMvc / RestAssured |
| Node.js | Jest / Vitest | Supertest | node-fetch |
| Python | pytest | httpx / TestClient | httpx |
| Go | testing + testify | httptest | net/http |

## 接口测试规范
- 每个接口至少测试：成功响应、参数校验失败、鉴权失败
- 边界值：空列表、超长字符串、非法字符
- 幂等性：重复请求结果一致（POST 除外）

## 测试数据
- 每个测试用例独立准备数据（不依赖其他用例的副作用）
- 测试后清理数据（`@AfterEach` / `teardown`）
- 使用工厂函数生成测试数据

## 常见接口测试场景
- CRUD 完整流程（创建 → 查询 → 更新 → 删除）
- 分页参数边界（page=0、page 超出范围、pageSize 极大）
- 并发安全（同时更新同一条记录）
- 鉴权 Token 过期/无效
