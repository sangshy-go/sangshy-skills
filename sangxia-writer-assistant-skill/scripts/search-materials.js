#!/usr/bin/env node

/**
 * 桑夏博客素材搜索工具
 *
 * 搜索与主题相关的资料，为写作提供素材
 *
 * 使用示例：
 * node scripts/search-materials.js --topic "<主题>" --output materials.md
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 搜索配置
const SEARCH_CONFIG = {
  // 本地文章目录
  localArticles: process.env.BLOG_DIR || path.join(__dirname, '../../../articles'),
  // 输出文件
  output: 'materials.md',
  // 最大结果数
  maxResults: 10
};

// 解析命令行参数
function parseArgs(args) {
  const result = {
    topic: null,
    output: SEARCH_CONFIG.output,
    localOnly: false
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--topic' && args[i + 1]) {
      result.topic = args[i + 1];
      i++;
    } else if (args[i] === '--output' && args[i + 1]) {
      result.output = args[i + 1];
      i++;
    } else if (args[i] === '--local-only') {
      result.localOnly = true;
    }
  }

  return result;
}

// 搜索本地文章
function searchLocalArticles(topic) {
  console.log(`📂 搜索本地文章：${topic}`);

  const keywords = topic.toLowerCase().split(/\s+/);
  const results = [];

  try {
    // 读取文章目录
    const articlesDir = SEARCH_CONFIG.localArticles;
    if (!fs.existsSync(articlesDir)) {
      console.log(`⚠️  文章目录不存在：${articlesDir}`);
      return results;
    }

    const files = fs.readdirSync(articlesDir)
      .filter(f => f.endsWith('.md'))
      .map(filename => {
        const filepath = path.join(articlesDir, filename);
        const content = fs.readFileSync(filepath, 'utf-8');
        return { filename, filepath, content };
      });

    // 搜索匹配的文章
    for (const file of files) {
      let score = 0;
      const contentLower = file.content.toLowerCase();
      const filenameLower = file.filename.toLowerCase();

      for (const keyword of keywords) {
        if (filenameLower.includes(keyword)) score += 5;
        if (contentLower.includes(keyword)) score += 1;
      }

      if (score > 0) {
        // 提取 Frontmatter
        const frontmatterMatch = file.content.match(/^---\n([\s\S]*?)\n---\n/);
        let title = file.filename;
        let category = '';
        let tags = [];

        if (frontmatterMatch) {
          const yaml = frontmatterMatch[1];
          const titleMatch = yaml.match(/title:\s*["']?([^"'\n]+)/);
          if (titleMatch) title = titleMatch[1].trim();
          const categoryMatch = yaml.match(/category:\s*(.+)/);
          if (categoryMatch) category = categoryMatch[1].trim();
          const tagsMatch = yaml.match(/tags:\s*\[([^\]]+)\]/);
          if (tagsMatch) tags = tagsMatch[1].split(',').map(t => t.trim().replace(/"/g, ''));
        }

        results.push({
          filename: file.filename,
          title,
          category,
          tags,
          score,
          preview: file.content.substring(0, 200).replace(/\n/g, ' ') + '...'
        });
      }
    }

    // 按分数排序
    results.sort((a, b) => b.score - a.score);
    return results.slice(0, SEARCH_CONFIG.maxResults);

  } catch (error) {
    console.error(`❌ 搜索失败：${error.message}`);
    return [];
  }
}

// 搜索网络资料（使用 curl 调用搜索引擎）
function searchWeb(topic) {
  console.log(`🌐 搜索网络资料：${topic}`);

  const results = [];

  try {
    // 使用 DuckDuckGo 搜索（无需 API key）
    const query = encodeURIComponent(`${topic} tutorial guide`);
    const cmd = `curl -s "https://html.duckduckgo.com/html/?q=${query}" | grep -oP '(?<=<a href=")[^"]+(?=" rel="nofollow")' | head -10`;

    try {
      const output = execSync(cmd, { encoding: 'utf-8', timeout: 10000 });
      const links = output.split('\n').filter(l => l.trim());

      for (const link of links.slice(0, 5)) {
        results.push({
          title: link,
          url: link,
          source: 'DuckDuckGo'
        });
      }
    } catch (e) {
      console.log('⚠️  网络搜索不可用，跳过');
    }

  } catch (error) {
    console.error(`❌ 网络搜索失败：${error.message}`);
  }

  return results;
}

// 生成素材文档
function generateMaterialsDoc(topic, localResults, webResults) {
  let doc = `---
# 写作素材：${topic}
# 生成时间：${new Date().toISOString().split('T')[0]}
---

# 写作素材：${topic}

> 本文档搜集了与 "${topic}" 相关的写作素材，供创作参考。

---

## 本地相关文章

`;

  if (localResults.length === 0) {
    doc += `暂无相关文章。\n\n`;
  } else {
    doc += `| 标题 | 分类 | 标签 | 相关度 |\n|------|------|------|--------|\n`;
    for (const r of localResults) {
      const stars = '★'.repeat(Math.min(5, Math.floor(r.score / 2))) + '☆'.repeat(5 - Math.min(5, Math.floor(r.score / 2)));
      doc += `| ${r.title} | ${r.category} | ${r.tags.join(', ')} | ${stars} |\n`;
    }

    doc += `\n### 文章摘要\n\n`;
    for (const r of localResults) {
      doc += `#### ${r.title}\n\n`;
      doc += `- **分类**: ${r.category}\n`;
      doc += `- **标签**: ${r.tags.join(', ')}\n`;
      doc += `- **预览**: ${r.preview}\n\n`;
      doc += `---\n\n`;
    }
  }

  doc += `## 网络参考资料\n\n`;

  if (webResults.length === 0) {
    doc += `暂无网络资料。\n\n`;
  } else {
    doc += `| 标题 | 来源 |\n|------|------|\n`;
    for (const r of webResults) {
      doc += `| [${r.title}](${r.url}) | ${r.source} |\n`;
    }
  }

  doc += `\n---\n\n## 写作建议\n\n`;
  doc += `### 推荐结构\n\n`;
  doc += `1. **开场** - 用引用块提出与 "${topic}" 相关的核心问题\n`;
  doc += `2. **场景对比** - 展示"${topic}"使用前后的差异\n`;
  doc += `3. **概念解释** - 用 3 个类比帮助理解\n`;
  doc += `4. **工作原理** - 用 ASCII 图展示流程\n`;
  doc += `5. **实战案例** - 提供可执行的示例\n`;
  doc += `6. **总结** - 核心要点 + 下一步行动\n\n`;

  doc += `### 推荐配图\n\n`;
  doc += `| 位置 | 配图类型 | 描述 |\n|------|---------|------|\n`;
  doc += `| 开场 | 场景对比图 | 展示${topic}使用前后差异 |\n`;
  doc += `| 概念 | 架构图 | 展示工作原理 |\n`;
  doc += `| 案例 | 截图/流程图 | 展示实际效果 |\n`;

  return doc;
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  const config = parseArgs(args);

  if (!config.topic) {
    console.log('用法：node search-materials.js --topic "<主题>" [选项]');
    console.log('\n选项:');
    console.log('  --topic <主题>     搜索主题（必需）');
    console.log('  --output <文件>    输出文件（默认：materials.md）');
    console.log('  --local-only       只搜索本地文章');
    console.log('\n示例:');
    console.log('  node scripts/search-materials.js --topic "Skills"');
    console.log('  node scripts/search-materials.js --topic "AI Agent" --output ai-materials.md');
    process.exit(1);
  }

  console.log(`🔍 开始搜索素材：${config.topic}\n`);

  // 搜索本地文章
  const localResults = searchLocalArticles(config.topic);
  console.log(`✅ 找到 ${localResults.length} 篇相关文章\n`);

  // 搜索网络资料
  let webResults = [];
  if (!config.localOnly) {
    webResults = searchWeb(config.topic);
    console.log(`✅ 找到 ${webResults.length} 条网络资料\n`);
  }

  // 生成素材文档
  const doc = generateMaterialsDoc(config.topic, localResults, webResults);
  const outputPath = path.resolve(config.output);
  fs.writeFileSync(outputPath, doc, 'utf-8');

  console.log(`📄 素材已保存到：${outputPath}`);
  console.log(`\n💡 下一步：阅读 materials.md，开始创作吧！`);
}

main();
