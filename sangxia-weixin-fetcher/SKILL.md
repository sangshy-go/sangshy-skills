---
name: sangxia-weixin-fetcher
description: 读取微信公众号文章内容。当用户发送微信文章链接时自动调用，提取标题、作者、发布时间、正文内容。
---

# 微信公众号阅读器

自动读取微信公众号文章内容，提取标题、作者、发布时间和正文内容。

## 使用方式

### 方式 1：直接使用（推荐）

直接发送微信文章链接即可：

```
https://mp.weixin.qq.com/s/xxxx
```

AI 会自动调用此 skill 读取文章内容。

### 方式 2：命令行

```bash
python3 scripts/fetch.py https://mp.weixin.qq.com/s/xxxx
```

### 方式 3：带输出文件

```bash
python3 scripts/fetch.py --url https://mp.weixin.qq.com/s/xxxx --output article.md
```

## 功能

- ✅ 自动识别微信文章链接（mp.weixin.qq.com）
- ✅ 提取文章标题
- ✅ 提取公众号名称
- ✅ 提取作者信息
- ✅ 提取发布时间
- ✅ 提取正文内容（Markdown 格式）
- ✅ 提取文章中的图片
- ✅ 统计字数和阅读时间

## 输出格式

```markdown
# 文章标题

**公众号**：公众号名称
**作者**：作者名
**发布时间**：2026-04-01
**字数**：2800 | **阅读时间**：9 分钟

---

正文内容...
```

## 脚本目录

```
sangxia-weixin-fetcher/
├── SKILL.md
├── README.md
├── requirements.txt
└── scripts/
    └── fetch.py    # 主脚本
```

## 依赖

- Python 3.8+
- requests
- beautifulsoup4

安装依赖：
```bash
pip install -r requirements.txt
```

## 质量检查清单

使用前确认：
- [ ] 已安装 Python 依赖
- [ ] 文章是公开的（不需要关注公众号）
- [ ] 网络连接正常

## 注意事项

- 仅支持公开文章
- 请遵守微信公众平台服务条款
- 不建议高频批量抓取

## 故障处理

### 无法获取文章
- 检查文章是否是公开的（有些需要关注公众号）
- 检查网络连接
- 检查链接是否正确

### 内容提取不完整
- 某些文章使用特殊格式，可能无法完全提取
- 可以尝试手动访问链接查看
