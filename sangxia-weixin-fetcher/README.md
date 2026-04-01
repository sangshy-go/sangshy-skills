# Weixin Fetcher - 微信公众号阅读器

读取微信公众号文章内容，提取标题、作者、发布时间和正文内容。

## 🚀 快速开始

### 安装依赖

```bash
cd ~/.openclaw/workspace/skills/weixin-fetcher
pip install -r requirements.txt
```

### 使用方法

#### 方式 1：命令行直接读取

```bash
python3 scripts/fetch.py <微信文章链接>
```

#### 方式 2：保存到文件

```bash
python3 scripts/fetch.py --url <链接> --output article.md
```

#### 方式 3：输出 JSON

```bash
python3 scripts/fetch.py <链接> --raw
```

## 📋 功能特性

- ✅ 提取文章标题
- ✅ 提取公众号名称
- ✅ 提取作者信息
- ✅ 提取发布时间
- ✅ 提取正文内容（Markdown 格式）
- ✅ 提取文章中的图片
- ✅ 统计字数和阅读时间
- ✅ 支持输出 JSON 格式

## 💡 使用示例

### 示例 1：读取文章并显示

```bash
python3 scripts/fetch.py https://mp.weixin.qq.com/s/xxxx
```

输出：
```markdown
# 文章标题

**公众号**：公众号名称
**作者**：作者名
**发布时间**：2026-04-01
**字数**：2800 | **阅读时间**：9 分钟

---

正文内容...
```

### 示例 2：保存到文件

```bash
python3 scripts/fetch.py https://mp.weixin.qq.com/s/xxxx -o article.md
```

### 示例 3：获取 JSON 数据

```bash
python3 scripts/fetch.py https://mp.weixin.qq.com/s/xxxx --raw
```

输出：
```json
{
  "success": true,
  "title": "文章标题",
  "account": "公众号名称",
  "author": "作者名",
  "publish_time": "2026-04-01",
  "content": "正文内容...",
  "images": [...],
  "stats": {...}
}
```

## 🔧 配置选项

| 参数 | 说明 | 示例 |
|------|------|------|
| `url` | 微信文章链接（位置参数） | `python3 fetch.py <链接>` |
| `--url, -u` | 微信文章链接（选项参数） | `--url https://...` |
| `--output, -o` | 输出文件路径 | `-o article.md` |
| `--raw` | 输出原始 JSON | `--raw` |

## ⚠️ 注意事项

1. **仅支持公开文章** - 需要关注公众号才能阅读的文章无法获取
2. **遵守服务条款** - 请遵守微信公众平台的服务条款
3. **避免高频抓取** - 不建议批量高频抓取，可能被限制
4. **网络连接** - 需要联网才能获取文章

## 📁 文件结构

```
weixin-fetcher/
├── SKILL.md              # Skill 描述文件
├── README.md             # 本文档
├── requirements.txt      # Python 依赖
└── scripts/
    └── fetch.py         # 主脚本
```

## 🛠️ 技术实现

- **请求库**：requests - HTTP 请求
- **解析库**：BeautifulSoup4 - HTML 解析
- **User-Agent**：模拟微信客户端，绕过基础反爬

## 📝 更新日志

### v1.0.0 (2026-04-01)

- ✅ 初始版本
- ✅ 支持提取标题、作者、正文
- ✅ 支持 Markdown 和 JSON 输出
- ✅ 统计字数和阅读时间
- ✅ 提取文章图片

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
