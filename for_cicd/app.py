from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from utils.test import generate_new_id

from src.test_chatbot import dummy_chatbot
from fastapi.middleware.cors import CORSMiddleware


# FastAPI 앱 생성
app = FastAPI(
    title="Vue.js Integration Backend",
    description="set path name",
    version="1.2.0"
)

origins = [
    "https://www.zelope.com",  # Route 53 연결된 도메인
    "http://localhost:8000"  # 로컬 개발 환경 (테스트용)
]

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, PATCH 등 모두 허용
    allow_headers=["*"],  # 모든 헤더 허용
)


# 데이터 모델 정의 (Pydantic)
class User(BaseModel):
    id: Optional[int] = None
    email: str
    name: str
    password:str
    
class Login_token(BaseModel):
    token: str
    password: str | None = None

# 임시 데이터 저장소
fake_db = {}

# ----------------- HTTP 메서드 예제 ------------------

#0. 기본

@app.get("/")
async def root():
    return {"message": "Hello World"}


#1. 회원가입
@app.post("/users")
def create_item(user: User):
    new_id = generate_new_id(fake_db)
    user.id = new_id
    fake_db[new_id] = user.dict()
    return {"message": "User created successfully", "user": fake_db[new_id]}


#2. 로그인

#2-1 소셜 로그인
@app.post("/login")
def create_item(Lt: Login_token):
    return {"message": "Social login"}

#2-2 토큰 재발급
@app.post("/reissue")
def create_item(Lt: Login_token):
    return {"message": "Token reissue"}

#2-3 소셜 로그인
@app.post("/logout")
def create_item(Lt: Login_token):
    return {"message": "Logout"}

@app.get("/ask")
def read_item(ask_query: str):
    chatbot = dummy_chatbot(ask_query)  # 클래스 인스턴스 생성
    answer = chatbot.reuturn_ANS()  # 인스턴스 메서드 호출
    return {"answer": answer}


# 6. Health Check (Vue.js와 연결 테스트)
@app.get("/health")
def health_check():
    return {"status": "Backend is up and running"}
