import streamlit as st

from quiz_generator import generate_quiz


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
    st.columns([3, 1, 1])
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
        index=1
    )


# ==========================================================
# QUICK TOPICS
# ==========================================================

st.markdown("#### 💡 Popular Topics")


quick1, quick2, quick3, quick4 = (
    st.columns(4)
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

        st.rerun()


with quick2:

    if st.button(
        "🗄️ DBMS",
        use_container_width=True
    ):

        st.session_state.quiz_topic = "DBMS"

        st.session_state.quiz_data = None
        st.session_state.quiz_submitted = False

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

        st.rerun()


with quick4:

    if st.button(
        "🐍 Python",
        use_container_width=True
    ):

        st.session_state.quiz_topic = "Python"

        st.session_state.quiz_data = None
        st.session_state.quiz_submitted = False

        st.rerun()


# ==========================================================
# GENERATE QUIZ BUTTON
# ==========================================================

if st.button(
    "🧠 Generate Quiz",
    type="primary",
    use_container_width=True
):

    if not topic.strip():

        st.warning(
            "⚠️ Please enter a topic first."
        )

    else:

        with st.spinner(
            "🧠 Creating your quiz..."
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

            st.session_state.quiz_topic = topic

            st.session_state.quiz_submitted = False

            st.session_state.quiz_score = None

            st.rerun()


# ==========================================================
# QUIZ DISPLAY
# ==========================================================

if st.session_state.quiz_data:

    quiz = st.session_state.quiz_data

    questions = quiz["questions"]


    # ======================================================
    # QUIZ HEADER
    # ======================================================

    st.divider()

    st.markdown(
        f"### 📝 Quiz: {quiz['topic']}"
    )

    st.caption(
        f"{len(questions)} questions • "
        f"Difficulty: {difficulty}"
    )


    # ======================================================
    # ALREADY SUBMITTED
    # ======================================================

    if st.session_state.quiz_submitted:

        score = st.session_state.quiz_score

        percentage = round(
            (score / len(questions)) * 100
        )


        if percentage >= 80:

            st.success(
                f"🎉 Excellent! Your score is "
                f"**{score}/{len(questions)} "
                f"({percentage}%)**"
            )

        elif percentage >= 50:

            st.info(
                f"👍 Good attempt! Your score is "
                f"**{score}/{len(questions)} "
                f"({percentage}%)**"
            )

        else:

            st.warning(
                f"📚 Keep practicing! Your score is "
                f"**{score}/{len(questions)} "
                f"({percentage}%)**"
            )


        st.progress(
            percentage / 100
        )


        # ==================================================
        # REVIEW ANSWERS
        # ==================================================

        st.markdown("### 📖 Answer Review")


        for index, question in enumerate(
            questions
        ):

            user_answer = st.session_state.get(
                f"quiz_answer_{index}",
                ""
            )


            st.markdown(
                f"**Question {index + 1}: "
                f"{question['question']}**"
            )


            if user_answer == question["correct_answer"]:

                st.success(
                    f"✅ Your answer: {user_answer}"
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

            st.divider()


        # ==================================================
        # NEW QUIZ
        # ==================================================

        if st.button(
            "🔄 Generate New Quiz",
            type="primary",
            use_container_width=True
        ):

            st.session_state.quiz_data = None

            st.session_state.quiz_submitted = False

            st.session_state.quiz_score = None

            for index in range(
                len(questions)
            ):

                key = f"quiz_answer_{index}"

                if key in st.session_state:

                    del st.session_state[key]

            st.rerun()


    # ======================================================
    # ACTIVE QUIZ
    # ======================================================

    else:

        st.markdown(
            "### ✍️ Answer the questions"
        )


        # --------------------------------------------------
        # Display questions
        # --------------------------------------------------

        for index, question in enumerate(
            questions
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


            st.markdown("---")


        # ==================================================
        # SUBMIT QUIZ
        # ==================================================

        if st.button(
            "✅ Submit Quiz",
            type="primary",
            use_container_width=True
        ):

            score = 0


            # ------------------------------------------------
            # Calculate score
            # ------------------------------------------------

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