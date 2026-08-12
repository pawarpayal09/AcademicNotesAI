import streamlit as st
from pathlib import Path

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Academic Notes AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOAD CUSTOM CSS
# =====================================================

css_file = Path("css/style.css")

if css_file.exists():

    with open(css_file, "r", encoding="utf-8") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
    # 📚 Academic Notes AI

    ### Learn Smarter with AI
    """)

    st.divider()

    st.info("""
### 🤖 About

An AI-powered academic assistant that helps students:

- 📚 Search academic notes
- 📄 Chat with uploaded PDFs
- 🧠 Learn difficult concepts
- ⚡ Get instant answers
""")

    st.divider()

    st.markdown("### 🚀 Technologies")

    st.success("🤖 Google Gemini")
    st.success("🦜 LangChain")
    st.success("📚 FAISS")
    st.success("🧠 RAG")
    st.success("⚡ Streamlit")

    st.divider()

    st.markdown("### 👩‍💻 Developer")

    st.info("""
**Payal Pawar**

🎓 MCA Student

Academic Notes AI

Version 1.0
""")

# =====================================================
# LOGO + TITLE HERO HEADER
# =====================================================

st.markdown("""
<h1 style="
text-align:center;
font-size:56px;
font-weight:800;
margin-bottom:0px;
">
📚 Academic Notes AI
</h1>

<h4 style="
text-align:center;
opacity:0.8;
font-weight:500;
margin-top:0px;
">
Learn Smarter • Search Faster • Understand Better
</h4>

""",
unsafe_allow_html=True)

st.markdown(
"""
Transform your learning experience with an **AI-powered academic assistant**
built using **Google Gemini, LangChain, FAISS Vector Search,
and Retrieval-Augmented Generation (RAG).**

Whether you're revising your university notes or chatting with your own uploaded PDF,
the chatbot retrieves the most relevant information and generates
accurate, detailed, student-friendly answers along with source references.

It is designed to help students understand concepts faster,
prepare for examinations, and interact naturally with academic documents.
"""
)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.success("🤖 Gemini")

with col2:
    st.success("🦜 LangChain")

with col3:
    st.success("📚 FAISS")

with col4:
    st.success("🧠 RAG")

with col5:
    st.success("⚡ Streamlit")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
## 🚀 Choose How You Want to Learn
"""
)

st.write(
    "Select one of the two learning modes from the sidebar. "
    "Both modes use the same AI engine but different knowledge sources."
)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# TWO FEATURE CARDS
# ==========================================

col1, col2 = st.columns(2)

# ------------------------------------------
# CARD 1 - ACADEMIC NOTES
# ------------------------------------------

with col1:

    with st.container(key="academic_notes_card"):

        st.info(
            """
### 📚 Academic Notes

Search across the academic notes that are already included in this project.

#### ✨ Features

- ✅ Multiple Subject PDFs
- ✅ Fast Semantic Search
- ✅ Gemini AI Answers
- ✅ Source References
- ✅ MCA Exam Preparation
- ✅ Accurate Context-Based Responses

Perfect for revising your syllabus quickly and preparing for university examinations.
"""
        )


# ------------------------------------------
# CARD 2 - UPLOAD PDF
# ------------------------------------------

with col2:

    with st.container(key="upload_pdf_card"):

        st.info(
            """
### 📄 Upload Your Own PDF

Upload any PDF and instantly start chatting with your own document.

#### ✨ Features

- ✅ Upload Your Own PDF
- ✅ Automatic Embedding Generation
- ✅ FAISS Vector Database
- ✅ Gemini Powered Answers
- ✅ Works with Notes, Books & Research Papers
- ✅ Private Document Question Answering

Perfect for studying your own notes, books, assignments, and research papers.
"""
        )

col1, col2, col3 = st.columns([1,2,1])

with col2:

    if st.button(
        "🚀 Start Chatting",
        use_container_width=True,
        type="primary"
    ):
        
        st.switch_page("pages/Chatbot.py")

    
