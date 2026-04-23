# Web (React/Next.js) 实现指南

## 项目结构模板
```
src/
├── app/                # Next.js App Router 路由 + 布局
├── components/         # 通用组件
│   └── ui/             # 基础 UI 组件
├── hooks/              # 自定义 Hooks
├── lib/                # 工具函数、API client
├── types/              # TypeScript 类型定义
└── styles/             # 全局样式
```

## 技术约束
- 使用 TypeScript strict 模式
- 状态管理：优先 React Server Components，需要客户端状态用 zustand
- API 调用：统一走 `lib/api.ts`，使用 fetch + SWR
- 样式：Tailwind CSS，禁止内联 style
- 组件规范：单文件组件，Props 用 interface 定义，导出必须有注释

## 常见模式
- 表单：react-hook-form + zod 校验
- 表格：@tanstack/react-table
- 通知：sonner
- 国际化：next-intl（如需要）

## 禁止事项
- 禁止使用 `any` 类型
- 禁止直接操作 DOM（useRef 除外）
- 禁止在 useEffect 里做数据请求（用 SWR/RSC）
- 禁止在服务端组件中使用 hooks
