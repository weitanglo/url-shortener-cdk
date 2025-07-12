import json
import boto3
import os
from decimal import Decimal
from boto3.dynamodb.conditions import Key

tableName = os.environ['URLSHORTNERTABLE_TABLE_NAME'] 
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tableName)
domainNameParam = os.environ['DOMAIN_NAME_PARAM']

def decimal_default(val):
    if isinstance(val, Decimal):
        return int(val)
    raise TypeError

def handler(event, context):
    """
    ユーザーのURL一覧取得（URL情報付き）
    Built with Amazon Q Developer
    """
    print(event)
    
    try:
        # ユーザーID取得
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

        # DynamoDBからユーザーのURL一覧を取得
        response = table.query(
            IndexName='createdByIndex',
            KeyConditionExpression=Key('createdBy').eq(user_id)
        )

        items = response['Items']
        
        # URL情報を含む形式に変換
        urls = []
        for item in items:
            url_data = {
                'id': item.get('id'),
                'shortCode': item.get('shortCode'),
                'originalUrl': item.get('originalUrl'),
                'shortUrl': f"https://{domainNameParam}/{item.get('shortCode')}",
                'createdAt': item.get('createdAt'),
                'clickCount': int(item.get('clickCount', 0)),
                'isActive': item.get('isActive', True),
                # URL情報を追加
                'urlInfo': {
                    'title': item.get('title', ''),
                    'description': item.get('description', ''),
                    'favicon': item.get('favicon', ''),
                    'image': item.get('image', ''),
                    'site_name': item.get('site_name', ''),
                    'domain': item.get('domain', ''),
                }
            }
            urls.append(url_data)
        
        # 作成日時でソート（新しい順）
        urls.sort(key=lambda x: x.get('createdAt', ''), reverse=True)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'urls': urls,
                'count': len(urls)
            }, default=decimal_default)
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

def get_user_id_from_token(event):
    """JWTトークンからユーザーIDを取得"""
    try:
        # Cognito JWT claims
        claims = event.get('requestContext', {}).get('authorizer', {}).get('jwt', {}).get('claims', {})
        user_id = claims.get('sub')
        
        if not user_id:
            # Fallback: email from claims
            user_id = claims.get('email')
        
        return user_id
    except Exception as e:
        print(f"Error getting user ID: {str(e)}")
        return None
