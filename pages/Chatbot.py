import os
import time
import streamlit as st
from datetime import datetime, timedelta
from speech import text_to_speech
from pdf_export import generate_chat_pdf
from favourites_manager import add_favourite

from rag import (
    ask_question,
    ask_uploaded_pdf_question
)

from pdf_processor import (
    create_uploaded_vectorstore
)

from chat_history_manager import (
    load_chat_history,
    add_chat,
    update_chat
)

st.set_page_config(
    page_title="Academic Notes AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)
    
# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_vectorstore" not in st.session_state:
    st.session_state.uploaded_vectorstore = None

# =====================================================
# CHAT HISTORY SESSION
# =====================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# =====================================================
# PROFESSIONAL HEADER
# =====================================================

st.markdown("""
<h1 style="
    font-size:42px;
    font-weight:800;
    margin-bottom:0px;
">
📚 Academic Notes AI
</h1>

<p style="
    color:gray;
    font-size:18px;
    margin-top:-8px;
">
Your Personal AI Study Assistant
</p>
""",
unsafe_allow_html=True)

badge1, badge2, badge3, badge4 = st.columns(4)

with badge1:
    st.success("🤖 Gemini")

with badge2:
    st.success("🦜 LangChain")

with badge3:
    st.success("📚 FAISS")

with badge4:
    st.success("🧠 RAG")

st.divider()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("app.py")

    st.divider()

    st.markdown("""
    # 📚 Academic Notes AI

    Learn Smarter with AI
    """,
    unsafe_allow_html=True)

    st.info("""
    ### 🎓 AI Study Assistant

    Ask questions from:

    📚 Academic Notes

    📄 Your Own PDF

    Receive accurate answers with source references.
    """)

    st.divider()

    # ==========================================
    # KNOWLEDGE SOURCE
    # ==========================================

    st.markdown("## 📖 Knowledge Source")

    knowledge_mode = st.radio(
        "Choose Chatbot Mode",
        (
            "📚 Academic Notes",
            "📄 Upload My Own PDF"
        )
    )

    st.divider()

    # ==========================================
    # MODE 1
    # ==========================================

    if knowledge_mode == "📚 Academic Notes":

        st.markdown("## 📚 Available Notes")

        data_folder = "data"

        pdf_files = sorted(
            [
                file
                for file in os.listdir(data_folder)
                if file.lower().endswith(".pdf")
            ]
        )

        if pdf_files:

            for pdf in pdf_files:

                st.success(f"📄 {pdf}")

            st.caption(f"📚 Total PDFs : {len(pdf_files)}")

        else:

            st.warning("No PDF files found.")

    # ==========================================
    # MODE 2
    # ==========================================

    else:

        st.markdown("## 📄 Upload PDF")

        uploaded_files = st.file_uploader(
            "📚 Upload One or More PDF Files",
            type=["pdf"],
            accept_multiple_files=True
        )

        if uploaded_files:

            st.success(f"✅ {len(uploaded_files)} PDF(s) selected")

            for pdf in uploaded_files:
                st.write(f"📄 {pdf.name}")

            if st.session_state.uploaded_vectorstore is None:

                with st.spinner(
                    "📖 Reading PDFs...\n\n"
                    "🧠 Creating Embeddings...\n\n"
                    "📚 Building Knowledge Base..."
                ):

                    st.session_state.uploaded_vectorstore = (
                        create_uploaded_vectorstore(uploaded_files)
                    )

                st.success("✅ All PDFs processed successfully.")

            else:

                st.info("✅ PDFs already processed.")

    st.divider()

    # ==========================================
    # SUGGESTED QUESTIONS
    # ==========================================

    st.markdown("💡 Suggested Questions")

    st.markdown(
        """
- What is Artificial Intelligence?
- What is Machine Learning?
- Explain Supervised Learning.
- Explain Unsupervised Learning.
- Explain Classification.
- Explain Regression.
- What is DBMS?
- Explain Normalization.
- Explain SQL.
- Explain Cloud Computing.
- Explain IaaS.
- Explain PaaS.
- Explain SaaS.
- Explain Cloud Security.
- Explain the concept of Data Stucture.
- What are the components of Operating System?
- Explain the structure of Operating System.
- What is Malware and its types.
- Explain the kinds of Cyber Crime.
- What is Data Science? Also explain Data Science Lifecycle.
- What are the Roles in Data Science?
"""
    )

    st.divider()
  
    # =====================================================
    # CHAT HISTORY
    # =====================================================


    st.subheader("💬 Chat History")

    history = load_chat_history()

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    today_chats = []
    yesterday_chats = []
    older_chats = []

    for chat in history:

        chat_date = datetime.strptime(
            chat["date"],
            "%Y-%m-%d"
        ).date()

        if chat_date == today:

            today_chats.append(chat)

        elif chat_date == yesterday:

            yesterday_chats.append(chat)

        else:

            older_chats.append(chat)

    # -----------------------------
    # TODAY
    # -----------------------------

    if today_chats:

        st.markdown("#### 📅 Today")

        for chat in reversed(today_chats):

            if st.button(
                f"📝 {chat['title']}",
                key=chat["id"],
                use_container_width=True
            ):

                st.session_state.messages = chat["messages"]

                st.session_state.current_chat_id = chat["id"]

                st.rerun()

    # -----------------------------
    # YESTERDAY
    # -----------------------------

    if yesterday_chats:

        st.markdown("#### 📅 Yesterday")

        for chat in reversed(yesterday_chats):

            if st.button(
                f"📝 {chat['title']}",
                key="y"+chat["id"],
                use_container_width=True
            ):

                st.session_state.messages = chat["messages"]

                st.session_state.current_chat_id = chat["id"]

                st.rerun()

    # -----------------------------
    # OLDER CHATS
    # -----------------------------

    if older_chats:

        st.markdown("#### 📅 Older")

        for chat in reversed(older_chats):

            if st.button(
                f"📝 {chat['title']}",
                key="o"+chat["id"],
                use_container_width=True
            ):

                st.session_state.messages = chat["messages"]

                st.session_state.current_chat_id = chat["id"]

                st.rerun()

    # -----------------------------
    # NEW CHAT
    # -----------------------------

    st.write("")

    if st.button(
        "➕ New Chat",
        use_container_width=True,
        type="primary"
    ):

        st.session_state.messages = []

        st.session_state.current_chat_id = None

        st.rerun()

    st.divider()
    
    # ==========================================
    # SAVED NOTES
    # ==========================================

    if st.button(
        "📌 Saved Notes",
        use_container_width=True
    ):
        st.switch_page("pages/FavouriteNotes.py")

    # ==========================================
    # CLEAR CHAT
    # ==========================================

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.current_chat_title = "New Chat"

        st.rerun()

    st.divider()

    # ==========================================
    # DEVELOPER
    # ==========================================

    st.markdown("👩‍💻 Developer")

    st.info(
        """
**Payal Pawar**

MCA Student

Academic Notes AI Chatbot

Gemini • LangChain • FAISS
"""
    )

st.divider()

# =====================================================
# SAVE SUCCESS POPUP
# =====================================================

if st.session_state.get("saved_success", False):

    st.toast(
        "✅ Note added to Saved Notes",
        icon="📌"
    )

    st.session_state.saved_success = False

# =====================================================
# CHAT HISTORY
# =====================================================

for i, message in enumerate(st.session_state.messages):

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            # ==========================================
            # ACTION BUTTONS
            # ==========================================

            col1, col2, col3 = st.columns(3)

            # ------------------------------------------
            # SAVE NOTE
            # ------------------------------------------

            with col1:

                if st.button(
                    "📌 Save Note",
                    key=f"fav_{i}",
                    use_container_width=True
                ):

                    # Find the user question just before this answer
                    question = ""

                    if i > 0:

                        previous = st.session_state.messages[i - 1]

                        if previous["role"] == "user":

                            question = previous["content"]

                    add_favourite(
                        question=question,
                        answer=message["content"],
                        sources=message.get("sources", [])
                    )

                    # Success message for 2 seconds
                    st.session_state.saved_success = True

                    st.rerun()

            # ------------------------------------------
            # LISTEN ANSWER
            # ------------------------------------------

            with col2:

                if st.button(
                    "🔊 Listen",
                    key=f"tts_{i}_{abs(hash(message['content']))}",
                    use_container_width=True
                ):

                    audio_file = text_to_speech(message["content"])

                    with open(audio_file, "rb") as f:

                        st.audio(
                            f.read(),
                            format="audio/mp3"
                        )

            # ------------------------------------------
            # DOWNLOAD PDF
            # ------------------------------------------

            with col3:

                pdf_buffer = generate_chat_pdf(
                    st.session_state.messages
                )

                st.download_button(
                    label="📥 Download",
                    data=pdf_buffer,
                    file_name="AcademicNotesAI_Chat.pdf",
                    mime="application/pdf",
                    key=f"download_chat_pdf_{i}_{abs(hash(message['content']))}",
                    use_container_width=True
                )

            # ==========================================
            # SOURCE DOCUMENTS
            # ==========================================

            if message.get("sources"):

                with st.expander("📚 Source Documents Used"):

                    for source in message["sources"]:

                        st.write(f"✅ {source}")

# =====================================================
# CHAT INPUT
# =====================================================

question = st.chat_input(
    "Ask your academic question..."
)

# =====================================================
# PROCESS USER QUESTION
# =====================================================

if question:
    # Save first question as chat title

    if len(st.session_state.messages) == 0:

        st.session_state.chat_history.append(question[:40])

    # -----------------------------
    # Save User Message
    # -----------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # -----------------------------
    # Display User Message
    # -----------------------------

    with st.chat_message("user"):

        st.markdown(question)

    # -----------------------------
    # Assistant Response
    # -----------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 Searching notes and generating answer..."
        ):            
                        
            # ==========================================
            # MODE 1 : Academic Notes
            # ==========================================

            if knowledge_mode == "📚 Academic Notes":

                result = ask_question(question)

            # ==========================================
            # MODE 2 : Uploaded PDF
            # ==========================================

            else:

                if st.session_state.uploaded_vectorstore is None:

                    st.warning("⚠ Please upload a PDF first.")

                    st.stop()

                result = ask_uploaded_pdf_question(
                    question,
                    st.session_state.uploaded_vectorstore
                )

            # ==========================================
            # Extract Result
            # ==========================================

            answer = result["answer"]
            sources = result["sources"]

        # ==========================================
        # Display Answer
        # ==========================================

        st.markdown(answer)

        # ==========================================
        # Source Documents
        # ==========================================

        if sources:

            with st.expander("📚 Source Documents Used"):

                for source in sources:

                    st.write(f"✅ {source}")

    # ==========================================
    # Save Assistant Message
    # ==========================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources
        }
    )

    # ==========================================
    # SAVE CHAT
    # ==========================================

    if st.session_state.current_chat_id is None:

        title = question[:50]

        add_chat(
            title,
            st.session_state.messages
        )

        st.session_state.chat_history = load_chat_history()

        st.session_state.current_chat_id = (
            st.session_state.chat_history[-1]["id"]
        )

    else:

        update_chat(
            st.session_state.current_chat_id,
            st.session_state.messages
        )

        st.session_state.chat_history = load_chat_history()

# =====================================================
# FOOTER
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:

    st.caption("📚 Academic Notes AI")

with col2:

    st.caption("⚡ Powered by Gemini + LangChain + FAISS")

with col3:

    st.caption("👩‍💻 Developed by Payal Pawar")
            
