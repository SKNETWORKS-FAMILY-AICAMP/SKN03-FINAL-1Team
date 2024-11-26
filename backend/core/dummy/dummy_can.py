""" loging with db
"""
    
    # try :
    #     code = data.get("code")
    #     print("code : ", code)
    # except Exception as e:
    #     print(f"Missing key in parameters: {e}")
    #     raise HTTPException(status_code=400, detail="Invalid parameters")

    # try :
    #     oauth = googleOAuth()
    #     token_response = requests.post(
    #         oauth.token_url,
    #         data={
    #             "code": code,
    #             "client_id": oauth.client_id,
    #             "client_secret": oauth.client_secret,
    #             "redirect_uri": oauth.redirect_uri,
    #             "grant_type": "authorization_code",
    #         },
    #     )
    #     token_response_data = token_response.json()

    #     access_token = token_response_data.get("access_token")
    #     if not access_token:
    #         raise HTTPException(status_code=400, detail="Invalid token")

    #     user_info_response = requests.get(
    #         oauth.user_info_url, headers={"Authorization": f"Bearer {access_token}"}
    #     )
    #     user_info = user_info_response.json()

    #     name = user_info.get("name", "")
    #     email = user_info.get("email", "")

    # except Exception as e:
    #     print(f"Error in OAuth callback: {e}")
    #     raise HTTPException(status_code=500, detail="OAuth callback error")
        
    # try :
    #     db_handler = MySQLHandler()
    #     db_handler.connect()
    #     insert_query = "INSERT INTO DOCUMENTO.user_tb (email, name) VALUES (%s, %s)"
    #     db_handler.execute_query(insert_query, (email, name))
    #     print(f"Inserted email: {email}, name: {name} into DOCUMENTO.user_tb")
    # except Exception as e:
    #     print(f"Error with insert to MySQL: {e}")
    # finally:
    #     db_handler.disconnect()
    
    # output_data = {}
    # return JSONResponse(content=output_data, status_code=200)