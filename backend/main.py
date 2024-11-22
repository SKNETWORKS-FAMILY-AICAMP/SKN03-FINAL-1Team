from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os
import requests

# 환경 변수 로드
load_dotenv()

app = FastAPI()

# Google OAuth2 설정
client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
authorization_url = "https://accounts.google.com/o/oauth2/v2/auth"
token_url = "https://oauth2.googleapis.com/token"
user_info_url = "https://openidconnect.googleapis.com/v1/userinfo"

@app.get("/login")
def login():
    return RedirectResponse(
        f"{authorization_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope=openid%20email%20profile"
    )

@app.get("/auth/callback")
def auth_callback(code: str):
    token_response = requests.post(
        token_url,
        data={
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
    )
    token_response_data = token_response.json()

    access_token = token_response_data.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Invalid token")

    user_info_response = requests.get(
        user_info_url, headers={"Authorization": f"Bearer {access_token}"}
    )
    user_info = user_info_response.json()

    return user_info

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
