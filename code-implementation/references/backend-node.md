# 后端 (Node.js/Express) 实现指南

## 项目结构模板
```
src/
├── routes/             # 路由定义
├── controllers/        # 控制器（路由处理函数）
├── services/           # 业务逻辑层
├── models/             # 数据模型
├── middleware/         # 中间件（鉴权、日志、错误处理）
├── utils/              # 工具函数
├── config/             # 配置管理
└── index.ts            # 入口文件
```

## 技术约束
- TypeScript strict 模式
- 框架：Express 或 Fastify（根据架构文档选择）
- ORM：Prisma 或 Drizzle（根据架构文档选择）
- 数据验证：zod（request body / query / params 校验）
- 错误处理：统一错误中间件，返回标准 JSON 错误格式
- 日志：pino

## API 规范
- RESTful 路由命名：`GET /api/v1/users`、`POST /api/v1/users`
- 响应格式统一：
  ```json
  { "code": 0, "data": {}, "message": "success" }
  { "code": 40001, "error": "描述", "message": "参数错误" }
  ```
- 鉴权：JWT，通过 Authorization header 传递
- 分页：`?page=1&pageSize=20`，响应中包含 total

## 禁止事项
- 禁止在 controller 中直接写业务逻辑（放 service 层）
- 禁止硬编码配置（走 config/ + 环境变量）
- 禁止吞掉错误（catch 后必须处理或上报）

## 单元测试
- 工具：Jest 或 Vitest + Supertest
- Service 层：Mock 外部依赖和数据库
- 接口层：Supertest 模拟 HTTP 请求，测试完整请求链路
- 测试文件与源文件同目录：`users.ts` → `users.test.ts`
