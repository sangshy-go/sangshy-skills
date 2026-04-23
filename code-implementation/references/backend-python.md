# 后端 (Python/FastAPI) 实现指南

## 项目结构模板
```
src/
├── main.py             # 入口
├── routers/            # 路由模块
├── services/           # 业务逻辑层
├── models/             # 数据模型（SQLAlchemy / Pydantic）
├── schemas/            # 请求/响应 Schema
├── middleware/         # 中间件
├── config.py           # 配置管理（pydantic-settings）
└── utils/              # 工具函数
```

## 技术约束
- Python 3.11+，类型注解全覆盖
- 框架：FastAPI
- ORM：SQLAlchemy 2.0（async）或 Tortoise ORM
- 数据验证：Pydantic v2
- 异步：优先 async/await
- 任务队列：Celery（如需要）

## API 规范
- RESTful 风格
- 自动文档：FastAPI 自带 Swagger UI（`/docs`）
- 响应模型用 Pydantic 定义

## 禁止事项
- 禁止 `any` 类型注解
- 禁止同步 IO 阻塞事件循环
- 禁止在路由中写业务逻辑

## 单元测试
- 工具：pytest + httpx TestClient（FastAPI 集成测试）
- Service 层：Mock 数据库和外部服务
- 接口层：`TestClient` 模拟 HTTP 请求
- 测试文件放在 `tests/` 目录
