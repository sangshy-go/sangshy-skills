#!/usr/bin/env python3
"""
微信公众号文章读取器

用法:
    python3 fetch.py <微信文章链接>
    python3 fetch.py --url <链接> --output <输出文件>
"""

import argparse
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path


class WeixinFetcher:
    """微信公众号文章读取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        })
    
    def fetch(self, url: str) -> dict:
        """获取微信文章内容"""
        try:
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                return {'success': False, 'error': f'HTTP {response.status_code}'}
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取元数据
            title = self._extract_text(soup, ['h1.rich_media_title', 'h1', 'title'])
            account = self._extract_account(soup)
            publish_time = self._extract_publish_time(soup)
            
            return {
                'success': True,
                'title': title,
                'account': account,
                'author': self._extract_author(soup),
                'publish_time': publish_time,
                'content': self._extract_content(soup),
                'images': self._extract_images(soup),
                'stats': self._calculate_stats(soup),
                'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _extract_text(self, soup: BeautifulSoup, selectors: list) -> str:
        """提取文本"""
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return ''
    
    def _extract_account(self, soup: BeautifulSoup) -> str:
        """提取公众号名称"""
        # 使用 CSS 选择器查找
        elem = soup.select_one('.rich_media_meta_nickname')
        if elem:
            return elem.get_text(strip=True)
        return ''
    
    def _extract_author(self, soup: BeautifulSoup) -> str:
        """提取作者"""
        elem = soup.find('div', class_='rich_media_meta_text')
        if elem:
            text = elem.get_text(strip=True)
            return text.replace('作者', '').strip() if '作者' in text else '佚名'
        return '佚名'
    
    def _extract_publish_time(self, soup: BeautifulSoup) -> str:
        """提取发布时间"""
        # 查找包含时间的元素
        meta_text = soup.find('div', class_='rich_media_meta_text')
        if meta_text:
            # 尝试提取时间部分（通常在最后）
            text = meta_text.get_text(strip=True)
            # 简单的日期格式匹配
            import re
            date_match = re.search(r'\d{4}年\d{1,2}月\d{1,2}日', text)
            if date_match:
                return date_match.group()
        return datetime.now().strftime('%Y-%m-%d')
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """提取正文"""
        content_div = soup.find('div', id='js_content') or soup.find('div', class_='rich_media_content')
        if not content_div:
            return ''
        
        paragraphs = []
        # 查找所有段落标签（p, section, div 等）
        for tag in content_div.find_all(['p', 'section', 'div'], recursive=True):
            text = tag.get_text(strip=True)
            # 忽略太短或空的段落
            if text and len(text) > 10:
                paragraphs.append(text)
        
        # 去重（微信文章有时会重复）
        seen = set()
        unique_paragraphs = []
        for p in paragraphs:
            if p not in seen:
                seen.add(p)
                unique_paragraphs.append(p)
        
        # 用两个换行符分隔段落，形成 Markdown 段落
        return '\n\n'.join(unique_paragraphs)
    
    def _extract_images(self, soup: BeautifulSoup) -> list:
        """提取图片"""
        images = []
        content_div = soup.find('div', id='js_content')
        if content_div:
            for img in content_div.find_all('img'):
                src = img.get('data-src') or img.get('src')
                if src and src.startswith('http'):
                    images.append({'url': src, 'alt': img.get('alt', '')})
        return images
    
    def _calculate_stats(self, soup: BeautifulSoup) -> dict:
        """统计信息"""
        content = self._extract_content(soup)
        images = self._extract_images(soup)
        return {
            'char_count': len(content),
            'image_count': len(images),
            'read_time_minutes': max(1, len(content) // 300)
        }
    
    def to_summary(self, data: dict) -> str:
        """生成内容总结"""
        if not data.get('success'):
            return f"❌ 获取失败：{data.get('error', '未知错误')}"
        
        # 提取关键信息
        paragraphs = data['content'].split('\n\n')
        
        # 生成总结（前 3 段 + 关键信息）
        summary = f"# {data['title']}\n\n"
        summary += f"**公众号**：{data['account']} | **作者**：{data['author']} | **发布时间**：{data['publish_time']}\n"
        summary += f"**字数**：{data['stats']['char_count']} | **阅读时间**：{data['stats']['read_time_minutes']} 分钟\n\n"
        summary += "---\n\n"
        summary += "## 📝 文章总结\n\n"
        
        # 输出前 3-5 段作为总结
        for i, para in enumerate(paragraphs[:5], 1):
            if len(para) > 20:  # 忽略太短的段落
                summary += f"{para}\n\n"
        
        summary += "...\n\n"
        summary += "> 💡 提示：完整内容请使用 `--full` 参数查看\n"
        
        return summary
    
    def to_markdown(self, data: dict) -> str:
        """转换成 Markdown 格式"""
        if not data.get('success'):
            return f"❌ 获取失败：{data.get('error', '未知错误')}"
        
        md = f"# {data['title']}\n\n"
        md += f"**公众号**：{data['account']}\n"
        md += f"**作者**：{data['author']}\n"
        md += f"**发布时间**：{data['publish_time']}\n"
        md += f"**字数**：{data['stats']['char_count']} | **阅读时间**：{data['stats']['read_time_minutes']} 分钟\n"
        md += f"\n---\n\n"
        md += data['content']
        
        if data['images']:
            md += f"\n\n---\n\n## 图片 ({len(data['images'])} 张)\n\n"
            for i, img in enumerate(data['images'], 1):
                md += f"![图片{i}]({img['url']})\n"
        
        md += f"\n\n---\n\n*获取时间：{data['fetched_at']}*\n"
        md += f"*来源：{data.get('url', '未知')}*\n"
        
        return md


def main():
    parser = argparse.ArgumentParser(description='读取微信公众号文章内容')
    parser.add_argument('--url', '-u', required=True, help='微信文章链接')
    parser.add_argument('--output', '-o', default='./wechat-article.md', help='输出文件路径（默认：./wechat-article.md）')
    parser.add_argument('--raw', action='store_true', help='输出原始 JSON')
    parser.add_argument('--full', '-f', action='store_true', help='输出完整内容（默认输出总结）')
    parser.add_argument('--stdout', action='store_true', help='输出到控制台（不保存文件）')
    
    args = parser.parse_args()
    
    print(f"📡 正在获取：{args.url}", file=sys.stderr)
    fetcher = WeixinFetcher()
    result = fetcher.fetch(args.url)
    
    if args.raw:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.full:
        # 输出完整内容到文件
        md = fetcher.to_markdown(result)
        
        import os
        output_path = os.path.abspath(os.path.expanduser(args.output))
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)
        print(f"✅ 完整内容已保存到：{output_path}", file=sys.stderr)
        print(f"\n📄 文件预览（前 10 行）：")
        with open(output_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i < 10:
                    print(line, end='')
                else:
                    print("...")
                    break
    else:
        # 默认输出总结到控制台
        summary = fetcher.to_summary(result)
        print(summary)


if __name__ == '__main__':
    main()
