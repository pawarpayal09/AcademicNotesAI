import os
import streamlit as st
from pathlib import Path

from firebase_manager import (
    require_login,
    is_authenticated,
    get_current_user,
    logout_user
)

from favourites_manager import (
    load_favourites,
    remove_favourite
)


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Saved Notes",
    page_icon="📌",
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

css_file = Path(
    os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ),
        "css",
        "style.css"
    )
)

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
        - 🧠 Learn difficult concepts
        - ⚡ Get instant answers
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

        Academic Notes AI

        Version 1.0
        """
    )


# =====================================================
# MAIN PAGE CONTAINER
# =====================================================

with st.container(
    key="saved_notes_page"
):

    # =================================================
    # LOAD FAVORITES
    # =================================================

    favorites = load_favourites()

    favorites = list(
        reversed(favorites)
    )


    # =================================================
    # EMPTY STATE
    # =================================================

    if not favorites:

        st.title(
            "📌 Saved Notes"
        )

        st.info(
            "⭐ No favorite notes saved yet."
        )

        st.stop()


    # =================================================
    # SESSION STATE
    # =================================================

    if "selected_favorite" not in st.session_state:

        st.session_state.selected_favorite = None


    # =================================================
    # PAGE HEADER
    # =================================================

    header_left, header_right = st.columns(
        [4, 1],
        gap="large"
    )

    with header_left:

        st.title(
            "📌 Saved Notes"
        )

        st.caption(
            "Your personal library of important AI answers."
        )


    # =================================================
    # SUMMARY BAR
    # =================================================

    summary1, summary2, summary3 = st.columns(
        [1, 1, 1],
        gap="medium"
    )

    with summary1:

        st.metric(
            "🗂️ Total Notes",
            len(favorites)
        )

    with summary2:

        latest_date = favorites[0]["date"]

        st.metric(
            "🕒 Latest Save",
            latest_date
        )

    with summary3:

        st.metric(
            "🤖 Generated By",
            "Gemini"
        )


    # =================================================
    # SEARCH
    # =================================================

    st.markdown(
        "### 🔎 Find a saved note"
    )

    search = st.text_input(
        "Search",
        placeholder="Search by question...",
        label_visibility="collapsed"
    )


    # =================================================
    # FILTER
    # =================================================

    filtered = []

    for fav in favorites:

        question = fav.get(
            "question",
            ""
        )

        if not search.strip():

            filtered.append(
                fav
            )

        elif search.lower() in question.lower():

            filtered.append(
                fav
            )


    # =================================================
    # TWO PANEL LAYOUT
    # =================================================

    left_panel, right_panel = st.columns(
        [1.15, 1.85],
        gap="large"
    )


    # =================================================
    # LEFT - SAVED NOTES
    # =================================================

    with left_panel:

        st.markdown(
            "### 📚 Saved Notes"
        )

        st.caption(
            f"{len(filtered)} note(s) available"
        )


        if not filtered:

            st.warning(
                "No matching notes found."
            )


        else:

            for fav in filtered:

                note_col1, note_col2, note_col3 = (
                    st.columns(
                        [5, 2.2, 1.6],
                        gap="small"
                    )
                )


                # -----------------------------------------
                # NOTE TITLE
                # -----------------------------------------

                with note_col1:

                    question = fav.get(
                        "question",
                        ""
                    ).strip()


                    if len(question) > 58:

                        display_question = (
                            question[:58]
                            + "..."
                        )

                    else:

                        display_question = question


                    st.markdown(
                        f"**📘 {display_question}**"
                    )

                    st.caption(
                        "Saved note"
                    )


                # -----------------------------------------
                # DATE
                # -----------------------------------------

                with note_col2:

                    st.caption(
                        f"📅 {fav['date']}"
                    )


                # -----------------------------------------
                # ACTIONS
                # -----------------------------------------

                with note_col3:

                    with st.container(
                        key=f"saved_note_actions_{fav['id']}"
                    ):

                        action_open, action_remove = (
                            st.columns(
                                [1, 1],
                                gap="small"
                            )
                        )


                        with action_open:

                            open_clicked = st.button(
                                "📖",
                                key=f"open_{fav['id']}",
                                help="Open saved note",
                                use_container_width=True
                            )


                        with action_remove:

                            remove_clicked = st.button(
                                "🗑️",
                                key=f"remove_{fav['id']}",
                                help="Remove saved note",
                                use_container_width=True
                            )


                    # -----------------------------------------
                    # OPEN
                    # -----------------------------------------

                    if open_clicked:

                        st.session_state.selected_favorite = (
                            fav
                        )

                        st.rerun()


                    # -----------------------------------------
                    # REMOVE
                    # -----------------------------------------

                    if remove_clicked:

                        remove_favourite(
                            fav["id"]
                        )

                        if (
                            st.session_state.selected_favorite
                            and
                            st.session_state.selected_favorite["id"]
                            == fav["id"]
                        ):

                            st.session_state.selected_favorite = None


                        st.toast(
                            "Note removed",
                            icon="🗑️"
                        )

                        st.rerun()


                st.divider()


    # =================================================
    # RIGHT - SELECTED NOTE
    # =================================================

    with right_panel:

        selected = (
            st.session_state.selected_favorite
        )


        if selected:

            fav = selected


            # -----------------------------------------
            # SELECTED NOTE HEADER
            # -----------------------------------------

            st.markdown(
                "### 🤖 AI Saved Answer"
            )

            st.caption(
                "Your complete saved response."
            )


            # -----------------------------------------
            # QUESTION
            # -----------------------------------------

            st.markdown(
                "#### 📘 Question"
            )

            st.info(
                fav["question"]
            )


            # -----------------------------------------
            # ANSWER
            # -----------------------------------------

            st.markdown(
                "#### 📚 AI Answer"
            )

            with st.container(
                border=True
            ):

                st.markdown(
                    fav["answer"]
                )


            # -----------------------------------------
            # SOURCES
            # -----------------------------------------

            st.markdown(
                "#### 📄 Source Documents"
            )


            sources = fav.get(
                "sources",
                []
            )


            if sources:

                for source in sources:

                    st.caption(
                        f"📄 {source}"
                    )

            else:

                st.caption(
                    "No source documents available."
                )


            # -----------------------------------------
            # NOTE INFORMATION
            # -----------------------------------------

            info_col1, info_col2 = st.columns(
                2,
                gap="small"
            )


            with info_col1:

                st.metric(
                    "📅 Saved On",
                    fav["date"]
                )


            with info_col2:

                st.metric(
                    "🤖 Model",
                    "Gemini"
                )


            # -----------------------------------------
            # REMOVE
            # -----------------------------------------

            if st.button(
                "🗑 Remove From Saved Notes",
                type="primary",
                use_container_width=True,
                key="remove_selected_saved_note"
            ):

                remove_favourite(
                    fav["id"]
                )

                st.session_state.selected_favorite = None

                st.toast(
                    "Note removed successfully",
                    icon="✅"
                )

                st.rerun()


        else:

            # -----------------------------------------
            # NO SELECTION
            # -----------------------------------------

            st.markdown(
                "### 📚 Select a Note"
            )

            st.info(
                """
                Choose a saved note from the left.

                The complete question, AI answer,
                source documents and saved date
                will appear here.
                """
            )


    # =================================================
    # FOOTER
    # =================================================

    st.divider()

    footer1, footer2, footer3 = st.columns(
        3
    )

    with footer1:

        st.caption(
            "📌 Saved Notes"
        )

    with footer2:

        st.caption(
            "⚡ Gemini • LangChain • FAISS"
        )

    with footer3:

        st.caption(
            "👩‍💻 Academic Notes AI"
        )