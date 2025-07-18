import json
import os
import boto3
import uuid
import random
import string
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin

# DynamoDB setup
dynamodb = boto3.resource('dynamodb')
url_table_name = os.environ['URLSHORTNERTABLE_TABLE_NAME']
url_info_table_name = os.environ.get('URLINFOTABLE_TABLE_NAME')
url_table = dynamodb.Table(url_table_name)
url_info_table = dynamodb.Table(url_info_table_name) if url_info_table_name else None
domain_name = os.environ.get('DOMAIN_NAME_PARAM', 'localhost')

def handler(event, context):
    """
    拡張版URL短縮作成関数 (キャッシュ機能付き)
    元サイト情報も同時に取得・保存
    Built with Amazon Q Developer
    """
    
    try:
        # 認証情報取得
        user_id = get_user_id_from_token(event)
        if not user_id:
            return {
                'statusCode': 401,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Unauthorized'})
            }
        
        # リクエストボディ解析
        body = json.loads(event['body']) if event.get('body') else {}
        original_url = body.get('url')
        custom_code = body.get('customCode')
        
        if not original_url:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'URL is required'})
            }
        
        # URL情報を取得（キャッシュ確認 → 新規取得）
        print(f"Getting URL info for: {original_url}")
        url_info = get_or_fetch_url_info(original_url)
        
        # 短縮コード生成
        short_code = custom_code if custom_code else generate_short_code()
        
        # 重複チェック
        if check_short_code_exists(short_code):
            return {
                'statusCode': 409,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Short code already exists'})
            }
        
        # URL短縮データ作成
        url_id = str(uuid.uuid4())
        
        url_data = {
            'id': url_id,
            'shortCode': short_code,
            'originalUrl': original_url,
            'createdBy': user_id,
            'createdAt': datetime.utcnow().isoformat(),
            'clickCount': 0,
            'isActive': True,
            # URL情報を追加
            'title': url_info.get('title', ''),
            'description': url_info.get('description', ''),
            'favicon': url_info.get('favicon', ''),
            'image': url_info.get('image', ''),
            'site_name': url_info.get('site_name', ''),
            'domain': url_info.get('domain', ''),
        }
        
        # DynamoDBに保存
        url_table.put_item(Item=url_data)
        
        # レスポンス
        short_url = f"https://{domain_name}/{short_code}"
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'id': url_id,
                'shortUrl': short_url,
                'shortCode': short_code,
                'originalUrl': original_url,
                'urlInfo': {
                    'title': url_info.get('title', ''),
                    'description': url_info.get('description', ''),
                    'favicon': url_info.get('favicon', ''),
                    'image': url_info.get('image', ''),
                    'site_name': url_info.get('site_name', ''),
                    'domain': url_info.get('domain', ''),
                },
                'createdAt': url_data['createdAt'],
                'cached': url_info.get('cached', False)
            })
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

def get_or_fetch_url_info(url):
    """
    URL情報をキャッシュから取得、なければ新規取得
    """
    if not url_info_table:
        print("No cache table, fetching directly")
        return fetch_url_info(url)
    
    try:
        # キャッシュから取得
        print(f"Checking cache for: {url}")
        response = url_info_table.get_item(Key={'url': url})
        
        if 'Item' in response:
            item = response['Item']
            print(f"Found cached item: {item.get('title', 'No title')}")
            
            # TTLチェック（7日以内）
            retrieved_at = datetime.fromisoformat(item['retrieved_at'])
            if datetime.utcnow() - retrieved_at < timedelta(days=7):
                print("Cache is fresh, using cached data")
                item['cached'] = True
                return item
            else:
                print("Cache expired, fetching new data")
        
        # キャッシュにない、または期限切れの場合は新規取得
        url_info = fetch_url_info(url)
        
        # キャッシュに保存
        if url_info and not url_info.get('error'):
            cache_item = url_info.copy()
            cache_item['ttl'] = int((datetime.utcnow() + timedelta(days=7)).timestamp())
            
            print(f"Saving to cache: {cache_item.get('title', 'No title')}")
            url_info_table.put_item(Item=cache_item)
        
        url_info['cached'] = False
        return url_info
        
    except Exception as e:
        print(f"Cache error: {str(e)}")
        return fetch_url_info(url)

