# 后端 (Java/Spring Boot) 实现指南

> 编码规范严格遵循《阿里巴巴 Java 开发手册》泰山版 + 业界资深专家最佳实践

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
│   ├── BusinessException.java
│   └── GlobalExceptionHandler.java
├── constant/           # 常量定义
└── util/               # 工具类
src/main/resources/
├── application.yml
├── application-dev.yml
├── application-prod.yml
└── mapper/             # MyBatis XML（如使用）
```

## 技术约束
- Java 17+，Spring Boot 3.x
- ORM：MyBatis-Plus 或 Spring Data JPA（根据架构文档选择）
- 数据验证：`jakarta.validation` 注解（`@NotNull`、`@Size`、`@Pattern` 等）
- 接口文档：SpringDoc OpenAPI（Swagger）
- 日志：SLF4J + Logback
- 工具库：Hutool 或 Apache Commons Lang3
- JSON：Jackson（Spring Boot 默认）

## 命名规范（阿里规范）

### 分层命名
- **DO**（Data Object）：数据库实体类，与表结构一一对应，如 `UserDO`
- **DTO**（Data Transfer Object）：服务间传输对象，如 `UserDTO`
- **VO**（View Object）：前端展示对象，如 `UserVO`
- **Query**：查询条件对象，如 `UserQuery`

### 方法命名
- 获取单个：`getById`、`getByUsername`
- 获取列表：`listAll`、`listByStatus`
- 查询（带条件）：`queryByName`、`queryByPage`
- 新增：`create`、`add`
- 更新：`update`、`modify`
- 删除：`delete`、`removeById`
- 统计：`count`、`countByStatus`
- 判断：`exists`、`checkPermission`

### 其他规范
- 布尔类型变量：不用 `is` 前缀（如 `success` 而非 `isSuccess`，Jackson 序列化会丢失前缀）
- 常量：全大写 + 下划线，放在常量类中（如 `UserConstant.DEFAULT_STATUS`）
- 抽象类：以 `Abstract` 或 `Base` 开头
- 异常类：以 `Exception` 结尾
- 测试类：以被测试类名 + `Test` 结尾

## API 规范

### 统一响应体
```java
@Data
public class Result<T> {
    private Integer code;    // 0=成功, 其他=错误码
    private String message;
    private T data;

    public static <T> Result<T> success(T data) { ... }
    public static <T> Result<T> fail(Integer code, String message) { ... }
}
```

### 接口设计
- RESTful 风格，统一 `/api/v1/` 前缀
- GET：查询（幂等），POST：新增，PUT：全量更新，PATCH：部分更新，DELETE：删除
- 接口参数校验用 `@Valid` / `@Validated`，校验失败返回 400
- 分页参数：`pageNo`（从 1 开始）、`pageSize`（默认 20，最大 100）
- 分页响应：`PageResult<T>`（total、list、pageNo、pageSize）
- 所有写操作接口必须做幂等性设计或明确标注非幂等

### Controller 示例
```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @GetMapping("/{id}")
    public Result<UserVO> getById(@PathVariable Long id) {
        return Result.success(userService.getById(id));
    }

    @PostMapping
    public Result<Long> create(@Valid @RequestBody UserCreateDTO dto) {
        return Result.success(userService.create(dto));
    }

    @PutMapping("/{id}")
    public Result<Void> update(@PathVariable Long id, @Valid @RequestBody UserUpdateDTO dto) {
        userService.update(id, dto);
        return Result.success(null);
    }

    @DeleteMapping("/{id}")
    public Result<Void> delete(@PathVariable Long id) {
        userService.deleteById(id);
        return Result.success(null);
    }
}
```

## 编码规范

### 分层职责
- **Controller**：只处理参数校验、请求转发、响应封装，不写业务逻辑
- **Service**：核心业务逻辑，事务管理，调用 Mapper/Repository
- **Mapper/Repository**：数据访问，只负责 SQL 或 JPA 查询
- 禁止跨层调用（Controller 不能直接调 Mapper）

### 对象转换
- DO ↔ DTO ↔ VO 逐层转换，禁止 DO 直接返回给前端
- 转换使用 `BeanUtils.copyProperties`（Hutool / Spring）或 MapStruct
- 字段名不一致时用 MapStruct 的 `@Mapping` 显式映射
- 嵌套对象（如 User 的 Role 列表）转换要处理空值

### 集合处理
- 集合判空用 `CollectionUtils.isEmpty()` 或 `CollUtil.isEmpty()`
- 禁止返回 `null` 集合，返回 `Collections.emptyList()` 或 `new ArrayList<>()`
- 批量操作优先：用 `IN` 查询代替循环单次查询
- 集合转 Map 用 `Collectors.toMap()`，注意处理 key 冲突

### 日志规范
- 使用 `@Slf4j` 注解，禁止手动创建 Logger
- 日志级别：ERROR（系统异常）、WARN（业务异常、降级）、INFO（关键操作）、DEBUG（调试）
- 日志格式：`log.error("操作失败, userId={}, reason={}", userId, e.getMessage(), e)`
- 禁止日志输出密码、Token、身份证号等敏感信息
- 关键操作（支付、删除、状态变更）必须记录 INFO 日志

### 事务管理
- 事务标注在 Service 层，不在 Controller 或 Mapper 层
- `@Transactional(rollbackFor = Exception.class)` 确保所有异常都回滚
- 事务粒度尽量小，避免长事务占用连接
- 同类方法间调用 `@Transactional` 不生效（Spring AOP 代理限制），需用 `AopContext.currentProxy()` 或拆到不同类
- 只读查询用 `@Transactional(readOnly = true)` 优化性能

### 配置管理
- 配置类统一放在 `config/` 包，用 `@Configuration` + `@ConfigurationProperties`
- 敏感配置（数据库密码、API Key）走环境变量或配置中心
- 不同环境用 `application-{profile}.yml`，启动时指定 `--spring.profiles.active=prod`

## 错误处理

### 自定义异常
```java
@Getter
public class BusinessException extends RuntimeException {
    private final Integer code;

