import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings


@st.cache_resource
def load_embedding_model():
    """
    Load the embedding model only once.
    """

    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )


class EmbeddingModel:
    """
    Generates embeddings using BGE-M3.
    """

    def __init__(self):

        self.model = load_embedding_model()

    def embed_documents(self, texts: list[str]):
        return self.model.embed_documents(texts)

    def embed_query(self, query: str):
        return self.model.embed_query(query)