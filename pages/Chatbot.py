import os
import time
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta

from speech import text_to_speech
from pdf_export import generate_chat_pdf
from favourites_manager import add_favourite
from speech_to_text import speech_to_text

from firebase_manager import (
    require_login,
    is_authenticated,
    get_current_user,
    logout_user
)

from progress_manager import (
    record_chat_question
)


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Academic Notes AI",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# LOGIN REQUIRED
# =====================================================

require_login()


# =====================================================
# LOAD SHARED CSS
# =====================================================

def load_css():

    css_path = os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ),
        "css",
        "style.css"
    )

    if os.path.exists(css_path):

        with open(
            css_path,
            "r",
            encoding="utf-8"
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

    else:

        st.warning(
            f"⚠️ CSS file not found: {css_path}"
        )


load_css()


# =====================================================
# RAG IMPORTS
# =====================================================

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


# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


if "uploaded_vectorstore" not in st.session_state:
    st.session_state.uploaded_vectorstore = None


if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()


if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None


if "regenerate_question" not in st.session_state:
    st.session_state.regenerate_question = None


if "regenerate_index" not in st.session_state:
    st.session_state.regenerate_index = None


# =====================================================
# LOGGED-IN USER PROFILE
# TOP-RIGHT PROFESSIONAL PROFILE BAR
# =====================================================

if is_authenticated():

    current_user = get_current_user()

    profile_spacer, profile_area = st.columns(
        [5.8, 1.8],
        gap="small"
    )

    with profile_area:

        with st.container(
            key="home_user_profile"
        ):

            # -----------------------------------------
            # USER NAME
            # -----------------------------------------

            st.markdown(
                f"""
                <div class="home-profile-name">
                    👤 {current_user['name']}
                </div>
                """,
                unsafe_allow_html=True
            )

            # -----------------------------------------
            # USER EMAIL
            # -----------------------------------------

            st.markdown(
                f"""
                <div class="home-profile-email">
                    {current_user['email']}
                </div>
                """,
                unsafe_allow_html=True
            )

            # -----------------------------------------
            # LOGOUT
            # -----------------------------------------

            if st.button(
                "🚪 Logout",
                key="home_logout_button",
                use_container_width=True
            ):

                logout_user()

                st.rerun()


# =====================================================
# PROFESSIONAL HEADER
# =====================================================

st.markdown(
    """
    <h1 style="
        font-size:42px;
        font-weight:800;
        margin-bottom:0px;
    ">
    🧑‍🎓 StudyNova
    </h1>

    <p style="
        color:gray;
        font-size:18px;
        margin-top:-8px;
    ">
    Your Personal AI Study Assistant
    </p>
    """,
    unsafe_allow_html=True
)


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

    # -----------------------------------------
    # BACK TO HOME
    # -----------------------------------------

    if st.button(
        "🏠 Back to Home",
        use_container_width=True,
        key="chatbot_back_home"
    ):

        st.switch_page(
            "app.py"
        )


    st.divider()


    # -----------------------------------------
    # SIDEBAR BRANDING
    # -----------------------------------------

    st.markdown(
        """
        # 🧑‍🎓 StudyNova

        Learn Smarter with AI
        """,
        unsafe_allow_html=True
    )


    st.info(
        """
        ### 🎓 AI Study Assistant

        Ask questions from:

        📚 Academic Notes

        📄 Your Own PDF

        Receive accurate answers with source references.
        """
    )


    st.divider()


    # =================================================
    # KNOWLEDGE SOURCE
    # =================================================

    st.markdown(
        "## 📖 Knowledge Source"
    )


    knowledge_mode = st.radio(
        "Choose Chatbot Mode",
        (
            "📚 Academic Notes",
            "📄 Upload My Own PDF"
        )
    )


    st.divider()


    # =================================================
    # MODE 1 — ACADEMIC NOTES
    # =================================================

    if knowledge_mode == "📚 Academic Notes":

        st.markdown(
            "## 📚 Available Notes"
        )


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

                st.success(
                    f"📄 {pdf}"
                )


            st.caption(
                f"📚 Total PDFs : {len(pdf_files)}"
            )


        else:

            st.warning(
                "No PDF files found."
            )


    # =================================================
    # MODE 2 — UPLOAD PDF
    # =================================================

    else:

        st.markdown(
            "## 📄 Upload PDF"
        )


        uploaded_files = st.file_uploader(
            "📚 Upload One or More PDF Files",
            type=["pdf"],
            accept_multiple_files=True
        )


        if uploaded_files:

            st.success(
                f"✅ {len(uploaded_files)} PDF(s) selected"
            )


            for pdf in uploaded_files:

                st.write(
                    f"📄 {pdf.name}"
                )


            if (
                st.session_state.uploaded_vectorstore
                is None
            ):

                with st.spinner(
                    "📖 Reading PDFs...\n\n"
                    "🧠 Creating Embeddings...\n\n"
                    "📚 Building Knowledge Base..."
                ):

                    st.session_state.uploaded_vectorstore = (
                        create_uploaded_vectorstore(
                            uploaded_files
                        )
                    )


                st.success(
                    "✅ All PDFs processed successfully."
                )


            else:

                st.info(
                    "✅ PDFs already processed."
                )


    st.divider()


    # =================================================
    # SUGGESTED QUESTIONS
    # =================================================

    st.markdown(
        "💡 Suggested Questions"
    )


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


    # =================================================
    # CHAT HISTORY
    # =================================================

    st.subheader(
        "💬 Chat History"
    )


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

            today_chats.append(
                chat
            )


        elif chat_date == yesterday:

            yesterday_chats.append(
                chat
            )


        else:

            older_chats.append(
                chat
            )


    with st.container(key="chatbot_history_list"):

        # -----------------------------------------
        # TODAY
        # -----------------------------------------

        if today_chats:

            st.markdown(
                "#### 📅 Today"
            )


            for chat in reversed(
                today_chats
            ):

                if st.button(
                    f"📝 {chat['title']}",
                    key=chat["id"],
                    use_container_width=True
                ):

                    st.session_state.messages = (
                        chat["messages"]
                    )

                    st.session_state.current_chat_id = (
                        chat["id"]
                    )

                    st.rerun()


        # -----------------------------------------
        # YESTERDAY
        # -----------------------------------------

        if yesterday_chats:

            st.markdown(
                "#### 📅 Yesterday"
            )


            for chat in reversed(
                yesterday_chats
            ):

                if st.button(
                    f"📝 {chat['title']}",
                    key="y" + chat["id"],
                    use_container_width=True
                ):

                    st.session_state.messages = (
                        chat["messages"]
                    )

                    st.session_state.current_chat_id = (
                        chat["id"]
                    )

                    st.rerun()


        # -----------------------------------------
        # OLDER
        # -----------------------------------------

        if older_chats:

            st.markdown(
                "#### 📅 Older"
            )


            for chat in reversed(
                older_chats
            ):

                if st.button(
                    f"📝 {chat['title']}",
                    key="o" + chat["id"],
                    use_container_width=True
                ):

                    st.session_state.messages = (
                        chat["messages"]
                    )

                    st.session_state.current_chat_id = (
                        chat["id"]
                    )

                    st.rerun()


    # -----------------------------------------
    # NEW CHAT
    # -----------------------------------------

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


    # =================================================
    # SAVED NOTES
    # =================================================

    if st.button(
        "📌 Saved Notes",
        use_container_width=True,
        key="chatbot_saved_notes"
    ):

        st.switch_page(
            "pages/FavouriteNotes.py"
        )


    # =================================================
    # CLEAR CHAT
    # =================================================

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True,
        key="chatbot_clear_chat"
    ):

        st.session_state.messages = []

        st.session_state.current_chat_title = (
            "New Chat"
        )

        st.rerun()


    st.divider()


    # =================================================
    # DEVELOPER
    # =================================================

    st.markdown(
        "👩‍💻 Developer"
    )


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

