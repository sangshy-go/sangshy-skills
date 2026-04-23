# 后端 (Java/Spring Boot) 实现指南

## 项目结构模板
```
src/main/java/com/example/
├── controller/         # 控制器
├── service/            # 业务逻辑层
│   └── impl/
├── mapper/             # MyBatis Mapper 或 JPA Repository
├── entity/             # 实体类
├── dto/                # 数据传输对象
├── config/             # 配置类
├── interceptor/        # 拦截器
├── exception/          # 全局异常处理
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

## API 规范
- RESTful 风格，统一 `/api/v1/` 前缀
- 统一响应体：`Result<T>`（code / message / data）
- 全局异常处理：`@RestControllerAdvice`
- 分页：PageHelper 或 Spring Data Page

## 禁止事项
- 禁止在 Controller 中写业务逻辑
- 禁止 `System.out.println`（用 Logger）
- 禁止大事务（事务粒度尽量小）
- 禁止循环调用数据库（批量查询）

## 单元测试
- 工具：JUnit 5 + Mockito
- Service 层：Mock repository，测试业务逻辑
- Controller 层：MockMvc 或 `@WebMvcTest` 测试接口
- 测试命名：`should_期望行为_when_条件`
