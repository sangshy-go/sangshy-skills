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

## 常见模式
- 分页加载：onReachBottom + 节流
- 下拉刷新：onPullDownRefresh
- 登录流程：wx.login → 后端换 token → 存储 storage
- 分包加载：`app.json` 中配置 subPackages

## 禁止事项
- 禁止在 wxml 中写复杂逻辑（提取到 wxs 或 computed）
- 禁止直接使用 `setData` 传递大量数据（只传变化的字段）
- 禁止在页面 onUnload 后继续 setData
- 禁止硬编码 appid 和 secret
