from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .utils import MySQLHandler
from fastapi.responses import JSONResponse

security = HTTPBearer()

# return handler
async def handle_request(func, data=None):
    try:
        # 요청 처리 함수 실행
        return await func(data)
    
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
    token = credentials.credentials  # Extract token
    
    try:
        insert_query = "SELECT user_id FROM DOCUMENTO.auth WHERE access_token = %s"
        request_result = db_handler.fetch_one(insert_query, (token, ))
        if not request_result:
            raise HTTPException(status_code=403, detail="User not found")
        return request_result["user_id"]
    finally:
        db_handler.disconnect()


def response_template(result:None, message:str, http_code:int=500):
    
    if (http_code == 200) or (http_code == 201):
        return JSONResponse(
            status_code=http_code,
            content={
                "resultCode": http_code,
                "message": message + " completed successfully" ,
                "result": result,
            },
        )
    elif http_code == 500:
        JSONResponse(
            status_code=500,
            content={
                "resultCode": 500,
                "errorCode": "UNEXPECTED_ERROR",
                "message": f"An unexpected error occurred while processing your request. \n Expected reason : {message}",
            },
        )
    else:
        return JSONResponse(
                    status_code=http_code,
                    content={
                        "resultCode" : http_code,
                        "errorCode": result,
                        "message": message
                    }
                )
        

