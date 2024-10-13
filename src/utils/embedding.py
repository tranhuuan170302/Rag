from sentence_transformers import SentenceTransformer

# Load pre-trained Sentence Transformer model
embedding_model = SentenceTransformer("thenlper/gte-large")

def get_embedding(text: str) -> list[float]:
    if not text.strip():
        print("Attempting to get embedding")
        return []
    embeddings = embedding_model.encode([text])
    return embeddings.tolist()