#!/usr/bin/env node

/**
 * 桑夏博客风格检查工具
 *
 * 检查文章是否符合桑夏写作风格
 *
 * 使用示例：
 * node scripts/check-style.js <文章.md>
 */

const fs = require('fs');
const path = require('path');

// 检查项配置
const CHECKS = {
  // 标题格式：是否有副标题（冒号或问号）
  titleFormat: {
    name: '标题格式',
    check: (content, frontmatter) => {
      const title = frontmatter?.title || '';
      if (!title) return { pass: false, message: '缺少标题' };
      // 检查是否有副标题（中文/英文冒号、问号、破折号）
      const hasSubtitle = /[:：？?!——-]/.test(title);
      if (!hasSubtitle) {
        return {
          pass: false,
          message: '标题缺少副标题，建议使用格式："主标题：副标题" 或 "主标题？问题式副标题"'
        };
      }
      return { pass: true };
    }
  },

  // 开场引用：是否有引用块提出问题
  openingQuote: {
    name: '开场引用',
    check: (content) => {
      // 在文章开头 500 字内查找引用块
      const earlyContent = content.substring(0, 500);
      const hasQuote = /^>\s+.+\n>\s*.+$/m.test(earlyContent);
      if (!hasQuote) {
        return {
          pass: false,
          message: '缺少开场引用块，建议用引用块提出核心问题引发读者思考'
        };
      }
      return { pass: true };
    }
  },

  // 场景对比：是否有"没有 X"vs"有 X"的对比
  scenarioCompare: {
    name: '场景对比',
    check: (content) => {
      const hasNegative = /没有 | 不使用 | 旧方式 | ❌/i.test(content);
      const hasPositive = /有 | 使用 | 新方式 | ✅/i.test(content);
      if (!hasNegative || !hasPositive) {
        return {
          pass: false,
          message: '缺少场景对比，建议用"没有 X 的情况"vs"有 X 之后"展示价值'
        };
      }
      return { pass: true };
    }
  },

  // 3 个类比：是否有类比帮助理解
  analogies: {
    name: '类比解释',
    check: (content) => {
      // 检查是否有类比表格或类比相关关键词
      const hasAnalogyTable = /\| 类比 | 类似 | 就像 | 如同/i.test(content);
      const hasAnalogySection = /##.*类比 | 个类比/i.test(content);
      if (!hasAnalogyTable && !hasAnalogySection) {
        return {
          pass: false,
          message: '缺少类比解释，建议用"3 个类比帮你理解"表格形式解释抽象概念'
        };
      }
      return { pass: true };
    }
  },

  // 表格使用：是否有表格总结信息
  tables: {
    name: '表格使用',
    check: (content) => {
      const hasTable = /^\|.+\|.+\|$/m.test(content);
      if (!hasTable) {
        return {
          pass: false,
          message: '缺少表格，建议在对比分析、参数说明、功能列表时使用表格'
        };
      }
      return { pass: true };
    }
  },

  // 架构图：是否有 ASCII 架构图
  architecture: {
    name: '架构图',
    check: (content) => {
      // 检查是否有 ASCII 框图
      const hasDiagram = /┌─┬─┐│└┘├┤┬┼└┴┌┐┍┑┎┒┏┓┣┫┳┻╋╭╮╰╯╞╡╤╧╪╢╙╜╟╫╨╬/.test(content);
      const hasCodeBlock = /```[\s\S]*?┌/.test(content);
      if (!hasDiagram && !hasCodeBlock) {
        return {
          pass: false,
          message: '缺少架构图，建议用 ASCII 图展示工作原理或流程'
        };
      }
      return { pass: true };
    }
  },

  // 检查清单：是否有可操作的 checklist
  checklist: {
    name: '检查清单',
    check: (content) => {
      const hasCheckbox = /- \[[ x]\]/i.test(content);
      if (!hasCheckbox) {
        return {
          pass: false,
          message: '缺少检查清单，建议在适当位置提供可操作的 checklist'
        };
      }
      return { pass: true };
    }
  },

  // 系列导航：是否有系列文章导航
  seriesNav: {
    name: '系列导航',
    check: (content) => {
      const hasNav = /系列 | 导航 | 下一篇 | 上一篇 | 本文/.test(content);
      const hasTable = /^\|.+\|.+\|.+\|$/m.test(content);
      const hasEmojiStatus = /✅|📝|❌/.test(content);
      // 有表格 + 导航关键词，或者有表格 + emoji 状态
      if ((hasNav && hasTable) || (hasTable && hasEmojiStatus)) {
        return { pass: true };
      }
      return {
        pass: false,
        message: '缺少系列导航，建议在文章末尾添加系列文章导航表格'
      };
    }
  },

  // 字数统计：是否有字数和阅读时间
  wordCount: {
    name: '字数统计',
    check: (content) => {
      const hasWordCount = /字数：| 约.*字/.test(content);
      const hasReadTime = /阅读时间：|.*分钟/.test(content);
      if (!hasWordCount || !hasReadTime) {
        return {
          pass: false,
          message: '缺少字数统计，建议在文章末尾添加"*字数：约 X,XXX 字 | 阅读时间：约 X-X 分钟*"'
        };
      }
      return { pass: true };
    }
  },

  // Frontmatter：是否完整
  frontmatter: {
    name: 'Frontmatter',
    check: (content, frontmatter) => {
      const required = ['title', 'date', 'category', 'tags'];
      const missing = required.filter(key => !frontmatter?.[key]);
      if (missing.length > 0) {
        return {
          pass: false,
          message: `Frontmatter 缺少字段：${missing.join(', ')}`
        };
      }
      return { pass: true };
    }
  },

  // 超长行检查：每行<100 字符
  longLines: {
    name: '超长行检查',
    check: (content) => {
      const lines = content.split('\n');
      const longLines = lines.filter(l => l.length > 100);
      if (longLines.length > 0) {
        return {
          pass: false,
          message: `发现 ${longLines.length} 行超长行 (>100 字符)，建议拆分或使用多行字符串`,
          details: longLines.slice(0, 3).map(l => `  - ${l.substring(0, 50)}...`)
        };
      }
      return { pass: true };
    }
  },

  // 代码块闭合检查
  codeBlocks: {
    name: '代码块闭合',
    check: (content) => {
      const blocks = content.match(/^```.*$/gm);
      if (!blocks || blocks.length % 2 !== 0) {
        return {
          pass: false,
          message: '代码块未闭合，检查 ``` 标记是否成对'
        };
      }
      return { pass: true };
    }
  }
};

