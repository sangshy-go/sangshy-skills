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
- Python 3.12+，类型注解全覆盖
- 框架：FastAPI
- ORM：SQLAlchemy 2.0（async）或 Tortoise ORM
- 数据验证：Pydantic v2
- 异步：优先 async/await

## API 规范
- RESTful 风格，自动文档：FastAPI 自带 Swagger（`/docs`）
- 响应模型用 Pydantic 定义，`response_model` 声明返回类型
- 路由加 `tags` 分类，加 `summary` 描述
- 分页用 `skip` / `limit` 参数

## 编码规范
- Router 只做参数接收、调用 service、返回响应
- 所有函数必须有类型注解
- 数据库连接用依赖注入（`get_db`），不全局共享
- 配置用 `pydantic-settings`，从 `.env` 读取

## 错误处理
- 用 `HTTPException(status_code, detail)` 返回 HTTP 错误
- 全局异常处理器捕获未预期异常
- 数据库事务用 `async with session.begin()`，异常自动回滚
- 外部服务调用失败要有超时时间和重试逻辑

## 安全规范
- 密码用 `passlib[bcrypt]` 哈希，禁止明文
- 使用 `python-jose` 生成和验证 JWT
- 敏感配置从环境变量读取
- SQL 用 SQLAlchemy ORM，禁止原始 SQL 拼接

## 禁止事项
- 禁止 `any` 类型注解（不知道类型用 `typing.Any` + 注释说明）
- 禁止同步 IO 阻塞事件循环（用 `aiohttp`、`asyncpg` 等）
- 禁止在路由中写业务逻辑
- 禁止裸 `except`（必须指定异常类型）
- 禁止 `print` 调试代码（用 logger）
- 禁止循环内逐个执行数据库操作（用批量）
- 禁止 `import *`（明确导入具体名称）

## 单元测试
- 工具：pytest + httpx TestClient
- Service 层：Mock 数据库和外部服务
- 测试文件放在 `tests/` 目录，镜像源码结构
- 使用 pytest fixtures 准备测试数据
