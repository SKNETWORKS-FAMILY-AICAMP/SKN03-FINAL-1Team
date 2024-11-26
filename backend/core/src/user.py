from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from utils import googleOAuth, MySQLHandler
import requests
from uuid import uuid4

# ********************************************* #
# ***************  About  User  *************** #
# ********************************************* #
# 세션 데이터를 저장할 딕셔너리 (임시)
session_data = {}
# async def create_new_user(data):
#     return JSONResponse(status_code=201, 
#                         content={
#                             "resultCode" : 201,
#                             "message" : "Keyword optimization successful.",
#                             "result" : "gooooooooooood"
#                         })
    

async def login_user():
    print("===  /login ===")
    oauth = googleOAuth()
    return RedirectResponse(
        f"{oauth.authorization_url}?response_type=code&client_id={oauth.client_id}&redirect_uri={oauth.redirect_uri}&scope=openid%20email%20profile"
    )

async def oauth_callback(code):
    print("=== GET /auth/callback ===")
    
    try:
        if not code:  # code None 또는 빈 문자열인 경우 처리
            raise HTTPException(status_code=400)
        
        oauth = googleOAuth()
        print("oauth is success")
        token_response = requests.post(
        oauth.token_url,
        data={
            "code": code,
            "client_id": oauth.client_id,
            "client_secret": oauth.client_secret,
            "redirect_uri": oauth.redirect_uri,
            "grant_type": "authorization_code",
            },
        )
        
        if token_response.status_code != 200:
            print("Failed to get token")
            raise HTTPException(status_code=token_response.status_code)
        
        token_response_data = token_response.json()
        access_token = token_response_data.get("access_token")
        
        if not access_token:
            print("Invalid token")
            raise HTTPException(status_code=404)

        # 구글에게 Access Token을 통해 사용자 정보 요청
        user_info_response = requests.get(
            oauth.user_info_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        if user_info_response.status_code != 200:
            print("Failed to get user info")
            raise HTTPException(status_code=user_info_response.status_code)  
        

        
        
    
    except HTTPException as he:
        if he.status_code == 404:
            return JSONResponse(
            status_code=404,
            content={
                "resultCode" : 404,
                "errorCode": "Invalid token",
                "message": "The Toekn is Invaild."
            }
        )
        elif he.status_code == 400:
            return JSONResponse(
            status_code=400,
            content={
                "resultCode" : 400,
                "errorCode": "INVALID PARAMETER",
                "message": "Parameter is Invalid. Check the input"
            }
        )
        else:
            return JSONResponse(
            status_code=he.status_code,
            content={
                "resultCode" : he.status_code,
                "errorCode": "UNEXPECTED_ERROR",
                "message": "An unexpected error occurred while processing your request."
            }
        )


    else:
        user_info = user_info_response.json()

        # 콘솔에 유저 정보 출력
        print("User Info received from Google:", user_info)
        # # 세션 ID를 생성하는 함수
        def generate_session_id():
            return str(uuid4())
        # 세션 생성
        session_id = generate_session_id()
        session_data[session_id] = user_info

        # 쿠키로 세션 아이디를 전달
        response = RedirectResponse(url="https://www.documento.click/")
        response.set_cookie(key="session_id", value=session_id, httponly=True)

        return response     
    
    
    
    
    
    
    


# async def logout_user(data):
#     """사용자 로그아웃 처리 로직"""
#     pass

async def reissue_user_token(data):
    """사용자 토큰 재발급 로직"""
    pass

# ********************************************* #
# ***************  5. bookmark  *************** #
# ********************************************* #

# 5. bookmarks
# 5.1. 북마크 리스트
async def fetch_user_bookmarks(uuid):
    """
    user_token -> user_id -> bookmarked_papers
    """
    print("=== GET /papers/bookmarks ===")
    try :
        user_id = uuid
        if user_id is None:
            raise HTTPException(status_code=400)
        
        #
        
        
    except HTTPException as he:
        if he.status_code == 404:
            return JSONResponse(
            status_code=404,
            content={
                "resultCode" : 404,
                "errorCode": "NO_RESULTS",
                "message": "No results found. Please refine your search."
            }
        )
        elif he.status_code == 400:
            return JSONResponse(
            status_code=400,
            content={
                "resultCode" : 400,
                "errorCode": "INVALID PARAMETER",
                "message": "Parameter is Invalid. Check the input"
            }
        )
        else:
            return JSONResponse(
            status_code=he.status_code,
            content={
                "resultCode" : he.status_code,
                "errorCode": "UNEXPECTED_ERROR",
                "message": "An unexpected error occurred while processing your request."
            }
        )

    
    
    else:
        output_data = {
                "paperList": [
                    {
                    "paperDoi": "10.18653/v1/2020.acl-demos.1",
                    "title": "Xiaomingbot: A Multilingual Robot News Reporter",
                    "userKeyword": "multilingual news generation"
                    },
                    {
                    "paperDoi": "10.18653/v1/2020.acl-demos.10",
                    "title": "SyntaxGym: An Online Platform for Targeted Evaluation of Language Models",
                    "userKeyword": "language model evaluation"
                    }
                ]
            }
        print("outputData : ", output_data)

        print("=== FIN /papers/bookmarks ===")
        return JSONResponse(status_code=201, 
                        content={
                            "resultCode" : 201,
                            "message" : "Bookmark list retrieved successfully.",
                            "result" : output_data
                        })
    
# 5.2. 북마크 추가 /삭제
async def handle_bookmark(header, data):
    print("=== POST /users/bookmarks ===")
    try :
        user_token = header.get("user_token")
        
        paper_doi = data.get("paperDoi")
        user_keyword = data.get("userKeyword")
        bookmark = data.get("bookmark")
        
        if not user_token:
            raise HTTPException(status_code=400, detail="Invalid parameters")
        if not paper_doi:
            raise HTTPException(status_code=400, detail="Invalid parameters")
        if not user_keyword:
            raise HTTPException(status_code=400, detail="Invalid parameters")
        if not bookmark:
            raise HTTPException(status_code=400, detail="Invalid parameters")
            

        print("paperDoi : ", paper_doi)
        print("userKeyword : ", user_token)
    except Exception as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")

    else:
        if bookmark:
            #True, 즉 bookMark 되어있던 것을 삭제
            return_obj = JSONResponse(status_code=201, 
                    content={
                        "resultCode" : 201,
                        "message" : "Bookmark removed successfully."
                    })
        else:
            return_obj = JSONResponse(status_code=201, 
                    content={
                        "resultCode" : 201,
                        "message" : "Bookmark list retrieved successfully."
                    })
   

    print("=== FIN /users/bookmarks ===")

    return return_obj
