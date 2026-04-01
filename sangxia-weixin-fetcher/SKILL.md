---
name: sangxia-weixin-fetcher
description: 读取微信公众号文章内容。支持任意公众号文章链接，提取标题、作者、发布时间、正文内容。
triggers:
  - "微信公众号"
  - "mp.weixin.qq.com"
  - "微信文章"
  - "读取微信"
allowed-tools: ["Bash", "Read", "Write"]
---

# 微信公众号阅读器

读取微信公众号文章内容，提取标题、作者、发布时间和正文内容。

## 使用方法

直接发送微信公众号文章链接即可：
- https://mp.weixin.qq.com/s/xxxx

## 功能

- ✅ 提取文章标题
- ✅ 提取公众号名称
- ✅ 提取发布时间
- ✅ 提取正文内容（Markdown 格式）
- ✅ 提取文章中的图片
- ✅ 统计字数和阅读时间

## 依赖

- Python 3.8+
- requests
- beautifulsoup4

安装依赖：
```bash
cd ~/.openclaw/workspace/skills/weixin-fetcher
pip install -r requirements.txt
```

## 使用示例

### 方式 1：命令行
```bash
python3 scripts/fetch.py https://mp.weixin.qq.com/s/xxxx
```

### 方式 2：直接调用
```bash
python3 scripts/fetch.py --url "https://mp.weixin.qq.com/s/xxxx" --output article.md
```

## 输出格式

```markdown
# 文章标题

**公众号**：公众号名称
**作者**：作者名
**发布时间**：2026-04-01

---

正文内容...
```

## 注意事项

- 仅支持公开文章
- 需要联网
- 请遵守目标网站的服务条款
- 不建议高频批量抓取

## 更新日志

### v1.0.0 (2026-04-01)
- 初始版本
- 支持提取标题、作者、正文
- 支持输出 Markdown 格式
