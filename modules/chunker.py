from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:
    """
    Splits cleaned text into overlapping chunks for RAG.
    """

    def __init__(
        self,
        chunk_size: int = 1200,
        chunk_overlap: int = 250
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "; ",
                " ",
                ""
            ]
        )

    def chunk(self, text: str) -> list[str]:
        """
        Split text into overlapping chunks.

        Args:
            text: Cleaned document text.

        Returns:
            A list of text chunks.
        """
        return self.splitter.split_text(text)