import re


class TextCleaner:
    """
    Cleans extracted text before chunking.
    """

    def clean(self, text: str) -> str:
        """
        Clean extracted document text.

        Args:
            text: Raw extracted text.

        Returns:
            Cleaned text.
        """

        if not text:
            return ""

        # Remove extra spaces and tabs
        text = re.sub(r"[ \t]+", " ", text)

        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Remove multiple empty lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()