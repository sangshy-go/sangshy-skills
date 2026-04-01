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
import re


class WeixinFetcher:
    """微信公众号文章读取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
    
    def fetch(self, url: str) -> dict:
        """
        获取微信文章内容
        
        Args:
            url: 微信文章链接
            
        Returns:
            包含文章信息的字典
        """
        print(f"📡 正在获取：{url}")
        
        try:
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取标题
            title = self._extract_title(soup)
            
            # 提取公众号信息
            account = self._extract_account(soup)
            
            # 提取作者
            author = self._extract_author(soup)
            
            # 提取发布时间
            publish_time = self._extract_time(soup)
            
            # 提取正文
            content = self._extract_content(soup)
            
            # 提取图片
            images = self._extract_images(soup)
            
            # 统计信息
            stats = self._calculate_stats(content, images)
            
            return {
                'success': True,
                'url': url,
                'title': title,
                'account': account,
                'author': author,
                'publish_time': publish_time,
                'content': content,
                'images': images,
                'stats': stats,
                'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """提取标题"""
        title = soup.find('h1', class_='rich_media_title')
        if not title:
            title = soup.find('h1')
        if not title:
            title = soup.find('title')
        return title.get_text(strip=True) if title else '未知标题'
    
    def _extract_account(self, soup: BeautifulSoup) -> str:
        """提取公众号名称"""
        account = soup.find('div', class_='rich_media_meta_nickname')
        if not account:
            account = soup.find('span', class_='profile_nickname')
        return account.get_text(strip=True) if account else '未知公众号'
    
    def _extract_author(self, soup: BeautifulSoup) -> str:
        """提取作者"""
        author = soup.find('div', class_='rich_media_meta_text')
        if author:
            text = author.get_text(strip=True)
            if '作者' in text:
                return text.replace('作者', '').strip()
        return '佚名'
    
    def _extract_time(self, soup: BeautifulSoup) -> str:
        """提取发布时间"""
        time_elem = soup.find('span', class_='rich_media_meta_text')
        if time_elem:
            return time_elem.get_text(strip=True)
        
        # 尝试从 script 中提取
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'ct_create_time' in script.string:
                match = re.search(r'ct_create_time\s*=\s*(\d+)', script.string)
                if match:
                    timestamp = int(match.group(1))
                    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
        
        return datetime.now().strftime('%Y-%m-%d')
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """提取正文内容"""
        content_div = soup.find('div', id='js_content')
        if not content_div:
            content_div = soup.find('div', class_='rich_media_content')
        
        if not content_div:
            return '无法提取正文内容'
        
        # 提取所有段落
        paragraphs = []
        for p in content_div.find_all(['p', 'section', 'div'], recursive=False):
            text = p.get_text(strip=True)
            if text and len(text) > 0:
                paragraphs.append(text)
        
        return '\n\n'.join(paragraphs)
    
    def _extract_images(self, soup: BeautifulSoup) -> list:
        """提取图片"""
        images = []
        content_div = soup.find('div', id='js_content')
        if not content_div:
            content_div = soup.find('div', class_='rich_media_content')
        
        if content_div:
            for img in content_div.find_all('img'):
                src = img.get('data-src') or img.get('src')
                if src and src.startswith('http'):
                    alt = img.get('alt', '')
                    images.append({'url': src, 'alt': alt})
        
        return images
    
    def _calculate_stats(self, content: str, images: list) -> dict:
        """计算统计信息"""
        char_count = len(content)
        para_count = len(content.split('\n\n'))
        img_count = len(images)
        read_time = max(1, char_count // 300)  # 假设每分钟 300 字
        
        return {
            'char_count': char_count,
            'paragraph_count': para_count,
            'image_count': img_count,
            'read_time_minutes': read_time
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
        md += f"*来源：{data['url']}*\n"
        
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
