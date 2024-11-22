import json


class googleOAuth:
    def __init__(self, credential_file: str = "../../../.config/googleOAuthKey.json"):
        """
        Initialize GoogleOAuth with credentials from a JSON file.
        """
        self.credential_file = credential_file
        self.authorization_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"
        self.user_info_url = "https://openidconnect.googleapis.com/v1/userinfo"
        self._load_credentials()
    
    def _load_credentials(self):
        """
        Load Google OAuth credentials from a JSON file.
        """
        try:
            with open(self.credential_file, "r") as f:
                credentials = json.load(f)
            self.client_id = credentials.get("GOOGLE_CLIENT_ID")
            self.client_secret = credentials.get("GOOGLE_CLIENT_SECRET")
            self.redirect_uri = credentials.get("GOOGLE_REDIRECT_URI")

        except FileNotFoundError:
            raise FileNotFoundError("Credential file not found.")
        except json.JSONDecodeError:
            raise ValueError("Error decoding JSON in credential file.")