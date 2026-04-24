# 后端 (Java/Spring Boot) 实现指南

> 编码规范遵循《阿里巴巴 Java 开发手册》

## 项目结构模板
```
src/main/java/com/example/
├── controller/         # 控制器（仅做参数校验、请求转发）
├── service/            # 业务接口
│   └── impl/           # 业务实现
├── mapper/             # MyBatis Mapper 或 JPA Repository
├── model/              # 数据模型
│   ├── entity/         # 数据库实体（DO）
│   ├── dto/            # 请求/响应数据传输对象
│   └── vo/             # 视图展示对象
├── config/             # 配置类
├── interceptor/        # 拦截器
├── exception/          # 全局异常处理 + 自定义异常
└── util/               # 工具类
src/main/resources/
├── application.yml
└── mapper/             # MyBatis XML（如使用）
```

## 技术约束
- Java 17+，Spring Boot 3.x
- ORM：MyBatis-Plus 或 Spring Data JPA（根据架构文档选择）
- 数据验证：`jakarta.validation` 注解（`@NotNull`、`@Size`、`@Pattern` 等）
- 接口文档：SpringDoc OpenAPI（Swagger）
- 日志：SLF4J + Logback（用 `@Slf4j` 注解）
- 工具库：Hutool 或 Apache Commons Lang3

## 命名规范（阿里规范）
- **DO**（Entity）：数据库实体类，如 `UserDO`
- **DTO**：服务间传输对象，如 `UserDTO`
- **VO**：前端展示对象，如 `UserVO`
- 方法名：`get/query`（查询）、`create/add`（新增）、`update/modify`（更新）、`delete/remove`（删除），动词在前
- 布尔类型变量：不用 `is` 前缀（Jackson 序列化会丢失前缀）
- 常量：全大写 + 下划线，放在常量类中

## API 规范
- RESTful 风格，统一 `/api/v1/` 前缀
- 统一响应体：`Result<T>`（code / message / data），code=0 表示成功
- Controller 层只做参数校验（`@Valid`）、请求转发、响应封装
- 全局异常处理：`@RestControllerAdvice` 捕获异常转为统一响应
- 分页参数：`pageNo`（从 1 开始）、`pageSize`（默认 20，最大 100）
- 所有写操作接口必须做幂等性设计或明确标注非幂等

## 编码规范
- 分层职责：Controller → Service → Mapper，禁止跨层调用
- DO → DTO → VO 逐层转换，禁止 DO 直接返回给前端
- 集合判空用 `CollectionUtils.isEmpty()`，返回空集合而非 null
- 事务标注在 Service 层，`@Transactional(rollbackFor = Exception.class)`
- 同类方法间调用 `@Transactional` 不生效（Spring AOP 代理），需拆分到不同类
- 只读查询用 `@Transactional(readOnly = true)` 优化
- 配置通过 `@ConfigurationProperties` 绑定，敏感配置走环境变量
- 日志级别：ERROR（系统异常）、WARN（业务异常）、INFO（关键操作）、DEBUG（调试）
- 关键操作（支付、删除、状态变更）必须记录 INFO 日志
- 批量操作优先：用 `IN` 查询代替循环单次查询

## 错误处理
- 自定义业务异常（`BusinessException`），携带错误码和消息，错误码用枚举管理
- `@RestControllerAdvice` 区分业务异常、参数校验异常、兜底异常
- 禁止 catch 后吞掉异常（至少 `log.error("上下文", e)`）
- 能用返回值表示错误的不用异常（如查询不到返回 null）
- 禁止在 finally 中 return 或 throw

## 安全规范
- 密码用 BCrypt 加密，禁止明文或 MD5
- SQL 用 MyBatis `#{}` 参数化查询，禁止 `${}` 拼接（SQL 注入风险）
- 接口鉴权用拦截器或 `@PreAuthorize`，操作数据前校验权限（防越权）
- 敏感日志禁止输出密码、Token、身份证号
- 文件上传限制大小和类型，不信任客户端传来的任何数据

## 禁止事项
- 禁止在 Controller 中写业务逻辑
- 禁止 `System.out.println`（用 Logger）
- 禁止魔法值（硬编码字符串/数字，提取为常量或枚举）
- 禁止使用 `==` 比较包装类型（如 `Integer`），用 `.equals()`
- 禁止大事务（事务粒度尽量小）
- 禁止循环内调用数据库（改用批量查询或 `IN` 查询）
- 禁止返回 `null` 集合（返回 `Collections.emptyList()`）
- 禁止 `@Transactional` 同类方法间调用（Spring AOP 代理失效）
- 禁止使用 `SimpleDateFormat`（线程不安全，用 `DateTimeFormatter`）
- 禁止 `new Date()` 不带时区（用 `LocalDateTime` / `Instant`）
- 禁止 DO 直接暴露给前端（必须转 DTO/VO）
- 禁止 catch 后什么都不做（空 catch 块）
- 禁止使用 `Executors` 创建线程池（用 `ThreadPoolExecutor` 显式指定参数）
- 禁止 `new Thread()` 直接创建（用线程池或 `@Async`）

## 单元测试
- 工具：JUnit 5 + Mockito
- Service 层：Mock repository，测试业务逻辑
- Controller 层：MockMvc 或 `@WebMvcTest` 测试接口
- 测试命名：`方法名_场景_期望结果`（如 `create_UserAlreadyExists_ThrowsException`）
- 每个测试用例独立准备数据，不依赖执行顺序
