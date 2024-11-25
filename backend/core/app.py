from fastapi import FastAPI, HTTPException, Query, Request
from typing import List, Optional
from fastapi.responses import JSONResponse
import uvicorn
from src import *

app = FastAPI(
    title="FIX : api func renewal",
    description="",
    version="2.0.2"
)


#기본 baseurl : https://api.documento.click


# ********************************************* #
# ******************  Utils  ****************** #
# ********************************************* #

async def handle_request(func, data=None):
    try:
        return await func(data)
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"statusCode": e.status_code, "message": str(e.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"statusCode": 500, "message": str(e)}
        )
        

# ********************************************* #
# ***************  About  User  *************** #
# ********************************************* #


# 1. 회원가입
@app.post("/users")
async def create_user(request: Request):
    data = await request.json()
    return await handle_request(create_new_user, data)


# 2. 로그인
@app.post("/login")
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
@app.post("/papers/search")
async def search_papers(request: Request):
    data = await request.json()
    return await handle_request(process_search, data)

# 4. 키워드 최적화
@app.post("/papers/transformation")
async def create_paper_transformation(request: Request):
    data = await request.json()
    return await handle_request(process_transformation, data)



# ***************  5. bookmark  *************** #
@app.get("/papers/bookmarks")
async def get_user_bookmarks(userId: int = Query(..., description="User ID for fetching bookmarked papers")):
    return await handle_request(fetch_user_bookmarks, {"userId": userId})


# 멘토님 曰 : 추가와 삭제는 같은 방식의 post
@app.post("/papers/bookmarks")
#쿼리문 형태 : ?paperDoi=”string”
async def add_to_bookmarks(request: Request):
    data = await request.json()
    return await handle_request(add_bookmark, data)

# ********************************************* #

# 6. 논문 선택
# notion에는 /papers/?paperDoi=”string” 이렇게 적혀있음 
@app.get("/papers")
async def get_paper_by_doi(paperDoi: str = Query(..., description="Paper DOI for fetching paper details")):
    return await handle_request(fetch_paper_details, {"paperDoi": paperDoi})

#7. 논문 요약
@app.post("/papers/summary")
async def create_paper_summary(request: Request):
    data = await request.json()
    return await handle_request(process_summary, data)

#8. 선행 논문 리스트
@app.get("/papers/priorpapers")
#쿼리문 : ?paperDoi=”string”
async def get_prior_papers(paperDoi: str = Query(..., description="Paper DOI for fetching prior papers")):
    return await handle_request(fetch_prior_papers, {"paperDoi": paperDoi})



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