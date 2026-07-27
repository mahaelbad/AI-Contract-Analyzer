from modules.llm import ContractLLM
from modules.retriever import ContractRetriever
from modules.prompt_loader import PromptLoader


class ContractAnalyzer:
    """
    Main business logic for contract analysis.
    """

    def __init__(self, vector_store):

        self.retriever = ContractRetriever(vector_store)
        self.llm = ContractLLM()
        self.prompt_loader = PromptLoader()

    def _build_context(self, query: str) -> str:
        """
        Retrieve the most relevant document chunks.
        """

        documents = self.retriever.retrieve(query)

        return "\n\n".join(
            doc.page_content
            for doc in documents
        )

    def _build_prompt(
    self,
    template_name: str,
    context: str,
    question: str = ""):
        template = self.prompt_loader.load(template_name)

        return template.format(
        context=context,
        question=question
      )

    def _run_analysis(
        self,
        retrieval_query: str,
        template_name: str,
        question: str = ""
    ) -> str:
        """
        Execute a complete RAG pipeline.
        """

        context = self._build_context(retrieval_query)

        if not context.strip():
            return "No relevant information was found in the contract."

        prompt = self._build_prompt(
            template_name,
            context,
            question
        )

        return self.llm.generate(prompt)

    def ask(self, question: str) -> str:

        return self._run_analysis(
            retrieval_query=question,
            template_name="custom",
            question=question
        )

    def summarize(self) -> str:

        return self._run_analysis(
            retrieval_query="Contract Summary",
            template_name="summary"
        )

    def detect_risks(self) -> str:

        return self._run_analysis(
            retrieval_query="Legal Risks",
            template_name="risks"
        )

    def payment_terms(self) -> str:

        return self._run_analysis(
            retrieval_query="Payment Terms",
            template_name="payment"
        )

    def important_dates(self) -> str:

        return self._run_analysis(
            retrieval_query="Important Dates",
            template_name="dates"
        )

    def termination_clause(self) -> str:

        return self._run_analysis(
            retrieval_query="Termination Clause",
            template_name="termination"
        )