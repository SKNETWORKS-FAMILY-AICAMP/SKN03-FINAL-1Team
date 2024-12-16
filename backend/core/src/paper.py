from fastapi import HTTPException
from .utils import *
from .error_template import *
import json


# ********************************************* #
# ***************  About Paper  *************** #
# ********************************************* #

# 3. 논문검색


async def paper_search(data: dict):  # seom-j
    print("=== POST /papers/search : default ===")

    try:
        uuid = data.get("uuid")

        # get data
        user_keyword = data.get("keyword").userKeyword
        user_keyword = user_keyword.strip()
        if not user_keyword:
            raise HTTPException(
                status_code=400,
                detail="Parameter is Empty. Check the userKeyword input.",
            )

        # get searcher, faiss_index, faiss_ids (global variables)
        request = data.get("request")
        searcher = request.app.state.searcher
        faiss_index = request.app.state.faiss_index
        faiss_ids = request.app.state.faiss_ids

        # search (utils/paperSearcher.py)
        json_results = searcher.search_faiss_index(
            user_keyword, faiss_index, faiss_ids, similarity_threshold=75
        )

        if isinstance(json_results, str):
            json_results = json.loads(json_results)
        if not isinstance(json_results, list):
            raise ValueError("jsonResults is not a valid list")

        sorted_results = sorted(
            json_results, key=lambda x: x["similarity"], reverse=True
        )

        if len(sorted_results) > 70:
            sorted_results = sorted_results[:70]

        # parse results
        doi_list = [
            {"paper_doi": result["paper_doi"], "similarity": result["similarity"]}
            for result in sorted_results
        ]

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
        raise HTTPException(
            status_code=500, detail=f"Error In processing FASIS: {un_expc}"
        )

    try:

        db_handler = MySQLHandler()
        db_handler.connect()

        paper_list = []
        for doi_item in doi_list:
            paper_doi = doi_item["paper_doi"]

            select_query = """
            SELECT title, authors, venue, publication_year, publication_month, eng_abstract, citation 
            FROM DOCUMENTO.paper 
            WHERE paper_doi = %s
            """
            paper_data = db_handler.fetch_one(select_query, (paper_doi,))

            if paper_data:
                paper_data["paperDoi"] = paper_doi
                paper_data["similarity"] = doi_item["similarity"]
                paper_list.append(paper_data)
            else:
                print(f"No data found for DOI: {paper_doi}")

        if not paper_list:
            raise HTTPException(
                status_code=404, detail="No results found. Please refine your search."
            )

    except HTTPException as http_e:
        if http_e.status_code == 404:
            return response_template(
                result="NO_RESULTS", message=http_e.detail, http_code=http_e.status_code
            )
        else:
            return response_template(
                result="UNEXPECTED_HTTP_ERROR",
                message=http_e.detail,
                http_code=http_e.status_code,
            )

    except Exception as un_expc:
        raise HTTPException(
            status_code=500, detail=f"Error In processing FASIS or MYSQL: {un_expc}"
        )

    try:
        totalSizes = len(paper_list)
        if totalSizes > 60:
            paper_list = paper_list[:60]
            totalSizes = 60

        totalPages = ((totalSizes - 1) // 3) + 1

        paperLists = []
        paperPage = dict()
        paperInfos = []

        for i, paperobj in enumerate(paper_list):
            if i % 3 == 0:
                # 초기화
                paperPage = dict()
                paperInfos = []
                currentPage = (i // 3) + 1

                paperPage["currentPage"] = currentPage
                paperPage["sizes"] = 3
                paperPage["hasPreviousPage"] = False if currentPage == 1 else True
                paperPage["hasNextPage"] = False if currentPage == totalPages else True

            paperInfos.append(paperobj)

            if (i % 3 == 2) or (i == totalSizes - 1):
                paperPage["paperInfos"] = paperInfos
                paperLists.append(paperPage)

        paperTotals = {
            "totalPages": totalPages,
            "totalSizes": totalSizes,
            "paperLists": paperLists,
        }
        output_data = {"paperTotals": paperTotals}

        print("=== FIN /papers/search ===")
        return response_template(result=output_data, message="Search", http_code=201)

    finally:
        db_handler.disconnect()


# 4. 키워드 최적화
async def process_transformation(data):
    """
    OPENAI로 출력된 결과로 output 수정
    """
    print("=== POST /papers/transformation ===")

    try:

        user_prompt = data.get("data").userPrompt
        user_prompt = user_prompt.strip()
        print("userPrompt : ", user_prompt)
        if not user_prompt:
            raise HTTPException(
                status_code=400,
                detail="Parameter is Empty. Check the userPrompt input.",
            )

        chatbot = openaiHandler()
        openai_output = chatbot.get_keywords(user_prompt)
        openai_output = json.loads(openai_output)
        eng_keywords_to_search = [
            item["eng"]
            for item in openai_output
            if isinstance(item, dict) and "eng" in item
        ]
        keywords = [
            f"{item['eng']} [{item['kor']}]"
            for item in openai_output
            if isinstance(item, dict) and "eng" in item and "kor" in item
        ]

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
        raise HTTPException(
            status_code=500, detail=f"Error In processing OPENAI: {un_expc}"
        )

        #########################################################################################
    try:
        request = data.get("request")
        searcher = request.app.state.searcher
        faiss_index = request.app.state.faiss_index
        faiss_ids = request.app.state.faiss_ids
        db_handler = MySQLHandler()
        db_handler.connect()

        generated_keyword_listm = []

        for idx, eng_keyword in enumerate(eng_keywords_to_search):
            top_results = searcher.search_faiss_index_top_n(
                eng_keyword, faiss_index, faiss_ids
            )
            if isinstance(top_results, str):
                try:
                    top_results = json.loads(top_results)
                except json.JSONDecodeError as e:
                    raise HTTPException(
                        status_code=500, detail=f"Error processing JSON: {e}"
                    )

            sorted_results = sorted(top_results, key=lambda x: -x["similarity"])
            doi_list = [
                {"paper_doi": result["paper_doi"], "similarity": result["similarity"]}
                for result in sorted_results
            ]
            print(sorted_results)
            paper_list = []
            for doi_item in doi_list:
                paper_doi = doi_item["paper_doi"]
                select_query = """
                SELECT title, eng_abstract, citation 
                FROM DOCUMENTO.paper 
                WHERE paper_doi = %s
                """
                paper_data = db_handler.fetch_one(select_query, (paper_doi,))
                if paper_data:
                    paper_data_dict = {
                        "paperDoi": paper_doi,
                        "title": paper_data["title"],
                        "engAbstract": paper_data["eng_abstract"],
                        "citation": paper_data["citation"],
                    }
                    paper_list.append(paper_data_dict)
                else:
                    print(f"No data found for DOI: {paper_doi}")

            generated_keyword_listm.append(
                {"generatedKeyword": keywords[idx], "paperList": paper_list}
            )

        filtered_keyword_listm = [
            item for item in generated_keyword_listm if item["paperList"]
        ]
        limited_keyword_listm = filtered_keyword_listm[:5]

        if not limited_keyword_listm:
            raise HTTPException(
                status_code=404, detail="No results found. Please refine your search."
            )

    except HTTPException as http_e:
        if http_e.status_code == 404:
            return response_template(
                result="NO_RESULTS", message=http_e.detail, http_code=http_e.status_code
            )
        else:
            return response_template(
                result="UNEXPECTED_HTTP_ERROR",
                message=http_e.detail,
                http_code=http_e.status_code,
            )
    except Exception as un_expc:
        raise HTTPException(status_code=500, detail=f"Error processing data: {un_expc}")

    else:
        output_data = {
            "generatedPrompt": f'"{user_prompt}"의 키워드 검색 결과입니다.\n\n',
            "generatedKeywordList": limited_keyword_listm,
        }
        print("outputData : ", output_data)

        print("=== FIN /papers/transformation ===")
        return response_template(
            result=output_data, message="Keyword optimization", http_code=201
        )

    finally:
        db_handler.disconnect()


# 6. 논문 선택
async def fetch_paper_details(data):
    print("=== GET /papers/select ===")
    try:
        paper_doi = data
        paper_doi = paper_doi.strip()
        if not paper_doi:
            raise HTTPException(
                status_code=400, detail="Parameter is Empty. Check the paperDoi Query."
            )

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
        raise HTTPException(status_code=500, detail=f"Error processing data: {un_expc}")

    try:
        # fetch paper data from MySQL & create output
        db_handler = MySQLHandler()
        db_handler.connect()
        select_query = """
        SELECT s3_path 
        FROM DOCUMENTO.paper 
        WHERE paper_doi = %s
        """
        paper_data = db_handler.fetch_one(select_query, (paper_doi,))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching data from MySQL {e}"
        )

    finally:
        db_handler.disconnect()

    try:
        # get s3 path & create output
        s3_path = paper_data["s3_path"]

        modified_doi = paper_doi.replace("/", "_")
        print("modified_doi : ", modified_doi)

        parts = s3_path.split("/", 2)  # 최대 3개의 조각으로 분리
        modified_s3_path = "/".join(parts[:2])  # 첫 두 조각만 다시 결합
        print("modified_s3_path : ", modified_s3_path)

        s3_handler = S3Handler()
        url = s3_handler.s3_client.generate_presigned_url(
            ClientMethod="get_object",  # object를 가져오겠다
            Params={
                "Bucket": "documento-s3",  # 버켓 이름
                "Key": "papers/" + modified_s3_path + "/" + modified_doi + ".pdf",
                # aws에 있는 object의 key 값 ( 그림 참조 )
            },
            # url 유효기간 (단위:second)
            ExpiresIn=60 * 60,  # 1시간
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error S3 presigned URL {e}")

    else:
        output_data = {"paperS3Path": url}

        return response_template(
            result=output_data, message="PDF provided", http_code=200
        )


# 7. 논문요약
async def process_summary(data):
    print("=== GET /papers/summary ===")
    try:

        paper_doi = data.strip()
        if not paper_doi:
            raise HTTPException(
                status_code=400, detail="Parameter is empty. Check the paperDoi input."
            )

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
        raise HTTPException(status_code=500, detail=f"Error processing data: {un_expc}")

    try:
        # 수정예정

        # 수정예정
        db_handler = MySQLHandler()
        db_handler.connect()
        select_query = """
        SELECT * 
        FROM DOCUMENTO.paper 
        WHERE paper_doi = %s
        """
        paper_data = db_handler.fetch_one(select_query, (paper_doi,))

        if not paper_data:
            raise HTTPException(
                status_code=404,
                detail="There is no such paperDoi. Check the paperDoi input.",
            )

        output_data = {
            "title": paper_data.get("title"),
            "authors": paper_data.get("authors"),
            "publicationYear": paper_data.get("publication_year"),
            "publicationMonth": paper_data.get("publication_month"),
            "generatedSummary": paper_data.get("generated_summarization"),
        }

    except HTTPException as http_e:
        if http_e.status_code == 404:
            return response_template(
                result="WRONG PAPERDOI",
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
        raise HTTPException(status_code=500, detail=f"Error in MYSQL: {un_expc}")
    else:
        print("=== FIN /papers/summary ===")
        return response_template(
            result=output_data,
            message="Paper summary and details provided",
            http_code=201,
        )
    finally:
        db_handler.disconnect()


# 8. 선행 논문 리스트
async def fetch_prior_papers(data):
    print("=== GET /papers/priorpapers ===")
    try:
        paper_doi = data
        paper_doi = paper_doi.strip()
        if not paper_doi:
            raise HTTPException(
                status_code=400, detail="Parameter is Empty. Check the paperDoi Query."
            )

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
        raise HTTPException(status_code=500, detail=f"Error processing data: {un_expc}")

    try:
        # fetch paper data from MySQL & create output
        db_handler = MySQLHandler()
        db_handler.connect()
        select_query = """
        SELECT reference_papers 
        FROM DOCUMENTO.paper 
        WHERE paper_doi = %s
        """
        paper_data = db_handler.fetch_one(select_query, (paper_doi,))

        # parse reference papers & fetch data
        reference_papers = (
            json.loads(paper_data["reference_papers"]) if paper_data else []
        )[:10]
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
                paper_list.append(
                    {
                        "paperDoi": ref_data["paper_doi"],
                        "parentPaperDoi": paper_doi,
                        "title": ref_data["title"],
                        "generatedKeyword": ref_data.get("generated_keyword", ""),
                        "similarity": ref["similarity"],
                    }
                )

        if not paper_list:
            raise HTTPException(status_code=404, detail="No previous papers found.")

    except HTTPException as http_e:
        if http_e.status_code == 404:
            return response_template(
                result="NO_PREVIOUS_PAPERS",
                message=http_e.detail,
                http_code=http_e.status_code,
            )

        else:
            return response_template(
                result="UNEXPECTED_HTTP_ERROR",
                message=http_e.detail,
                http_code=http_e.status_code,
            )

    except Exception as e:
        print(f"MySQL error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching data from MySQL {e}"
        )

    else:
        output_data = {"paperList": paper_list}

        print("=== FIN /papers/priorpapers ===")
        return response_template(
            result=output_data, message="Preceding papers retrieved", http_code=200
        )

    finally:
        db_handler.disconnect()
