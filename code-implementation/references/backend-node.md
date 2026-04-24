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
- 日志：pino

## API 规范
- RESTful 路由：`GET /api/v1/users`、`POST /api/v1/users`
- 响应格式：`{ "code": 0, "data": {}, "message": "success" }`
- 鉴权：JWT，通过 Authorization header 传递
- 分页：`?page=1&pageSize=20`，响应包含 total
- 所有路由必须做参数校验（zod schema）

## 编码规范
- Controller 只做参数解析、调用 service、返回响应
- 异步函数用 async/await，禁止 callback 和 `.then()` 链
- 数据库操作封装在 Model/Repository 层
- zod 做运行时校验，类型推导自动生成 TypeScript 类型

## 错误处理
- 自定义错误类（`AppError`）携带错误码和 HTTP 状态码
- 全局错误中间件统一捕获，未预期错误返回 500
- Promise rejection 必须 catch，禁止 unhandledRejection
- 错误日志记录请求路径、方法、错误堆栈，不记录敏感参数

## 安全规范
- 使用 `helmet` 设置安全响应头，`cors` 配置白名单
- 使用 `express-rate-limit` 做接口限流
- 密码用 `bcrypt` 哈希，禁止明文
- 参数化查询防 SQL 注入（Prisma/Drizzle 自带）
- JWT secret 从环境变量读取，设置合理的 `expiresIn`

## 禁止事项
- 禁止 controller 中写业务逻辑（放 service 层）
- 禁止硬编码配置（走 config/ + 环境变量）
- 禁止吞掉错误（catch 后必须处理或上报）
- 禁止 `any` 类型（不知道类型用 `unknown`）
- 禁止同步阻塞操作（如 `fs.readFileSync`）
- 禁止未鉴权的写操作接口
- 禁止 `.then().catch()` 和 async/await 混用
- 禁止未处理的 Promise rejection

## 单元测试
- 工具：Jest 或 Vitest + Supertest
- Service 层：Mock 外部依赖和数据库
- 接口层：Supertest 模拟 HTTP 请求
- 测试文件与源文件同目录
