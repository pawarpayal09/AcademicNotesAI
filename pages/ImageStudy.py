import os
import streamlit as st
import streamlit.components.v1 as components

from image_processor import analyze_study_image
from progress_manager import record_image_study

from firebase_manager import (
    require_login,
    is_authenticated,
    get_current_user,
    logout_user
)

from progress_manager import (
    record_image_study
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Image Study Assistant",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# LOGIN REQUIRED
# ==========================================================

require_login()


# ==========================================================
# LOAD SHARED CSS
# ==========================================================

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


# ==========================================================
# IMAGE STUDY SESSION STATE
# ==========================================================

if "image_answer" not in st.session_state:

    st.session_state.image_answer = None


if "image_instruction" not in st.session_state:

    st.session_state.image_instruction = None


# ==========================================================
# LOGGED-IN USER PROFILE
# TOP-RIGHT PROFESSIONAL PROFILE BAR
# ==========================================================

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


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        """
        # 📚 Academic Notes AI

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


# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "🖼️ Image Study Assistant"
)

st.write(
    "Upload your study material and let AI explain it "
    "in simple, student-friendly language."
)

st.divider()


# ==========================================================
# FEATURE INTRO
# ==========================================================

info_col1, info_col2, info_col3 = st.columns(
    3
)


with info_col1:

    st.info(
        """
        📷 **Upload**

        Upload notes, textbook pages,
        diagrams, questions or screenshots.
        """
    )


with info_col2:

    st.info(
        """
        🧠 **Analyze**

        Gemini understands the visible
        academic content in your image.
        """
    )


with info_col3:

    st.info(
        """
        📚 **Learn**

        Get a clear and concise explanation
        designed for students.
        """
    )


st.markdown(
    "<br>",
    unsafe_allow_html=True
)


# ==========================================================
# IMAGE UPLOAD
# ==========================================================

st.markdown(
    "### 📤 Upload Study Material"
)


uploaded_image = st.file_uploader(
    "Choose an image from your device",
    type=[
        "png",
        "jpg",
        "jpeg",
        "webp"
    ],
    accept_multiple_files=False,
    help=(
        "Upload textbook pages, handwritten notes, "
        "diagrams, questions, charts, or academic screenshots."
    )
)


# ==========================================================
# IMAGE SELECTED
# ==========================================================

if uploaded_image:

    # ======================================================
    # IMAGE DATA
    # ======================================================

    image_bytes = uploaded_image.getvalue()

    file_size_kb = len(image_bytes) / 1024

    mime_type = uploaded_image.type


    # ======================================================
    # IMAGE PREVIEW
    # ======================================================

    st.markdown(
        "### 🖼️ Image Preview"
    )


    preview_col1, preview_col2, preview_col3 = st.columns(
        [1, 2, 1]
    )


    with preview_col2:

        st.image(
            uploaded_image,
            caption=uploaded_image.name,
            width=500
        )


    # ======================================================
    # FILE INFORMATION
    # ======================================================

    detail_col1, detail_col2, detail_col3 = st.columns(
        3
    )


    with detail_col1:

        st.metric(
            "📄 File",
            uploaded_image.name
        )


    with detail_col2:

        st.metric(
            "📦 Size",
            f"{file_size_kb:.1f} KB"
        )


    with detail_col3:

        st.metric(
            "🖼️ Type",
            mime_type
        )


    st.divider()


    # ======================================================
    # USER INSTRUCTION
    # ======================================================

    st.markdown(
        "### 📝 What do you want to know from this image?"
    )


    instruction = st.text_area(
        "Enter your request",
        placeholder=(
            "Example:\n"
            "Explain this topic in simple language.\n"
            "Summarize these notes.\n"
            "Solve this question step-by-step.\n"
            "Explain this diagram.\n"
            "Extract the important points."
        ),
        height=120,
        key="image_instruction_box"
    )


    # ======================================================
    # QUICK PROMPTS
    # ======================================================

    with st.expander(
        "💡 Quick Prompts"
    ):

        quick_col1, quick_col2 = st.columns(
            2
        )


        with quick_col1:

            if st.button(
                "✨ Explain Simply",
                use_container_width=True,
                key="quick_explain"
            ):

                st.session_state.image_instruction = (
                    "Explain this topic in simple "
                    "student-friendly language."
                )

                st.rerun()


        with quick_col2:

            if st.button(
                "📝 Summarize",
                use_container_width=True,
                key="quick_summary"
            ):

                st.session_state.image_instruction = (
                    "Summarize the important points "
                    "from this image."
                )

                st.rerun()


        quick_col3, quick_col4 = st.columns(
            2
        )


        with quick_col3:

            if st.button(
                "🎯 Key Points",
                use_container_width=True,
                key="quick_points"
            ):

                st.session_state.image_instruction = (
                    "Extract the most important key "
                    "points from this image."
                )

                st.rerun()


        with quick_col4:

            if st.button(
                "🔍 Explain Diagram",
                use_container_width=True,
                key="quick_diagram"
            ):

                st.session_state.image_instruction = (
                    "Explain the diagram in this image "
                    "clearly and simply."
                )

                st.rerun()


    # ======================================================
    # CURRENT INSTRUCTION
    # ======================================================

    current_instruction = (
        st.session_state.image_instruction
        if st.session_state.image_instruction
        else instruction
    )


    # ======================================================
    # ANALYZE IMAGE
    # ======================================================

    if st.button(
        "🧠 Analyze Image",
        type="primary",
        use_container_width=True,
        key="analyze_image_button"
    ):

        if not current_instruction.strip():

            current_instruction = (
                "Explain the important academic content "
                "visible in this image in simple language."
            )


        # --------------------------------------------------
        # VALIDATE IMAGE
        # --------------------------------------------------

        if not image_bytes:

            st.error(
                "❌ The uploaded image could not be read."
            )


        else:

            # ------------------------------------------------
            # GEMINI ANALYSIS
            # ------------------------------------------------

            with st.spinner(
                "🧠 Reading the image and generating an answer..."
            ):

                answer = analyze_study_image(
                    image_bytes=image_bytes,
                    mime_type=mime_type,
                    instruction=current_instruction
                )
                st.session_state.image_answer = answer

                st.session_state.image_instruction = (
                    current_instruction
                )

                record_image_study(
                    instruction=current_instruction,
                    image_name=uploaded_image.name
                )

                # --------------------------------------------
                # SAVE ANSWER
                # --------------------------------------------

                st.session_state.image_answer = answer

                st.session_state.image_instruction = (
                    current_instruction
                )


                # --------------------------------------------
                # DASHBOARD TRACKING
                # --------------------------------------------
                # Record ONE image-study activity only when
                # the Analyze Image button is used.
                #
                # Regenerate does not create another image
                # activity because it is the same uploaded image.

                if answer and not str(answer).startswith("⚠️"):

                    record_image_study(
                        instruction=current_instruction,
                        image_name=uploaded_image.name
                    )


    # ======================================================
    # DISPLAY AI ANSWER
    # ======================================================

    if st.session_state.image_answer:

        st.divider()


        st.markdown(
            "### 📚 AI Explanation"
        )


        st.success(
            "✅ Image analyzed successfully."
        )


        st.markdown(
            st.session_state.image_answer
        )


        # ==================================================
        # COPY + REGENERATE + FEEDBACK
        # ==================================================

        copy_col, regenerate_col, feedback_col, empty_col = (
            st.columns(
                [0.05, 0.07, 0.14, 0.74],
                gap="small"
            )
        )


        # ==================================================
        # COPY
        # ==================================================

        with copy_col:

            if st.button(
                "⧉",
                key="copy_image_answer",
                help="Copy answer"
            ):

                st.toast(
                    "✅ Answer copied!"
                )


        # ==================================================
        # REGENERATE
        # ==================================================

        with regenerate_col:

            if st.button(
                "↻",
                key="regenerate_image_answer",
                help="Regenerate answer"
            ):

                if uploaded_image:

                    regenerate_instruction = (
                        st.session_state.get(
                            "image_instruction"
                        )
                    )


                    if not regenerate_instruction:

                        regenerate_instruction = (
                            "Explain the important academic "
                            "content visible in this image "
                            "in simple language."
                        )


                    with st.spinner(
                        "🔄 Regenerating answer..."
                    ):

                        st.session_state.image_answer = (
                            analyze_study_image(
                                image_bytes=uploaded_image.getvalue(),
                                mime_type=uploaded_image.type,
                                instruction=regenerate_instruction
                            )
                        )


                    st.rerun()


        # ==================================================
        # FEEDBACK
        # ==================================================

        with feedback_col:

            feedback = st.feedback(
                "thumbs",
                key="feedback_rating_image"
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


# ==========================================================
# EMPTY STATE
# ==========================================================

else:

    st.info(
        """
        🖼️ **Upload an image to begin**

        You can upload:

        📚 Notes  
        📖 Textbook pages  
        ✍️ Handwritten questions  
        📊 Charts and diagrams  
        💻 Academic screenshots
        """
    )


    st.markdown(
        "### 🚀 Example Uses"
    )


    example_col1, example_col2 = st.columns(
        2
    )


    with example_col1:

        st.markdown(
            """
            **📚 Academic Notes**

            Upload a page of notes and ask:

            *"Explain this topic in simple language."*
            """
        )


    with example_col2:

        st.markdown(
            """
            **❓ Exam Questions**

            Upload a question and ask:

            *"Solve this question step-by-step."*
            """
        )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()


footer_col1, footer_col2, footer_col3 = st.columns(
    3
)


with footer_col1:

    st.caption(
        "🖼️ Image Study Assistant"
    )


with footer_col2:

    st.caption(
        "⚡ Powered by Gemini"
    )


with footer_col3:

    st.caption(
        "👩‍💻 Academic Notes AI"
    )