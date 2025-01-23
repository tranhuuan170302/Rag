from sentence_transformers import SentenceTransformer
import os
from sklearn.metrics.pairwise import cosine_similarity

class Embedding:
    def __init__(self):
        self.embedding_for_document = SentenceTransformer("D:\\WorkSpace\\RAG\\API\\Model_LLM\\models--BAAI--bge-m3\\snapshots\\5617a9f61b028005a4858fdac845db406aefb181")
        self.embedding_for_query = SentenceTransformer("D:\\WorkSpace\\RAG\\API\\Model_LLM\\models--intfloat--multilingual-e5-large\\snapshots\\ab10c1a7f42e74530fe7ae5be82e6d4f11a719eb")
        self.embedding = SentenceTransformer("D:\\WorkSpace\\RAG\\API\\Model_LLM\\models--thenlper--gte-large\\snapshots\\4bef63f39fcc5e2d6b0aae83089f307af4970164")
    def encoder_document(self, text: str) -> list[float]:
        if not text.strip():
            print("Attempting to get embedding")
            return []
        embeddings = self.embedding.encode(text)
        return embeddings.tolist()

    def encoder_query(self, text: str) -> list[float]:
        if not text.strip():
            print("Attempting to get embedding")
            return []
        embeddings = self.embedding.encode(text)
        return embeddings.tolist()

    def retrivel_document(self, text_query: str) -> dict:

        project_stage = {
            "$project": {
                "_id": 0,  # Không lấy ObjectId
            "name": 1,
                "type": 1,
                "short_description": 1,
                "description": 1,
                "thumbnail_url": 1,
                "short_url": 1,
                "rating_average": 1,
                "quantity_sold": 1,
                "score": {
                    "$meta": "vectorSearchScore"  # Lấy điểm số vector search
                }
            }
        }

        try:
            query_embedding = self.encoder_query(text_query)
            if query_embedding is None:
                logger.error("Invalid query embedding")
                return None
            # Stage 1: Vector search (must be the first stage)
            vector_search_stage = {
                "$vectorSearch": {
                    "index": "vector_index",          # name index vector
                    "path": "embedding",              # url embedding in content_chunks collection
                    "queryVector": query_embedding,   # Embedding query
                    "numCandidates": 400,             # number of candidates
                    "limit": 100                       # number of result
                }
            }
            # generate pipeline
            pipeline = [vector_search_stage, project_stage]
            # get result from vector search
            results = list(collection.aggregate(pipeline))
            return results
        except Exception as e:
            logger.error(f"Error when get embedding: {e}")
            return None

get_embedding = Embedding()
# if __name__ == "__main__":

#     sentence_query = "Tôi đang có nhu cầu tìm mua một chiếc lap top"
#     sentence_document = "Bên tôi đang có các mặt hàng về chiếc lap top"
#     embedding = Embedding()
#     embedding_query = embedding.encoder_query(sentence_query)
#     embedding_document = embedding.encoder_document(sentence_document)

#     score = cosine_similarity([embedding_query], [embedding_document])[0][0]
#     print(score)