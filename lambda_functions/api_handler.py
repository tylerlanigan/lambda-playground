"""
API Gateway Lambda Handler

Demonstrates HTTP request/response handling with API Gateway.
Shows path parameters, query strings, and JSON body parsing.
"""

import json
import os
from typing import Dict, Any


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for API Gateway HTTP requests.
    
    Args:
        event: API Gateway event containing HTTP request details
        context: Lambda context object
        
    Returns:
        API Gateway formatted response
    """
    try:
        # Extract HTTP method and path
        http_method = event.get('httpMethod', event.get('requestContext', {}).get('http', {}).get('method', 'GET'))
        path = event.get('path', event.get('rawPath', '/'))
        path_parameters = event.get('pathParameters') or {}
        query_string_parameters = event.get('queryStringParameters') or {}
        
        # Parse request body if present
        body = None
        if event.get('body'):
            try:
                body = json.loads(event['body'])
            except json.JSONDecodeError:
                body = event['body']
        
        # Build response data
        response_data = {
            'message': 'Hello from API Gateway Lambda!',
            'method': http_method,
            'path': path,
            'pathParameters': path_parameters,
            'queryParameters': query_string_parameters,
            'body': body,
            'headers': event.get('headers', {}),
            'requestId': context.request_id if context else 'local-test'
        }
        
        # Handle different routes
        if path == '/health' or path == '/health/':
            response_data['status'] = 'healthy'
            status_code = 200
        elif http_method == 'POST' and body:
            response_data['message'] = 'POST request received successfully'
            response_data['receivedData'] = body
            status_code = 201
        elif http_method == 'GET':
            status_code = 200
        else:
            status_code = 200
        
        # Return API Gateway formatted response
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            'body': json.dumps(response_data, indent=2)
        }
        
    except Exception as e:
        # Error handling
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }

