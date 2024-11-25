from fastapi import HTTPException
from fastapi.responses import JSONResponse
from utils import *


# ********************************************* #
# ***************  About Paper  *************** #
# ********************************************* #

# 3. 논문 검색
async def process_search(data):
    """
    키워드를 받아 유사도 높은 논문 리스트를 반환
    및 
    페이지네이션
    
    """
    print("=== POST /papers/search ===")
    try:
        user_keyword = data.userKeyword  # 요청 데이터에서 userKeyword 가져오기
        if not user_keyword:  # user_keyword가 None 또는 빈 문자열인 경우 처리
            raise HTTPException(status_code=400, detail="Invalid parameters: userKeyword cannot be None or empty")
        print("userKeyword:", user_keyword)
    except AttributeError as e:  # 키가 없는 경우
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters: Missing userKeyword")
    except Exception as e:  # 기타 예외 처리
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


    output_data = {
        "paperList": [
            {
                "paperDoi": "10.18653/v1/2023.nmt.1",
                "title": "Advancements in Neural Machine Translation",
                "authors": "John Doe, Jane Smith, Alex Johnson",
                "publicationYear": 2023,
                "publicationMonth": "October",
                "abstract": "This paper explores recent developments in neural machine translation, focusing on transformer models and their impact on translation quality.",
                "citation": 120
            },
            {
                "paperDoi": "10.18653/v1/2023.ai.2",
                "title": "Artificial Intelligence in Healthcare",
                "authors": "Emily Brown, Michael White",
                "publicationYear": 2022,
                "publicationMonth": "June",
                "abstract": "A comprehensive analysis of artificial intelligence applications in healthcare, highlighting benefits and ethical considerations.",
                "citation": 95
            },
            {
                "paperDoi": "10.18653/v1/2023.lm.3",
                "title": "Large Language Models and Their Applications",
                "authors": "Chris Green, Sarah Blue",
                "publicationYear": 2023,
                "publicationMonth": "January",
                "abstract": "This study examines large language models, their architecture, and how they are applied in real-world scenarios.",
                "citation": 150
            }
        ],
        "pagination": {
        "currentPage": 999,
        "pageSize": 999,
        "totalPages": 999,
        "totalResults": 999,
        "hasNextPage": False,
        "hasPreviousPage": False
      }
    }
    print("outputData : ", output_data)

    print("=== FIN /papers/search ===")
    return JSONResponse(status_code=200, 
                        content={
                            "resultCode" : 200,
                            "message" : "Search completed successfully",
                            "result" : output_data
                        })

# 4. 키워드 최적화
async def process_transformation(data):
    """
    OPENAI로 출력된 결과로 output 수정 
    
    """
    print("=== POST /papers/transformation ===")
    try :
        user_prompt = data.userPrompt
        print("userPrompt : ", user_prompt)
    except Exception as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")

    output_data = {
        "generatedPrompt": "Neural Machine Translation and Transformer Models",
        "generatedKeywordList": [
            {
            "generatedKeyword": "neural translation",
            "paperList": [
                {
                "paperDoi": "10.1234/v1/2023.nmt.1",
                "title": "Advancements in Neural Machine Translation",
                "korAbstract": "This paper explores recent developments in neural machine translation, focusing on transformer models and their applications.",
                "citation": 120
                },
                {
                "paperDoi": "10.1234/v1/2023.nmt.2",
                "title": "Challenges in Multilingual Neural Translation Systems",
                "korAbstract": "A detailed analysis of challenges faced by multilingual neural translation systems, including resource constraints and training data requirements.",
                "citation": 95
                }
            ]
            },
            {
            "generatedKeyword": "transformer architecture",
            "paperList": [
                {
                "paperDoi": "10.5678/v1/2023.trans.1",
                "title": "Understanding Transformer Models in NLP",
                "korAbstract": "An overview of transformer architecture and its significance in natural language processing tasks.",
                "citation": 150
                },
                {
                "paperDoi": "10.5678/v1/2023.trans.2",
                "title": "Optimizing Transformer Models for Low-Resource Languages",
                "korAbstract": "This study proposes optimization techniques for transformer models to enhance performance in low-resource languages.",
                "citation": 80
                }
            ]
            }
        ]
    }

    print("outputData : ", output_data)

    print("=== FIN /papers/transformation ===")
    return JSONResponse(status_code=200, 
                    content={
                        "resultCode" : 200,
                        "message" : "Keyword optimization successful.",
                        "result" : output_data
                    })

