#!/usr/bin/env node

/**
 * 桑夏自动写作流程脚本
 *
 * 使用方式：
 * node scripts/write.js "主题" [风格]
 *
 * 风格选项：principle(默认), tutorial, review
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const STYLE_GUIDES = {
  principle: {
    name: '原理科普',
    structure: [
      '问题驱动开场（引用块提出核心问题）',
      '官方定义（引用原始来源）',
      '架构图 + 文字解释',
      '核心组件/原理分点说明（最多 2 层序号）',
      '工作流程/示例',
      '总结 + 参考资料'
    ],
    requirements: [
      '无 emoji（除引用外）',
      '序号清晰（最多 2 层）',
      '表格对比信息',
      'ASCII 架构图配文字解释',
      '字数统计和阅读时间',
      '所有核心概念必须有来源'
    ]
  },
  tutorial: {
    name: '教程实战',
    structure: [
      '场景引入（为什么要学这个）',
      '前置知识',
      'Step-by-Step 实战',
      '常见问题',
      '总结'
    ],
    requirements: [
      '每步有明确操作和预期结果',
      '代码示例可运行',
      '截图或输出示例'
    ]
  },
  review: {
    name: '评测对比',
    structure: [
      '评测对象和目的',
      '评测维度',
      '对比表格',
      '优缺点分析',
      '推荐建议'
    ],
    requirements: [
      '对比维度清晰',
      '数据支撑结论',
      '优缺点客观'
    ]
  }
};

// 搜索素材
function searchMaterials(topic) {
  console.log(`🔍 开始搜索素材：${topic}\n`);

  const searches = [
    `${topic} official documentation`,
    `${topic} tutorial guide 2025 2026`,
    `${topic} explained`,
    `${topic} architecture deep dive`,
    `${topic} best practices`
  ];

  const results = [];

  for (const query of searches) {
    console.log(`搜索：${query}`);
    try {
      const cmd = `cd ~/.openclaw/workspace/skills/tavily-search && node scripts/search.mjs "${query}" -n 5 --deep`;
      const output = execSync(cmd, { encoding: 'utf-8' });
      results.push({ query, output });
      console.log(`✅ 找到相关内容\n`);
    } catch (e) {
      console.log(`❌ 搜索失败：${e.message}\n`);
    }
  }

  return results;
}

// 提取 URL 内容
function extractContent(url) {
  console.log(`提取内容：${url}`);
  try {
    const cmd = `cd ~/.openclaw/workspace/skills/tavily-search && node scripts/extract.mjs "${url}"`;
    const output = execSync(cmd, { encoding: 'utf-8' });
    return output;
  } catch (e) {
    console.log(`提取失败：${e.message}`);
    return null;
  }
}

// 生成文章大纲
function generateOutline(topic, materials, style) {
  const guide = STYLE_GUIDES[style] || STYLE_GUIDES.principle;

  console.log(`\n📋 生成文章大纲（风格：${guide.name}）\n`);

  // 整理素材来源
  const sources = [];
  for (const result of materials) {
    const match = result.output.match(/\*\*(.+?)\*\*\s*\n\s*(https?:\/\/\S+)/g);
    if (match) {
      match.forEach(m => {
        const [, title, url] = m.match(/\*\*(.+?)\*\*\s*\n\s*(https?:\/\/\S+)/) || [];
        if (title && url) {
          sources.push({ title, url });
        }
      });
    }
  }

  console.log(`找到 ${sources.length} 个素材来源`);
  sources.forEach((s, i) => console.log(`  ${i + 1}. ${s.title}`));

  // 生成大纲
  const outline = {
    topic,
    style: guide.name,
    structure: guide.structure,
    sources,
    title: `YYYY-MM-DD-${topic}.md`
  };

  console.log('\n文章结构：');
  guide.structure.forEach((s, i) => console.log(`  ${i + 1}. ${s}`));

  console.log('\n风格要求：');
  guide.requirements.forEach(r => console.log(`  - ${r}`));

  return outline;
}

// 主函数
function write(topic, style = 'principle') {
  console.log('╔════════════════════════════════════════╗');
  console.log('║     桑夏自动写作流程                   ║');
  console.log('╚════════════════════════════════════════╝\n');

  // Step 1: 搜索素材
  const materials = searchMaterials(topic);

  // Step 2: 整理信息
  const outline = generateOutline(topic, materials, style);

  // Step 3: 输出大纲供用户确认
  console.log('\n' + '='.repeat(50));
  console.log('📝 大纲已生成，请确认：');
  console.log(`主题：${outline.topic}`);
  console.log(`风格：${outline.style}`);
  console.log(`素材：${outline.sources.length} 篇`);
  console.log('');
  console.log('确认大纲后，将继续写作...');
  console.log('(按回车继续，或 Ctrl+C 取消)');

  // 等待用户确认
  return outline;
}

// 命令行处理
const args = process.argv.slice(2);
if (args.length === 0) {
  console.log('用法：node write.js "主题" [风格]');
  console.log('\n风格选项：');
  Object.entries(STYLE_GUIDES).forEach(([key, val]) => {
    console.log(`  ${key}: ${val.name}`);
  });
  process.exit(1);
}

const topic = args[0];
const style = args[1] || 'principle';

write(topic, style);
