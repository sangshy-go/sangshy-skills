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
- ORM：GORM 或 sqlx（简单项目优先 sqlx，避免 ORM 黑盒）
- 配置：viper
- 日志：zap 或 zerolog
- 错误处理：`fmt.Errorf("%w")` 包装错误，自定义 error 类型

## API 规范
- RESTful 风格
- 统一错误响应：`{"code": 0, "msg": "success", "data": {}}`
- 优雅关闭：捕获 SIGINT/SIGTERM，完成进行中的请求后退出
- 请求参数校验用结构体 + `binding` tag，失败直接 400
- 分页参数：`page` / `page_size`，响应中包含 `total`

## 命名规范
- 包名：全小写，简短有意义（`user` 而非 `usermanager`）
- 导出标识：PascalCase
- 非导出标识：camelCase
- 接口命名：单方法接口加 `-er` 后缀（`Reader`、`Writer`）
- 错误变量：以 `Err` 开头（`ErrNotFound`）
- 常量：PascalCase 或 UPPER_SNAKE_CASE

## 编码规范
- handler 只做参数解析、调用 service、返回响应，不写业务逻辑
- service 层处理业务，调用 repository 完成数据操作
- 函数超过 50 行应考虑拆分
- context.Context 作为第一个参数传递，用于超时控制和请求取消
- 配置通过 viper 从环境变量/配置文件读取，不硬编码
- 使用 `defer` 及时释放资源（关闭连接、解锁、取消 context）
- 使用 sync.Pool 复用频繁创建/销毁的对象（如 buffer）

## 错误处理
- 错误是值，必须处理或显式传递
- 用 `fmt.Errorf("context: %w", err)` 包装错误，保留原始错误链
- 顶层用 `errors.Is` / `errors.As` 判断具体错误类型
- 未知错误记录详细上下文（请求路径、参数摘要）后返回 500
- 禁止吞掉错误（`_` 忽略错误必须有注释说明）

## 安全规范
- SQL 使用参数化查询（`?` 占位符），禁止字符串拼接
- JWT secret 从环境变量读取，禁止硬编码
- 用户输入做长度和格式校验后再处理
- 敏感信息（密码、Token）禁止记录到日志
- CORS 配置白名单域名，禁止 `*`（生产环境）

## 并发规范
- goroutine 生命周期必须可控（用 context 或 channel 控制退出）
- 共享数据用 `sync.Mutex` / `sync.RWMutex` 保护，或使用 channel 通信
- 禁止在 HTTP handler 中启动不追踪的 goroutine（请求结束后可能继续运行）
- 使用 `errgroup` 管理一组相关 goroutine

## 禁止事项
- 禁止 `panic`（除 init 阶段或不可恢复的启动错误外）
- 禁止忽略 error 返回值
- 禁止全局变量（用依赖注入或 context 传递）
- 禁止裸指针解引用（先判 nil）
- 禁止在 handler 中写业务逻辑
- 禁止在循环内逐个查询数据库（改用批量操作）
- 禁止硬编码配置（走 viper + 环境变量）
- 禁止 `time.Sleep` 做重试/等待（用 `time.Ticker` 或 `context.AfterFunc`）
- 禁止 `_ = json.Unmarshal` 不处理错误

## 单元测试
- 工具：`testing` 标准库 + testify（断言）+ gomock（Mock）
- Service 层：Mock repository 接口，测试业务逻辑
- Handler 层：`httptest` 模拟 HTTP 请求
- 测试文件与源文件同目录：`users.go` → `users_test.go`
- 表驱动测试（table-driven tests）优先
