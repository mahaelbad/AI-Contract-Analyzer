import easyocr


class OCRProcessor:
    """
    Extracts text from image-based PDF pages using EasyOCR.
    """

    def __init__(self):
        self.reader = easyocr.Reader(
            ["en", "ar"],
            gpu=False
        )

    def extract_text(self, image_paths: list[str]) -> str:
        """
        Extract text from a list of images.

        Args:
            image_paths: List of image file paths.

        Returns:
            Extracted text as a single string.
        """

        extracted_pages = []

        for image_path in image_paths:

            page_text = self.reader.readtext(
                image_path,
                detail=0
            )

            extracted_pages.append("\n".join(page_text))

        return "\n\n".join(extracted_pages).strip()