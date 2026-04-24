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
- 数据验证：`jakarta.validation` 注解（`@NotNull`、`@Size` 等）
- 接口文档：SpringDoc OpenAPI（Swagger）
- 日志：SLF4J + Logback
- 工具库：Hutool 或 Apache Commons Lang3

## API 规范
- RESTful 风格，统一 `/api/v1/` 前缀
- 统一响应体：`Result<T>`（code / message / data）
- 全局异常处理：`@RestControllerAdvice`
- 分页：PageHelper 或 Spring Data Page
- 接口参数校验用 `@Valid` / `@Validated`，校验失败返回 400
- 所有写操作接口必须做幂等性设计或明确标注非幂等

## 命名规范（阿里规范）
- **DO**（Entity）：数据库实体类，如 `UserDO`
- **DTO**：服务间传输对象，如 `UserDTO`
- **VO**：前端展示对象，如 `UserVO`
- 方法名：`get/query`（查询）、`create/add`（新增）、`update/modify`（更新）、`delete/remove`（删除），动词在前
- 布尔类型变量：不用 `is` 前缀（Jackson 序列化会丢失前缀）
- 常量：全大写 + 下划线，放在常量类中

## 编码规范
- Controller 只处理参数校验和请求转发，业务逻辑放 Service
- Service 接口定义行为，impl 实现（方便多实现和 Mock）
- DO → DTO → VO 逐层转换，禁止 DO 直接返回给前端
- 工具类用 `final` + 私有构造函数，防止实例化
- 集合判空用 `CollectionUtils.isEmpty()`，不手动 `== null || .isEmpty()`
- 配置类统一放在 `config/` 包，用 `@ConfigurationProperties` 绑定
- 日志使用 `@Slf4j` 注解，禁止手动创建 Logger

## 错误处理
- 自定义业务异常（`BusinessException`），携带错误码和消息
- 全局异常处理 `@RestControllerAdvice` 捕获并转为统一响应格式
- 禁止 catch 后吞掉异常（至少 log.error）
- 事务回滚只针对 RuntimeException，checked exception 需配置 `rollbackFor`

## 安全规范
- 密码等敏感字段禁止明文存储，使用 BCrypt 加密
- SQL 使用参数化查询（MyBatis `#{}`），禁止 `${}` 拼接
- 接口鉴权用拦截器或 `@PreAuthorize`，不依赖客户端传参
- 敏感日志（密码、Token、身份证号）禁止输出到日志
- XSS 防护：输出到前端的字符串做 HTML 转义

## 禁止事项
- 禁止在 Controller 中写业务逻辑
- 禁止 `System.out.println`（用 Logger）
- 禁止大事务（事务粒度尽量小）
- 禁止循环内调用数据库（改用批量查询）
- 禁止魔法值（硬编码字符串/数字，提取为常量或枚举）
- 禁止使用 `==` 比较包装类型（如 `Integer`）
- 禁止返回 `null` 集合（返回 `Collections.emptyList()`）
- 禁止 `@Transactional` 注解在同类方法间调用（Spring AOP 代理失效）
- 禁止在循环中创建数据库连接或 HTTP 请求
- 禁止使用 `SimpleDateFormat`（线程不安全，用 `DateTimeFormatter`）
- 禁止 `new Date()` 不带时区（用 `LocalDateTime` / `Instant`）
- 禁止 DO 直接暴露给前端（必须转 DTO/VO）

## 单元测试
- 工具：JUnit 5 + Mockito
- Service 层：Mock repository，测试业务逻辑
- Controller 层：MockMvc 或 `@WebMvcTest` 测试接口
- 测试命名：`should_期望行为_when_条件`
- 每个测试用例独立准备数据，不依赖执行顺序
