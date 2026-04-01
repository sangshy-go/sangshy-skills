---
name: sangxia-weixin-fetcher
description: 读取微信公众号文章内容。当用户发送微信文章链接（mp.weixin.qq.com）时自动触发，提取标题、作者、发布时间、正文内容。支持 OpenClaw 和 Claude Code。
---

# 微信公众号阅读器

自动读取微信公众号文章内容，提取标题、作者、发布时间和正文内容。

## 何时使用

**当用户发送微信文章链接时，自动使用此 skill 读取内容。**

例如：
- `https://mp.weixin.qq.com/s/xxxx`
- "帮我读一下这篇文章：https://..."
- "总结这篇微信文章：https://..."

## 功能

- ✅ 自动识别微信文章链接（mp.weixin.qq.com）
- ✅ 提取文章标题
- ✅ 提取公众号名称
- ✅ 提取作者信息
- ✅ 提取发布时间
- ✅ 提取正文内容（Markdown 格式）
- ✅ 提取文章中的图片
- ✅ 统计字数和阅读时间

## 使用方法

### 方式 1：自动触发（推荐）

用户直接发送微信文章链接，skill 自动触发并读取内容。

### 方式 2：MCP 调用

通过 MCP 协议调用 `fetch_article` 工具：

```json
{
  "name": "fetch_article",
  "arguments": {
    "url": "https://mp.weixin.qq.com/s/xxxx"
  }
}
```

## 技术实现

### MCP 服务器

使用标准 MCP (Model Context Protocol) 协议，支持 OpenClaw 和 Claude Code。

**启动命令**：
```bash
python3 scripts/mcp_server.py
```

**配置示例**（Claude Code）：
```json
{
  "mcpServers": {
    "sangxia-weixin-fetcher": {
      "command": "python3",
      "args": ["scripts/mcp_server.py"],
      "cwd": "/path/to/sangxia-weixin-fetcher"
    }
  }
}
```

### 核心逻辑

1. **HTTP 请求** - 使用 requests 库获取网页内容
2. **HTML 解析** - 使用 BeautifulSoup4 解析 HTML
3. **User-Agent** - 模拟微信客户端，绕过基础反爬
4. **内容提取** - 提取标题、作者、正文、图片等

## 输出格式

返回 Markdown 格式的文章内容：

```markdown
# 文章标题

**公众号**：公众号名称
**作者**：作者名
**发布时间**：2026-04-01
**字数**：2800 | **阅读时间**：9 分钟

---

正文内容...
```

## 依赖

- Python 3.8+
- requests
- beautifulsoup4

安装依赖：
```bash
pip install -r requirements.txt
```

## 注意事项

- 仅支持公开文章（需要关注公众号才能阅读的文章无法获取）
- 需要联网
- 请遵守微信公众平台服务条款
- 不建议高频批量抓取（可能被限制）

## 相关文件

- `scripts/mcp_server.py` - MCP 服务器（主要入口）
- `scripts/fetch.py` - 命令行工具（备用）
- `mcp-config.json` - MCP 配置示例
- `requirements.txt` - Python 依赖

## 更新日志

### v2.0.0 (2026-04-01)
- 重构为通用 MCP Skill
- 支持 OpenClaw 和 Claude Code
- 自动触发微信链接识别
- 改进错误处理

### v1.0.0 (2026-04-01)
- 初始版本
- 基础文章读取功能