# 5. bookmarks
# 5.1. 북마크 리스트
async def fetch_user_bookmarks(header):
    """
    user_token -> user_id -> bookmarked_papers
    """
    print("=== GET /papers/bookmarks ===")
    try :
        user_token = header.get("user_token")
        if user_token is None:
            raise HTTPException(status_code=400, detail="Invalid parameters")
    except Exception as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")
    
    
    
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
    return JSONResponse(status_code=200, 
                    content={
                        "resultCode" : 200,
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
            return_obj = JSONResponse(status_code=200, 
                    content={
                        "resultCode" : 200,
                        "message" : "Bookmark removed successfully."
                    })
        else:
            return_obj = JSONResponse(status_code=200, 
                    content={
                        "resultCode" : 200,
                        "message" : "Bookmark list retrieved successfully."
                    })
   

    print("=== FIN /users/bookmarks ===")

    return return_obj


# 6. 논문 선택
async def fetch_paper_details(data):
    print("=== GET /papers ===")
    try :
        paper_doi = data
        print("paperDoi : ", paper_doi)
    except Exception as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")
    """
    doi -> 논문 찾기 -> S3 path
    """
    output_data = {
                    "paperS3Path": "THIS/IS/DUMMY/PATH"
                    }
    return JSONResponse(status_code=200, 
                    content={
                        "resultCode" : 200,
                        "message" : "fetch_bookmark completed successfully",
                        "result" : output_data
                    })
    
# 7. 논문요약

async def process_summary(data):
    print("=== POST /papers/summary ===")
    try :
        paper_doi = data.paperDoi
        print("paperDoi : ", paper_doi)
    except Exception as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")
    

    output_data = {
        "title": "Advancements in Neural Machine Translation",
        "userKeyword" : "NLP",
        "authors": "John Doe, Jane Smith, Alex Johnson",
        "publicationYear": 2023,
        "publicationMonth": "October",
        "generatedKeyword": "Neural Machine Translation and AI",
        "generatedCoreMethod" : "Method",
        "generatedTechnologies": "This paper explores recent advancements in neural machine translation, highlighting improvements in accuracy and speed using transformer-based architectures. It discusses practical applications and potential challenges in multilingual systems."
    }
    print("outputData : ", output_data)

    print("=== FIN /papers/summary ===")
    return JSONResponse(status_code=200, 
                    content={
                        "resultCode" : 200,
                        "message" : "Paper summary and details provided successfully.",
                        "result" : output_data
                    })
    

#8. 선행 논문 리스트

async def fetch_prior_papers(data):
    print("=== GET /papers/priorpapers ===")
    try :
        paper_doi = data
        print("paperDoi : ", paper_doi)
    except Exception as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")
    
    """
    
    """
    output_data = {
        "paperList": [
            {
            "paperDoi": "10.18653/v1/2020.acl-demos.1",
            "parentPaperDoi": "10.18653/v1/2020.acl-demos.10",
            "title": "Xiaomingbot: A Multilingual Robot News Reporter",
            "generatedKeyword": "multilingual news generation",
            "similarity": 0.92
            },
            {
            "paperDoi": "10.18653/v1/2020.acl-demos.10",
            "parentPaperDoi": "10.18653/v1/2020.acl-demos.1",
            "title": "SyntaxGym: An Online Platform for Targeted Evaluation of Language Models",
            "generatedKeyword": "language model evaluation",
            "similarity": 0.85
            }
        ]
    }
    print("outputData : ", output_data)

    print("=== FIN /papers/priorpapers ===")
    return JSONResponse(status_code=200, 
                    content={
                        "resultCode" : 200,
                        "message" : "Preceding papers retrieved successfully.",
                        "result" : output_data
                    })

