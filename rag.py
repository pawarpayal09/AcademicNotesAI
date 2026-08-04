import os
import time
import streamlit as st
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ==========================================================
# Cached Embedding Model
# ==========================================================

@st.cache_resource(show_spinner=False)
def load_embeddings():

    print("Loading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    print("Embedding model loaded.")

    return embeddings


embeddings = load_embeddings()

# ==========================================================
# Cached FAISS Database
# ==========================================================

@st.cache_resource(show_spinner=False)
def load_vectorstore():

    print("Loading FAISS vector database...")

    db = FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("Vector database loaded.")

    return db


db = load_vectorstore()

# ==========================================================
# Optimized Retriever
# ==========================================================

retriever = db.as_retriever(

    search_type="mmr",

    search_kwargs={

        # Final chunks sent to Gemini
        "k": 3,

        # Search more internally
        "fetch_k": 10,

        # Balance relevance & diversity
        "lambda_mult": 0.7

    }

)

# ==========================================================
# Gemini Model
# ==========================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0.2,
)

# ==========================================================
# Extract Gemini Response
# ==========================================================

def extract_answer(response):

    if hasattr(response, "content"):

        content = response.content

        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):

            answer = ""

            for item in content:

                if hasattr(item, "text"):
                    answer += item.text + "\n"

                elif isinstance(item, dict):
                    answer += item.get("text", "") + "\n"

                else:
                    answer += str(item)

            return answer.strip()

    return str(response)

# ==========================================================
# Ask Question
# ==========================================================

def ask_question(question):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are an expert Academic Notes AI Assistant.

IMPORTANT RULES

1. Answer ONLY using the provided notes.
2. Never use outside knowledge.
3. If the notes do not contain the answer, reply exactly:

"I couldn't find this information in the uploaded notes."

4. Write the answer in simple student-friendly language.
5. Be detailed whenever sufficient information exists.
6. Use proper headings and bullet points.
7. Do not repeat the same information.

----------------------------------------

NOTES

{context}

----------------------------------------

QUESTION

{question}

----------------------------------------

Write the answer using this structure whenever applicable:

 Definition

 Explanation

 Key Points

 Advantages

 Disadvantages

 Applications

 Example

 Conclusion

Keep the answer detailed but concise.
"""

    for attempt in range(3):

        try:

            response = llm.invoke(prompt)

            answer = extract_answer(response)

            source_list = []

            for doc in docs:

                pdf_name = os.path.basename(
                    doc.metadata.get("source", "Unknown.pdf")
                )

                if pdf_name not in source_list:
                    source_list.append(pdf_name)

            return {
                "answer": answer,
                "sources": source_list
            }

        except Exception as e:

            print(f"\nAttempt {attempt+1} failed.")
            print(e)

            if attempt < 2:
                print("\nRetrying in 5 seconds...\n")
                time.sleep(5)

    return {
        "answer": """⚠ Gemini server is currently busy.

Please try again after a few seconds.

Your documents are already loaded correctly.
Only the Gemini server is temporarily unavailable.""",
        "sources": []
    }
# ==========================================================
# MODE 2 : Uploaded PDF Chat
# ==========================================================

def ask_uploaded_pdf_question(question, vectorstore):

    retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 3,
        "fetch_k": 10,
        "lambda_mult": 0.7
    }
)

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are an expert PDF AI Assistant.

Answer ONLY using the uploaded PDF.

Never use outside knowledge.

If the answer exists inside the PDF,
explain it clearly and in detail.

Your answer should contain:

# Definition

# Explanation

# Key Points

# Advantages (if applicable)

# Disadvantages (if applicable)

# Applications (if applicable)

# Example (if available)

# Conclusion

Formatting Rules:

- Use proper headings.
- Use bullet points.
- Write in simple language.
- Do not invent information.
- If the answer is not found, reply:

"I couldn't find this information in the uploaded PDF."

========================

PDF CONTENT

{context}

========================

QUESTION

{question}

========================

ANSWER
"""

    for attempt in range(3):

        try:

            response = llm.invoke(prompt)

            answer = extract_answer(response)

            source_list = []

            for doc in docs:

                file_name = doc.metadata.get("source", "Uploaded PDF")

                file_name = file_name.split("\\")[-1]
                file_name = file_name.split("/")[-1]

                if file_name not in source_list:
                    source_list.append(file_name)

            return {
                "answer": answer,
                "sources": source_list
            }

        except Exception as e:

            print(f"Attempt {attempt+1} failed.")

            print(e)

            time.sleep(5)

    return {

        "answer":
        "⚠ Gemini server is currently busy. Please try again.",

        "sources": []

    }