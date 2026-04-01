#!/usr/bin/env python3
"""
Weixin Fetcher MCP Server

微信公众号阅读器 - MCP 服务器
支持 OpenClaw、Claude Code 等 AI 助手调用

用法:
    python3 mcp_server.py
"""

import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Any


class WeixinFetcher:
    """微信公众号文章读取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        })
    
    def fetch_article(self, url: str) -> dict:
        """
        获取微信文章内容
        
        Args:
            url: 微信文章链接
            
        Returns:
            包含文章信息的字典
        """
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
                'fetched_at': datetime.now().isoformat()
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
        char_count = len(content)
        
        return {
            'char_count': char_count,
            'image_count': len(images),
            'read_time_minutes': max(1, char_count // 300)
        }


# MCP 协议处理
def get_tools() -> list:
    """返回可用的工具列表"""
    return [
        {
            'name': 'fetch_article',
            'description': '读取微信公众号文章内容，提取标题、作者、发布时间和正文',
            'inputSchema': {
                'type': 'object',
                'properties': {
                    'url': {
                        'type': 'string',
                        'description': '微信文章链接，例如：https://mp.weixin.qq.com/s/xxxx'
                    }
                },
                'required': ['url']
            }
        }
    ]


def call_tool(name: str, arguments: dict) -> dict:
    """调用工具"""
    if name == 'fetch_article':
        url = arguments.get('url')
        if not url:
            return {'success': False, 'error': '缺少 url 参数'}
        
        fetcher = WeixinFetcher()
        return fetcher.fetch_article(url)
    
    return {'success': False, 'error': f'未知工具：{name}'}


def handle_message(message: dict) -> dict:
    """处理 MCP 消息"""
    method = message.get('method')
    params = message.get('params', {})
    msg_id = message.get('id')
    
    if method == 'tools/list':
        return {
            'jsonrpc': '2.0',
            'id': msg_id,
            'result': {'tools': get_tools()}
        }
    
    elif method == 'tools/call':
        tool_name = params.get('name')
        arguments = params.get('arguments', {})
        result = call_tool(tool_name, arguments)
        
        return {
            'jsonrpc': '2.0',
            'id': msg_id,
            'result': {
                'content': [
                    {
                        'type': 'text',
                        'text': json.dumps(result, ensure_ascii=False, indent=2)
                    }
                ]
            }
        }
    
    else:
        return {
            'jsonrpc': '2.0',
            'id': msg_id,
            'error': {
                'code': -32601,
                'message': f'未知方法：{method}'
            }
        }


def main():
    """MCP 服务器主循环"""
    print("🚀 Weixin Fetcher MCP Server 已启动", file=sys.stderr)
    print("等待请求...", file=sys.stderr)
    
    for line in sys.stdin:
        try:
            message = json.loads(line.strip())
            response = handle_message(message)
            print(json.dumps(response, ensure_ascii=False), flush=True)
        except json.JSONDecodeError as e:
            error_response = {
                'jsonrpc': '2.0',
                'id': None,
                'error': {
                    'code': -32700,
                    'message': f'JSON 解析错误：{str(e)}'
                }
            }
            print(json.dumps(error_response), flush=True)
        except Exception as e:
            error_response = {
                'jsonrpc': '2.0',
                'id': None,
                'error': {
                    'code': -32603,
                    'message': f'内部错误：{str(e)}'
                }
            }
            print(json.dumps(error_response), flush=True)


if __name__ == '__main__':
    main()
