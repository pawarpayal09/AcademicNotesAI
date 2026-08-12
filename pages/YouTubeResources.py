import streamlit as st

from youtube_service import (
    search_youtube_videos
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="YouTube Learning Resources",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# SIDEBAR
# ==========================================================

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
    st.success("🎥 YouTube API")
    st.success("⚡ Streamlit")

    st.divider()

    st.markdown("### 👩‍💻 Developer")

    st.info("""
    **Payal Pawar**

    🎓 MCA Student

    Academic Notes AI

    Version 1.0
    """)


# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("🎥 YouTube Learning Resources")

st.write(
    "Find educational YouTube videos related to your "
    "academic topic."
)

st.divider()


# ==========================================================
# INTRODUCTION
# ==========================================================

info_col1, info_col2, info_col3 = st.columns(3)


with info_col1:

    st.info(
        """
        🔎 **Search**

        Enter any academic topic,
        subject or concept.
        """
    )


with info_col2:

    st.info(
        """
        🎓 **Learn**

        Discover relevant educational
        videos and tutorials.
        """
    )


with info_col3:

    st.info(
        """
        ▶️ **Watch**

        Open the selected video
        directly on YouTube.
        """
    )


st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# SEARCH SECTION
# ==========================================================

st.markdown(
    "### 🔍 Search Learning Videos"
)


search_col1, search_col2 = st.columns(
    [4, 1]
)


with search_col1:

    search_query = st.text_input(
        "Enter your topic",
        placeholder=(
            "Example: Machine Learning, DBMS, "
            "Cloud Computing, Python..."
        ),
        label_visibility="collapsed"
    )


with search_col2:

    search_button = st.button(
        "🔎 Search",
        type="primary",
        use_container_width=True
    )


# ==========================================================
# QUICK SEARCH TOPICS
# ==========================================================

st.markdown(
    "#### 💡 Popular Topics"
)


quick1, quick2, quick3, quick4 = st.columns(4)


def run_topic_search(topic):

    st.session_state.youtube_search_query = topic


with quick1:

    if st.button(
        "🤖 Machine Learning",
        use_container_width=True
    ):

        run_topic_search(
            "Machine Learning tutorial"
        )

        st.rerun()


with quick2:

    if st.button(
        "🗄️ DBMS",
        use_container_width=True
    ):

        run_topic_search(
            "DBMS tutorial"
        )

        st.rerun()


with quick3:

    if st.button(
        "☁️ Cloud Computing",
        use_container_width=True
    ):

        run_topic_search(
            "Cloud Computing tutorial"
        )

        st.rerun()


with quick4:

    if st.button(
        "🐍 Python",
        use_container_width=True
    ):

        run_topic_search(
            "Python programming tutorial"
        )

        st.rerun()


# ==========================================================
# SEARCH QUERY SESSION STATE
# ==========================================================

if "youtube_search_query" not in st.session_state:

    st.session_state.youtube_search_query = ""


# ==========================================================
# DETERMINE QUERY
# ==========================================================

query = st.session_state.youtube_search_query


if search_button:

    if search_query.strip():

        query = search_query.strip()

        st.session_state.youtube_search_query = query

    else:

        st.warning(
            "⚠️ Please enter a topic first."
        )


# ==========================================================
# SEARCH YOUTUBE
# ==========================================================

if query:

    st.divider()

    st.markdown(
        f"### 🎥 Learning Resources for: "
        f"**{query}**"
    )


    with st.spinner(
        "🔎 Searching educational videos..."
    ):

        result = search_youtube_videos(
            query=query,
            max_results=6
        )


    # ======================================================
    # ERROR
    # ======================================================

    if not result["success"]:

        st.error(
            f"❌ {result['error']}"
        )


    # ======================================================
    # NO RESULTS
    # ======================================================

    elif not result["videos"]:

        st.warning(
            "📭 No videos were found for this topic."
        )


    # ======================================================
    # DISPLAY RESULTS
    # ======================================================

    else:

        st.success(
            f"✅ Found {len(result['videos'])} "
            f"learning resources."
        )


        for index, video in enumerate(
            result["videos"],
            start=1
        ):

            # ------------------------------------------------
            # Video card
            # ------------------------------------------------

            card_col1, card_col2 = st.columns(
                [1.35, 2.65],
                gap="large"
            )


            # ------------------------------------------------
            # Thumbnail
            # ------------------------------------------------

            with card_col1:

                if video["thumbnail"]:

                    st.image(
                        video["thumbnail"],
                        use_container_width=True
                    )


            # ------------------------------------------------
            # Details
            # ------------------------------------------------

            with card_col2:

                st.markdown(
                    f"### {index}. "
                    f"{video['title']}"
                )


                st.caption(
                    f"📺 {video['channel']}"
                )


                if video["published_at"]:

                    published_date = (
                        video["published_at"]
                        .split("T")[0]
                    )

                    st.caption(
                        f"📅 Published: "
                        f"{published_date}"
                    )


                if video["description"]:

                    st.write(
                        video["description"]
                    )


                st.link_button(
                    "▶️ Watch on YouTube",
                    video["url"],
                    use_container_width=False
                )


            st.divider()


# ==========================================================
# EMPTY STATE
# ==========================================================

else:

    st.info(
        """
        🎓 **Search for a learning topic**

        Try:

        - Machine Learning
        - DBMS
        - Data Science
        - Cloud Computing
        - Python
        - Artificial Intelligence
        """
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

footer1, footer2, footer3 = st.columns(3)


with footer1:

    st.caption(
        "🎥 YouTube Learning Resources"
    )


with footer2:

    st.caption(
        "⚡ Powered by YouTube Data API v3"
    )


with footer3:

    st.caption(
        "👩‍💻 Academic Notes AI"
    )