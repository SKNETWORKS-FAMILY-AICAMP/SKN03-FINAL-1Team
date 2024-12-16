from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .utils import MySQLHandler
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

security = HTTPBearer()

# ********************************************* #
# ***********  use in app.py file  ***********  #
# ********************************************* #


# Golbal custom error
async def top_http_exchandler(request: Request, exc: HTTPException):
    if exc.status_code == 403:
        return response_template(
            result="AUTHENTICATION_FAILED",
            message=exc.detail,
            http_code=exc.status_code,
        )
    elif exc.status_code == 401:
        return response_template(
            result="NO_USER_INFO", message=exc.detail, http_code=exc.status_code
        )

    return await request.app.default_exception_handler(request, exc)


async def custom_405_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 405:
        exc_mess = f"Invalid request method. Only  '{request.method}' is not allowed for this endpoint: {request.url.path}"
        return response_template(
            result="METHOD_NOT_ALLOWED", message=exc_mess, http_code=405
        )

    # # 다른 예외는 기본 처리
    # return JSONResponse(
    #     status_code=exc.status_code,
    #     content={"detail": exc.detail},
    # )


async def top_validation_exchandler(request: Request, exc: RequestValidationError):

    error_list = exc.errors()
    error_set = set()
    message = ""

    for error in error_list:
        error_set.add(" " + error.get("type", ""))
        message += f"{error['loc'][-1]} : {error['msg']} \n "

    errorCode = "".join(sorted(error_set))
    errorCode = errorCode.upper()
    errorCode = errorCode.strip()

    return await response_template(result=errorCode, message=message, http_code=422)


# return handler
async def handle_request(func, data=None):
    try:
        # 요청 처리 함수 실행
        return await func(data)

    except HTTPException as he:
        return response_template(
            result="UNEXPECTED_ERROR: MAYBE SRC",
            message=he.detail,
            http_code=he.status_code,
        )
    except Exception as e:
        # 예상치 못한 오류 처리
        return JSONResponse(
            status_code=500,
            content={
                "resultCode": 500,
                "errorCode": "UNEXPECTED_ERROR : MAYBE SERVER",
                "message": str(e),
            },
        )


# access토큰 인식
def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Validate the Bearer token.
    """
    db_handler = MySQLHandler()
    db_handler.connect()
    try:
        token = credentials.credentials  # Extract token
        
        insert_query = "SELECT user_id FROM DOCUMENTO.auth WHERE access_token = %s"
        request_result = db_handler.fetch_one(insert_query, (token,))
        if not request_result:
            raise HTTPException(
                status_code=403,
                detail="Authentication failed. Please log_in with valid credentials.",
            )
        return request_result["user_id"]

    finally:
        db_handler.disconnect()


# ********************************************* #
# **********  use in src directory  **********  #
# ********************************************* #


def response_template(result: None, message: str, http_code: int = 500):

    if (http_code == 200) or (http_code == 201):
        return JSONResponse(
            status_code=http_code,
            content={
                "resultCode": http_code,
                "message": message + " successfully",
                "result": result,
            },
        )
    elif http_code == 500:
        return JSONResponse(
            status_code=500,
            content={
                "resultCode": 500,
                "errorCode": "UNEXPECTED_ERROR",
                "message": f"An unexpected error occurred while processing your request. \n Expected reason : {message}",
            },
        )
    elif http_code == 503:
        return JSONResponse(
            status_code=503,
            content={
                "resultCode": 503,
                "errorCode": result,
                "message": message,
            },
        )

    else:
        return JSONResponse(
            status_code=http_code,
            content={"resultCode": http_code, "errorCode": result, "message": message},
        )
