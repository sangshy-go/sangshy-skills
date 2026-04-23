# 后端 (Go) 实现指南

## 项目结构模板
```
cmd/
└── server/
    └── main.go         # 入口
internal/
├── handler/            # HTTP handler
├── service/            # 业务逻辑
├── repository/         # 数据访问层
├── model/              # 数据模型
├── middleware/         # 中间件
└── config/             # 配置
pkg/                    # 可复用的公共包
```

## 技术约束
- Go 1.21+
- 框架：Gin 或 Echo（根据架构文档选择）
- ORM：GORM 或 sqlx
- 配置：viper
- 日志：zap 或 zerolog
- 错误处理：自定义 error 类型 + pkg/errors

## API 规范
- RESTful 风格
- 统一错误响应：`{"code": 0, "msg": "success", "data": {}}`
- 优雅关闭：捕获 SIGINT/SIGTERM

## 禁止事项
- 禁止 `panic`（除 init 阶段外）
- 禁止忽略 error 返回值
- 禁止全局变量（用依赖注入）

## 单元测试
- 工具：`testing` 标准库 + testify（断言）+ gomock（Mock）
- Service 层：Mock repository 接口，测试业务逻辑
- Handler 层：`httptest` 模拟 HTTP 请求
- 测试文件与源文件同目录：`users.go` → `users_test.go`
