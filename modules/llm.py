import os

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


@st.cache_resource
def load_llm():
    """
    Load the language model only once.
    """

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not set.")

    return ChatOpenAI(
        model="openrouter/free",
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.2,
        max_retries=2,
        timeout=120,
    )


class ContractLLM:
    """
    Handles communication with the language model.
    """

    def __init__(self):

        self.llm = load_llm()

    def generate(self, prompt: str) -> str:
        """
        Generate a response from the language model.
        """

        response = self.llm.invoke(prompt)

        return response.content