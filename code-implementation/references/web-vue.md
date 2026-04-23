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
- 使用 TypeScript + `<script setup>` 语法
- 状态管理：Pinia
- API 调用：统一走 `lib/api.ts`，使用 `useFetch`（Nuxt 内置）
- 样式：Tailwind CSS 或 UnoCSS
- 组件规范：单文件组件，Props 用 `defineProps` + TypeScript，Emits 用 `defineEmits`

## 常见模式
- 表单：vee-validate + zod 校验
- 表格：v-data-table 或 AG Grid
- 通知：VueUse 的 useToast

## 禁止事项
- 禁止使用 `any` 类型
- 禁止 Options API（统一 Composition API）
- 禁止在模板中使用复杂表达式（提取到 computed）
