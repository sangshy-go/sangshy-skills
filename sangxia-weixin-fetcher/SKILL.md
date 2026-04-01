---
name: sangxia-weixin-fetcher
description: 读取微信公众号文章内容。自动提取标题、作者、发布时间、正文内容。支持任意公众号文章链接。
triggers:
  - "微信公众号"
  - "mp.weixin.qq.com"
  - "微信文章"
  - "读取微信"
  - "fetch wechat"
  - "read weixin"
tools:
  - fetch_article
---

# 微信公众号阅读器

自动读取微信公众号文章内容，提取标题、作者、发布时间和正文内容。

## 使用方法

**直接发送微信文章链接即可**，例如：
- https://mp.weixin.qq.com/s/xxxx

## 功能

- ✅ 自动识别微信文章链接
- ✅ 提取文章标题
- ✅ 提取公众号名称
- ✅ 提取作者信息
- ✅ 提取发布时间
- ✅ 提取正文内容（Markdown 格式）
- ✅ 提取文章中的图片
- ✅ 统计字数和阅读时间

## 使用示例

### 示例 1：直接读取

```
用户：https://mp.weixin.qq.com/s/udSpp7eMqwiRo5yVShRzLw

助手：[自动读取文章内容并总结]
```

### 示例 2：读取并保存

```
用户：帮我读取这篇文章并保存：https://mp.weixin.qq.com/s/xxxx

助手：[读取内容并保存到文件]
```

### 示例 3：读取并总结

```
用户：总结一下这篇文章：https://mp.weixin.qq.com/s/xxxx

助手：[读取内容并生成总结]
```

## 技术实现

- **HTTP 请求**：requests 库
- **HTML 解析**：BeautifulSoup4
- **User-Agent**：模拟微信客户端

## 依赖

- Python 3.8+
- requests
- beautifulsoup4

## 注意事项

- 仅支持公开文章
- 需要联网
- 请遵守微信公众平台服务条款
- 不建议高频批量抓取
