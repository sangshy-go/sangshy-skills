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

## 命名规范（阿里规范）
- **DO**（Entity）：数据库实体类，如 `UserDO`
- **DTO**：服务间传输对象，如 `UserDTO`
- **VO**：前端展示对象，如 `UserVO`
- 方法名：`get/put/delete/query/update/create` 开头，动词在前
- 布尔类型变量：不用 `is` 前缀（序列化会丢失前缀）

## 禁止事项
- 禁止在 Controller 中写业务逻辑
- 禁止 `System.out.println`（用 Logger）
- 禁止大事务（事务粒度尽量小）
- 禁止循环调用数据库（批量查询）
- 禁止魔法值（硬编码字符串/数字，提取为常量或枚举）
- 禁止使用 `==` 比较包装类型（如 `Integer`）
- 禁止返回 `null` 集合（返回空集合 `Collections.emptyList()`）

## 单元测试
- 工具：JUnit 5 + Mockito
- Service 层：Mock repository，测试业务逻辑
- Controller 层：MockMvc 或 `@WebMvcTest` 测试接口
- 测试命名：`should_期望行为_when_条件`