if st.session_state.get(
    "saved_success",
    False
):

    st.toast(
        "✅ Note added to Saved Notes",
        icon="📌"
    )


    st.session_state.saved_success = False


# =====================================================
# CHAT HISTORY / MESSAGES
# =====================================================

for i, message in enumerate(
    st.session_state.messages
):

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


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

                    question = ""


                    if i > 0:

                        previous = (
                            st.session_state.messages[
                                i - 1
                            ]
                        )


                        if previous["role"] == "user":

                            question = (
                                previous["content"]
                            )


                    add_favourite(
                        question=question,
                        answer=message["content"],
                        sources=message.get(
                            "sources",
                            []
                        )
                    )


                    st.session_state.saved_success = (
                        True
                    )


                    st.rerun()


            # ------------------------------------------
            # LISTEN ANSWER
            # ------------------------------------------

            with col2:

                if st.button(
                    "🔊 Listen",
                    key=(
                        f"tts_{i}_"
                        f"{abs(hash(message['content']))}"
                    ),
                    use_container_width=True
                ):

                    audio_file = text_to_speech(
                        message["content"]
                    )


                    with open(
                        audio_file,
                        "rb"
                    ) as f:

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
                    key=(
                        f"download_chat_pdf_{i}_"
                        f"{abs(hash(message['content']))}"
                    ),
                    use_container_width=True
                )


            # ==========================================
            # SOURCE DOCUMENTS
            # ==========================================

            if message.get(
                "sources"
            ):

                with st.expander(
                    "📚 Source Documents Used"
                ):

                    for source in message[
                        "sources"
                    ]:

                        st.write(
                            f"✅ {source}"
                        )


            # ==========================================
            # COPY + REGENERATE + FEEDBACK
            # ==========================================

            copy_col, regenerate_col, feedback_col, empty_col = (
                st.columns(
                    [0.05, 0.07, 0.07, 0.79],
                    gap="small"
                )
            )


            # ------------------------------------------
            # COPY
            # ------------------------------------------

            with copy_col:

                if st.button(
                    "⧉",
                    key=f"copy_{i}",
                    help="Copy answer"
                ):

                    st.toast(
                        "✅ Answer copied!"
                    )


            # ------------------------------------------
            # REGENERATE
            # ------------------------------------------

            with regenerate_col:

                if st.button(
                    "↻",
                    key=f"regenerate_{i}",
                    help="Regenerate answer"
                ):

                    if i > 0:

                        previous_message = (
                            st.session_state.messages[
                                i - 1
                            ]
                        )


                        if (
                            previous_message["role"]
                            == "user"
                        ):

                            st.session_state.regenerate_question = (
                                previous_message[
                                    "content"
                                ]
                            )


                            st.session_state.regenerate_index = (
                                i
                            )


                            st.rerun()


            # ------------------------------------------
            # FEEDBACK
            # ------------------------------------------

            with feedback_col:

                feedback = st.feedback(
                    "thumbs",
                    key=f"feedback_rating_{i}"
                )


                if feedback is not None:

                    if feedback == 1:

                        st.toast(
                            "👍 Thanks! Glad the answer was helpful."
                        )

                    else:

                        st.toast(
                            "👎 Thanks for feedback. We'll improve it."
                        )


# =====================================================
# VOICE INPUT + CHAT INPUT
# =====================================================

if "voice_question" not in st.session_state:

    st.session_state.voice_question = None


if "voice_reset" not in st.session_state:

    st.session_state.voice_reset = 0


# =====================================================
# CHAT INPUT + MICROPHONE
# =====================================================

chat_input_value = st.chat_input(
    "Ask your academic question...",
    key="main_chat_input",
    accept_audio=True
)


# =====================================================
# GET INPUT
# =====================================================

typed_question = None
audio_value = None


if chat_input_value:

    typed_question = (
        chat_input_value.get("text")
    )

    audio_value = (
        chat_input_value.get("audio")
    )


# =====================================================
# PROCESS VOICE INPUT
# =====================================================

voice_question = None


if audio_value:

    with st.spinner(
        "🔄 Converting your voice into text..."
    ):

        try:

            voice_question = speech_to_text(
                audio_value.getvalue()
            )

        except Exception as e:

            voice_question = None

            st.error(
                f"❌ Error converting your voice: {e}"
            )


# =====================================================
# SUCCESSFUL VOICE INPUT
# =====================================================

if voice_question:

    voice_question = (
        voice_question.strip()
    )


    if voice_question:

        st.session_state.voice_question = (
            voice_question
        )


        st.success(
            f"🎤 Recognized: {voice_question}"
        )


# =====================================================
# VOICE RECOGNITION FAILED
# =====================================================

elif audio_value:

    st.error(
        "❌ I could not understand your voice."
    )

    st.warning(
        "🎤 Please record your question again."
    )


# =====================================================
# FINAL QUESTION
# =====================================================

question = typed_question


# -----------------------------------------------------
# CHECK REGENERATION
# -----------------------------------------------------

is_regenerating = (
    st.session_state.get(
        "regenerate_question"
    ) is not None
)


# -----------------------------------------------------
# VOICE QUESTION
# -----------------------------------------------------

if not question:

    question = (
        st.session_state.get(
            "voice_question"
        )
    )


# -----------------------------------------------------
# REGENERATION QUESTION
# -----------------------------------------------------

if not question:

    question = (
        st.session_state.get(
            "regenerate_question"
        )
    )


# -----------------------------------------------------
# CLEAR VOICE QUESTION
# -----------------------------------------------------

if question:

    st.session_state.voice_question = None


# =====================================================
# PROCESS USER QUESTION
# =====================================================

if question:

    # ==========================================
    # SAVE USER MESSAGE
    # ==========================================

    if not is_regenerating:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )


    # ==========================================
    # DISPLAY USER QUESTION
    # ==========================================

    if not is_regenerating:

        with st.chat_message(
            "user"
        ):

            st.markdown(
                question
            )


    # ==========================================
    # GENERATE ASSISTANT ANSWER
    # ==========================================

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "🤖 Searching notes and generating answer..."
        ):

            # --------------------------------------
            # ACADEMIC NOTES
            # --------------------------------------

            if (
                knowledge_mode
                == "📚 Academic Notes"
            ):

                result = ask_question(
                    question
                )

                # ==================================
                # DASHBOARD TRACKING
                # ==================================
                # Record only after the RAG request
                # succeeds.

                record_chat_question(
                    question=question,
                    topic="Academic Notes"
                )


            # --------------------------------------
            # UPLOADED PDF
            # --------------------------------------

            else:

                if (
                    st.session_state.uploaded_vectorstore
                    is None
                ):

                    st.warning(
                        "⚠️ Please upload a PDF first."
                    )

                    st.stop()


                result = ask_uploaded_pdf_question(
                    question,
                    st.session_state.uploaded_vectorstore
                )


            # ======================================
            # EXTRACT ANSWER
            # ======================================

            answer = result["answer"]

            sources = result["sources"]


        # ==========================================
        # DISPLAY ANSWER
        # ==========================================

        st.markdown(
            answer
        )


        # ==========================================
        # SOURCE DOCUMENTS
        # ==========================================

        if sources:

            with st.expander(
                "📚 Source Documents Used"
            ):

                for source in sources:

                    st.write(
                        f"✅ {source}"
                    )


    # =================================================
    # SAVE / REPLACE ASSISTANT MESSAGE
    # =================================================

    if is_regenerating:

        regenerate_index = (
            st.session_state.get(
                "regenerate_index"
            )
        )


        if regenerate_index is not None:

            st.session_state.messages[
                regenerate_index
            ] = {
                "role": "assistant",
                "content": answer,
                "sources": sources
            }


    else:

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources
            }
        )


    # =================================================
    # SAVE CHAT HISTORY
    # =================================================

    if st.session_state.current_chat_id is None:

        title = question[:50]


        add_chat(
            title,
            st.session_state.messages
        )


        st.session_state.chat_history = (
            load_chat_history()
        )


        if st.session_state.chat_history:

            st.session_state.current_chat_id = (
                st.session_state.chat_history[
                    -1
                ]["id"]
            )


    else:

        update_chat(
            st.session_state.current_chat_id,
            st.session_state.messages
        )


        st.session_state.chat_history = (
            load_chat_history()
        )


    # =================================================
    # CLEAR REGENERATION STATE
    # =================================================

    if is_regenerating:

        st.session_state.regenerate_question = None

        st.session_state.regenerate_index = None


# =====================================================
# FOOTER
# =====================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)


st.markdown(
    "---"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.caption(
        "🧑‍🎓 StudyNova"
    )


with col2:

    st.caption(
        "⚡ Powered by Gemini + LangChain + FAISS"
    )


with col3:

    st.caption(
        "👩‍💻 Developed by Payal Pawar"
    )