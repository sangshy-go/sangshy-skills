# sangxia-weixin-fetcher

微信公众号阅读器 - 通用 MCP Skill

## 🎯 特点

- ✅ **通用兼容** - 支持 OpenClaw、Claude Code
- ✅ **MCP 协议** - 标准 Model Context Protocol
- ✅ **自动触发** - 发送微信链接自动读取
- ✅ **开箱即用** - 简单安装

## 📦 安装

```bash
# 克隆仓库
git clone https://github.com/sangshy-go/sangshy-skills.git
cd sangshy-skills/sangxia-weixin-fetcher

# 安装依赖
pip install -r requirements.txt
```

## 🚀 使用

### OpenClaw

Skill 会自动加载，发送微信链接即可：

```
用户：https://mp.weixin.qq.com/s/xxxx
助手：[自动读取并返回内容]
```

### Claude Code

在配置中添加：

```json
{
  "mcpServers": {
    "sangxia-weixin-fetcher": {
      "command": "python3",
      "args": ["scripts/mcp_server.py"]
    }
  }
}
```

## 📋 功能

- 提取标题、公众号、作者、发布时间
- 提取正文内容
- 提取图片
- 统计字数和阅读时间

## ⚠️ 注意

- 仅支持公开文章
- 遵守微信服务条款
- 避免高频抓取

## 📁 结构

```
sangxia-weixin-fetcher/
├── SKILL.md
├── README.md
├── requirements.txt
└── scripts/
    └── mcp_server.py
```

## 📄 许可证

MIT
