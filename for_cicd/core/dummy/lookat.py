# from fastapi import FastAPI, HTTPException, Depends, Response, Cookie, status
# from fastapi.responses import RedirectResponse, JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
# from typing import Optional
# from uuid import uuid4
# import os
# import requests

# # 환경 변수 로드
# load_dotenv()

# app = FastAPI()

# # CORS 설정
# origins = [
#     "http://localhost:5173",  # 프론트엔드가 실행되는 URL
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,  # 특정 도메인을 명시적으로 허용
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Google OAuth2 설정
# client_id = os.getenv("GOOGLE_CLIENT_ID")
# client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
# redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
# authorization_url = "https://accounts.google.com/o/oauth2/v2/auth"
# token_url = "https://oauth2.googleapis.com/token"
# user_info_url = "https://openidconnect.googleapis.com/v1/userinfo"

# # 세션 데이터를 저장할 딕셔너리 (임시)
# session_data = {}

# # 세션 ID를 생성하는 함수
# def generate_session_id():
#     return str(uuid4())

# @app.get("/login")
# def login():
#     # 구글 로그인 페이지로 리디렉션
#     return RedirectResponse(
#         f"{authorization_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope=openid%20email%20profile"
#     )

# @app.get("/auth/callback")
# def auth_callback(code: str, response: Response):
#     # 콜백 엔드포인트에서 구글에게 Access Token 요청
#     token_response = requests.post(
#         token_url,
#         data={
#             "code": code,
#             "client_id": client_id,
#             "client_secret": client_secret,
#             "redirect_uri": redirect_uri,
#             "grant_type": "authorization_code",
#         },
#     )
#     if token_response.status_code != 200:
#         raise HTTPException(status_code=token_response.status_code, detail="Failed to get token")
        
#     token_response_data = token_response.json()
#     access_token = token_response_data.get("access_token")
#     if not access_token:
#         raise HTTPException(status_code=400, detail="Invalid token")

#     # 구글에게 Access Token을 통해 사용자 정보 요청
#     user_info_response = requests.get(
#         user_info_url, headers={"Authorization": f"Bearer {access_token}"}
#     )
#     if user_info_response.status_code != 200:
#         raise HTTPException(status_code=user_info_response.status_code, detail="Failed to get user info")

#     user_info = user_info_response.json()

#     # 콘솔에 유저 정보 출력
#     print("User Info received from Google:", user_info)

#     # 세션 생성
#     session_id = generate_session_id()
#     session_data[session_id] = user_info

#     # 쿠키로 세션 아이디를 전달
#     response = RedirectResponse(url="http://localhost:5173/")
#     response.set_cookie(key="session_id", value=session_id, httponly=True)

#     return response

# @app.get("/user_info")
# def get_user_info(session_id: Optional[str] = Cookie(None)):
#     if session_id is None or session_id not in session_data:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="세션이 유효하지 않습니다.")
#     return session_data[session_id]


# @app.get("/logout")
# def logout(session_id: Optional[str] = Cookie(None), response: Response = None):
#     if session_id and session_id in session_data:
#         # 세션 데이터 삭제
#         del session_data[session_id]
#     # 쿠키 삭제
#     response = JSONResponse(content={"message": "Logged out successfully"})
#     response.delete_cookie(key="session_id")
#     return response


# @app.get("/")
# def read_root():
#     return {"message": "Hello, World!"}