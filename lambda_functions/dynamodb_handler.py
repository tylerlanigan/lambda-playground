"""
DynamoDB Integration Lambda Handler

Demonstrates DynamoDB read/write operations using boto3.
Shows AWS SDK usage and environment variable configuration.
Loads credentials from .env file (local) or IAM role (AWS).
"""

import json
import os
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables from .env file (for local testing)
load_dotenv()

# Initialize DynamoDB client
# In AWS, credentials come from IAM role
# Locally, credentials come from .env file or AWS credentials file
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)

# Get table name from environment variable
TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME', 'lambda-playground-table')


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for DynamoDB operations.
    
    Supports the following operations via event:
    - GET: Retrieve item by key
    - PUT: Create or update item
    - DELETE: Delete item by key
    - LIST: List all items (scan)
    
    Args:
        event: Event containing operation type and data
        context: Lambda context object
        
    Returns:
        Dictionary with operation results
    """
    try:
        # Get table reference
        table = dynamodb.Table(TABLE_NAME)
        
        # Extract operation from event
        operation = event.get('operation', event.get('httpMethod', 'GET')).upper()
        
        if operation == 'GET' or operation == 'READ':
            # Read item
            key = event.get('key', {})
            if not key:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'error': 'Key is required for GET operation',
                        'event': event
                    })
                }
            
            try:
                response = table.get_item(Key=key)
                item = response.get('Item')
                
                if item:
                    return {
                        'statusCode': 200,
                        'body': json.dumps({
                            'message': 'Item retrieved successfully',
                            'item': item
                        }, default=str)
                    }
                else:
                    return {
                        'statusCode': 404,
                        'body': json.dumps({
                            'message': 'Item not found',
                            'key': key
                        })
                    }
            except ClientError as e:
                return {
                    'statusCode': 500,
                    'body': json.dumps({
                        'error': 'DynamoDB error',
                        'message': str(e)
                    })
                }
        
        elif operation == 'PUT' or operation == 'CREATE' or operation == 'UPDATE':
            # Create or update item
            item = event.get('item', event.get('body', {}))
            
            # If body is a string, parse it
            if isinstance(item, str):
                item = json.loads(item)
            
            if not item:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'error': 'Item data is required for PUT operation',
                        'event': event
                    })
                }
            
            try:
                table.put_item(Item=item)
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Item created/updated successfully',
                        'item': item
                    }, default=str)
                }
            except ClientError as e:
                return {
                    'statusCode': 500,
                    'body': json.dumps({
                        'error': 'DynamoDB error',
                        'message': str(e)
                    })
                }
        
        elif operation == 'DELETE':
            # Delete item
            key = event.get('key', {})
            if not key:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'error': 'Key is required for DELETE operation',
                        'event': event
                    })
                }
            
            try:
                response = table.delete_item(Key=key)
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Item deleted successfully',
                        'key': key
                    })
                }
            except ClientError as e:
                return {
                    'statusCode': 500,
                    'body': json.dumps({
                        'error': 'DynamoDB error',
                        'message': str(e)
                    })
                }
        
        elif operation == 'LIST' or operation == 'SCAN':
            # List all items (scan)
            try:
                response = table.scan()
                items = response.get('Items', [])
                
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': f'Retrieved {len(items)} item(s)',
                        'count': len(items),
                        'items': items
                    }, default=str)
                }
            except ClientError as e:
                return {
                    'statusCode': 500,
                    'body': json.dumps({
                        'error': 'DynamoDB error',
                        'message': str(e)
                    })
                }
        
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': f'Unsupported operation: {operation}',
                    'supportedOperations': ['GET', 'PUT', 'DELETE', 'LIST']
                })
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e),
                'tableName': TABLE_NAME
            })
        }

