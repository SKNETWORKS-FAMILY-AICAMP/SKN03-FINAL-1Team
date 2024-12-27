from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn
from src import *
from src.reqeust_model import *

app = FastAPI()

# #local
# allowed = ["https://www.documento.click", "http://localhost:5173"]

allowed = ["https://www.documento.click"]

# ******************  CORS 처리  ****************** #
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed,  # 프론트엔드 서브 도메인
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
    allow_credentials=True,  # 인증 정보 허용 (쿠키 등)
)

# ************  app.py custom 예외처리  ************ #
# 403, 405
app.add_exception_handler(HTTPException, top_http_exchandler)
# 422 input error
app.add_exception_handler(RequestValidationError, top_validation_exchandler)

app.add_exception_handler(StarletteHTTPException, custom_405_handler)


# 수정예정
@app.on_event("startup")
async def initialize_globals():
    try:
        await initialize_global_objects(app)
        print("Global objects initialized successfully.")
    except Exception as e:
        print(f"Error initializing global objects: {e}")
        raise RuntimeError("Failed to initialize global objects during startup.")


@app.on_event("shutdown")
async def cleanup_resources():
    print("Cleaning up resources...")


# ********************************************* #
# ***************  About  User  *************** #
# ********************************************* #


# 2. 로그인
@app.get("/login/")
async def login():
    # Input parmeter 오류 처리 오류
    data = "success"
    return await handle_request(login_user, data)


# 2-1. 회원가입/로그인 용
@app.get("/auth/callback")
async def auth_callback(code: str = ""):

    return await handle_request(oauth_callback, code)


# 2-2. 세션 저장용
@app.get("/user_info")
async def user_info(request: Request):

    return await handle_request(get_userinfo, request)


@app.post("/logout")
async def logout(uuid: str = Depends(validate_token)):
    print("logout")
    # 여기에 세션 삭제 또는 토큰 무효화 처리
    return await handle_request(user_logout, uuid)


# ********************************************* #
# ***************  About Paper  *************** #
# ********************************************* #


# 3. 논문검색
@app.get("/papers/search/", dependencies=[Depends(validate_token)])
async def search_papers(
    request: Request,
    userKeyword :str = "",
    uuid: str = Depends(validate_token)
):

    return await handle_request(paper_search, {"keyword": userKeyword, "request": request, "uuid":uuid})

# 4.-1 키워드 최적화
@app.post("/papers/transformation/", dependencies=[Depends(validate_token)])
async def create_paper_transformation(request: Request, data: paperTransformation):
    # data = await request.json()
    return await handle_request(
        paper_dummy, {"data": data, "request": request}
    )

# 4.1 키워드 최적화
@app.post("/papers/dummy/", dependencies=[Depends(validate_token)])
async def create_paper_transformation(request: Request, data: paperTransformation):
    # data = await request.json()
    return await handle_request(
        process_transformation, {"data": data, "request": request}
    )


# ***************  5. bookmark  *************** #
# 5.1. 북마크 리스트
@app.get("/users/bookmarks/")
async def get_user_bookmarks(uuid: str = Depends(validate_token)):

    return await handle_request(fetch_user_bookmarks, uuid)


# 멘토님 曰 : 추가와 삭제는 같은 방식의 post
@app.post("/users/bookmarks/")
async def add_to_bookmarks(data: bookMarking, uuid: str = Depends(validate_token)):

    request_data = {"request_data": data, "uuid": uuid}
    return await handle_request(handle_bookmark, request_data)


# ********************************************* #


# 6. 논문 선택
# notion에는 /papers/select/?paperDoi=”string” 이렇게 적혀있음
@app.get("/papers/detail/", dependencies=[Depends(validate_token)])
async def get_paper_by_doi(paperDoi: str = ""):
   print(paperDoi)
   return await handle_request(fetch_paper_details, paperDoi)


# 7. 논문 요약
@app.get("/papers/summary/", dependencies=[Depends(validate_token)])
async def create_paper_summary(paperDoi: str = ""):
    return await handle_request(process_summary, paperDoi)


# 8. 선행 논문 리스트
@app.get("/papers/priorpapers/", dependencies=[Depends(validate_token)])
# 쿼리문 : ?paperDoi=”string”
async def get_prior_papers(paperDoi: str = ""):
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
