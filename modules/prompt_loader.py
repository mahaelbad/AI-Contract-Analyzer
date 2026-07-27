from pathlib import Path


class PromptLoader:
    """
    Loads prompt templates from the prompts directory.
    """

    def __init__(self):
        self.prompts_path = Path("prompts")

    def load(self, prompt_name: str) -> str:
        """
        Load a prompt template by name.

        Args:
            prompt_name: Name of the prompt file (without .txt).

        Returns:
            The prompt template as a string.

        Raises:
            FileNotFoundError: If the prompt file does not exist.
        """

        file_path = self.prompts_path / f"{prompt_name}.txt"

        if not file_path.exists():
            raise FileNotFoundError(
                f"Prompt '{prompt_name}' not found."
            )

        return file_path.read_text(encoding="utf-8")