from docling.document_converter import DocumentConverter


class PDFLoader:
    """
    Extracts text from text-based PDF documents using Docling.
    """

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.converter = DocumentConverter()

    def extract_text(self) -> str:
        """
        Extract text from the PDF document.

        Returns:
            str: Extracted document text.

        Raises:
            RuntimeError: If the document cannot be processed.
        """
        try:
            result = self.converter.convert(self.pdf_path)

            text = result.document.export_to_markdown().strip()

            if not text:
                raise ValueError("No readable text found.")

            return text

        except Exception as e:
            raise RuntimeError(f"Failed to process document: {e}") from e