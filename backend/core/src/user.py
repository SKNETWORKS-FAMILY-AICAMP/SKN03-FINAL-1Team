from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from .utils import googleOAuth, MySQLHandler

import requests, json
from uuid import uuid4

db_handler = MySQLHandler()
# ********************************************* #
# ***************  About  User  *************** #
# ********************************************* #


# ***************  Oauth Logic  *************** #
async def login_user(data):
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
        print("raw_data : ",user_info_response )
        print("json_data : ", user_info)
        print("header : ", user_info_response.headers)
        # 콘솔에 유저 정보 출력
        print("User Info received from Google:", user_info)
        # # 세션 ID를 생성하는 함수
        def generate_session_id():
            numeric_id = int(uuid4().int % 10**15)  # 숫자 15자리 제한
            return numeric_id
        # 세션 생성
        session_id = generate_session_id()
        email = user_info.get("email", "")
        name = user_info.get("name", "")
        try: 
            #싱글톤 시 수정
            
            db_handler.connect()
            
            insert_query = "SELECT * FROM DOCUMENTO.user WHERE email = %s"
            request_result = db_handler.fetch_one(insert_query, (email, ))
            if request_result:
                update_query = "UPDATE DOCUMENTO.user SET user_id = %s WHERE email = %s"
                db_handler.execute_query(update_query, session_id, email)

            else:
                insert_query = "INSERT INTO DOCUMENTO.user (user_id, email, name) VALUES (%s, %s, %s)"
                db_handler.execute_query(insert_query, (session_id, email, name))
        except Exception as e:
            print(f"Error with insert to MySQL: {e}")
        else:
        
            print("++++++++++++++++++++++++==SSID++++++++++++++++++++++++++++++++")
            # 쿠키로 세션 아이디를 전달
            response = RedirectResponse(url="https://www.documento.click/")
            response.set_cookie(key="session_id", 
                                value=session_id, 
                                httponly=True, 
                                max_age=3600 * 60,)

        # 쿠키 설정 검증 출력
            print("Set-Cookie Header:", response.headers.get("set-cookie"))
            return response
        
        finally:
            db_handler.disconnect()
    
    
  
