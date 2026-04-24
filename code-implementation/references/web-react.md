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
- TypeScript strict 模式
- 状态管理：优先 React Server Components，客户端状态用 zustand
- API 调用：统一走 `lib/api.ts`，使用 fetch + SWR
- 样式：Tailwind CSS，避免内联 style（动态颜色/尺寸除外）
- 组件规范：Props 用 interface 定义

## API 规范
- Server Component 优先，仅需要交互的组件标注 `"use client"`
- 数据获取优先在服务端完成，避免客户端 useEffect 拉取
- 敏感操作（删除、支付）必须做服务端鉴权

## 编码规范
- 组件逻辑超过 150 行应拆分为子组件或抽离为 hook
- 表单统一用 react-hook-form + zod
- 列表数据必须有 key（用唯一 ID，禁止用 index）
- 公共组件放在 `components/`，页面级组件放在 `app/` 路由内

## 错误处理
- 使用 `error.tsx` 边界组件捕获路由级错误
- `not-found.tsx` 处理 404
- 异步操作必须有 loading 状态和错误提示

## 禁止事项
- 禁止 `any` 类型（不知道类型用 `unknown`）
- 禁止直接操作 DOM（useRef 除外）
- 禁止在 useEffect 里做数据请求（用 SWR/RSC）
- 禁止在服务端组件中使用 hooks
- 禁止 `useEffect` 空依赖做一次性初始化（用懒初始化）
- 禁止循环中使用 index 作为 key
- 禁止组件内部直接调 API（统一走 `lib/api` 层）

## 单元测试
- 工具：Vitest + Testing Library
- 测试文件与源文件同目录：`button.tsx` → `button.test.tsx`
- 只测公共 API 和用户行为，Mock 外部依赖
