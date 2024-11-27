import json
import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError

class googleOAuth:
    def __init__(self):
        """
        Initialize GoogleOAuth with credentials from aws ssm.
        """
        self.authorization_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"
        self.user_info_url = "https://openidconnect.googleapis.com/v1/userinfo"
        self._load_credentials()
    
    def _load_credentials(self):
        """
        Load Google OAuth credentials from aws ssm and initialize connection details.
        """
        try:
            ssm = boto3.client('ssm')

            parameter = ssm.get_parameter(Name='/DOCUMENTO/KEY/GOOGLE_OAUTH_KEY/GOOGLE_CLIENT_ID', WithDecryption=True)
            self.client_id = parameter['Parameter']['Value']

            parameter = ssm.get_parameter(Name='/DOCUMENTO/KEY/GOOGLE_OAUTH_KEY/GOOGLE_CLIENT_SECRET', WithDecryption=True)
            self.client_secret = parameter['Parameter']['Value']

            parameter = ssm.get_parameter(Name='/DOCUMENTO/KEY/GOOGLE_OAUTH_KEY/GOOGLE_REDIRECT_URI', WithDecryption=True)
            self.redirect_uri = parameter['Parameter']['Value']

        except (BotoCoreError, ClientError) as e:
            print(f"Error retrieving parameter from SSM: {e}")
            raise