async def get_userinfo(ssid):
    print("=== GET /user_info ===")
    
    try:
        if not ssid:  # ssid None 또는 빈 문자열인 경우 처리
            raise HTTPException(status_code=401)
        ssid = int(ssid) 
        
        #싱글톤 시 수정
        
        db_handler.connect()
        select_query = "SELECT * FROM user WHERE user_id = %s"
        result = db_handler.fetch_one(select_query, (ssid, ))
        print("====================serch db====================")
        print(result)
        if not result:
            raise HTTPException(status_code=404)
        
        
        
    except HTTPException as he:
        if he.status_code == 404:
            return JSONResponse(
            status_code=404,
            content={
                "resultCode" : 404,
                "errorCode": "NO_RESULTS",
                "message": "No results found. ."
            }
        )
        elif he.status_code == 401:
            return JSONResponse(
            status_code=401,
            content={
                "resultCode" : 401,
                "errorCode": "NO SSID",
                "message": "No session id. There is No ssid in Cookies"
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
        output = {
            "session_id" : ssid,
            "email" : result.get("email"),
            "name" : result.get("name", "홍길동")
            
        }
        return JSONResponse(status_code=200, 
                    content={
                        "resultCode" : 200,
                        "message" : "user_info retrieved successfully.",
                        "result" : output
                    })
    finally:
        db_handler.disconnect()


# async def logout_user(data):
#     """사용자 로그아웃 처리 로직"""
#     # logout 기능 삭제
#     pass

# async def reissue_user_token(data):
#     """사용자 토큰 재발급 로직"""
#     pass





# 5. bookmarks
# 5.1. 북마크 리스트
async def fetch_user_bookmarks(request:Request):
    
    # 1. Data 검증 : 없음
    
    # 2. Auth 검증
    try:
        print("=== Checking Auth ===")
        authorization: str = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="There is No Acess Token in Header")
        token = authorization.split(" ")[1]  # "Bearer " 이후의 토큰 값만 추출

        db_handler.connect()
        insert_query = "SELECT user_id FROM DOCUMENTO.auth WHERE access_token = %s"
        request_result = db_handler.fetch_one(insert_query, (token, ))

        if not request_result: 
            raise HTTPException(status_code=401, detail="Invaild User. Pleasr sign up first")
        
        uuid = request_result['user_id']

    
    # 2-1. Auth error 코드
    except HTTPException as he:
        if he.status_code == 401:
                return JSONResponse(
                status_code=401,
                content={
                    "resultCode" : 401,
                    "errorCode": "Invaild Token",
                    "message": he.detail
                }
            )
        else:
                return JSONResponse(
                status_code=he.status_code,
                content={
                    "resultCode" : he.status_code,
                    "errorCode": "UNEXPECTED_HTTP ERROR",
                    "message": "An unexpected error occurred while processing your request."
                }
            )
        
                
    else:
    # 3. 프로세스
        print("=== GET /users/bookmarks ===")
        try:

            db_handler.connect()
            insert_query = "SELECT bookmarked_papers FROM DOCUMENTO.user WHERE user_id = %s"
            request_result = db_handler.fetch_one(insert_query, (uuid, ))

            print("reuqest_result : ", request_result)
            
            if not request_result['bookmarked_papers'] or not request_result:
                raise HTTPException(status_code=404)       
            bookmark_datas = json.loads(request_result['bookmarked_papers'])
            
            output_data = []
            for bkm in bookmark_datas:
                bookmark = dict()
                bookmark["userKeyword"] = bkm.get("userKeyword")
                bookmark["paperDoi"] = bkm.get("paperDoi")
                insert_query = "SELECT title FROM DOCUMENTO.paper WHERE paper_doi = %s"
                response_result = db_handler.fetch_one(insert_query, (bookmark["paperDoi"] , ))
                if not response_result:
                    bookmark["title"] = "We Don't have this Paper Yet"
                else:
                    bookmark["title"] = response_result['title']

                output_data.append(bookmark)
            
        # 3-1. 프로세스 에러코드
        except HTTPException as he:
            if he.status_code == 404:
                    return JSONResponse(
            status_code=404,
            content={
                "resultCode" : 404,
                "errorCode": "NO_BOOKMARKS",
                "message": "No bookmarks found. Add papers to your bookmarks to see them here.",
                    }
                )
            else:
                return JSONResponse(
                status_code=he.status_code,
                content={
                    "resultCode" : he.status_code,
                    "errorCode": "UNEXPECTED_HTTP ERROR",
                    "message": "An unexpected error occurred while processing your request."
                }
            )
                
        else:
            print("=== FIN GET - /users/bookmarks ===")
            return JSONResponse(status_code=200, 
                        content={
                            "resultCode" : 200,
                            "message" : "Bookmark list retrieved successfully.",
                            "result" : output_data
                        })
        
    finally:
        db_handler.disconnect()
    


    
    
# 5.2. 북마크 추가 /삭제
async def handle_bookmark(request:Request):
    print("=== POST /users/bookmarks ===")
    
    # 1. Data 검증 
    try :
        print("=== Check data annotation ===")
        request_data = await request.json()
        paperDoi = request_data.get("paperDoi", None)
        userKeyword = request_data.get("userKeyword", None)
        bookMark = request_data.get("bookMark", None)
        
        if not paperDoi or (type(paperDoi) != str):
            raise HTTPException(status_code=404, detail= "There is Error with paperDoi")   
        if not userKeyword or (type(userKeyword) != str):
            raise HTTPException(status_code=404, detail= "There is Error with userKeyword")   
        if (type(bookMark) != bool):
            raise HTTPException(status_code=404, detail= "There is Error with bookMark") 
    
    # 1-1. Data 오류 검증
    except HTTPException as he:
        if he.status_code == 404:
                return JSONResponse(
                status_code=404,
                content={
                    "resultCode" : 404,
                    "errorCode": "Invaild Parameter",
                    "message": he.detail
                }
            )
        else:
                return JSONResponse(
                status_code=he.status_code,
                content={
                    "resultCode" : he.status_code,
                    "errorCode": "UNEXPECTED_HTTP ERROR",
                    "message": "An unexpected error occurred while processing your request."
                }
            )
    
    
    else:
        
        # 2. Auth 검증
        try:
            print("=== Checking Auth ===")
            authorization: str = request.headers.get("Authorization")
            if not authorization or not authorization.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="There is No Acess Token in Header")
            token = authorization.split(" ")[1]  # "Bearer " 이후의 토큰 값만 추출

            db_handler.connect()
            insert_query = "SELECT user_id FROM DOCUMENTO.auth WHERE access_token = %s"
            request_result = db_handler.fetch_one(insert_query, (token, ))

            if not request_result: 
                raise HTTPException(status_code=401, detail="Invaild User. Pleasr sign up first")
            
            uuid = request_result['user_id']

        
        # 2-1. Auth error 코드
        except HTTPException as he:
            if he.status_code == 401:
                    return JSONResponse(
                    status_code=401,
                    content={
                        "resultCode" : 401,
                        "errorCode": "Invaild Token",
                        "message": he.detail
                    }
                )
            else:
                    return JSONResponse(
                    status_code=he.status_code,
                    content={
                        "resultCode" : he.status_code,
                        "errorCode": "UNEXPECTED_HTTP ERROR",
                        "message": "An unexpected error occurred while processing your request."
                    }
                )
        
        
        else:
            
            # 3. 프로세스
            try:
                db_handler.connect()
                insert_query = "SELECT bookmarked_papers FROM DOCUMENTO.user WHERE user_id = %s"
                result = db_handler.fetch_one(insert_query, (uuid, ))
                bookmark_data = result.get('bookmarked_papers', None)
                
                # True, 즉 추가하는 기능
                if bookMark:
                    bookmark_list = json.loads(bookmark_data)
                    if bookmark_list:
                        for bml in bookmark_list:
                            if bml["paperDoi"] == paperDoi:
                                bml["userKeyword"] = userKeyword
                                break
                        else:
                            bookmark_list.append(request_data)
                    else:
                        bookmark_list = [request_data]
                    
                    update_query = "UPDATE DOCUMENTO.user SET bookmarked_papers = %s WHERE user_id = %s"
                    db_handler.execute_query(update_query, (json.dumps(bookmark_list), uuid))

                    output_data = {
                        "paperDoi" : paperDoi,
                        "bookMark" : bookMark
                    }
                    
                    response_json = JSONResponse(status_code=201, 
                                content={
                                    "resultCode" : 201,
                                    "message" : "Bookmark save successfully.",
                                    "result" : output_data
                                })
                        
                        
                # False, 즉 삭제하는 기능    
                else:
                    
                    bookmark_list = json.loads(bookmark_data)
                    if  not bookmark_list:

                        raise HTTPException(status_code=400, detail="Bookmark is Empty. You cannot delete from it")
                    else:
                        del_cnt = -99
                        for i, bml in enumerate(bookmark_list):
                            if bml["paperDoi"] == paperDoi:
                                del_cnt = i-1
                        if del_cnt == -99 :
                            raise HTTPException(status_code=400, detail="The item is not bookmarked. Cannot remove a non-existent bookmark.")
                        else:
                            bookmark_list.pop(i)
                                    
                    update_query = "UPDATE DOCUMENTO.user SET bookmarked_papers = %s WHERE user_id = %s"
                    db_handler.execute_query(update_query, (json.dumps(bookmark_list), uuid))

                    output_data = {
                        "paperDoi" : paperDoi,
                        "bookMark" : bookMark
                    }
                    
                    response_json = JSONResponse(status_code=201, 
                                content={
                                    "resultCode" : 201,
                                    "message" : "Bookmark removed successfully.",
                                    "result" : output_data
                                })
            
            # 3-1 프로세스 error 코드
            except HTTPException as he:
            #오류코드도 TRUE False 나누어서
                # True, 즉 추가하는 기능
                if not bookMark:
                    if he.status_code == 400:
                        return JSONResponse(
                        status_code=400,
                        content={
                            "resultCode" : 400,
                            "errorCode": "NOT_A_BOOKMARK",
                            "message": he.detail,
                        }
                    )
                elif he.status_code == 404:
                    return JSONResponse(
                    status_code=404,
                    content={
                        "resultCode" : 404,
                        "errorCode": "PAPER_NOT_FOUND",
                        "message": "Paper not found in BookMark. Please check the DOI."
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
                print("=== FIN /users/bookmarks ===")
                return response_json
    finally:
        db_handler.disconnect()
            
            
