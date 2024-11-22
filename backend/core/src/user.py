from fastapi import HTTPException
from fastapi.responses import JSONResponse

# ********************************************* #
# ***************  About  User  *************** #
# ********************************************* #

async def create_new_user(data):
    """새로운 사용자 생성 로직"""
    pass

async def login_user(data):
    """사용자 로그인 처리 로직"""
    pass

async def logout_user(data):
    """사용자 로그아웃 처리 로직"""
    pass

async def reissue_user_token(data):
    """사용자 토큰 재발급 로직"""
    pass

async def fetch_user_bookmarks(data):
    print("=== GET /papers/bookmarks ===")
    try :
        user_id = data.get("userId")
        print("userId : ", user_id)
    except Exception as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")
    
    try :
        pass
    except Exception as e:
        pass
    
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
            ],
            "count": 2
        }
    print("outputData : ", output_data)

    print("=== FIN /papers/bookmarks ===")
    return JSONResponse(content=output_data, status_code=200)


async def add_bookmark(data):
    print("=== POST /users/bookmarks ===")
    try :
        user_id = data.get("userId")
        paper_doi = data.get("paperDoi")
        user_keyword = data.get("userKeyword")
        print("userId : ", user_id)
        print("paperDoi : ", paper_doi)
        print("userKeyword : ", user_keyword)
    except Exception as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")

    try :
        pass
    except Exception as e:
        pass
    
    output_data = {
        "title": "Xiaomingbot: A Multilingual Robot News Reporter",
        "authors": "Runxin Xu, Jun Cao, Mingxuan Wang, Jiaze Chen, Hao Zhou, Ying Zeng, Yuping Wang, Li Chen, Xiang Yin, Xijin Zhang, Songcheng Jiang, Yuxuan Wang, Lei Li",
        "publicationYear": 2020,
        "publicationMonth": "July",
        "generatedTopic": "Multilingual News Reporting",
        "generatedSummary": "Xiaomingbot is an innovative multilingual robot news reporter designed to generate and deliver news articles in various languages efficiently. It leverages state-of-the-art natural language processing techniques to enhance accuracy and adaptability across different linguistic contexts."
    }
    print("outputData : ", output_data)

    print("=== FIN /users/bookmarks ===")

    return JSONResponse(content=output_data, status_code=200)


async def remove_bookmark(data):
    print("=== DELETE /users/bookmarks ===")
    try :
        user_id = data.get("userId")
        paper_doi = data.get("paperDoi")
        print("userId : ", user_id)
        print("paperDoi : ", paper_doi)
    except Exception as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")
    
    try :
        pass
    except Exception as e:
        pass
    
    output_data = {}
    print("outputData : ", output_data)

    print("=== FIN /users/bookmarks ===")
    return JSONResponse(content=output_data, status_code=200)