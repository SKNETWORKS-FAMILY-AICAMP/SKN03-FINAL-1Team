<<<<<<< HEAD
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
=======
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv
import os
import logging
from fastapi.middleware.cors import CORSMiddleware

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS 설정 추가
origins = [
    "http://localhost:8080",
    "http://localhost:5173",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# .env 파일 로드
load_dotenv()

# 환경 변수에서 Google Client ID 가져오기
GOOGLE_ = os.getenv("GOOGLE_CLIENT_ID")

class Token(BaseModel):
    token: str

@app.post("/verify-token/")
async def verify_token(token: Token):
    logger.info("Token: %s", token.token)
    
    try:
        # Token을 검증합니다
        id_info = id_token.verify_oauth2_token(token.token, requests.Request(), GOOGLE_CLIENT_ID)
        
        # Token이 유효한 경우 사용자 정보를 반환합니다
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        user_id = id_info['sub']
        logger.info("User ID: %s", user_id)
        return {"status": "success", "user_id": user_id, "user_info": id_info}

    except ValueError as e:
        logger.error("Token validation error: %s", e)
        # Token이 유효하지 않은 경우
        raise HTTPException(status_code=401, detail="Invalid token")
>>>>>>> a08fef817b7365195cddf428e8618dbb7745344e
