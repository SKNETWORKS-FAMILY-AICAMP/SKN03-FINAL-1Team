""" api func that 
determine not to used
it comment out prevent to error
"""

# @app.post("/logout")
# async def logout(request: Request):
#     data = await request.json()
#     return await handle_request(logout_user, data)

# @app.get("/reissue")
# async def reissue_token(userId: int = Query(..., description="User ID for reissue")):
#     return await handle_request(reissue_user_token, {"userId": userId})

# async def handle_request(func, data=None):
#     try:
#         return await func(data)
#     except HTTPException as e:
#         return JSONResponse(
#             status_code=e.status_code,
#             content={"statusCode": e.status_code, "message": str(e.detail)}
#         )
#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"statusCode": 500, "message": str(e)}
#         )