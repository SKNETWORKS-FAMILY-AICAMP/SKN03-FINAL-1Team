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
