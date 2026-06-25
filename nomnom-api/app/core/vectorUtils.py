from functools import lru_cache

from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def foodVectorGenerate(description: str) -> list[float]:
    model = _get_model()
    embedding = model.encode(description, convert_to_numpy=True)
    return embedding.tolist()
