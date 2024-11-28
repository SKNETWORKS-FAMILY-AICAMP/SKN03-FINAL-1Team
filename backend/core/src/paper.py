from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from .utils import *

#이 부분은 실제 AI 모델 구축하면 변경
from dummy import *
import json


# ********************************************* #
# ***************  About Paper  *************** #
# ********************************************* #
async def process_search(data): # seom-j
    print("=== POST /papers/search ===")
    try:
        # get data
        user_keyword = data.get("data").userKeyword
        if not user_keyword:
            raise HTTPException(status_code=400)
        print("userKeyword : ", user_keyword)

        # get searcher, faiss_index, faiss_ids (global variables)
        request = data.get("request")
        searcher = request.app.state.searcher
        faiss_index = request.app.state.faiss_index
        faiss_ids = request.app.state.faiss_ids

        # search (utils/paperSearcher.py)
        json_results = searcher.search_faiss_index(user_keyword, faiss_index, faiss_ids, similarity_threshold=75)

        if isinstance(json_results, str):
            json_results = json.loads(json_results)
        if not isinstance(json_results, list):
            raise ValueError("jsonResults is not a valid list")

        # parse results
        doi_list = [
            {"paper_doi": result["paper_doi"], "similarity": result["similarity"]}
            for result in json_results[:3]
        ]

        # fetch paper data from MySQL & create output
        db_handler = MySQLHandler()
        db_handler.connect()

        paper_list = []
        for doi_item in doi_list:
            paper_doi = doi_item["paper_doi"]

            select_query = """
            SELECT title, authors, venue, publication_year, publication_month, eng_abstract, citation 
            FROM paper 
            WHERE paper_doi = %s
            """
            paper_data = db_handler.fetch_one(select_query, (paper_doi,))

            if paper_data:
                paper_data["paperDoi"] = paper_doi
                paper_data["similarity"] = doi_item["similarity"]
                paper_list.append(paper_data)
            else:
                print(f"No data found for DOI: {paper_doi}")

        db_handler.disconnect()

        if not paper_list:
            raise HTTPException(status_code=404)

        # pagination
        current_page = 1  
        page_size = 3  
        total_results = len(paper_list)
        total_pages = (total_results + page_size - 1) // page_size
        has_next_page = current_page < total_pages
        has_previous_page = current_page > 1

        start_index = (current_page - 1) * page_size
        end_index = start_index + page_size
        paginated_paper_list = paper_list[start_index:end_index]

        # output
        output_data = {
            "paperList": paginated_paper_list,
            "pagination": {
                "currentPage": current_page,
                "pageSize": page_size,
                "totalPages": total_pages,
                "totalResults": total_results,
                "hasNextPage": has_next_page,
                "hasPreviousPage": has_previous_page,
            },
        }

        print("outputData : ", output_data)
        print("=== FIN /papers/search ===")
        return JSONResponse(
            status_code=201,
            content={
                "resultCode": 201,
                "message": "Search completed successfully",
                "result": output_data,
            },
        )

    except HTTPException as e:
        if e.status_code == 404:
            return JSONResponse(
                status_code=404,
                content={
                    "resultCode": 404,
                    "errorCode": "NO_RESULTS",
                    "message": "No results found. Please refine your search.",
                },
            )
        elif e.status_code == 400:
            return JSONResponse(
                status_code=400,
                content={
                    "resultCode": 400,
                    "errorCode": "INVALID PARAMETER",
                    "message": "Parameter is invalid. Check the input.",
                },
            )
        else:
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "resultCode": e.status_code,
                    "errorCode": "UNEXPECTED_ERROR",
                    "message": "An unexpected error occurred while processing your request.",
                },
            )
    except Exception as e:
        print(f"Unexpected error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "resultCode": 500,
                "errorCode": "UNEXPECTED_ERROR",
                "message": "An unexpected error occurred while processing your request.",
            },
        )

