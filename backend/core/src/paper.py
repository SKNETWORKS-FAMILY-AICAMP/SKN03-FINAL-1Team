from fastapi import HTTPException
from fastapi.responses import JSONResponse
from utils import *


# ********************************************* #
# ***************  About Paper  *************** #
# ********************************************* #

async def fetch_paper_details(data):
    print("=== GET /papers ===")
    try :
        paper_doi = data.get("paperDoi")
        print("paperDoi : ", paper_doi)
    except Exception as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")
    # paper_pdf = 
    pass

async def fetch_prior_papers(data):
    print("=== GET /papers/priorpapers ===")
    try :
        paper_doi = data.get("paperDoi")
        print("paperDoi : ", paper_doi)
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
            "parentPaperDoi": "10.18653/v1/2020.acl-demos.10",
            "title": "Xiaomingbot: A Multilingual Robot News Reporter",
            "userKeyword": "multilingual news generation",
            "similarity": 0.92
            },
            {
            "paperDoi": "10.18653/v1/2020.acl-demos.10",
            "parentPaperDoi": "10.18653/v1/2020.acl-demos.1",
            "title": "SyntaxGym: An Online Platform for Targeted Evaluation of Language Models",
            "userKeyword": "language model evaluation",
            "similarity": 0.85
            }
        ],
        "count": 2
    }
    print("outputData : ", output_data)

    print("=== FIN /papers/priorpapers ===")
    return JSONResponse(content=output_data, status_code=200)

async def process_summary(data):
    print("=== POST /papers/summary ===")
    try :
        paper_doi = data.get("paperDoi")
        print("paperDoi : ", paper_doi)
    except Exception as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")
    
    try :
        pass
    except Exception as e:
        pass

    output_data = {
        "title": "Advancements in Neural Machine Translation",
        "authors": "John Doe, Jane Smith, Alex Johnson",
        "publicationYear": 2023,
        "publicationMonth": "October",
        "generatedTopic": "Neural Machine Translation and AI",
        "generatedSummary": "This paper explores recent advancements in neural machine translation, highlighting improvements in accuracy and speed using transformer-based architectures. It discusses practical applications and potential challenges in multilingual systems."
    }
    print("outputData : ", output_data)

    print("=== FIN /papers/summary ===")
    return JSONResponse(content=output_data, status_code=200)


async def process_transformation(data):
    print("=== POST /papers/transformation ===")
    try :
        user_prompt = data.get("userPrompt")
        print("userPrompt : ", user_prompt)
    except Exception as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")

    try :
        pass
    except Exception as e:
        pass

    output_data = {
        "generatedPrompt": "Neural Machine Translation and Transformer Models",
        "generatedKeywordList": [
            {
            "generatedKeyword": "neural translation",
            "paperList": [
                {
                "paperDoi": "10.1234/v1/2023.nmt.1",
                "title": "Advancements in Neural Machine Translation",
                "abstract": "This paper explores recent developments in neural machine translation, focusing on transformer models and their applications.",
                "citation": 120
                },
                {
                "paperDoi": "10.1234/v1/2023.nmt.2",
                "title": "Challenges in Multilingual Neural Translation Systems",
                "abstract": "A detailed analysis of challenges faced by multilingual neural translation systems, including resource constraints and training data requirements.",
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
                "abstract": "An overview of transformer architecture and its significance in natural language processing tasks.",
                "citation": 150
                },
                {
                "paperDoi": "10.5678/v1/2023.trans.2",
                "title": "Optimizing Transformer Models for Low-Resource Languages",
                "abstract": "This study proposes optimization techniques for transformer models to enhance performance in low-resource languages.",
                "citation": 80
                }
            ]
            }
        ],
        "count": 2
    }

    print("outputData : ", output_data)

    print("=== FIN /papers/transformation ===")
    return JSONResponse(content=output_data, status_code=200)

async def process_search(data):
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