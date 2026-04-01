# sangxia-weixin-fetcher

微信公众号阅读器 - 通用 MCP Skill

## 🎯 特点

- ✅ **通用兼容** - 支持 OpenClaw、Claude Code 等 AI 助手
- ✅ **MCP 协议** - 使用标准 MCP (Model Context Protocol)
- ✅ **自动触发** - 发送微信链接自动读取
- ✅ **开箱即用** - 简单安装，无需配置

## 📦 安装

### 方式 1：OpenClaw

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/sangshy-go/sangshy-skills.git temp-skills
cp -r temp-skills/sangxia-weixin-fetcher .
rm -rf temp-skills
cd sangxia-weixin-fetcher
pip install -r requirements.txt
```

### 方式 2：Claude Code

在 Claude Code 配置中添加：

```json
{
  "mcpServers": {
    "sangxia-weixin-fetcher": {
      "command": "python3",
      "args": ["/path/to/sangxia-weixin-fetcher/scripts/mcp_server.py"]
    }
  }
}
```

### 方式 3：手动安装

```bash
git clone https://github.com/sangshy-go/sangshy-skills.git
cd sangshy-skills/sangxia-weixin-fetcher
pip install -r requirements.txt
```

## 🚀 使用

### 直接使用（推荐）

直接发送微信文章链接即可：

```
用户：https://mp.weixin.qq.com/s/xxxx

助手：[自动读取并返回文章内容]
```

### 通过 MCP 调用

```python
# MCP 客户端调用示例
import requests

response = requests.post('http://localhost:8080/mcp', json={
    'method': 'tools/call',
    'params': {
        'name': 'fetch_article',
        'arguments': {
            'url': 'https://mp.weixin.qq.com/s/xxxx'
        }
    }
})

result = response.json()
print(result)
```

## 📋 功能

- ✅ 提取文章标题
- ✅ 提取公众号名称
- ✅ 提取作者信息
- ✅ 提取发布时间
- ✅ 提取正文内容
- ✅ 提取文章图片
- ✅ 统计字数和阅读时间

## 🔧 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `PYTHONPATH` | Python 路径 | 自动检测 |
| `REQUESTS_TIMEOUT` | 请求超时（秒） | 15 |

### MCP 配置

```json
{
  "mcpServers": {
    "sangxia-weixin-fetcher": {
      "command": "python3",
      "args": ["scripts/mcp_server.py"],
      "cwd": "/path/to/sangxia-weixin-fetcher",
      "env": {
        "REQUESTS_TIMEOUT": "30"
      }
    }
  }
}
```

## 📁 文件结构

```
sangxia-weixin-fetcher/
├── SKILL.md              # Skill 描述（OpenClaw）
├── README.md             # 本文档
├── mcp-config.json       # MCP 配置
├── requirements.txt      # Python 依赖
└── scripts/
    ├── mcp_server.py    # MCP 服务器
    └── fetch.py         # 命令行工具（兼容旧版）
```

## 💡 使用示例

### 示例 1：读取文章

```
用户：https://mp.weixin.qq.com/s/udSpp7eMqwiRo5yVShRzLw

助手：
# 分享 6 个我觉得应该必装的 Skills。

**公众号**：数字生命卡兹克
**作者**：佚名
**发布时间**：2026-04-01
**字数**：5741 | **阅读时间**：19 分钟

---

上周发了给 Agent 用的 superpowers 插件那篇文章...
```

### 示例 2：读取并总结

```
用户：总结一下这篇文章：https://mp.weixin.qq.com/s/xxxx

助手：
这篇文章主要介绍了 6 个必装的 Skills：

1. Frontend Design - 解决 AI 生成前端的审美问题
2. 办公四件套 (docx/xlsx/pdf/pptx) - 读取编辑办公文档
3. Web Access - 联网搜索和浏览器操作
4. PUA - 优化 AI 输出质量
5. Claude-mem - 记忆机制
6. Skill-Creator - 创建自定义 Skills
...
```

## ⚠️ 注意事项

1. **仅支持公开文章** - 需要关注公众号的文章无法获取
2. **遵守服务条款** - 请遵守微信公众平台服务条款
3. **避免高频抓取** - 不建议批量高频抓取
4. **网络连接** - 需要联网才能获取文章

## 🛠️ 开发

### 本地测试

```bash
# 测试 MCP 服务器
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python3 scripts/mcp_server.py

# 测试命令行工具
python3 scripts/fetch.py https://mp.weixin.qq.com/s/xxxx
```

### 添加新功能

1. 在 `WeixinFetcher` 类中添加新方法
2. 在 `get_tools()` 中注册新工具
3. 在 `call_tool()` 中添加调用逻辑
4. 更新 `SKILL.md` 文档

## 📝 更新日志

### v2.0.0 (2026-04-01)

- ✅ 重构为通用 MCP Skill
- ✅ 支持 OpenClaw 和 Claude Code
- ✅ 自动触发微信链接识别
- ✅ 改进错误处理
- ✅ 添加完整的 MCP 协议支持

### v1.0.0 (2026-04-01)

- ✅ 初始版本
- ✅ 基础文章读取功能
- ✅ 命令行工具

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