    public BusinessException(Integer code, String message) {
        super(message);
        this.code = code;
    }
}

// 错误码枚举
@Getter
@AllArgsConstructor
public enum ErrorCode {
    USER_NOT_FOUND(10001, "用户不存在"),
    PERMISSION_DENIED(10002, "无权限操作"),
    PARAM_INVALID(40001, "参数校验失败");

    private final Integer code;
    private final String message;
}
```

### 全局异常处理
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public Result<Void> handleBusinessException(BusinessException e) {
        log.warn("业务异常: code={}, msg={}", e.getCode(), e.getMessage());
        return Result.fail(e.getCode(), e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public Result<Void> handleValidationException(MethodArgumentNotValidException e) {
        String msg = e.getBindingResult().getFieldErrors().stream()
            .map(f -> f.getField() + ": " + f.getDefaultMessage())
            .collect(Collectors.joining(", "));
        return Result.fail(ErrorCode.PARAM_INVALID.getCode(), msg);
    }

    @ExceptionHandler(Exception.class)
    public Result<Void> handleException(Exception e) {
        log.error("系统异常", e);
        return Result.fail(500, "系统内部异常");
    }
}
```

### 异常处理原则
- 禁止 catch 后吞掉异常（至少 `log.error("上下文信息", e)`）
- 能用返回值表示错误的不用异常（如查询不到返回 null，而非抛异常）
- 第三方服务调用异常要包装为自定义异常，记录原始错误信息
- 不要在 finally 中 return 或 throw（会覆盖原始异常）

## 安全规范

### 数据安全
- 密码用 BCrypt 加密（`BCryptPasswordEncoder`），禁止明文或 MD5
- 手机号、身份证号等敏感数据入库前加密，展示时脱敏
- Token 设置合理的过期时间（Access Token 2h，Refresh Token 7d）

### SQL 安全
- MyBatis 用 `#{}` 参数化查询，禁止 `${}` 拼接（`${}` 有 SQL 注入风险）
- 动态排序字段用白名单校验，不直接拼接用户输入
- `LIKE` 查询用 `CONCAT('%', #{keyword}, '%')` 而非字符串拼接

### 接口安全
- 接口鉴权用拦截器或 `@PreAuthorize`，不依赖客户端传参判断权限
- 越权检查：操作数据前校验当前用户是否有权限操作该资源
- 接口限流：关键接口（登录、短信验证码）用 Redis 做频率限制
- XSS 防护：输出到前端的字符串做 HTML 转义（使用 `HtmlUtils.htmlEscape`）

### 请求安全
- 文件上传限制大小（`spring.servlet.multipart.max-file-size`）和类型
- 不信任客户端传来的任何数据，服务端二次校验
- 敏感操作（支付、删除）加签名或二次确认

## 禁止事项

### 代码质量
- 禁止在 Controller 中写业务逻辑
- 禁止 `System.out.println`（用 Logger）
- 禁止魔法值（硬编码字符串/数字，提取为常量或枚举）
- 禁止使用 `==` 比较包装类型（如 `Integer`），用 `.equals()`
- 禁止使用 `any` 类型注解

### 数据库
- 禁止大事务（事务粒度尽量小）
- 禁止循环内调用数据库（改用批量查询或 `IN` 查询）
- 禁止返回 `null` 集合（返回 `Collections.emptyList()`）
- 禁止 `@Transactional` 同类方法间调用（Spring AOP 代理失效）
- 禁止在循环中创建数据库连接或 HTTP 请求
- 禁止使用 `SimpleDateFormat`（线程不安全，用 `DateTimeFormatter`）
- 禁止 `new Date()` 不带时区（用 `LocalDateTime` / `Instant`）
- 禁止 DO 直接暴露给前端（必须转 DTO/VO）

### 异常与日志
- 禁止 catch 后什么都不做（空 catch 块）
- 禁止用 `e.printStackTrace()`（用 log.error）
- 禁止在 finally 中 return 或 throw
- 禁止日志输出密码、Token、身份证号等敏感信息

### 并发与性能
- 禁止在 HTTP 请求线程中做耗时操作（用异步或消息队列）
- 禁止使用 `Executors` 创建线程池（用 `ThreadPoolExecutor` 显式指定参数）
- 禁止无界队列（`LinkedBlockingQueue` 指定容量）
- 禁止 `new Thread()` 直接创建（用线程池或 `@Async`）

## 单元测试

### 测试工具
- JUnit 5 + Mockito
- Service 层：Mock repository，测试业务逻辑
- Controller 层：MockMvc 或 `@WebMvcTest` 测试接口

### 测试命名
```
方法名_场景_期望结果
例如：create_UserAlreadyExists_ThrowsException
     getById_ValidId_ReturnsUser
     delete_UserNotFound_DoesNothing
```

### 测试规范
- 使用 `@MockBean` Mock 外部依赖
- 使用 `@SpringBootTest` 做集成测试时，用 H2 内存数据库
- 每个测试用例独立准备数据（`@BeforeEach`），不依赖执行顺序
- 测试覆盖率目标：Service 层 > 80%，Controller 层 > 60%
- 使用 AssertJ 做流式断言（`assertThat(result).isNotNull().hasField("id")`）
