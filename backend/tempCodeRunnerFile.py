from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv
import os
import logging
from fastapi.testclient import TestClient

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# .env 파일 로드
load_dotenv()

# 환경 변수에서 Google Client ID 가져오기
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

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

# 테스트 클라이언트 설정
client = TestClient(app)

def test_verify_token():
    # 클라이언트 ID 로그 출력
    print("Google Client ID:", GOOGLE_CLIENT_ID)
    
    # 실제 Google OAuth ID Token 설정
    test_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ5NzQwYTcwYjA5NzJkY2NmNzVmYTg4YmM1MjliZDE2YTMwNTczYmQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIyMjQ2NTQxMDQ4MDItbTNnbGdvYTVnMTI5MXNhNGxlZm1pbzdrdXFjamg3ZnEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIyMjQ2NTQxMDQ4MDItbTNnbGdvYTVnMTI5MXNhNGxlZm1pbzdrdXFjamg3ZnEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTIzNDA0NDAzOTIxMjQ3MTMwMTAiLCJlbWFpbCI6ImRic2doazMyMEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6ImF4MGdOcjBYMmRQdXphTmZBVGRfWnciLCJuYW1lIjoi7KeE7Jyk7ZmUIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xGUHJVRmduMjNnQ3pZRkxCa21NblFPbU8tU3JRdXlNd3ZUcl9LbzFXQW9rcndGUT1zOTYtYyIsImdpdmVuX25hbWUiOiLsnKTtmZQiLCJmYW1pbHlfbmFtZSI6IuynhCIsImlhdCI6MTczMjE4NTExMSwiZXhwIjoxNzMyMTg4NzExfQ.B1IJq1Wn3GK3lEBAZJeiCrymk3_IL38n-_Rwdf6ytZKnht0aSe6Cy3jreD1XhHRSNXIWh4tmU80WI09Bv-oYJ5_O0DYHZW0g0vv6JtQdfplGSL-bSGXUmntO4dRtDRKRTc879BS2URorQH0hKHwAaHp43sim20xyb1exGHOw4SA5Op6yTPfRHXKM5HlA5gIEmwoii1ecNyjiLvKLlXQ5RBsgFWd7Npp5dvsSC9IxeCAscu782szUi0sSBO6dWHLK_gvsKQqaR8hvJXBIvtztTK_Qp5b1BBSoAwOnimfiQnGVvXUM78Awgu4cpRBUzT-zzcYzLDbx86thXmiV08oIsA"
    
    response = client.post("/verify-token/", json={"token": test_token})
    
    assert response.status_code == 200, response.text
    data = response.json()
    
    assert data["status"] == "success"
    assert "user_id" in data
    assert "user_info" in data

    # 검증 결과를 콘솔에 출력
    print("Response Data:", data)

if __name__ == "__main__":
    test_verify_token()
