# 微信小程序实现指南

## 项目结构模板
```
miniprogram/
├── app.js              # 小程序入口
├── app.json            # 全局配置
├── app.wxss            # 全局样式
├── pages/              # 页面
│   ├── index/
│   │   ├── index.js
│   │   ├── index.wxml
│   │   ├── index.wxss
│   │   └── index.json
│   └── ...
├── components/         # 自定义组件
├── utils/              # 工具函数
├── services/           # API 请求封装
├── store/              # 全局状态（简单状态用 app.js globalData）
└── static/             # 静态资源
```

## 技术约束
- 原生小程序语法（非 uni-app/Taro，除非架构文档明确指定）
- API 请求统一封装：`services/request.js`，处理 token、错误码、登录态过期
- 样式单位：rpx
- 组件通信：props + triggerEvent，跨组件用事件总线或全局状态

## 页面规范
- 页面逻辑优先提取到 utils/services，保持 page.js 简洁
- `data` 只存放页面展示需要的数据，业务数据走接口
- `setData` 只更新变化的字段，不整体替换
- 页面生命周期：`onLoad` 初始化、`onShow` 刷新、`onUnload` 清理

## 命名规范
- 页面/组件目录：kebab-case（`user-profile/`）
- JS 函数/变量：camelCase
- 自定义组件标签：kebab-case（`<user-card />`）
- 事件处理函数：`on` 开头 + 动作（`onTapSubmit`）
- CSS 类名：kebab-case（`.user-card-title`）

## 编码规范
- API 请求统一走 `services/request.js`，带 token 自动刷新和错误重试
- 表单提交做防抖处理（`wx.createSelectorQuery` + 节流）
- 图片使用 WebP 格式，配置 CDN 域名
- 长列表用 `recycle-view` 或分页加载，避免一次性渲染过多节点
- 自定义组件用 `options: { virtualHost: true }` 减少节点层级

## 错误处理
- 网络请求失败要有重试和降级提示
- 登录态过期自动跳转登录页，回来后恢复原页面状态
- 页面加载失败显示友好提示，提供重试入口
- 关键操作（支付、删除）要二次确认

## 禁止事项
- 禁止在 wxml 中写复杂逻辑（提取到 wxs 或 computed）
- 禁止直接使用 `setData` 传递大量数据（只传变化的字段）
- 禁止在页面 onUnload 后继续 setData
- 禁止硬编码 appid 和 secret
- 禁止在页面中使用 `eval` 或 `new Function`
- 禁止一次性 setData 超过 1MB
- 禁止在 `onLaunch` 中做耗时操作（用异步 + loading）
- 禁止直接使用 `wx.request`（统一走 `services/request.js`）
- 禁止在循环中绑定动态事件（用 data- 属性 + 事件委托）

## 性能优化
- 分包加载：首屏无关的页面放到 subPackages
- 图片资源压缩，使用 `image` 组件的 `lazy-load`
- 避免在 scroll 事件中频繁 setData（用节流）
- 使用 `wx.nextTick` 批量 setData 操作
- 首屏渲染数据量控制在 200 条以内

## 单元测试
- 工具：miniprogram-simulate + jest
- 页面逻辑提取到 utils/services 中测试，不直接测试 wxml
- 重点测试：登录流程、分页加载、数据格式化
