import boto3
from typing import List
import json
from io import BytesIO

def load_aws_credentials(credential_file: str) -> dict:
    try:
        with open(credential_file, 'r') as f:
            credentials = json.load(f)
        return credentials
    except FileNotFoundError:
        print("Credential file not found.")
        raise
    except json.JSONDecodeError:
        print("Error decoding JSON in credential file.")
        raise

def create_s3_client(credentials: dict, region: str = 'us-west-2') -> boto3.client:
    return boto3.Session(
        aws_access_key_id=credentials['accessKeyId'],
        aws_secret_access_key=credentials['secretAccessKeyId'],
        region_name=region
    ).client('s3')

def list_s3_buckets(s3_client: boto3.client) -> List[dict]:
    try:
        response = s3_client.list_buckets()
        return response['Buckets']
    except Exception as e:
        print(f"Error listing S3 buckets: {e}")
        raise

def download_s3_file_to_memory(s3_client, bucket_name: str, file_key: str) -> BytesIO:
    try:
        file_obj = BytesIO()
        s3_client.download_fileobj(bucket_name, file_key, file_obj)
        
        file_obj.seek(0)
        
        return file_obj
    except Exception as e:
        print(f"Error downloading file from S3: {e}")
        raise

# if __name__ == "__main__":
#     credential_file = './.config/s3AwsAccessKey.json'
    
#     credentials = load_aws_credentials(credential_file)
    
#     s3_client = create_s3_client(credentials)
    
#     bucket_name = 'documento-s3'
#     file_key = 'sample-papers/cmcl,ws/2024/10.18653_v1_2024.cmcl-1.1.pdf'

#     file_obj = download_s3_file_to_memory(s3_client, bucket_name, file_key)

#     print(f"File downloaded to memory: {file_obj}")