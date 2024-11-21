from fastapi.testclient import TestClient
from main import app  # main.py 파일에서 FastAPI 앱을 가져옵니다
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 환경 변수에서 Google Client ID 가져오기
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

client = TestClient(app)

def test_verify_token():
    # 클라이언트 ID 로그 출력
    print("Google Client ID:", GOOGLE_CLIENT_ID)
    
    # 실제 Google OAuth ID Token 설정
    test_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ5NzQwYTcwYjA5NzJkY2NmNzVmYTg4YmM1MjliZDE2YTMwNTczYmQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIyMjQ2NTQxMDQ4MDItbTNnbGdvYTVnMTI5MXNhNGxlZm1pbzdrdXFjamg3ZnEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIyMjQ2NTQxMDQ4MDItbTNnbGdvYTVnMTI5MXNhNGxlZm1pbzdrdXFjamg3ZnEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTIzNDA0NDAzOTIxMjQ3MTMwMTAiLCJlbWFpbCI6ImRic2doazMyMEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6InRsWHl6Q29QXzRLRXBUdHlwanBXVkEiLCJuYW1lIjoi7KeE7Jyk7ZmUIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xGUHJVRmduMjNnQ3pZRkxCa21NblFPbU8tU3JRdXlNd3ZUcl9LbzFXQW9rcndGUT1zOTYtYyIsImdpdmVuX25hbWUiOiLsnKTtmZQiLCJmYW1pbHlfbmFtZSI6IuynhCIsImlhdCI6MTczMjE4MDk1NCwiZXhwIjoxNzMyMTg0NTU0fQ.arxvzOy9qZRuaGdUzBZ2OdY4fFeVWGw3r-Xu-3UIC7RSPrnxRejcTOEEyEYfXuBgvV4DweeK-glmtxAVVCrNTMoy9ESk6NinQtqlnHgohdvuAUpIiHblEBai2bd8rDtCDDCoOQGzaB2EGg6A8ImeumWAc6vBi0pkeDm0ygZsL8cs9uYNH6hyL_0LJWZpLxgmc2YtnpJZeKfoSZjMUnuXP3gNPhRDtLdXRpWRlM-vAEUH9RbkqYCCHswyMxe5qhTEFfJ8DeGjEJ-Wsn2SZN0a9o6J6fB9RkpLQg1J0O2RqTTYQP02yCQdmZmyP8N_q-Q286JsY3PqONjGYelWuneYzQ"

    response = client.post("/verify-token/", json={"token": test_token})
    
    assert response.status_code == 200, response.text
    data = response.json()
    
    assert data["status"] == "success"
    assert "user_id" in data
    assert "user_info" in data

if __name__ == "__main__":
    test_verify_token()
