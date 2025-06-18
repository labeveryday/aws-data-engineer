"""
Amazon Bedrock Client for AWS Data Engineer Course

This module provides utilities for interacting with Amazon Bedrock and Claude models.
"""

import boto3
import json
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError, NoCredentialsError
import os


class BedrockClient:
    """Client for interacting with Amazon Bedrock."""
    
    def __init__(self, region: str = None, profile: str = None):
        """
        Initialize the Bedrock client.
        
        Args:
            region: AWS region (defaults to environment variable or us-west-2)
            profile: AWS profile name (defaults to environment variable or default)
        """
        self.region = region or os.getenv('BEDROCK_REGION', 'us-west-2')
        self.profile = profile or os.getenv('AWS_PROFILE', 'default')
        
        try:
            # Create session with profile if specified
            if self.profile != 'default':
                session = boto3.Session(profile_name=self.profile)
                self.bedrock_runtime = session.client(
                    'bedrock-runtime',
                    region_name=self.region
                )
            else:
                self.bedrock_runtime = boto3.client(
                    'bedrock-runtime',
                    region_name=self.region
                )
                
            # Test the connection
            self._test_connection()
            
        except NoCredentialsError:
            raise Exception("AWS credentials not found. Please configure your credentials.")
        except ClientError as e:
            raise Exception(f"Failed to initialize Bedrock client: {str(e)}")
    
    def _test_connection(self):
        """Test the Bedrock connection."""
        try:
            # Try to list foundation models to test connection
            bedrock = boto3.client('bedrock', region_name=self.region)
            bedrock.list_foundation_models()
        except ClientError as e:
            if e.response['Error']['Code'] == 'UnauthorizedOperation':
                raise Exception("Access denied to Bedrock. Please check your permissions.")
            else:
                raise Exception(f"Bedrock connection test failed: {str(e)}")
    
    def invoke_claude(self, 
                     prompt: str, 
                     model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
                     max_tokens: int = 4000,
                     temperature: float = 0.1) -> str:
        """
        Invoke Claude model with a prompt.
        
        Args:
            prompt: The prompt to send to Claude
            model_id: The Claude model ID
            max_tokens: Maximum tokens in response
            temperature: Temperature for response generation
            
        Returns:
            Claude's response text
        """
        try:
            # Prepare the request body
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            # Invoke the model
            response = self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(body),
                contentType='application/json'
            )
            
            # Parse the response
            response_body = json.loads(response['body'].read())
            
            if 'content' in response_body and response_body['content']:
                return response_body['content'][0]['text']
            else:
                return "No response generated"
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ValidationException':
                raise Exception(f"Invalid request to Bedrock: {str(e)}")
            elif error_code == 'AccessDeniedException':
                raise Exception("Access denied to Claude model. Please check your permissions and model access.")
            else:
                raise Exception(f"Bedrock API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error invoking Claude: {str(e)}")
    
    def check_model_access(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0") -> bool:
        """
        Check if the specified model is accessible.
        
        Args:
            model_id: The model ID to check
            
        Returns:
            True if model is accessible, False otherwise
        """
        try:
            # Try a simple test invocation
            test_prompt = "Hello"
            self.invoke_claude(test_prompt, model_id, max_tokens=10)
            return True
        except Exception:
            return False
    
    def get_available_models(self) -> list:
        """
        Get list of available foundation models.
        
        Returns:
            List of available model information
        """
        try:
            bedrock = boto3.client('bedrock', region_name=self.region)
            response = bedrock.list_foundation_models()
            
            # Filter for Claude models
            claude_models = []
            for model in response.get('modelSummaries', []):
                if 'claude' in model.get('modelId', '').lower():
                    claude_models.append({
                        'modelId': model.get('modelId'),
                        'modelName': model.get('modelName'),
                        'providerName': model.get('providerName')
                    })
            
            return claude_models
            
        except ClientError as e:
            raise Exception(f"Error listing models: {str(e)}")


def get_bedrock_client() -> BedrockClient:
    """
    Get a configured Bedrock client instance.
    
    Returns:
        BedrockClient instance
    """
    return BedrockClient()


def test_bedrock_connection() -> Dict[str, Any]:
    """
    Test the Bedrock connection and return status information.
    
    Returns:
        Dictionary with connection status and details
    """
    try:
        client = get_bedrock_client()
        
        # Test model access
        model_id = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')
        model_accessible = client.check_model_access(model_id)
        
        return {
            'status': 'success',
            'region': client.region,
            'profile': client.profile,
            'model_accessible': model_accessible,
            'model_id': model_id
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }
