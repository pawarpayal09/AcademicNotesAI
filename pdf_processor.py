import tempfile
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ==========================================================
# Embedding Model (Loaded Only Once)
# ==========================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)


# ==========================================================
# Create Vector Database From Uploaded PDF
# ==========================================================

def create_uploaded_vectorstore(uploaded_files):

    all_documents = []

    # Process every uploaded PDF
    for uploaded_file in uploaded_files:

        # Save temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp:

            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        # Read PDF
        loader = PyPDFLoader(temp_path)

        documents = loader.load()

        # Add documents to combined list
        all_documents.extend(documents)

        # Delete temporary file
        os.remove(temp_path)

    # Split all documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(all_documents)

    # Create one FAISS database
    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vectorstore
