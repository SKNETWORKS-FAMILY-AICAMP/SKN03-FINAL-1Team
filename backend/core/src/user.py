from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from .utils import googleOAuth, MySQLHandler
from .error_template import *
import requests, json
from uuid import uuid4
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta, timezone


def _check_expiretime(expire: int):
    expires_in = expire - 60
    # 현재 시간 계산
    current_time = datetime.now(timezone.utc)
    # 만료 시간 계산
    expiration_time = current_time + timedelta(seconds=expires_in)
    # MySQL에 저장 가능한 TIMESTAMP 형식으로 변환
    expiration_time_str = expiration_time.strftime("%Y-%m-%d %H:%M:%S")

    return expiration_time_str


# ********************************************* #
# ***************  About  User  *************** #
# ********************************************* #


# ***************  Oauth Logic / JWT  *************** #
async def login_user(data):
    print("===  /login ===")
    oauth = googleOAuth()
    return RedirectResponse(
        f"{oauth.authorization_url}?scope=openid%20email%20profile&access_type=offline&response_type=code&redirect_uri={oauth.redirect_uri}&client_id={oauth.client_id}&prompt=consent"
    )


async def oauth_callback(code):
    print("=== GET /auth/callback ===")

    try:
        if not code:  # code None 또는 빈 문자열인 경우 처리
            raise HTTPException(
                status_code=500, detail="Parameter is Invalid or Empty. Check the input"
            )

        oauth = googleOAuth()  # unefficient

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
            raise HTTPException(
                status_code=token_response.status_code, detail=token_response.content
            )

        token_response_data = token_response.json()

        access_token = token_response_data.get("access_token")
        refresh_token = token_response_data.get("refresh_token")

        expires_in = token_response_data.get("expires_in")
        expires_in = _check_expiretime(expires_in)

        if not access_token:
            raise HTTPException(status_code=500, detail="Invalid token")

        # 구글에게 Access Token을 통해 사용자 정보 요청
        user_info_response = requests.get(
            oauth.user_info_url, headers={"Authorization": f"Bearer {access_token}"}
        )

        if user_info_response.status_code != 200:
            raise HTTPException(
                status_code=user_info_response.status_code,
                detail=user_info_response.content,
            )

        user_info = user_info_response.json()
        email = user_info.get("email", "")
        name = user_info.get("name", "")
        picture = user_info.get("picture", "")

    except HTTPException as he:
        oauth = googleOAuth()  # unefficient
        redirect_url = f"{oauth.home_uri}"
        return RedirectResponse(url=redirect_url)

    # DB에 저장
    try:
        db_handler = MySQLHandler()
        db_handler.connect()

        check_query = "SELECT user_id FROM DOCUMENTO.user WHERE email = %s"
        check_result = db_handler.fetch_one(check_query, (email,))

        if check_result:
            print("=== EXIST CUSTOMER ===")
            update_query = "UPDATE DOCUMENTO.auth SET access_token = %s, expires_at = %s, refresh_token = %s WHERE user_id = %s"
            db_handler.execute_query(
                update_query,
                (access_token, expires_in, refresh_token, check_result["user_id"]),
            )
            update_img_query = (
                "UPDATE DOCUMENTO.user SET profile_img = %s WHERE user_id = %s"
            )
            db_handler.execute_query(
                update_img_query,
                (picture, check_result["user_id"]),
            )

        else:
            print("=== NEW CUSTOMER ===")

            def generate_session_id():
                numeric_id = int(uuid4().int % 10**6)  # 숫자 15자리 제한
                return numeric_id

            uuid = generate_session_id()

            user_insert_query = "INSERT INTO DOCUMENTO.user (user_id, email, name, profile_img) VALUES (%s, %s, %s, %s)"
            db_handler.execute_query(user_insert_query, (uuid, email, name, picture))
            auth_insert_query = "INSERT INTO DOCUMENTO.auth (user_id, access_token, refresh_token, expires_at) VALUES (%s, %s, %s, %s)"
            db_handler.execute_query(
                auth_insert_query, (uuid, access_token, refresh_token, expires_in)
            )

    except Exception as un_expc:
        raise HTTPException(
            status_code=500, detail=f"Error In processing MYSQL: {un_expc}"
        )
    else:

        # 프론트엔드 URL로 리다이렉트하며 Access Token 전달
        redirect_url = f"{oauth.home_uri}/auth/callback/?access_token={access_token}"
        db_handler.disconnect()
        return RedirectResponse(url=redirect_url)

    finally:
        db_handler.disconnect()


async def user_logout(uuid):
    print("===  /logout ===")
    try:
        reset_time = _check_expiretime(60)
        db_handler = MySQLHandler()

        db_handler.connect()
        update_query = "UPDATE DOCUMENTO.auth SET expires_at = %s WHERE user_id = %s"
        db_handler.execute_query(
            update_query,
            (reset_time, uuid),
        )
    except Exception as un_expc:
        raise HTTPException(
            status_code=500, detail=f"Error In processing MYSQL: {un_expc}"
        )

    else:
        output_data = {"message": "Success"}
        return response_template(
            result=output_data, message="User Logout", http_code=200
        )


