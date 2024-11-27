from fastapi import HTTPException
from fastapi.responses import JSONResponse
from utils import *

#이 부분은 실제 AI 모델 구축하면 변경
from dummy import *



# ********************************************* #
# ***************  About Paper  *************** #
# ********************************************* #

# 3. 논문 검색
async def process_search(data):

    print("=== POST /papers/search ===")
    try:
        user_keyword = data.userKeyword  # 요청 데이터에서 userKeyword 가져오기
        if not user_keyword:  # user_keyword가 None 또는 빈 문자열인 경우 처리
            raise HTTPException(status_code=400)

        # doi_list : [ {doi(str): similarity}]
        doi_list = dummy_search(user_keyword)

    # DOI -> DB에서 
    # title, authors, publicationYear, publicationMonth, abstract, citation, venue 뽑고
    # 그거 "paperList": [ {}, {}, ...] 붙히고
    # pagination
        
        if not doi_list:
            print(f"NO_RESULTS")
            raise HTTPException(status_code=404)
        
        print(f"Real data format : {doi_list[:3]} ...")
        
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
                "paperDoi": "10.18653/v1/2023.nmt.1",
                "title": "Advancements in Neural Machine Translation",
                "authors": "John Doe, Jane Smith, Alex Johnson",
                "venue": "venue",
                "publicationYear": 2023,
                "publicationMonth": "October",
                "abstract": "This paper explores recent developments in neural machine translation, focusing on transformer models and their impact on translation quality.",
                "citation": 120
            },
            {
                "paperDoi": "10.18653/v1/2023.ai.2",
                "title": "Artificial Intelligence in Healthcare",
                "authors": "Emily Brown, Michael White",
                "venue": "venue",
                "publicationYear": 2022,
                "publicationMonth": "June",
                "abstract": "A comprehensive analysis of artificial intelligence applications in healthcare, highlighting benefits and ethical considerations.",
                "citation": 95
            },
            {
                "paperDoi": "10.18653/v1/2023.lm.3",
                "title": "Large Language Models and Their Applications",
                "authors": "Chris Green, Sarah Blue",
                "venue": "venue",
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
        return JSONResponse(status_code=201, 
                            content={
                                "resultCode" : 201,
                                "message" : "Search completed successfully",
                                "result" : output_data
                            })
    
    
#####################################################################################################

    

# 4. 키워드 최적화
async def process_transformation(data):
    """
    OPENAI로 출력된 결과로 output 수정 
    
    """
    print("=== POST /papers/transformation ===")
    try :
        user_prompt = data.userPrompt
        print("userPrompt : ", user_prompt)
        
        if not user_prompt:  # user_keyword가 None 또는 빈 문자열인 경우 처리
            raise HTTPException(status_code=400)
        
        # doi_list : [ {generatedKeyword(str): [paperdoi,paerpaerdoi,...]}, ...]
        doi_list = dummy_transformation(user_prompt)
        print(f"Real data format : {doi_list[:3]} ...")

    # DOI -> DB에서 
    # title,  korAbstract, citation 뽑고
    # 그거 "paperList": [ {}, {}, ...] 붙히고
        
        if not doi_list:
            print(f"NO_RESULTS")
            raise HTTPException(status_code=404)
        
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

        print("outputData: ", output_data)

        print("=== FIN /papers/transformation ===")
        return JSONResponse(status_code=201, 
                        content={
                            "resultCode" : 201,
                            "message" : "Keyword optimization successful.",
                            "result" : output_data
                        })


############################################################################################################


# 6. 논문 선택
async def fetch_paper_details(data):
    print("=== GET /papers ===")
    try :
        paper_doi = data
        print("paperDoi : ", paper_doi)
        if not paper_doi:  # user_keyword가 None 또는 빈 문자열인 경우 처리
            raise HTTPException(status_code=400)
        
    except HTTPException as he:
        
        if he.status_code == 400:
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
        # """
        # doi -> 논문 찾기 -> S3 path
        # """
        output_data = {
                        "paperS3Path": "THIS/IS/DUMMY/PATH"
                        }
        return JSONResponse(status_code=200, 
                        content={
                            "resultCode" : 200,
                            "message" : "fetch_bookmark completed successfully",
                            "result" : output_data
                        })
        
        
#########################################################################################################

        
# 7. 논문요약

async def process_summary(data):
    print("=== POST /papers/summary ===")
    try :
        paper_doi = data.paperDoi
        print("paperDoi : ", paper_doi)
        if not paper_doi:  # user_keyword가 None 또는 빈 문자열인 경우 처리
            raise HTTPException(status_code=400)
        
        # doi_list : [ {} ]
        doi_list = dummy_summary(paper_doi)
        print(f"Real data format : {doi_list} ...")

    # DOI -> DB에서 
    # title,  korAbstract, citation 뽑고
    # 그거 "paperList": [ {}, {}, ...] 붙히고
        
        if not doi_list:
            print(f"NO_RESULTS")
            raise HTTPException(status_code=404)
        
        
        
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
        output_data = {"summary":
            {
            "title": "Advancements in Neural Machine Translation",
            "userKeyword" : "NLP",
            "authors": "John Doe, Jane Smith, Alex Johnson",
            "publicationYear": 2023,
            "publicationMonth": "October",
            "generatedKeyword": "Neural Machine Translation and AI",
            "generatedCoreMethod" : "Method",
            "generatedTechnologies": "This paper explores recent advancements in neural machine translation, highlighting improvements in accuracy and speed using transformer-based architectures. It discusses practical applications and potential challenges in multilingual systems."
        }
        }
        print("outputData : ", output_data)

        print("=== FIN /papers/summary ===")
        return JSONResponse(status_code=201, 
                        content={
                            "resultCode" : 201,
                            "message" : "Paper summary and details provided successfully.",
                            "result" : output_data
                        })
    

###############################################################################################################3


#8. 선행 논문 리스트

async def fetch_prior_papers(data):
    print("=== GET /papers/priorpapers ===")
    try :
        paper_doi = data
        print("paperDoi : ", paper_doi)
        if not paper_doi:  # user_keyword가 None 또는 빈 문자열인 경우 처리
            raise HTTPException(status_code=400)
        
        doi_list = dummy_referencelist(paper_doi)
        if not doi_list:
            print(f"NO_PREVIOUS_PAPERS")
            raise HTTPException(status_code=404)
        
    except HTTPException as he:
        if he.status_code == 404:
            return JSONResponse(
            status_code=404,
            content={
                "resultCode" : 404,
                "errorCode": "NO_PREVIOUS_PAPERS",
	            "message" : "Paper not found. Please check the DOI."
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