def fetch_url_info(url):
    """
    URLから情報を取得（エラーハンドリング強化版）
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; URL-Shortener-Bot/1.0; +https://url.loweitang.com)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        print(f"Making request to: {url}")
        response = requests.get(
            url, 
            headers=headers, 
            timeout=15, 
            allow_redirects=True,
            verify=True,
            stream=False
        )
        response.raise_for_status()
        
        print(f"Response status: {response.status_code}, Content-Type: {response.headers.get('content-type', 'unknown')}")
        
        # Content-Typeチェック
        content_type = response.headers.get('content-type', '').lower()
        if 'text/html' not in content_type and 'application/xhtml' not in content_type:
            print(f"Non-HTML content type: {content_type}")
            return get_fallback_info(url, "Non-HTML content")
        
        # HTMLパース
        soup = BeautifulSoup(response.content, 'html.parser')
        
        url_info = {
            'url': url,
            'title': get_title(soup),
            'description': get_description(soup),
            'favicon': get_favicon(soup, url),
            'image': get_og_image(soup, url),
            'site_name': get_site_name(soup),
            'domain': urlparse(url).netloc,
            'retrieved_at': datetime.utcnow().isoformat(),
            'status_code': response.status_code,
            'content_type': content_type
        }
        
        print(f"Successfully extracted info: {url_info.get('title', 'No title')}")
        return url_info
        
    except requests.exceptions.Timeout:
        print(f"Timeout error for: {url}")
        return get_fallback_info(url, "Request timeout")
    except requests.exceptions.ConnectionError:
        print(f"Connection error for: {url}")
        return get_fallback_info(url, "Connection failed")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error for {url}: {e}")
        return get_fallback_info(url, f"HTTP {e.response.status_code}")
    except Exception as e:
        print(f"Unexpected error for {url}: {str(e)}")
        return get_fallback_info(url, str(e))

def get_fallback_info(url, error_msg):
    """
    エラー時のフォールバック情報
    """
    return {
        'url': url,
        'title': get_domain_title(url),
        'description': f'サイト情報を取得できませんでした: {error_msg}',
        'favicon': get_default_favicon(url),
        'image': None,
        'site_name': urlparse(url).netloc,
        'domain': urlparse(url).netloc,
        'retrieved_at': datetime.utcnow().isoformat(),
        'error': error_msg
    }

def get_title(soup):
    """タイトル取得（優先順位付き）"""
    # Open Graph title
    og_title = soup.find('meta', property='og:title')
    if og_title and og_title.get('content'):
        return clean_text(og_title['content'])
    
    # Twitter title
    twitter_title = soup.find('meta', name='twitter:title')
    if twitter_title and twitter_title.get('content'):
        return clean_text(twitter_title['content'])
    
    # HTML title
    title_tag = soup.find('title')
    if title_tag:
        return clean_text(title_tag.get_text())
    
    return 'タイトル不明'

def get_description(soup):
    """説明文取得（優先順位付き）"""
    # Open Graph description
    og_desc = soup.find('meta', property='og:description')
    if og_desc and og_desc.get('content'):
        return clean_text(og_desc['content'])
    
    # Twitter description
    twitter_desc = soup.find('meta', name='twitter:description')
    if twitter_desc and twitter_desc.get('content'):
        return clean_text(twitter_desc['content'])
    
    # Meta description
    meta_desc = soup.find('meta', name='description')
    if meta_desc and meta_desc.get('content'):
        return clean_text(meta_desc['content'])
    
    return '説明なし'

def get_favicon(soup, base_url):
    """ファビコン取得（複数パターン対応）"""
    # Link rel="icon"
    favicon_selectors = [
        'link[rel="icon"]',
        'link[rel="shortcut icon"]',
        'link[rel="apple-touch-icon"]',
        'link[rel="apple-touch-icon-precomposed"]'
    ]
    
    for selector in favicon_selectors:
        favicon_link = soup.select_one(selector)
        if favicon_link and favicon_link.get('href'):
            return urljoin(base_url, favicon_link['href'])
    
    # デフォルトファビコン
    return get_default_favicon(base_url)

def get_default_favicon(base_url):
    """デフォルトファビコンURL生成"""
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
        return clean_text(og_site_name['content'])
    
    return None

def get_domain_title(url):
    """ドメインからタイトル生成"""
    domain = urlparse(url).netloc
    return domain.replace('www.', '').title()

def clean_text(text):
    """テキストクリーニング"""
    if not text:
        return ''
    return ' '.join(text.strip().split())

def get_user_id_from_token(event):
    """JWTトークンからユーザーIDを取得"""
    try:
        claims = event.get('requestContext', {}).get('authorizer', {}).get('jwt', {}).get('claims', {})
        return claims.get('sub')
    except:
        return None

def generate_short_code(length=6):
    """短縮コード生成"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def check_short_code_exists(short_code):
    """短縮コード重複チェック"""
    try:
        response = url_table.query(
            IndexName='UniqueKeyIndex',
            KeyConditionExpression='shortCode = :shortCode',
            ExpressionAttributeValues={':shortCode': short_code}
        )
        return len(response['Items']) > 0
    except Exception as e:
        print(f"Error checking short code: {str(e)}")
        return False
