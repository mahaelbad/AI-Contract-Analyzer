from modules.pdf_loader import PDFLoader
from modules.pdf_to_image import PDFToImageConverter
from modules.ocr import OCRProcessor
from modules.text_cleaner import TextCleaner


class DocumentLoader:
    """
    Handles document loading and automatically selects
    the best text extraction method.
    """

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.cleaner = TextCleaner()

    def extract_text(self) -> str:
        """
        Extract text using Docling first.
        If the extracted text is invalid, automatically
        switch to OCR.
        """

        try:
            loader = PDFLoader(self.pdf_path)

            text = loader.extract_text()

            if self._is_valid_text(text):
                return self.cleaner.clean(text)

            print("Poor text quality detected. Switching to OCR...")

        except Exception as e:
            print(f"Docling failed: {e}")

        return self._extract_with_ocr()

    def _extract_with_ocr(self) -> str:
        """
        Extract text using OCR.
        """

        converter = PDFToImageConverter(self.pdf_path)

        image_paths = converter.convert()

        ocr = OCRProcessor()

        text = ocr.extract_text(image_paths)

        return self.cleaner.clean(text)

    def _is_valid_text(self, text: str) -> bool:
        """
        Check whether the extracted text is valid.
        """

        if not text:
            return False

        words = text.split()

        if len(words) < 20:
            return False

        strange_chars = sum(
            1
            for c in text
            if not (
                c.isalnum()
                or c.isspace()
                or c in ".,;:-()/%$"
            )
        )

        ratio = strange_chars / max(len(text), 1)

        return ratio <= 0.30