# 4. 키워드 최적화
async def process_transformation(data):
    """
    OPENAI로 출력된 결과로 output 수정 
    
    """
    print("=== POST /papers/transformation ===")
    try :
        user_prompt = data.get("data").userPrompt
        print("userPrompt : ", user_prompt)
    except Exception as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")
    
    try :
        chatbot = openaiHandler()
        openai_output = chatbot.get_keywords(user_prompt)
        openai_output = json.loads(openai_output)
        eng_keywords_to_search = [
            item["eng"] for item in openai_output
            if isinstance(item, dict) and "eng" in item
        ]
        keywords = [
            f"{item['eng']} [{item['kor']}]"
            for item in openai_output
            if isinstance(item, dict) and "eng" in item and "kor" in item
        ]
    except Exception as e:
        print(f"Error processing data: {e}")
        raise HTTPException(status_code=500, detail="Error processing data")
    
    try:
        request = data.get("request")
        searcher = request.app.state.searcher
        faiss_index = request.app.state.faiss_index
        faiss_ids = request.app.state.faiss_ids
        db_handler = MySQLHandler()
        db_handler.connect()

        generated_keyword_listm = []

        for idx, eng_keyword in enumerate(eng_keywords_to_search):
            top_results = searcher.search_faiss_index_top_n(eng_keyword, faiss_index, faiss_ids)
            if isinstance(top_results, str):
                try:
                    top_results = json.loads(top_results)
                except json.JSONDecodeError as e:
                    print(f"Error decoding top_results JSON: {e}")
                    top_results = []

            doi_list = [
                {"paper_doi": result["paper_doi"], "similarity": result["similarity"]}
                for result in top_results
            ]

            paper_list = []
            for doi_item in doi_list:
                paper_doi = doi_item["paper_doi"]
                select_query = """
                SELECT title, eng_abstract, citation 
                FROM paper 
                WHERE paper_doi = %s
                """
                paper_data = db_handler.fetch_one(select_query, (paper_doi,))
                if paper_data:
                    paper_data_dict = {
                        "paperDoi": paper_doi,
                        "title": paper_data["title"],
                        "engAbstract": paper_data["eng_abstract"],
                        "citation": paper_data["citation"]
                    }
                    paper_list.append(paper_data_dict)
                else:
                    print(f"No data found for DOI: {paper_doi}")
            
            generated_keyword_listm.append({
                "generatedKeyword": keywords[idx], 
                "paperList": paper_list
            })
        db_handler.disconnect()
        filtered_keyword_listm = [item for item in generated_keyword_listm if item["paperList"]]
        limited_keyword_listm = filtered_keyword_listm[:5]
    except Exception as e:
        print(f"Error processing data: {e}")
        raise HTTPException(status_code=500, detail="Error processing data")
    
    if not limited_keyword_listm :
        raise HTTPException(status_code=404, detail="No results found. Please refine your search.")

    output_data = {
        "generatedPrompt": f"\"{user_prompt}\"의 키워드 검색 결과입니다.\n\n",
        "generatedKeywordList": limited_keyword_listm
    }
    print("outputData : ", output_data)

    print("=== FIN /papers/transformation ===")
    return JSONResponse(status_code=201, 
                    content={
                        "resultCode" : 201,
                        "message" : "Keyword optimization successful.",
                        "result" : output_data
                    })



# 6. 논문 선택
async def fetch_paper_details(data):
    print("=== GET /papers ===")
    try :
        paper_doi = data
        print("paperDoi : ", paper_doi)
    except Exception as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")
    

    try :
        # fetch paper data from MySQL & create output
        db_handler = MySQLHandler()
        db_handler.connect()
        select_query = """
        SELECT s3_path 
        FROM paper 
        WHERE paper_doi = %s
        """
        paper_data = db_handler.fetch_one(select_query, (paper_doi,))
        db_handler.disconnect()
    except Exception as e:
        print(f"MySQL error: {e}")
        raise HTTPException(status_code=500, detail="Error fetching data from MySQL")
    
    try :
        # get s3 path & create output
        s3_path = paper_data["s3_path"]
        print("s3Path : ", s3_path)
        output_data = {
            "paperS3Path": s3_path
        }
    except Exception as e:
        print(f"Error processing data: {e}")
        raise HTTPException(status_code=500, detail="Error processing data")

    return JSONResponse(status_code=200, 
                    content={
                        "resultCode" : 200,
                        "message" : "PDF provided successfully.",
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
    return JSONResponse(status_code=201, 
                    content={
                        "resultCode" : 201,
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
    
    try :
        # fetch paper data from MySQL & create output
        db_handler = MySQLHandler()
        db_handler.connect()
        select_query = """
        SELECT reference_papers 
        FROM paper 
        WHERE paper_doi = %s
        """
        paper_data = db_handler.fetch_one(select_query, (paper_doi,))

        # parse reference papers & fetch data
        reference_papers = (json.loads(paper_data["reference_papers"]) if paper_data else [])[:10]
        paper_list = []
        for ref in reference_papers:
            ref_doi = ref["paper_doi"]

            select_query = """
            SELECT paper_doi, title, generated_keyword 
            FROM paper 
            WHERE paper_doi = %s
            """
            ref_data = db_handler.fetch_one(select_query, (ref_doi,))

            # create output
            if ref_data:
                paper_list.append({
                    "paperDoi": ref_data["paper_doi"],
                    "parentPaperDoi": paper_doi,
                    "title": ref_data["title"],
                    "generatedKeyword": ref_data.get("generated_keyword", ""),
                    "similarity": ref["similarity"],
                })
        db_handler.disconnect()
    except Exception as e:
        print(f"MySQL error: {e}")
        raise HTTPException(status_code=500, detail="Error fetching data from MySQL")

    output_data = {
            "paperList": paper_list
        }
    print("outputData : ", output_data)

    print("=== FIN /papers/priorpapers ===")
    return JSONResponse(status_code=201, 
                    content={
                        "resultCode" : 201,
                        "message" : "Preceding papers retrieved successfully.",
                        "result" : output_data
                    })

