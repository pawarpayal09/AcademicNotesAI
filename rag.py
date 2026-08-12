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
    MAIN_CHAT_API_KEY_5 = st.secrets["MAIN_CHAT_API_KEY_5"]
except Exception:
    MAIN_CHAT_API_KEY_5 = os.getenv("MAIN_CHAT_API_KEY_5")

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
# Gemini API Keys
# ==========================================================

def get_google_api_keys():

    keys = []

    # Streamlit Cloud / deployed project
    for key_name in [
        "MAIN_CHAT_API_KEY_5",
        "IMAGE_STUDY_API_KEY_4",
        "Text_to_Speech_API_KEY_3",
        "Speech_to_Text_API_KEY_2",
        "MAIN_CHAT_API_KEY_1"
    ]:

        try:
            key = st.secrets.get(key_name)
        except Exception:
            key = None

        if key:
            keys.append(key)

    # Local .env
    for key_name in [
        "MAIN_CHAT_API_KEY_5",
        "IMAGE_STUDY_API_KEY_4",
        "Text_to_Speech_API_KEY_3",
        "Speech_to_Text_API_KEY_2",
        "MAIN_CHAT_API_KEY_1"
    ]:

        key = os.getenv(key_name)

        if key and key not in keys:
            keys.append(key)

    return keys


GOOGLE_API_KEYS = get_google_api_keys()


# ==========================================================
# Gemini Model Factory
# ==========================================================

def create_gemini_model(api_key):

    return ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0.2,
        google_api_key=api_key
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

    # ==========================================================
    # Try Gemini API Keys
    # ==========================================================

    last_error = None

    for key_number, api_key in enumerate(
        GOOGLE_API_KEYS,
        start=1
    ):

        try:

            print(
                f"\nTrying Gemini API Key {key_number}..."
            )

            current_llm = create_gemini_model(
                api_key
            )

            response = current_llm.invoke(
                prompt
            )

            answer = extract_answer(
                response
            )

            source_list = []

            for doc in docs:

                pdf_name = os.path.basename(
                    doc.metadata.get(
                        "source",
                        "Unknown.pdf"
                    )
                )

                if pdf_name not in source_list:
                    source_list.append(
                        pdf_name
                    )

            print(
                f"Gemini API Key "
                f"{key_number} succeeded."
            )

            return {
                "answer": answer,
                "sources": source_list
            }

        except Exception as e:

            last_error = e

            print(
                f"\nGemini API Key "
                f"{key_number} failed."
            )

            print(e)

            if key_number < len(
                GOOGLE_API_KEYS
            ):

                print(
                    f"Trying Gemini API Key "
                    f"{key_number + 1}..."
                )

                time.sleep(2)

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

def ask_uploaded_pdf_question(
    question,
    vectorstore
):

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

    # ==========================================================
    # Try Gemini API Keys
    # ==========================================================

    last_error = None

    for key_number, api_key in enumerate(
        GOOGLE_API_KEYS,
        start=1
    ):

        try:

            print(
                f"\nTrying Gemini API Key "
                f"{key_number}..."
            )

            current_llm = create_gemini_model(
                api_key
            )

            response = current_llm.invoke(
                prompt
            )

            answer = extract_answer(
                response
            )

            source_list = []

            for doc in docs:

                file_name = doc.metadata.get(
                    "source",
                    "Uploaded PDF"
                )

                file_name = file_name.split("\\")[-1]
                file_name = file_name.split("/")[-1]

                if file_name not in source_list:

                    source_list.append(
                        file_name
                    )

            print(
                f"Gemini API Key "
                f"{key_number} succeeded."
            )

            return {
                "answer": answer,
                "sources": source_list
            }

        except Exception as e:

            last_error = e

            print(
                f"\nGemini API Key "
                f"{key_number} failed."
            )

            print(e)

            if key_number < len(
                GOOGLE_API_KEYS
            ):

                print(
                    f"Trying Gemini API Key "
                    f"{key_number + 1}..."
                )

                time.sleep(2)

    return {

        "answer":
        "⚠ Gemini server is currently busy. Please try again.",

        "sources": []

    }