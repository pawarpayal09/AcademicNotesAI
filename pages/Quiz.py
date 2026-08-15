import streamlit as st
from quiz_generator import generate_quiz
from firebase_manager import require_login

require_login()

from firebase_manager import (
    is_authenticated,
    get_current_user,
    logout_user
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

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Automatic Quiz Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# LOAD SHARED CSS
# ==========================================================

import os

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


# ==========================================================
# SESSION STATE
# ==========================================================

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None


if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False


if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = None


if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = ""


if "quiz_difficulty" not in st.session_state:
    st.session_state.quiz_difficulty = "Medium"


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
    st.success("🧠 Quiz Generator")
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

st.title("🧠 Automatic Quiz Generator")

st.write(
    "Enter any academic topic and generate an "
    "AI-powered multiple-choice quiz."
)

st.divider()


# ==========================================================
# QUIZ SETTINGS
# ==========================================================

st.markdown("### ⚙️ Quiz Settings")


settings_col1, settings_col2, settings_col3 = (
    st.columns(
        [3, 1, 1],
        gap="medium"
    )
)


with settings_col1:

    topic = st.text_input(
        "📚 Topic",
        placeholder=(
            "Example: Machine Learning, DBMS, "
            "Cloud Computing, Python..."
        ),
        value=st.session_state.quiz_topic
    )


with settings_col2:

    number_of_questions = st.selectbox(
        "🔢 Questions",
        [5, 10, 15],
        index=0
    )


with settings_col3:

    difficulty = st.selectbox(
        "🎯 Difficulty",
        [
            "Easy",
            "Medium",
            "Hard"
        ],
        index=[
            "Easy",
            "Medium",
            "Hard"
        ].index(
            st.session_state.quiz_difficulty
        )
    )


# Keep selected settings
st.session_state.quiz_topic = topic
st.session_state.quiz_difficulty = difficulty


# ==========================================================
# QUICK TOPICS
# ==========================================================

st.markdown(
    "#### 💡 Popular Topics"
)


quick1, quick2, quick3, quick4 = st.columns(
    4,
    gap="small"
)


with quick1:

    if st.button(
        "🤖 Machine Learning",
        use_container_width=True
    ):

        st.session_state.quiz_topic = (
            "Machine Learning"
        )

        st.session_state.quiz_data = None
        st.session_state.quiz_submitted = False
        st.session_state.quiz_score = None

        st.rerun()


with quick2:

    if st.button(
        "🗄️ DBMS",
        use_container_width=True
    ):

        st.session_state.quiz_topic = "DBMS"

        st.session_state.quiz_data = None
        st.session_state.quiz_submitted = False
        st.session_state.quiz_score = None

        st.rerun()


with quick3:

    if st.button(
        "☁️ Cloud Computing",
        use_container_width=True
    ):

        st.session_state.quiz_topic = (
            "Cloud Computing"
        )

        st.session_state.quiz_data = None
        st.session_state.quiz_submitted = False
        st.session_state.quiz_score = None

        st.rerun()


with quick4:

    if st.button(
        "🐍 Python",
        use_container_width=True
    ):

        st.session_state.quiz_topic = "Python"

        st.session_state.quiz_data = None
        st.session_state.quiz_submitted = False
        st.session_state.quiz_score = None

        st.rerun()


# ==========================================================
# GENERATE QUIZ
# ==========================================================

st.markdown("")


if st.button(
    "🧠 Generate Quiz",
    type="primary",
    use_container_width=True,
    key="generate_quiz_button"
):

    if not topic.strip():

        st.warning(
            "⚠️ Please enter a topic first."
        )

    else:

        st.session_state.quiz_topic = topic

        st.session_state.quiz_difficulty = difficulty

        with st.spinner(
            f"🧠 Creating {difficulty.lower()} "
            "difficulty quiz..."
        ):

            result = generate_quiz(
                topic=topic,
                number_of_questions=number_of_questions,
                difficulty=difficulty
            )


        if not result["success"]:

            st.error(
                f"❌ {result['error']}"
            )

        else:

            st.session_state.quiz_data = (
                result["quiz"]
            )

            st.session_state.quiz_submitted = False

            st.session_state.quiz_score = None

            # Clear old answers
            for index in range(15):

                key = f"quiz_answer_{index}"

                if key in st.session_state:

                    del st.session_state[key]

            st.rerun()


# ==========================================================
# QUIZ DISPLAY
# ==========================================================

if st.session_state.quiz_data:

    quiz = st.session_state.quiz_data

    questions = quiz.get(
        "questions",
        []
    )


    # ======================================================
    # QUIZ HEADER
    # ======================================================

    st.divider()

    st.subheader(
        f"📝 Quiz: {quiz.get('topic', topic)}"
    )

    st.caption(
        f"{len(questions)} questions • "
        f"Difficulty: "
        f"{st.session_state.quiz_difficulty}"
    )


    # ======================================================
    # SUBMITTED
    # ======================================================

    if st.session_state.quiz_submitted:

        score = st.session_state.quiz_score or 0

        total = len(questions)

        percentage = round(
            (score / total) * 100
        ) if total else 0


        # ==================================================
        # BROAD SCORE DISPLAY
        # ==================================================

        score1, score2, score3 = st.columns(
            3,
            gap="medium"
        )


        with score1:

            st.metric(
                "🏆 Your Score",
                f"{score} / {total}"
            )


        with score2:

            st.metric(
                "📊 Accuracy",
                f"{percentage}%"
            )


        with score3:

            correct_count = score
            wrong_count = total - score

            st.metric(
                "✅ Correct / ❌ Wrong",
                f"{correct_count} / {wrong_count}"
            )


        # --------------------------------------------------
        # Large result message
        # --------------------------------------------------

        if percentage >= 80:

            st.success(
                f"🎉 Excellent performance! "
                f"You scored {score}/{total} ({percentage}%)."
            )

        elif percentage >= 50:

            st.info(
                f"👍 Good attempt! "
                f"You scored {score}/{total} ({percentage}%)."
            )

        else:

            st.warning(
                f"📚 Keep practicing! "
                f"You scored {score}/{total} ({percentage}%)."
            )


        st.progress(
            percentage / 100
        )


        # ==================================================
        # ANSWER REVIEW
        # ==================================================

        st.markdown(
            "### 📖 Answer Review"
        )


        for index, question in enumerate(
            questions
        ):

            user_answer = st.session_state.get(
                f"quiz_answer_{index}"
            )


            with st.container(
                border=True
            ):

                st.markdown(
                    f"**Question {index + 1}**"
                )

                st.write(
                    question["question"]
                )


                if (
                    user_answer
                    == question["correct_answer"]
                ):

                    st.success(
                        f"✅ Your answer: "
                        f"{user_answer}"
                    )

                else:

                    st.error(
                        f"❌ Your answer: "
                        f"{user_answer or 'Not answered'}"
                    )

                    st.success(
                        f"✅ Correct answer: "
                        f"{question['correct_answer']}"
                    )


                st.info(
                    f"💡 {question['explanation']}"
                )


        # ==================================================
        # NEW QUIZ
        # ==================================================

        st.markdown("")


        if st.button(
            "🔄 Generate New Quiz",
            type="primary",
            use_container_width=True,
            key="new_quiz_button"
        ):

            st.session_state.quiz_data = None

            st.session_state.quiz_submitted = False

            st.session_state.quiz_score = None

            for index in range(15):

                key = f"quiz_answer_{index}"

                if key in st.session_state:

                    del st.session_state[key]

            st.rerun()


    # ======================================================
    # ACTIVE QUIZ
    # ======================================================

    else:

        st.markdown(
            "### ✍️ Answer the Questions"
        )


        for index, question in enumerate(
            questions
        ):

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### Question {index + 1}"
                )

                st.write(
                    question["question"]
                )


                st.radio(
                    "Choose your answer:",
                    question["options"],
                    key=f"quiz_answer_{index}",
                    index=None
                )


        st.markdown("")


        # ==================================================
        # SUBMIT
        # ==================================================

        if st.button(
            "✅ Submit Quiz",
            type="primary",
            use_container_width=True,
            key="submit_quiz_button"
        ):

            score = 0


            for index, question in enumerate(
                questions
            ):

                user_answer = st.session_state.get(
                    f"quiz_answer_{index}"
                )


                if (
                    user_answer
                    == question["correct_answer"]
                ):

                    score += 1


            st.session_state.quiz_score = score

            st.session_state.quiz_submitted = True

            st.rerun()


# ==========================================================
# EMPTY STATE
# ==========================================================

else:

    st.info(
        """
        🧠 **Enter a topic to generate your quiz**

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
        "🧠 Automatic Quiz Generator"
    )

with footer2:

    st.caption(
        "⚡ Powered by Gemini"
    )

with footer3:

    st.caption(
        "👩‍💻 Academic Notes AI"
    )