# 微信小程序实现指南

## 项目结构模板
```
miniprogram/
├── app.js              # 小程序入口
├── app.json            # 全局配置
├── app.wxss            # 全局样式
├── pages/              # 页面
│   ├── index/
│   │   ├── index.js / .wxml / .wxss / .json
│   └── ...
├── components/         # 自定义组件
├── utils/              # 工具函数
├── services/           # API 请求封装
├── store/              # 全局状态（app.js globalData）
└── static/             # 静态资源
```

## 技术约束
- 原生小程序语法（非 uni-app/Taro，除非架构文档指定）
- API 请求统一封装：`services/request.js`，处理 token、错误码、登录态
- 样式单位：rpx
- 组件通信：props + triggerEvent，跨组件用事件总线或全局状态

## 编码规范
- 页面逻辑优先提取到 utils/services，保持 page.js 简洁
- `data` 只存放展示需要的数据，业务数据走接口
- `setData` 只更新变化的字段，不整体替换
- API 请求带 token 自动刷新和错误重试

## 错误处理
- 网络请求失败要有重试和降级提示
- 登录态过期自动跳转登录页，恢复原页面状态
- 关键操作（支付、删除）要二次确认

## 性能优化
- 分包加载：首屏无关的页面放到 subPackages
- 图片使用 WebP，配置 CDN，`lazy-load`
- 避免在 scroll 事件中频繁 setData（用节流）
- 首屏渲染数据量控制在 200 条以内
- 使用 `wx.nextTick` 批量 setData 操作

## 禁止事项
- 禁止在 wxml 中写复杂逻辑（提取到 wxs）
- 禁止 `setData` 传递大量数据（只传变化的字段）
- 禁止页面 onUnload 后继续 setData
- 禁止硬编码 appid 和 secret
- 禁止一次性 setData 超过 1MB
- 禁止 `onLaunch` 中做耗时操作（用异步 + loading）
- 禁止直接使用 `wx.request`（统一走 `services/request.js`）
- 禁止循环中绑定动态事件（用 data- 属性 + 事件委托）

## 单元测试
- 工具：miniprogram-simulate + jest
- 页面逻辑提取到 utils/services 中测试
- 重点测试：登录流程、分页加载、数据格式化
