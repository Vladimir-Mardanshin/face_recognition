from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

COLLECTION_NAME = "face_embeddings"

qdrant_client = QdrantClient(
    url="https://25e39288-f739-4a00-900b-e9fc20483a7e.eu-central-1-0.aws.cloud.qdrant.io:6333",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.y6gFejDaz_7Vy2IItsLeV-QQJmJwa7qIC-eajFw5XPc"
)

_global_id_counter = 0


def setup_collection():
    collections = qdrant_client.get_collections().collections
    if not any(c.name == COLLECTION_NAME for c in collections):
        qdrant_client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=512, distance=Distance.COSINE),
        )


def save_embedding(name: str, embedding: list):
    global _global_id_counter
    point = PointStruct(
        id=_global_id_counter,
        vector=embedding,
        payload={"name": name}
    )
    _global_id_counter += 1

    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=[point])


def search_embedding(query_embedding: list, top_k=1):
    results = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k,
        with_payload=True
    )
    return results


def get_all_embeddings():
    scroll = qdrant_client.scroll(
        collection_name=COLLECTION_NAME,
        with_vectors=True,
        with_payload=True,
        limit=10000
    )
    points = scroll[0]
    return [
        {
            "id": point.id,
            "name": point.payload.get("name"),
            "vector": point.vector
        }
        for point in points
    ]
