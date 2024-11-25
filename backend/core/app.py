from fastapi import FastAPI, HTTPException, Query, Request, Header

from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from fastapi.responses import JSONResponse
import uvicorn
from src import *
from src.reqeust_model import *
from typing import Annotated

app = FastAPI(
    title="FIX : API with dummy",
    description="",
    version="2.2.0"
)

#기본 baseurl : https://api.documento.click
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.documento.click"],  # 프론트엔드 서브 도메인
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
    allow_credentials=True,  # 인증 정보 허용 (쿠키 등)
)



# ********************************************* #
# ******************  Utils  ****************** #
# ********************************************* #

"""
기본 리턴 형태
"response" : {
	"resultCode" : 200,
	"message" : "Search completed successfully",
	"result" : { .... }
}
"""


async def handle_request(func, data=None):
    try:
        return await func(data)
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                    "resultCode" : e.status_code,
                    "message" : str(e),
                    "result" : []
                    
                        }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                    "resultCode" : 500,
                    "message" : str(e),
                    "result" : []
                    
                        }
        )
        
        

# ********************************************* #
# ***************  About  User  *************** #
# ********************************************* #


# 1. 회원가입
@app.get("/users")
async def create_user(request: Request):
    data = await request.json()
    return await handle_request(create_new_user, data)


# 2. 로그인
@app.get("/login")
async def login():
    return await handle_request(login_user)

# 회원가입/로그인 용
@app.get("/auth/callback")
async def auth_callback(code: str = Query(..., description="OAuth2 code for login")):
    return await handle_request(oauth_callback, {"code": code})



# ********************************************* #
# ***************  About Paper  *************** #
# ********************************************* #

# 3. 논문검색
@app.post("/papers/search/")
async def search_papers(data: userKeyword):
    #data = await request.json()
    return await handle_request(process_search, data)

# 4. 키워드 최적화
@app.post("/papers/transformation/")
async def create_paper_transformation(data: userPrompt):
    #data = await request.json()
    return await handle_request(process_transformation, data)



# ***************  5. bookmark  *************** #
# 5.1. 북마크 리스트
@app.get("/papers/bookmarks/")
async def get_user_bookmarks(request: Request):
    headers = request.headers
    
    return await handle_request(fetch_user_bookmarks, headers)


# 멘토님 曰 : 추가와 삭제는 같은 방식의 post
@app.post("/papers/bookmarks/")
#쿼리문 형태 : ?paperDoi=”string”
async def add_to_bookmarks(request: Request):
    body = await request.body()
    if not body:
        raise HTTPException(status_code=400, detail="Request body is empty")
    
    data = await request.json()
    headers = request.headers
    return await handle_request(handle_bookmark, headers,data)

# ********************************************* #

# 6. 논문 선택
# notion에는 /papers/?paperDoi=”string” 이렇게 적혀있음 
@app.get("/papers/select/")
async def get_paper_by_doi(paperDoi: str = "default"):
    print(paperDoi)
    print(type(paperDoi))
    return await handle_request(fetch_paper_details, paperDoi)

#7. 논문 요약
@app.post("/papers/summary/")
async def create_paper_summary(data: paperDoi):
    return await handle_request(process_summary, data)

#8. 선행 논문 리스트
@app.get("/papers/priorpapers/")
#쿼리문 : ?paperDoi=”string”
async def get_prior_papers(paperDoi: str = "default"):
    return await handle_request(fetch_prior_papers, paperDoi)



# ********************************************* #
# ***************  health check *************** #
# ********************************************* #

@app.get("/health")
def health_check():
    return {"status": "Backend is up and running"}

@app.get("/")
def welcome_check():
    return {"status": "Welcome to documento"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)