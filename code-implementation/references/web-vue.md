# Web (Vue/Nuxt) 实现指南

## 项目结构模板
```
src/
├── pages/              # Nuxt 页面路由
├── components/         # 通用组件
│   └── ui/             # 基础 UI 组件
├── composables/        # 组合式函数
├── stores/             # Pinia 状态管理
├── lib/                # 工具函数、API client
├── types/              # TypeScript 类型定义
└── assets/             # 静态资源、样式
```

## 技术约束
- TypeScript + `<script setup>` 语法
- 状态管理：Pinia
- API 调用：统一走 `lib/api.ts`，使用 `useFetch`（Nuxt 内置）
- 样式：Tailwind CSS 或 UnoCSS
- 组件规范：单文件组件，Props 用 `defineProps` + TypeScript，Emits 用 `defineEmits`

## API 规范
- Server-side 数据获取优先（Nuxt `useFetch` / `useAsyncData`）
- 客户端表单提交统一走 `lib/api.ts`，不直接发请求
- API 响应统一格式，错误用 `useCatch` 或 try/catch 处理
- 敏感操作必须做服务端鉴权

## 命名规范
- 组件文件：PascalCase（`UserProfile.vue`）
- Composables：camelCase 且以 `use` 开头（`useAuth.ts`）
- Stores：camelCase（`useUserStore.ts`）
- 工具函数：camelCase，纯函数优先

## 编码规范
- 组件模板表达式只放简单逻辑，复杂逻辑提取到 computed
- 组件超过 200 行应拆分，逻辑提取到 composables
- v-for 必须带 key（用唯一 ID，禁止用 index）
- 使用 Nuxt `<NuxtImg>` 组件做图片优化
- 公共组件放 `components/`，页面级组件放 `pages/` 路由内
- Pinia store 中 action 处理异步，state 只存数据

## 错误处理
- 使用 `error.vue` 全局错误页
- 使用 `useCatch` 捕获 Nuxt 数据请求错误
- 表单提交必须有 loading 状态和错误提示
- 网络错误要有用户友好的重试提示

## 禁止事项
- 禁止使用 `any` 类型
- 禁止 Options API（统一 Composition API）
- 禁止在模板中使用复杂表达式（提取到 computed）
- 禁止在 v-for 中使用 index 作为 key
- 禁止组件内直接发 API 请求（统一走 `lib/api`）
- 禁止在 setup 顶层使用 await（用 `useAsyncData` 包装）
- 禁止把业务逻辑写在组件里（提取到 composables）
- 禁止直接修改 Pinia store 的 state（通过 action 修改）

## 单元测试
- 工具：Vitest + Vue Testing Library
- 测试文件放在 `__tests__/` 目录或与源文件同目录
- 测试组件渲染、用户交互、computed 逻辑
- Mock 外部依赖（API 调用、路由、Pinia store）
