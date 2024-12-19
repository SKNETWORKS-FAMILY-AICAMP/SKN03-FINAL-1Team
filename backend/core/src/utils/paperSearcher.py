import pickle
import torch
import faiss
from io import BytesIO
from transformers import AutoTokenizer, AutoModel
import json
import numpy as np
import logging

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class paperSearcher:
    """
    Singleton class to manage scibert_scivocab_cased model, tokenizer, and FAISS index operations.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(paperSearcher, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Initialize the scibert_scivocab_cased model and tokenizer for CPU.
        """
        logger.info("Initializing scibert_scivocab_cased model and tokenizer.")
        self.tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_cased")
        self.model = AutoModel.from_pretrained("allenai/scibert_scivocab_cased").cpu()
        logger.info("Initialization complete.")

    def embed_text(self, text):
        """
        Embed a single query text using the scibert_scivocab_cased model on CPU.
        """
        logger.debug(f"Embedding text: {text[:50]}...")
        inputs = self.tokenizer(
            text, return_tensors="pt", padding=True, truncation=True, max_length=512
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        logger.debug("Embedding complete.")
        return embedding

    @staticmethod
    def read_faiss_index_from_bytesio(file_obj: BytesIO) -> faiss.Index:
        """
        Read a FAISS index from a BytesIO object.
        """
        logger.info("Reading FAISS index from BytesIO.")
        file_obj.seek(0)
        reader = faiss.PyCallbackIOReader(file_obj.read)
        index = faiss.read_index(reader)
        logger.info("FAISS index read complete.")
        return index

    def load_faiss_files_from_s3(
        self, s3_handler, faiss_index_key: str, faiss_ids_key: str
    ):
        """
        Load FAISS index and IDs from S3.
        """
        logger.info(f"Loading FAISS index and metadata from S3: {faiss_index_key}, {faiss_ids_key}.")
        faiss_index_file = s3_handler.download_file_to_memory(faiss_index_key)
        index = self.read_faiss_index_from_bytesio(faiss_index_file)

        faiss_ids_file = s3_handler.download_file_to_memory(faiss_ids_key)
        ids = pickle.load(faiss_ids_file)
        logger.info("FAISS index and metadata loaded successfully.")

        return index, ids

    def search_faiss_index(
        self,
        query: str,
        index,
        ids,
        similarity_threshold: float = 70.0,
        max_distance: float = 500.0,
        chunk_size: int = 2048,
    ) -> str:
        """
        Search the FAISS index for the given query and return matching results in JSON format.

        Args:
            query (str): The query text to search for.
            index: The FAISS index object.
            ids (List[str]): A list of IDs corresponding to the FAISS index entries.
            similarity_threshold (float): Minimum similarity score to consider a match (0-100).
            max_distance (float): Maximum allowable distance for 100% similarity.
            chunk_size (int): Number of index entries to process per chunk.

        Returns:
            str: JSON string with a list of dictionaries containing "paper_doi" and "similarity".
        """
        logger.info("Starting FAISS index search.")
        query_embedding = self.embed_text(query).astype(np.float32)
        logger.debug("Query embedding generated.")

        total_results = len(ids)
        results = []

        for i in range(0, total_results, chunk_size):
            chunk_start = i
            chunk_end = min(i + chunk_size, total_results)
            logger.debug(f"Processing chunk: {chunk_start} to {chunk_end}.")

            try:
                chunk_embeddings = np.array(
                    [index.reconstruct(idx) for idx in range(chunk_start, chunk_end)]
                )

                chunk_index = faiss.IndexFlatL2(query_embedding.shape[0])
                chunk_index.add(chunk_embeddings)

                distances, indices = chunk_index.search(
                    query_embedding.reshape(1, -1), len(chunk_embeddings)
                )

                chunk_results = [
                    {
                        "paper_doi": ids[chunk_start + idx]['paper_doi'],
                        "similarity": round(max(0, (1 - (dist / max_distance)) * 100), 2),
                    }
                    for idx, dist in zip(indices[0], distances[0])
                    if max(0, (1 - (dist / max_distance)) * 100) >= similarity_threshold
                ]

                results.extend(chunk_results)
            except Exception as e:
                logger.error(f"Error processing chunk {chunk_start}-{chunk_end}: {e}")

        results = sorted(results, key=lambda x: x["similarity"], reverse=True)
        logger.info("FAISS index search complete.")
        return json.dumps(results, indent=4)

    def search_faiss_index_top_n(
            self,
            query: str,
            index,
            ids,  
            max_results: int = 3,
            similarity_threshold: float = 70.0,
            max_distance: float = 500.0,
            chunk_size: int = 2048,
        ) -> str:
        """
        Search the FAISS index for the given query and return the top N matching results in JSON format.

        Args:
            query (str): The query text to search for.
            index: The FAISS index object.
            ids (List[dict]): A list of metadata dictionaries corresponding to the FAISS index entries.
                Each dictionary must include a "paper_doi" key.
            max_results (int): Maximum number of top results to return.
            similarity_threshold (float): Minimum similarity score to consider a match (0-100).
            max_distance (float): Maximum allowable distance for 100% similarity.
            chunk_size (int): Number of index entries to process per chunk.

        Returns:
            str: JSON string with a list of dictionaries containing "metadata" and "similarity".
        """
        logger.info("Starting FAISS top-N index search.")
        query_embedding = self.embed_text(query).astype(np.float32)
        logger.debug("Query embedding generated.")

        total_results = len(ids)
        results = []

        for i in range(0, total_results, chunk_size):
            chunk_start = i
            chunk_end = min(i + chunk_size, total_results)
            logger.debug(f"Processing chunk: {chunk_start} to {chunk_end}.")

            try:
                chunk_embeddings = np.array(
                    [index.reconstruct(idx) for idx in range(chunk_start, chunk_end)]
                )

                chunk_index = faiss.IndexFlatL2(query_embedding.shape[0])
                chunk_index.add(chunk_embeddings)

                distances, indices = chunk_index.search(
                    query_embedding.reshape(1, -1), len(chunk_embeddings)
                )

                chunk_results = [
                    {
                        "paper_doi": ids[chunk_start + idx]['paper_doi'],
                        "similarity": round(max(0, (1 - (dist / max_distance)) * 100), 2),
                    }
                    for idx, dist in zip(indices[0], distances[0])
                    if max(0, (1 - (dist / max_distance)) * 100) >= similarity_threshold
                ]

                results.extend(chunk_results)
            except Exception as e:
                logger.error(f"Error processing chunk {chunk_start}-{chunk_end}: {e}")

        # Remove duplicates by 'paper_doi', keeping the highest similarity
        unique_results = {}
        for result in results:
            paper_doi = result["paper_doi"]
            if not paper_doi:
                logger.warning(f"Missing 'paper_doi' in metadata: {result}")
                continue

            if paper_doi not in unique_results or result["similarity"] > unique_results[paper_doi]["similarity"]:
                unique_results[paper_doi] = result

        # Convert back to a sorted list
        top_results = sorted(unique_results.values(), key=lambda x: x["similarity"], reverse=True)[:max_results]
        logger.info("FAISS top-N index search complete.")
        return json.dumps(top_results, indent=4)