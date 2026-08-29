import streamlit as st
from pathlib import Path

from firebase_manager import (
    is_authenticated,
    get_current_user,
    logout_user
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Academic Notes AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOAD CUSTOM CSS
# =====================================================

css_file = Path("css/style.css")

if css_file.exists():

    with open(
        css_file,
        "r",
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

if (
    is_authenticated()
    and st.session_state.get(
        "redirect_to_chatbot",
        False
    )
):

    # Remove the flag BEFORE redirecting.
    #
    # This is important because otherwise returning
    # to app.py later from the sidebar would redirect
    # to Chatbot again.

    st.session_state["redirect_to_chatbot"] = False

    st.switch_page(
        "pages/Chatbot.py"
    )


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
                    👤 {current_user.get('name', 'Student')}
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
                    {current_user.get('email', '')}
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

                # Make sure the redirect flag is removed.

                st.session_state.pop(
                    "redirect_to_chatbot",
                    None
                )

                st.rerun()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        """
        # 🧑‍🎓 StudyNova

        ### Learn Smarter with AI
        """
    )

    st.divider()

    st.info(
        """
### 🤖 About

An AI-powered academic assistant that helps students:

- 📚 Search academic notes
- 📄 Chat with uploaded PDFs
- 🖼️ Understand study images
- 🧠 Generate practice quizzes
- 🎥 Find educational YouTube resources
- 📌 Save important AI answers
- 📊 Track learning activity
- 📈 View personal study progress
"""
    )

    st.divider()

    st.markdown(
        "### 🚀 Technologies"
    )

    st.success(
        "🤖 Google Gemini"
    )

    st.success(
        "🦜 LangChain"
    )

    st.success(
        "📚 FAISS"
    )

    st.success(
        "🧠 RAG"
    )

    st.success(
        "🔥 Firebase"
    )

    st.success(
        "🎥 YouTube API"
    )

    st.success(
        "⚡ Streamlit"
    )

    st.divider()

    st.markdown(
        "### 👩‍💻 Developer"
    )

    st.info(
        """
**Payal Pawar**

🎓 MCA Student

StudyNova

Academic Notes AI

Version 1.0
"""
    )


# =====================================================
# LOGO + TITLE HERO HEADER
# =====================================================

st.markdown(
    """
<h1 style="
text-align:center;
font-size:56px;
font-weight:800;
margin-bottom:0px;
">
🧑‍🎓 StudyNova
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
    unsafe_allow_html=True
)


# =====================================================
# UPDATED PROJECT INTRODUCTION
# =====================================================

st.markdown(
    """
Transform your learning experience with an **AI-powered academic assistant**
built using **Google Gemini, LangChain, FAISS Vector Search,
Retrieval-Augmented Generation (RAG), Firebase, and YouTube Data API.**

Whether you're revising your university notes, chatting with your own
uploaded PDF, studying an image, generating a quiz, or searching for
learning videos, StudyNova provides tools for different stages of learning.

It is designed to help students **understand concepts faster,
practice for examinations, find useful learning resources,
save important answers, and monitor their study activity.**
"""
)


st.markdown(
    "<br>",
    unsafe_allow_html=True
)


# =====================================================
# TECHNOLOGY BADGES
# =====================================================

col1, col2, col3, col4, col5 = st.columns(
    5
)


with col1:

    st.success(
        "🤖 Gemini"
    )


with col2:

    st.success(
        "🦜 LangChain"
    )


with col3:

    st.success(
        "📚 FAISS"
    )


with col4:

    st.success(
        "🧠 RAG"
    )


with col5:

    st.success(
        "⚡ Streamlit"
    )


st.markdown(
    "<br>",
    unsafe_allow_html=True
)


# =====================================================
# CHOOSE HOW YOU WANT TO LEARN
# =====================================================

st.markdown(
    """
## 🚀 Choose How You Want to Learn
"""
)

st.markdown(
    "<br>",
    unsafe_allow_html=True
)


# =====================================================
# TWO EXISTING FEATURE CARDS
# =====================================================

col1, col2 = st.columns(
    2
)


# =====================================================
# CARD 1 - ACADEMIC NOTES
# =====================================================

with col1:

    with st.container(
        key="academic_notes_card"
    ):

        st.info(
            """
### 📚 Academic Notes

Search the academic notes that are already included in this project.

#### ✨ Features

- ✅ Multiple Subject PDFs
- ✅ Fast Semantic Search
- ✅ Gemini AI Answers
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Personalized Learning Activity

Perfect for revising your syllabus quickly and preparing for examinations.
"""
        )


# =====================================================
# CARD 2 - UPLOAD PDF
# =====================================================

with col2:

    with st.container(
        key="upload_pdf_card"
    ):

        st.info(
            """
### 📄 Upload Your Own PDF

Upload any PDF and start chatting with your own document.

#### ✨ Features

- ✅ Upload Your Own PDF
- ✅ Automatic Embedding Generation
- ✅ Gemini Powered Answers
- ✅ Works with Notes, Books & Research Papers
- ✅ Student-Friendly Explanations

Perfect for studying your own notes, books, assignments, and research papers.
"""
        )


# =====================================================
# ADDITIONAL FEATURES
# =====================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

st.markdown(
    """
## 🌟 More Study Features
"""
)

st.write(
    "StudyNova also includes additional tools that support "
    "practice, visual learning, external resources and progress tracking."
)


st.markdown(
    "<br>",
    unsafe_allow_html=True
)


# =====================================================
# FEATURE TEXT CARDS
# =====================================================

feature_col1, feature_col2, feature_col3 = st.columns(
    3
)


# -----------------------------------------------------
# QUIZ
# -----------------------------------------------------

with feature_col1:

    st.info(
        """
### 🧠 Automatic Quiz Generator

Create AI-powered multiple-choice quizzes
from any academic topic.

**Includes:**

- ✅ Easy, Medium and Hard difficulty
- ✅ 5, 10 or 15 questions
- ✅ Automatic answer checking
- ✅ Score and percentage
- ✅ Answer explanations
- ✅ Quiz result tracking

Useful for self-practice and examination preparation.
"""
    )


# -----------------------------------------------------
# YOUTUBE
# -----------------------------------------------------

with feature_col2:

    st.info(
        """
### 🎥 YouTube Learning Resources

Search real educational YouTube videos
for an academic topic.

**Provides:**

- ✅ Video title
- ✅ Channel name
- ✅ Publication date
- ✅ Thumbnail
- ✅ Description
- ✅ Direct YouTube link

Useful for finding additional learning material
and boosting performance.
"""
    )


# -----------------------------------------------------
# IMAGE STUDY
# -----------------------------------------------------

with feature_col3:

    st.info(
        """
### 🖼️ Image Study Assistant

Upload academic images and allow AI
to explain the visible content.

**Supports:**

- ✅ Textbook pages
- ✅ Handwritten notes
- ✅ Diagrams
- ✅ Questions
- ✅ Charts
- ✅ Screenshots

The user can ask AI to explain, summarize,
solve or extract important points.
"""
    )


st.markdown(
    "<br>",
    unsafe_allow_html=True
)


# =====================================================
# SECOND FEATURE ROW
# =====================================================

feature_col4, feature_col5, feature_col6 = st.columns(
    3
)


# -----------------------------------------------------
# SAVED NOTES
# -----------------------------------------------------

with feature_col4:

    st.info(
        """
### 📌 Saved Notes

Save useful AI answers for later study.

**Includes:**

- ✅ Save important answers
- ✅ Search saved notes
- ✅ Open complete answers
- ✅ View source documents
- ✅ Remove saved notes

Creates a personal library of useful study content.
"""
    )


# -----------------------------------------------------
# DASHBOARD
# -----------------------------------------------------

with feature_col5:

    st.info(
        """
### 📊 Study Dashboard

View your personal learning progress
in one place.

**Shows information such as:**

- ✅ Quiz activity
- ✅ Image-study activity
- ✅ YouTube activity
- ✅ Saved notes
- ✅ Study progress
- ✅ Recent activities

Useful for understanding your learning pattern.
"""
    )


# -----------------------------------------------------
# DATASET
# -----------------------------------------------------

with feature_col6:

    st.info(
        """
### 📋 Dataset & Analysis

View the activity data generated while
using StudyNova.

**Includes:**

- ✅ User activity records
- ✅ Chat records
- ✅ Combined dataset
- ✅ Excel dataset download

Useful for data science and analysis work.
"""
    )


st.markdown(
    "<br>",
    unsafe_allow_html=True
)


# =====================================================
# FIREBASE / USER ACCOUNT INFORMATION
# =====================================================

st.markdown(
    """
## 🔐 Personalized Study Workspace
"""
)

st.write(
    "StudyNova uses Firebase Authentication to provide "
    "secure user signup and login. After login, user activity "
    "can be connected to the correct account so that the "
    "Dashboard, Saved Notes and Dataset features show "
    "personalized information."
)


st.markdown(
    "<br>",
    unsafe_allow_html=True
)


# =====================================================
# START CHAT BUTTON
# =====================================================

col1, col2, col3 = st.columns(
    [1, 2, 1]
)


with col2:

    if st.button(
        "🚀 Start Chatting",
        use_container_width=True,
        type="primary"
    ):

        if is_authenticated():

            st.switch_page(
                "pages/Chatbot.py"
            )

        else:

            st.switch_page(
                "pages/Login.py"
            )