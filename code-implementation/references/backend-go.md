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
- Go 1.22+
- 框架：Gin 或 Echo（根据架构文档选择）
- ORM：GORM 或 sqlx（简单项目优先 sqlx）
- 配置：viper
- 日志：zap 或 zerolog
- 错误处理：`fmt.Errorf("%w")` 包装错误

## API 规范
- RESTful 风格，统一错误响应：`{"code": 0, "msg": "success", "data": {}}`
- 优雅关闭：捕获 SIGINT/SIGTERM，完成进行中的请求后退出
- 请求参数用结构体 + `binding` tag 校验
- 分页参数：`page` / `page_size`，响应包含 `total`

## 编码规范
- handler 只做参数解析、调用 service、返回响应
- context.Context 作为第一个参数传递
- 使用 `defer` 及时释放资源（关闭连接、解锁、取消 context）
- 使用 `errgroup` 管理一组相关 goroutine

## 错误处理
- 错误是值，必须处理或显式传递
- 用 `fmt.Errorf("context: %w", err)` 包装错误
- 顶层用 `errors.Is` / `errors.As` 判断具体错误类型
- 未知错误记录详细上下文后返回 500

## 安全规范
- SQL 用参数化查询（`?` 占位符），禁止字符串拼接
- JWT secret 从环境变量读取，禁止硬编码
- CORS 配置白名单域名，生产环境禁止 `*`

## 并发规范
- goroutine 生命周期必须可控（用 context 或 channel 控制退出）
- 禁止在 HTTP handler 中启动不追踪的 goroutine
- 共享数据用 `sync.Mutex` / `sync.RWMutex` 保护

## 禁止事项
- 禁止 `panic`（除 init 阶段或不可恢复的启动错误外）
- 禁止忽略 error 返回值
- 禁止全局变量（用依赖注入或 context 传递）
- 禁止在 handler 中写业务逻辑
- 禁止循环内逐个查询数据库（改用批量操作）
- 禁止硬编码配置（走 viper + 环境变量）
- 禁止 `_ = json.Unmarshal` 不处理错误
- 禁止裸指针解引用（先判 nil）
- 禁止 `time.Sleep` 做重试/等待（用 `time.Ticker`）

## 单元测试
- 工具：`testing` 标准库 + testify + gomock
- 表驱动测试（table-driven tests）优先
- Handler 层用 `httptest` 模拟 HTTP 请求
- 测试文件与源文件同目录：`users.go` → `users_test.go`
