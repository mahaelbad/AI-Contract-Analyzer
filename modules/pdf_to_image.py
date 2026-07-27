import os
import shutil
import fitz


class PDFToImageConverter:
    """
    Converts each PDF page into a high-resolution image.
    """

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def convert(self, output_folder: str = "temp_images") -> list[str]:
        """
        Convert PDF pages to PNG images.

        Args:
            output_folder: Folder where images will be saved.

        Returns:
            List of generated image paths.
        """

        # Remove old images if the folder already exists
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)

        os.makedirs(output_folder, exist_ok=True)

        image_paths = []

        with fitz.open(self.pdf_path) as pdf:

            for page_index, page in enumerate(pdf):

                pixmap = page.get_pixmap(dpi=300)

                image_path = os.path.join(
                    output_folder,
                    f"page_{page_index + 1}.png"
                )

                pixmap.save(image_path)

                image_paths.append(image_path)

        return image_paths