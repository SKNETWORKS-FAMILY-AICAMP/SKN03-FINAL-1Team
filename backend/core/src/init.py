from fastapi import FastAPI
from .utils import *


async def initialize_global_objects(app):  # seom-j
    print("=== Initialize Global Objects ===")
    try:
        searcher = paperSearcher()
        s3_handler = S3Handler()

        faiss_index_key = "vector_store/search_vectors/faiss_index.bin"
        faiss_ids_key = "vector_store/search_vectors/faiss_ids.pkl"

        faiss_index, faiss_ids = searcher.load_faiss_files_from_s3(
            s3_handler, faiss_index_key, faiss_ids_key
        )

        app.state.searcher = searcher
        app.state.s3_handler = s3_handler
        app.state.faiss_index = faiss_index
        app.state.faiss_ids = faiss_ids

    except Exception as e:
        print(f"Error initializing global objects: {e}")
        raise
