from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


class VectorStore:
    """
    Manages the Qdrant vector database using an in-memory database.
    """

    COLLECTION_NAME = "contracts"
    VECTOR_SIZE = 1024

    def __init__(self, embedding_model):

        self.embedding_model = embedding_model

        self.client = QdrantClient(":memory:")

        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=self.VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )

        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.COLLECTION_NAME,
            embedding=self.embedding_model.model
        )

    def add_documents(self, chunks: list[str]) -> None:
        """
        Store text chunks in Qdrant.
        """

        if not chunks:
            return

        self.vector_store.add_texts(texts=chunks)

    def as_retriever(self):

        return self.vector_store.as_retriever(
            search_kwargs={"k": 3}
        )