# app.py
import tempfile
import streamlit as st

from modules.analyzer import ContractAnalyzer
from modules.chunker import TextChunker
from modules.document_loader import DocumentLoader
from modules.embedding import EmbeddingModel
from modules.vector_store import VectorStore

st.set_page_config(page_title="AI Contract Analyzer", page_icon="📄", layout="wide")
st.title("📄 AI Contract Analyzer")

if "processed" not in st.session_state:
    st.session_state.processed = False
if "analyzer" not in st.session_state:
    st.session_state.analyzer = None
if "analysis_cache" not in st.session_state:
    st.session_state.analysis_cache = {}

uploaded_file = st.file_uploader("Upload Contract", type=["pdf"])

def process_contract(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file.read())
        pdf_path = temp_file.name

    print("="*50)
    print("Starting contract processing...")

    loader = DocumentLoader(pdf_path)
    text = loader.extract_text()
    print(f"Text extracted: {len(text)} chars")

    chunks = TextChunker().chunk(text)
    print(f"Chunks: {len(chunks)}")

    embedding = EmbeddingModel()
    vector_store = VectorStore(embedding)
    vector_store.add_documents(chunks)

    print("Contract indexed successfully")
    return ContractAnalyzer(vector_store)

if uploaded_file is not None:
    if st.button("Process Contract"):
        with st.spinner("Processing contract..."):
            st.session_state.analyzer = process_contract(uploaded_file)
            st.session_state.analysis_cache = {}
            st.session_state.processed = True
        st.success("✅ Contract processed successfully!")

if st.session_state.processed:
    analyzer = st.session_state.analyzer

    st.sidebar.title("Analysis")

    analysis_options = {
        "📄 Contract Summary": analyzer.summarize,
        "⚠️ Detect Risks": analyzer.detect_risks,
        "💰 Payment Terms": analyzer.payment_terms,
        "📅 Important Dates": analyzer.important_dates,
        "🛑 Termination Clause": analyzer.termination_clause,
    }

    for label, action in analysis_options.items():
        if st.sidebar.button(label):
            if label not in st.session_state.analysis_cache:
                with st.spinner("Processing..."):
                    st.session_state.analysis_cache[label] = action()

            st.subheader(label)
            st.write(st.session_state.analysis_cache[label])

    st.divider()

    question = st.text_input("Ask a question about the contract")

    if st.button("Ask AI"):
        if question.strip():
            cache_key = f"chat_{question}"

            if cache_key not in st.session_state.analysis_cache:
                with st.spinner("Thinking..."):
                    st.session_state.analysis_cache[cache_key] = analyzer.ask(question)

            st.subheader("Answer")
            st.write(st.session_state.analysis_cache[cache_key])
