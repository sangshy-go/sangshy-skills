#!/usr/bin/env python3
"""
微信公众号文章读取器

用法:
    python3 fetch.py <微信文章链接>
    python3 fetch.py --url <链接> --output <输出文件>
"""

import argparse
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
            
            return {
                'success': True,
                'title': self._extract_text(soup, ['h1.rich_media_title', 'h1', 'title']),
                'account': self._extract_text(soup, ['div.rich_media_meta_nickname', 'span.profile_nickname']),
                'author': self._extract_author(soup),
                'publish_time': self._extract_time(soup),
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
    
    def _extract_author(self, soup: BeautifulSoup) -> str:
        """提取作者"""
        elem = soup.find('div', class_='rich_media_meta_text')
        if elem:
            text = elem.get_text(strip=True)
            return text.replace('作者', '').strip() if '作者' in text else '佚名'
        return '佚名'
    
    def _extract_time(self, soup: BeautifulSoup) -> str:
        """提取发布时间"""
        elem = soup.find('span', class_='rich_media_meta_text')
        if elem:
            return elem.get_text(strip=True)
        return datetime.now().strftime('%Y-%m-%d')
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """提取正文"""
        content_div = soup.find('div', id='js_content') or soup.find('div', class_='rich_media_content')
        if not content_div:
            return ''
        
        paragraphs = []
        for p in content_div.find_all(['p', 'section'], recursive=False):
            text = p.get_text(strip=True)
            if text:
                paragraphs.append(text)
        
        return '\n\n'.join(paragraphs)
    
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
    parser.add_argument('url', nargs='?', help='微信文章链接')
    parser.add_argument('--url', '-u', dest='url_opt', help='微信文章链接')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--raw', action='store_true', help='输出原始 JSON')
    
    args = parser.parse_args()
    url = args.url or args.url_opt
    
    if not url:
        print("❌ 请提供微信文章链接")
        print("\n用法:")
        print("  python3 fetch.py <链接>")
        print("  python3 fetch.py --url <链接> --output article.md")
        return
    
    fetcher = WeixinFetcher()
    result = fetcher.fetch(url)
    
    if args.raw:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        md = fetcher.to_markdown(result)
        
        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(md)
            print(f"✅ 已保存到：{args.output}")
        else:
            print(md)


if __name__ == '__main__':
    main()