# 수정예정
async def get_userinfo(request: Request):
    print("=== GET /user_info ===")

    try:
        authorization: str = request.headers.get("Authorization")

        if (not authorization) or (not authorization.startswith("Bearer ")):
            raise HTTPException(
                status_code=401, detail="user not login yet. please login firtst"
            )

        authorization = authorization.strip()
        parts = authorization.split(" ")

        if (not parts[1]) or (len(parts) < 2):
            raise HTTPException(
                status_code=401, detail="user not login yet. please login firtst"
            )

        token = parts[1]

    except HTTPException as http_e:
        if http_e.status_code == 401:
            return response_template(
                result="NOT_LOGIN", message=http_e.detail, http_code=http_e.status_code
            )

    try:
        db_handler = MySQLHandler()
        db_handler.connect()
        isuser_query = "SELECT * FROM DOCUMENTO.auth WHERE access_token = %s"
        result = db_handler.fetch_one(isuser_query, (token,))
        if not result:
            raise HTTPException(status_code=401, detail="Access Token is expired")
        uuid = result["user_id"]
        expired = result["expires_at"]
        expired_time = expired.replace(tzinfo=timezone.utc)
        current_time = datetime.now(timezone.utc)

        if expired_time < current_time:
            raise HTTPException(status_code=401, detail="Access Token is expired")

        select_query = "SELECT * FROM DOCUMENTO.user WHERE user_id = %s"
        result = db_handler.fetch_one(select_query, (uuid,))

    except HTTPException as http_e:
        if http_e.status_code == 401:
            return response_template(
                result="NOT_LOGIN", message=http_e.detail, http_code=http_e.status_code
            )
    except Exception as un_expc:
        raise HTTPException(
            status_code=500, detail=f"Error In processing MYSQL: {un_expc}"
        )

    else:
        # S3에 default 프로필 이미지 없로드 해야할듯
        output_data = {
            "accessToken": token,  # 멘토님이 북마크에서 말했던것 처럼
            "userEmail": result.get("email", ""),
            "userName": result.get("name", "홍길동"),
            "userImg": result.get("profile_img", ""),
        }

        print("=== FIN /user_info ===")

        return response_template(
            result=output_data, message="User INFO retrieved", http_code=200
        )

    finally:
        db_handler.disconnect()


# ***************  Bookmark Logic  *************** #
# 5. bookmarks
# 5.1. 북마크 리스트
async def fetch_user_bookmarks(uuid):
    print(uuid)
    print("=== GET /users/bookmarks ===")
    try:
        db_handler = MySQLHandler()
        db_handler.connect()
        insert_query = "SELECT bookmarked_papers FROM DOCUMENTO.user WHERE user_id = %s"
        request_result = db_handler.fetch_one(insert_query, (uuid,))

        if not request_result["bookmarked_papers"] or not request_result:
            raise HTTPException(
                status_code=404,
                detail="No bookmarks found. Add papers to your bookmarks to see them here.",
            )
        bookmark_datas = json.loads(request_result["bookmarked_papers"])

        output_data = []
        for bkm in bookmark_datas:
            bookmark = dict()
            bookmark["userKeyword"] = bkm.get("userKeyword")
            bookmark["paperDoi"] = bkm.get("paperDoi")
            insert_query = "SELECT title FROM DOCUMENTO.paper WHERE paper_doi = %s"
            response_result = db_handler.fetch_one(
                insert_query, (bookmark["paperDoi"],)
            )
            if not response_result:
                continue
            else:
                bookmark["title"] = response_result["title"]

            output_data.append(bookmark)
            
        if not output_data:
            raise HTTPException(
                status_code=404,
                detail="No bookmarks found. Add papers to your bookmarks to see them here.",
            )

    except HTTPException as http_e:
        if http_e.status_code == 404:
            return response_template(
                result="NO_BOOKMARKS",
                message=http_e.detail,
                http_code=http_e.status_code,
            )

        else:
            return response_template(
                result="UNEXPECTED_HTTP_ERROR",
                message=http_e.detail,
                http_code=http_e.status_code,
            )

    except Exception as un_expc:
        raise HTTPException(status_code=500, detail=f"Error In processing : {un_expc}")

    else:
        print("=== FIN GET /users/bookmarks ===")
        output_data = {"paperList" : output_data}
        
        return response_template(
            result=output_data, message="Bookmark list retrieved", http_code=200
        )

    finally:
        db_handler.disconnect()


