from sentence_transformers import SentenceTransformer
from API.settings.settings import embedding_model
class Embedding:
    def __init__(self):
        self.embedding = SentenceTransformer(embedding_model)
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
