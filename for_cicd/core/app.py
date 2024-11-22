from fastapi import FastAPI, HTTPException, Query, Request
from typing import List, Optional
from fastapi.responses import JSONResponse

from src import paper, user

app = FastAPI()

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
# ***************  About Paper  *************** #
# ********************************************* #

@app.get("/papers")
async def get_paper_by_doi(paperDoi: str = Query(..., description="Paper DOI for fetching paper details")):
    return await handle_request(paper.fetch_paper_details, {"paperDoi": paperDoi})

@app.get("/papers/priorpapers")
async def get_prior_papers(paperDoi: str = Query(..., description="Paper DOI for fetching prior papers")):
    return await handle_request(paper.fetch_prior_papers, {"paperDoi": paperDoi})

@app.post("/papers/summary")
async def create_paper_summary(request: Request):
    data = await request.json()
    return await handle_request(paper.process_summary, data)

@app.post("/papers/transformation")
async def create_paper_transformation(request: Request):
    data = await request.json()
    return await handle_request(paper.process_transformation, data)

@app.post("/papers/search")
async def search_papers(request: Request):
    data = await request.json()
    return await handle_request(paper.process_search, data)


# ********************************************* #
# ***************  About  User  *************** #
# ********************************************* #

@app.post("/users")
async def create_user(request: Request):
    data = await request.json()
    return await handle_request(user.create_new_user, data)

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    return await handle_request(user.login_user, data)

@app.post("/logout")
async def logout(request: Request):
    data = await request.json()
    return await handle_request(user.logout_user, data)

@app.get("/reissue")
async def reissue_token(userId: int = Query(..., description="User ID for reissue")):
    return await handle_request(user.reissue_user_token, {"userId": userId})

@app.get("/users/bookmarks")
async def get_user_bookmarks(userId: int = Query(..., description="User ID for fetching bookmarked papers")):
    return await handle_request(user.fetch_user_bookmarks, {"userId": userId})

@app.post("/users/bookmarks")
async def add_to_bookmarks(request: Request):
    data = await request.json()
    return await handle_request(user.add_bookmark, data)

@app.delete("/users/bookmarks")
async def remove_from_bookmarks(
    userId: int = Query(..., description="User ID for removing bookmark"),
    paperDoi: str = Query(..., description="Paper DOI for removing from bookmarks")
):
    return await handle_request(user.remove_bookmark, {"userId": userId, "paperDoi": paperDoi})



# ***************  health check *************** #


# 6. Health Check (Vue.js와 연결 테스트)
@app.get("/health")
def health_check():
    return {"status": "Backend is up and running"}

@app.get("/")
def welcome_check():
    return {"status": "Welcome to documento"}



# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)