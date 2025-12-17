"""
S3 Event-Driven Lambda Handler

Processes S3 PUT events and demonstrates event-driven architecture.
Shows event parsing and error handling.
"""

import json
import os
from typing import Dict, Any
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file (for local testing)
load_dotenv()

# Initialize S3 client
# In AWS, credentials come from IAM role
# Locally, credentials come from .env file or AWS credentials file
s3_client = boto3.client(
    's3',
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for S3 event notifications.
    
    Args:
        event: S3 event notification containing bucket and object information
        context: Lambda context object
        
    Returns:
        Dictionary with processing results
    """
    results = []
    
    try:
        # S3 events come in a Records array
        records = event.get('Records', [])
        
        if not records:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'No S3 records found in event',
                    'event': event
                })
            }
        
        for record in records:
            try:
                # Extract S3 event details
                event_name = record.get('eventName', '')
                s3_data = record.get('s3', {})
                bucket_name = s3_data.get('bucket', {}).get('name', '')
                object_key = s3_data.get('object', {}).get('key', '')
                object_size = s3_data.get('object', {}).get('size', 0)
                
                # Process the event
                result = {
                    'eventName': event_name,
                    'bucket': bucket_name,
                    'key': object_key,
                    'size': object_size,
                    'processed': True
                }
                
                # Example: Only process PUT events
                if 'ObjectCreated' in event_name or 'Put' in event_name:
                    # Get object metadata
                    try:
                        response = s3_client.head_object(
                            Bucket=bucket_name,
                            Key=object_key
                        )
                        result['contentType'] = response.get('ContentType', 'unknown')
                        result['lastModified'] = str(response.get('LastModified', ''))
                        result['metadata'] = response.get('Metadata', {})
                    except Exception as e:
                        result['error'] = f'Failed to get object metadata: {str(e)}'
                    
                    result['message'] = f'Successfully processed S3 object: {object_key}'
                else:
                    result['message'] = f'Event {event_name} not processed (only processing PUT events)'
                    result['processed'] = False
                
                results.append(result)
                
            except Exception as e:
                # Handle errors for individual records
                results.append({
                    'error': str(e),
                    'record': record,
                    'processed': False
                })
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Processed {len(records)} S3 event(s)',
                'results': results,
                'requestId': context.request_id if context else 'local-test'
            }, indent=2)
        }
        
    except Exception as e:
        # Handle overall errors
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Failed to process S3 events',
                'message': str(e),
                'event': event
            })
        }

