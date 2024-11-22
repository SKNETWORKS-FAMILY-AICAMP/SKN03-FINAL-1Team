import boto3
from typing import List
import json
from io import BytesIO


class S3Handler:
    def __init__(self, credential_file: str = "../../../.config/s3AwsAccessKey.json"):
        """
        Initialize the S3Handler with credentials from a JSON file and region.
        """
        self.credential_file = credential_file
        self.s3_client = None
        self._load_credentials_and_create_client()

    def _load_credentials_and_create_client(self):
        """
        Load AWS credentials from a file and initialize the S3 client.
        """
        try:
            with open(self.credential_file, "r") as f:
                credentials = json.load(f)

            self.s3_client = boto3.Session(
                aws_access_key_id=credentials["accessKeyId"],
                aws_secret_access_key=credentials["secretAccessKeyId"],
                region_name=credentials["region"]
            ).client("s3")
        except FileNotFoundError:
            raise FileNotFoundError("Credential file not found.")
        except json.JSONDecodeError:
            raise ValueError("Error decoding JSON in credential file.")
        except Exception as e:
            raise RuntimeError(f"Error creating S3 client: {e}")

    def list_buckets(self) -> List[dict]:
        """
        List all S3 buckets in the account.
        """
        try:
            response = self.s3_client.list_buckets()
            return response.get("Buckets", [])
        except Exception as e:
            raise RuntimeError(f"Error listing S3 buckets: {e}")

    def download_file_to_memory(self, file_key: str, bucket_name: str = "documento-s3") -> BytesIO:
        """
        Download a file from S3 into memory as a BytesIO object.
        """
        try:
            file_obj = BytesIO()
            self.s3_client.download_fileobj(bucket_name, file_key, file_obj)
            file_obj.seek(0)
            return file_obj
        except Exception as e:
            raise RuntimeError(f"Error downloading file from S3: {e}")


# if __name__ == "__main__":
#     file_key = "sample-papers/cmcl,ws/2024/10.18653_v1_2024.cmcl-1.1.pdf"

#     try:
#         s3_handler = S3Handler()

#         buckets = s3_handler.list_buckets()
#         print(f"S3 Buckets: {buckets}")

#         file_obj = s3_handler.download_file_to_memory(file_key)
#         print(f"File downloaded to memory: {file_obj}")
#     except Exception as e:
#         print(f"Error: {e}")