# 5.2. 북마크 추가 /삭제
async def handle_bookmark(data):
    print("=== POST /users/bookmarks ===")

    # 1. Data 검증
    try:
        request_data = data["request_data"]
        request_json = jsonable_encoder(request_data)

        paperDoi = request_data.paperDoi
        paperDoi = paperDoi.strip()
        userKeyword = request_data.userKeyword
        userKeyword = userKeyword.strip()
        bookMark = request_data.bookMark

        data_check = ""
        if not paperDoi:
            data_check += "paperDoi "
        if not userKeyword:
            data_check += "userKeyword "
        if type(bookMark) != bool:
            data_check += "bookMark "

        if data_check:
            raise HTTPException(
                status_code=400, detail=f"{data_check}Parmeter is Empty"
            )
        print("succ")
    # 1-1. Data 오류 검증
    except HTTPException as http_e:
        if http_e.status_code == 400:
            return response_template(
                result="EMPTY_PARAMETER",
                message=http_e.detail,
                http_code=http_e.status_code,
            )
        else:
            return response_template(
                result="UNEXPECTED_HTTP_ERROR",
                message=http_e.detail,
                http_code=http_e.status_code,
            )
    except Exception as un_expc:
        raise HTTPException(status_code=500, detail=f"Error In processing : {un_expc}")
    # 3. 프로세스
    try:
        db_handler = MySQLHandler()
        uuid = data["uuid"]
        print(uuid)
        db_handler.connect()

        select_query = "SELECT * FROM DOCUMENTO.user WHERE user_id = %s"
        result = db_handler.fetch_one(select_query, (uuid,))
        print(result)
        bookmark_data = result.get("bookmarked_papers", None)
        print(bookmark_data)
        doi_data = result.get("bookmark_doi", None)
        if doi_data:
            doi_data = doi_data.split(',')
        else:
            doi_data = list()
        # True, 즉 추가하는 기능
        if bookMark:
            if bookmark_data:
                bookmark_list = json.loads(bookmark_data)
                if len(bookmark_list) > 1000:
                    raise HTTPException(
                        status_code=400,
                        detail="Bookmark limit exceeded. Please remove existing bookmarks to add new ones.",
                    )
                
                for bml in bookmark_list:
                    if bml["paperDoi"] == paperDoi:
                        bml["userKeyword"] = userKeyword
                        break
                else:
                    bookmark_list.append(request_json)
                    doi_data.append(paperDoi)
                        
            else:
                bookmark_list = [request_json]
                doi_data.append(paperDoi)
            
            doi_data = ','.join(doi_data)
            print(doi_data)
            
            update_query = (
                "UPDATE DOCUMENTO.user SET bookmarked_papers = %s, bookmark_doi = %s WHERE user_id = %s"
            )
            db_handler.execute_query(update_query, (json.dumps(bookmark_list), doi_data, uuid))

            output_data = {
                "paperDoi": paperDoi,
                "bookMark": bookMark,
                "bookMarkLists": bookmark_list,
            }

            response_json = response_template(
                result=output_data, message="Bookmark save", http_code=201
            )

        # False, 즉 삭제하는 기능
        else:
            bookmark_list = json.loads(bookmark_data)
            if not bookmark_list:
                raise HTTPException(
                    status_code=400,
                    detail="Bookmark is Empty. You cannot delete from it",
                )

            else:
                del_cnt = -99
                for i, bml in enumerate(bookmark_list):
                    if bml["paperDoi"] == paperDoi:
                        del_cnt = i
                        break
                if del_cnt == -99:
                    raise HTTPException(
                        status_code=404,
                        detail="The item is not bookmarked. Cannot remove a non-existent bookmark.",
                    )
                else:
                    bookmark_list.pop(del_cnt)
                    doi_data.remove(paperDoi)
                    
            doi_data = ','.join(doi_data)
            update_query = (
                "UPDATE DOCUMENTO.user SET bookmarked_papers = %s, bookmark_doi = %s WHERE user_id = %s"
            )
            db_handler.execute_query(update_query, (json.dumps(bookmark_list), doi_data, uuid))
            output_data = {
                "paperDoi": paperDoi,
                "bookMark": bookMark,
                "bookmark_list": bookmark_list,
            }

            response_json = response_template(
                result=output_data, message="Bookmark removed", http_code=201
            )

    except HTTPException as http_e:
        if http_e.status_code == 404:
            return response_template(
                result="NOT_A_BOOKMARK",
                message=http_e.detail,
                http_code=http_e.status_code,
            )

        elif http_e.status_code == 400:
            return response_template(
                result="BOOKMARK_LIMIT",
                message=http_e.detail,
                http_code=http_e.status_code,
            )

        else:
            return response_template(
                result="UNEXPECTED_HTTP_ERROR",
                message=http_e.detail,
                http_code=http_e.status_code,
            )

    except Exception as un_expc:
        raise HTTPException(
            status_code=500, detail=f"Error In processing MYSQL: {un_expc}"
        )

    else:
        print("=== FIN POST /users/bookmarks ===")
        return response_json

    finally:
        db_handler.disconnect()
