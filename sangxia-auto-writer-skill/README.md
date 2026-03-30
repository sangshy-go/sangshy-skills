# sangxia-auto-writer

桑夏自动写作流程 Skill：先搜索素材，再按指定风格写文章。

## 核心流程

```
1. 接收命题 → 2. 搜索素材 → 3. 整理信息 → 4. 按风格写作
```

## 使用方法

### 命令行

```bash
cd ~/.openclaw/workspace/skills/sangxia-auto-writer
node scripts/write.js "主题" [风格]
```

### 风格选项

| 风格 | 说明 | 适用场景 |
|------|------|---------|
| `principle` (默认) | 原理科普 | 技术原理、架构讲解 |
| `tutorial` | 教程实战 | Step-by-Step 教学 |
| `review` | 评测对比 | 产品/技术对比评测 |

### 示例

```bash
# 写原理科普文章
node scripts/write.js "Agent Harness 原理"

# 写教程文章
node scripts/write.js "TypeScript 泛型教程" tutorial

# 写评测文章
node scripts/write.js "Vercel vs Netlify 对比" review
```

## 写作原则

> **先搜索，后写作。不知道的不编造。**

1. 所有核心概念必须有来源
2. 定义优先引用官方
3. 不确定内容明确标注
4. 参考资料列表完整

## 风格指南

详见 `styles/` 目录：

- [`styles/principle.md`](styles/principle.md) - 原理科普风格
- `styles/tutorial.md` - 教程实战风格（待创建）
- `styles/review.md` - 评测对比风格（待创建）

## 搜索配置

默认使用 `tavily-search` 搜索素材：

- 官方文档（优先级最高）
- 热门教程（3-5 篇）
- 深度分析（1-2 篇）

## 输出

文章保存到：
```
articles/YYYY-MM-DD-<主题>.md
```

## License

MIT
