from API.Rag.embedding import get_embedding
from abc import ABC, abstractmethod
# Search query

class VectorSearch(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def vector_search(**kwargs):
        pass

class VectorSearchImpl(VectorSearch):
    def __init__(self):
        pass
    
    def vector_search(self, user_query, category, collection):
        """
        Thực hiện vector search trong content_chunks của một document theo document_id.
        """
        # Lấy embedding từ truy vấn người dùng
        query_embedding = get_embedding.encoder_query(user_query)
        if query_embedding is None:
            return "Invalid query embedding"
        
        match_stage = {
            "$match": {
                "nameCategory": category
            }
        }
        # Stage 1: Vector search (phải là stage đầu tiên)
        vector_search_stage = {
            "$vectorSearch": {
                "index": "vector_index",          # Tên index vector
                "path": "embedding",  # Đường dẫn tới embedding trong content_chunks
                "queryVector": query_embedding,   # Embedding query
                "numCandidates": 400,             # Số lượng ứng viên ban đầu
                "limit": 3                       # Số lượng kết quả trả về
            }
        }


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

        # Tạo pipeline
        pipeline = [vector_search_stage, match_stage, project_stage]

        # Thực thi truy vấn
        try:
            results = list(collection.aggregate(pipeline))
            return results
        except Exception as e:
            return {"error": str(e)}


class VectorSearchQaImpl(VectorSearch):
    def __init__(self):
        pass

    def vector_search(self, user_query, collection):
        """
        Thực hiện vector search trong content_chunks của một document theo document_id.
        """
        # Lấy embedding từ truy vấn người dùng
        query_embedding = get_embedding.encoder_query(user_query)
        if query_embedding is None:
            return "Invalid query embedding"
        
        # Stage 1: Vector search (phải là stage đầu tiên)
        vector_search_stage = {
            "$vectorSearch": {
                "index": "vector_index",          # name index vector
                "path": "embedding",                # url embedding in content_chunks
                "queryVector": query_embedding,   # Embedding query
                "numCandidates": 400,             # number candidates
                "limit": 2                       # number return
            }
        }


        project_stage = {
            "$project": {
                "_id": 0,  # Không lấy ObjectId
            "answer": 1,
                "score": {
                    "$meta": "vectorSearchScore"  # Lấy điểm số vector search
                }
            }
        }

        # Tạo pipeline
        pipeline = [vector_search_stage, project_stage]

        # Thực thi truy vấn
        try:
            results = list(collection.aggregate(pipeline))
            print(f"đây là câu trả lời {results}")
            return results
        except Exception as e:
            return {"error": str(e)}

class SearchResult(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_search_result(self, **kwargs):
        pass

class SearchResultImpl(SearchResult):
    def __init__(self):
        pass
    
    def get_search_result(self, get_knowledge):
        search_result = ""
        for index, result in enumerate(get_knowledge):
            search_result += f""" - tên sản phẩm {index}: {result["name"]} \n
                                - đường dẫn sản phẩm {index}: {result["short_url"]} \n
                                - mô tả sản phẩm {index}: {result["short_description"]} \n
                                - đánh giá trung bình của sản phẩm {index}: {result["rating_average"]} \n
                                - số lượt bán của sản phẩm {index}: {result["quantity_sold"]} \n
                                """
        return search_result
