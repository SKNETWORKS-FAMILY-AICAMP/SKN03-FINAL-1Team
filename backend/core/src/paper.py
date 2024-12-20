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

        # get data
        user_keyword = data.get("keyword"," ")
        user_keyword = user_keyword.strip()
        if not user_keyword:
            raise HTTPException(
                status_code=400,
                detail="탐색 키워드를 입력하지 않았습니다!\n키워드를 입력해서 DOCUMENTO 서비스를 이용해주세요!",
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
            SELECT title, authors, venue, publication_year, publication_month, eng_abstract, kor_abstract,citation 
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
                status_code=404,
                detail="해당 키워드와 충분한 유사도를 가진 논문이 아직 존재하지 않습니다!\n다른 키워드를 검색해서 DOCUMENTO 서비스를 이용해주세요!",
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
        return response_template(result=output_data, message="Search", http_code=200)

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
                detail="아무것도 입력되지 않았습니다!\n원하는 논문의 내용을 자신만의 언어로 표현해보세요",
            )

        chatbot = openaiHandler()
        openai_output = chatbot.get_keywords(user_prompt)
        openai_output = json.loads(openai_output)
        print(openai_output)
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
        print(un_expc)
        detail="해당 문구와 관련된 키워드 및 논문을 찾을 수 없습니다!\n좀 더 길고 자세하게 서술해 주세요!"
        return response_template(
                result="NO_RESULTS", message=detail, http_code=404
            )

        #########################################################################################
    try:
        print("?????")
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
            if not paper_list:
                raise HTTPException(
                    status_code=404, detail="해당 문구와 관련된 키워드 및 논문을 찾을 수 없습니다!\n좀 더 길고 자세하게 서술해 주세요!"
                )
            
            
            
            generated_keyword_listm.append(
                {"generatedKeyword": keywords[idx], "paperList": paper_list}
            )

        filtered_keyword_listm = [
            item for item in generated_keyword_listm if item["paperList"]
        ]
        limited_keyword_listm = filtered_keyword_listm[:5]

        if not limited_keyword_listm:
            raise HTTPException(
                status_code=404, detail="해당 문구와 관련된 키워드 및 논문을 찾을 수 없습니다!\n좀 더 길고 자세하게 서술해 주세요!"
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


        print("=== FIN /papers/transformation ===")
        return response_template(
            result=output_data, message="Keyword optimization", http_code=201
        )

    finally:
        db_handler.disconnect()

async def paper_dummy(data):
    try:
        user_prompt = data.get("data").userPrompt
        user_prompt = user_prompt.strip()

        if not user_prompt:
            raise HTTPException(
                status_code=400,
                detail="Parameter is Empty. Check the userPrompt input.",
            )
            
        if user_prompt == "FAKE":
            raise HTTPException(
                status_code=404, detail="No results found. Please refine your search."
            )
        
        if user_prompt == "EMPTY":
            raise HTTPException(
                status_code=404, detail="No results found. Please refine your search."
            )

    except HTTPException as http_e:
        if http_e.status_code == 400:
            return response_template(
                result="EMPTY_PARAMETER",
                message=http_e.detail,
                http_code=http_e.status_code,
            )
        elif http_e.status_code == 404:
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
        output_data= {
    "generatedPrompt": "\"Efficient fine-tuning strategies for large-scale pre-trained language models\"의 키워드 검색 결과입니다.\n\n",
    "generatedKeywordList": [
      {
        "generatedKeyword": "Optimization of Large-Scale Language Models [대규모 언어 모델의 최적화]",
        "paperList": [
          {
            "paperDoi": "10.18653/v1/2020.acl-main.417",
            "title": "ParaCrawl: Web-Scale Acquisition of Parallel Corpora",
            "engAbstract": "We report on methods to create the largest publicly available parallel corpora by crawling the web, using open source software. We empirically compare alternative methods and publish benchmark data sets for sentence alignment and sentence pair filtering. We also describe the parallel corpora released and evaluate their quality and their usefulness to create machine translation systems.",
            "citation": 227
          },
          {
            "paperDoi": "10.18653/v1/2022.acl-long.264",
            "title": "The Trade-offs of Domain Adaptation for Neural Language Models",
            "engAbstract": "This work connects language model adaptation with concepts of machine learning theory. We consider a training setup with a large out-of-domain set and a small in-domain set. We derive how the benefit of training a model on either set depends on the size of the sets and the distance between their underlying distributions. We analyze how out-of-domain pre-training before in-domain fine-tuning achieves better generalization than either solution independently. Finally, we present how adaptation techniques based on data selection, such as importance sampling, intelligent data selection and influence functions, can be presented in a common framework which highlights their similarity and also their subtle differences.",
            "citation": 18
          }
        ]
      },
      {
        "generatedKeyword": "Fine-Tuning Techniques in Language Modelling [언어 모델링에서의 미세 조정 기법]",
        "paperList": [
          {
            "paperDoi": "10.18653/v1/2022.acl-long.264",
            "title": "The Trade-offs of Domain Adaptation for Neural Language Models",
            "engAbstract": "This work connects language model adaptation with concepts of machine learning theory. We consider a training setup with a large out-of-domain set and a small in-domain set. We derive how the benefit of training a model on either set depends on the size of the sets and the distance between their underlying distributions. We analyze how out-of-domain pre-training before in-domain fine-tuning achieves better generalization than either solution independently. Finally, we present how adaptation techniques based on data selection, such as importance sampling, intelligent data selection and influence functions, can be presented in a common framework which highlights their similarity and also their subtle differences.",
            "citation": 18
          }
        ]
      },
      {
        "generatedKeyword": "Efficacy of Pre-trained Language Model Tuning [미리 훈련된 언어 모델 튜닝의 효율성]",
        "paperList": [
          {
            "paperDoi": "10.18653/v1/2020.acl-demos.15",
            "title": "jiant: A Software Toolkit for Research on General-Purpose Text Understanding Models",
            "engAbstract": "We introduce jiant, an open source toolkit for conducting multitask and transfer learning experiments on English NLU tasks. jiant enables modular and configuration driven experimentation with state-of-the-art models and a broad set of tasks for probing, transfer learning, and multitask training experiments. jiant implements over 50 NLU tasks, including all GLUE and SuperGLUE benchmark tasks. We demonstrate that jiant reproduces published performance on a variety of tasks and models, e.g., RoBERTa and BERT.",
            "citation": 92
          }
        ]
      },
      {
        "generatedKeyword": "Performance Evaluation of Large-Scale Language Models [대규모 언어 모델의 성능 평가]",
        "paperList": [
          {
            "paperDoi": "10.18653/v1/2020.acl-main.417",
            "title": "ParaCrawl: Web-Scale Acquisition of Parallel Corpora",
            "engAbstract": "We report on methods to create the largest publicly available parallel corpora by crawling the web, using open source software. We empirically compare alternative methods and publish benchmark data sets for sentence alignment and sentence pair filtering. We also describe the parallel corpora released and evaluate their quality and their usefulness to create machine translation systems.",
            "citation": 227
          }
        ]
      },]}
     
        return response_template(result=output_data,message="Keyword optimization",http_code=201)


# 6. 논문 선택
async def fetch_paper_details(data):
    print("=== GET /papers/detail ===")
    try:
        paper_doi = data
        paper_doi = paper_doi.strip()
        if not paper_doi:
            raise HTTPException(
                status_code=400, detail="논문을 선택하지 않으셨습니다!\n북마크에서 논문을 선택하거나 우측 돋보기 아이콘을 통해 논문 탐색을 먼저 해주세요!"
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

        if not paper_data:
            raise HTTPException(
                status_code=404, detail="해당 논문은 아직 준비되지 않았습니다!\n북마크에서 논문을 선택하거나 우측 돋보기 아이콘을 통해 논문 탐색을 먼저 해주세요!"
            )
    except HTTPException as http_e:
        if http_e.status_code == 404:
            return response_template(
                result="NO_DATA",
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
        raise HTTPException(
            status_code=500, detail=f"Error fetching data from MySQL {e}"
        )

    finally:
        db_handler.disconnect()

    try:
        # get s3 path & create output
        s3_path = paper_data["s3_path"]

        modified_doi = paper_doi.replace("/", "_")
 

        parts = s3_path.split("/", 2)  # 최대 3개의 조각으로 분리
        modified_s3_path = "/".join(parts[:2])  # 첫 두 조각만 다시 결합


        s3_handler = S3Handler()
        url = s3_handler.s3_client.generate_presigned_url(
            ClientMethod="get_object",  # object를 가져오겠다
            Params={
                "Bucket": "documento-s3",  # 버켓 이름
                "Key": "papers/" + modified_s3_path + "/" + modified_doi + ".pdf",
                'ResponseContentType': 'application/pdf',
                'ResponseContentDisposition': 'inline'
                
                # aws에 있는 object의 key 값 ( 그림 참조 )
            },
            # url 유효기간 (단위:second)
            ExpiresIn=60 * 60 * 5,  # 1시간
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
                detail="There is no such data. Check the paperDoi input.",
            )
        generated_summary = json.loads(paper_data.get("generated_summarization")) if paper_data.get("generated_summarization") else None
        
        if not generated_summary:
            raise HTTPException(
                status_code=404,
                detail="There is no such data. Check the paperDoi input.",
            )
        
        default_msg = "아직 준비중 입니다다"
        
        output_data = [{
            "title": paper_data.get("title"),
            "Summary" : generated_summary.get("논문 요약", default_msg),
            "experimentResult" : generated_summary.get("실험 결과", default_msg),
            "experimentContext" : generated_summary.get("실험 내용", default_msg),
            "Keyword" : generated_summary.get("논문의 키워드", default_msg),
            "coreMethod" : generated_summary.get("논문의 핵심 방법론", default_msg),
            "coreExplain" : generated_summary.get("핵심 활용 기술 및 설명", default_msg),
        }]

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
            http_code=200,
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
