# sangxia-weixin-fetcher

微信公众号阅读器 - 通用 Skill

## 🎯 特点

- ✅ **通用兼容** - 支持 OpenClaw、Claude Code
- ✅ **自动触发** - 发送微信链接自动读取
- ✅ **开箱即用** - 简单安装，无需配置
- ✅ **格式清晰** - 输出 Markdown 格式

## 📦 安装

```bash
# 克隆仓库
git clone https://github.com/sangshy-go/sangshy-skills.git
cd sangshy-skills/sangxia-weixin-fetcher

# 安装依赖
pip install -r requirements.txt
```

## 🚀 使用

### 方式 1：直接发送链接（推荐）

在 OpenClaw 或 Claude Code 中直接发送微信文章链接：

```
https://mp.weixin.qq.com/s/xxxx
```

AI 会自动调用此 skill 读取内容。

### 方式 2：命令行

```bash
python3 scripts/fetch.py https://mp.weixin.qq.com/s/xxxx
```

### 方式 3：保存到文件

```bash
python3 scripts/fetch.py --url https://mp.weixin.qq.com/s/xxxx --output article.md
```

## 📋 功能

- ✅ 提取文章标题
- ✅ 提取公众号名称
- ✅ 提取作者信息
- ✅ 提取发布时间
- ✅ 提取正文内容（Markdown 格式）
- ✅ 提取文章图片
- ✅ 统计字数和阅读时间

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

1. **仅支持公开文章** - 需要关注公众号才能阅读的文章无法获取
2. **遵守服务条款** - 请遵守微信公众平台的服务条款
3. **避免高频抓取** - 不建议批量高频抓取
4. **网络连接** - 需要联网才能获取文章

## 📁 文件结构

```
sangxia-weixin-fetcher/
├── SKILL.md              # Skill 描述
├── README.md             # 本文档
├── requirements.txt      # Python 依赖
└── scripts/
    └── fetch.py         # 主脚本
```

## 🛠️ 技术实现

- **HTTP 请求**：requests 库
- **HTML 解析**：BeautifulSoup4
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
