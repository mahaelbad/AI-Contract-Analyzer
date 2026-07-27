class ContractRetriever:
    """
    Retrieves the most relevant chunks from the vector database.
    """

    def __init__(self, vector_store):
        self.retriever = vector_store.as_retriever()

    def retrieve(self, query: str):
        """
        Retrieve relevant document chunks.
        """
        return self.retriever.invoke(query)