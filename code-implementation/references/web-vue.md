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

## API 规范
- Server-side 数据获取优先（Nuxt `useFetch` / `useAsyncData`）
- 客户端表单提交统一走 `lib/api.ts`
- 敏感操作必须做服务端鉴权

## 编码规范
- 模板表达式只放简单逻辑，复杂逻辑提取到 computed
- 组件超过 200 行应拆分，逻辑提取到 composables
- v-for 必须带 key（用唯一 ID，禁止用 index）
- Pinia store 中 action 处理异步，state 只存数据

## 错误处理
- 使用 `error.vue` 全局错误页
- 表单提交必须有 loading 状态和错误提示
- 网络错误要有用户友好的重试提示

## 禁止事项
- 禁止 `any` 类型
- 禁止 Options API（统一 Composition API）
- 禁止在模板中使用复杂表达式（提取到 computed）
- 禁止 v-for 使用 index 作为 key
- 禁止组件内直接发 API 请求（统一走 `lib/api`）
- 禁止在 setup 顶层使用 await（用 `useAsyncData` 包装）
- 禁止直接修改 Pinia store 的 state（通过 action 修改）

## 单元测试
- 工具：Vitest + Vue Testing Library
- 测试组件渲染、用户交互、computed 逻辑
- Mock 外部依赖（API、路由、Pinia）