// 解析 Frontmatter
function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n/);
  if (!match) return null;

  const yaml = match[1];
  const result = {};

  // 简单 YAML 解析
  yaml.split('\n').forEach(line => {
    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.substring(0, colonIndex).trim();
      let value = line.substring(colonIndex + 1).trim();
      // 跳过数组（已经处理过）
      if (value.startsWith('[') && value.endsWith(']')) {
        value = value.slice(1, -1).split(',').map(v => v.trim().replace(/"/g, ''));
      }
      // 处理字符串（确保 value 是字符串类型）
      else if (typeof value === 'string' && value.startsWith('"') && value.endsWith('"')) {
        value = value.slice(1, -1);
      }
      result[key] = value;
    }
  });

  return result;
}

// 主函数
function checkStyle(filePath) {
  console.log(`📄 风格检查：${path.basename(filePath)}\n`);

  const content = fs.readFileSync(filePath, 'utf-8');
  const frontmatter = parseFrontmatter(content);

  let allPass = true;
  const results = [];

  // 执行所有检查
  for (const [key, config] of Object.entries(CHECKS)) {
    const result = config.check(content, frontmatter);
    results.push({ name: config.name, ...result });
    if (!result.pass) allPass = false;
  }

  // 输出结果
  for (const result of results) {
    const icon = result.pass ? '✅' : '❌';
    console.log(`${icon} ${result.name}: ${result.pass ? '通过' : result.message}`);
    if (result.details) {
      result.details.forEach(d => console.log(d));
    }
  }

  console.log('\n' + '='.repeat(50));
  const passCount = results.filter(r => r.pass).length;
  console.log(`总计：${passCount}/${results.length} 通过`);

  if (allPass) {
    console.log('🎉 恭喜！文章符合桑夏写作风格');
  } else {
    console.log('⚠️  建议修复上述问题后再发布');
  }

  process.exit(allPass ? 0 : 1);
}

// 命令行参数处理
const args = process.argv.slice(2);
if (args.length === 0) {
  console.log('用法：node check-style.js <文章.md>');
  console.log('\n检查文章是否符合桑夏写作风格');
  console.log('\n检查项：');
  Object.entries(CHECKS).forEach(([key, config]) => {
    console.log(`  - ${config.name}`);
  });
  process.exit(1);
}

const filePath = args[0];
if (!fs.existsSync(filePath)) {
  console.error(`错误：文件不存在：${filePath}`);
  process.exit(1);
}

checkStyle(filePath);
