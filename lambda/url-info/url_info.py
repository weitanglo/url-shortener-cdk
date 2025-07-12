import json
import os
import boto3
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
from datetime import datetime

# DynamoDB setup
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['URLSHORTNERTABLE_TABLE_NAME']
table = dynamodb.Table(table_name)

def handler(event, context):
    """
    URL情報取得Lambda関数
    元サイトの情報（タイトル、説明、ファビコンなど）を取得
    Built with Amazon Q Developer
    """
    
    try:
        # リクエストボディの解析
        body = json.loads(event['body']) if event.get('body') else {}
        url = body.get('url')
        
        if not url:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'URL is required'
                })
            }
        
        # URL情報を取得
        url_info = get_url_info(url)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(url_info)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }

def get_url_info(url):
    """
    URLから基本情報を取得
    """
    try:
        # HTTPリクエスト
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # HTMLパース
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 基本情報取得
        info = {
            'url': url,
            'title': get_title(soup),
            'description': get_description(soup),
            'favicon': get_favicon(soup, url),
            'image': get_og_image(soup, url),
            'site_name': get_site_name(soup),
            'domain': urlparse(url).netloc,
            'retrieved_at': datetime.utcnow().isoformat()
        }
        
        return info
        
    except requests.RequestException as e:
        return {
            'url': url,
            'title': get_domain_title(url),
            'description': 'サイト情報を取得できませんでした',
            'favicon': None,
            'image': None,
            'site_name': urlparse(url).netloc,
            'domain': urlparse(url).netloc,
            'error': str(e),
            'retrieved_at': datetime.utcnow().isoformat()
        }

def get_title(soup):
    """タイトル取得"""
    # Open Graph title
    og_title = soup.find('meta', property='og:title')
    if og_title and og_title.get('content'):
        return og_title['content']
    
    # Twitter title
    twitter_title = soup.find('meta', name='twitter:title')
    if twitter_title and twitter_title.get('content'):
        return twitter_title['content']
    
    # HTML title
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.get_text().strip()
    
    return 'タイトル不明'

def get_description(soup):
    """説明文取得"""
    # Open Graph description
    og_desc = soup.find('meta', property='og:description')
    if og_desc and og_desc.get('content'):
        return og_desc['content']
    
    # Twitter description
    twitter_desc = soup.find('meta', name='twitter:description')
    if twitter_desc and twitter_desc.get('content'):
        return twitter_desc['content']
    
    # Meta description
    meta_desc = soup.find('meta', name='description')
    if meta_desc and meta_desc.get('content'):
        return meta_desc['content']
    
    return '説明なし'

def get_favicon(soup, base_url):
    """ファビコン取得"""
    # Link rel="icon"
    favicon_link = soup.find('link', rel=lambda x: x and 'icon' in x.lower())
    if favicon_link and favicon_link.get('href'):
        return urljoin(base_url, favicon_link['href'])
    
    # デフォルトファビコン
    parsed_url = urlparse(base_url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"

def get_og_image(soup, base_url):
    """OG画像取得"""
    og_image = soup.find('meta', property='og:image')
    if og_image and og_image.get('content'):
        return urljoin(base_url, og_image['content'])
    
    # Twitter image
    twitter_image = soup.find('meta', name='twitter:image')
    if twitter_image and twitter_image.get('content'):
        return urljoin(base_url, twitter_image['content'])
    
    return None

def get_site_name(soup):
    """サイト名取得"""
    og_site_name = soup.find('meta', property='og:site_name')
    if og_site_name and og_site_name.get('content'):
        return og_site_name['content']
    
    return None

def get_domain_title(url):
    """ドメインからタイトル生成"""
    domain = urlparse(url).netloc
    return domain.replace('www.', '').title()
