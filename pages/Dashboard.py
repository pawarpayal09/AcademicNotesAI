import os
import requests
import streamlit as st
from datetime import datetime, timezone

from firebase_manager import (
    require_login,
    is_authenticated,
    get_current_user,
    get_user_profile,
    logout_user
)

from progress_manager import (
    get_dashboard_stats,
    get_quiz_results,
    get_recent_activity,
    get_top_topics,
    get_difficulty_performance,
    get_study_streak,
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
    page_title="Study Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# LOAD CSS
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


load_css()


# ==========================================================
# LOGIN REQUIRED
# ==========================================================

require_login()


# ==========================================================
# USER
# ==========================================================

user = get_current_user()

profile = get_user_profile() or {}


user_name = (
    profile.get(
        "name"
    )
    or
    user.get(
        "name",
        "Student"
    )
)

user_email = (
    profile.get(
        "email"
    )
    or
    user.get(
        "email",
        ""
    )
)


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

# ==========================================================
# HEADER
# ==========================================================

header1, header2 = st.columns(
    [4.5, 1.5],
    gap="medium"
)

with header1:

    st.title(
        "📊 My Study Dashboard"
    )

    st.caption(
        f"Welcome back, {user_name}. "
        "Track your learning activity and progress."
    )

# ==========================================================
# LOAD DATA
# ==========================================================

stats = get_dashboard_stats()

quiz_results = get_quiz_results()

recent_activity = get_recent_activity()

top_topics = get_top_topics()

difficulty_performance = (
    get_difficulty_performance()
)

streak = get_study_streak()


# ==========================================================
# CALCULATE AVERAGE SCORE
# ==========================================================

total_quizzes = int(
    stats.get(
        "total_quizzes",
        0
    )
)

quiz_score_sum = float(
    stats.get(
        "quiz_score_sum",
        0
    )
)

average_score = 0

if total_quizzes > 0:

    average_score = round(
        quiz_score_sum /
        total_quizzes
    )


# ==========================================================
# SUMMARY CARDS
# ==========================================================

st.divider()

card1, card2, card3 = st.columns(
    3,
    gap="medium"
)

with card1:

    st.metric(
        "💬 Questions Asked",
        int(
            stats.get(
                "total_questions",
                0
            )
        )
    )

with card2:

    st.metric(
        "🧠 Quizzes Completed",
        total_quizzes
    )

with card3:

    st.metric(
        "🎯 Average Quiz Score",
        f"{average_score}%"
    )


card4, card5, card6 = st.columns(
    3,
    gap="medium"
)

with card4:

    st.metric(
        "🖼️ Images Analyzed",
        int(
            stats.get(
                "total_images",
                0
            )
        )
    )

with card5:

    st.metric(
        "📌 Saved Notes",
        int(
            stats.get(
                "total_saved_notes",
                0
            )
        )
    )

with card6:

    st.metric(
        "🎥 YouTube Searches",
        int(
            stats.get(
                "total_youtube_searches",
                0
            )
        )
    )


# ==========================================================
# QUIZ PERFORMANCE
# ==========================================================

st.divider()

left_chart, right_chart = st.columns(
    [1.6, 1],
    gap="large"
)


with left_chart:

    st.subheader(
        "📈 Quiz Performance"
    )

    if quiz_results:

        chart_data = {
            "Quiz": [],
            "Score": [],
        }

        for index, quiz in enumerate(
            reversed(
                quiz_results[-10:]
            ),
            start=1
        ):

            chart_data["Quiz"].append(
                f"Quiz {index}"
            )

            chart_data["Score"].append(
                quiz.get(
                    "percentage",
                    0
                )
            )


        st.line_chart(
            chart_data,
            x="Quiz",
            y="Score",
            height=300
        )

    else:

        st.info(
            "Complete a quiz to see your performance chart."
        )


with right_chart:

    st.subheader(
        "🎯 Performance by Difficulty"
    )

    difficulty_chart = {
        "Easy": difficulty_performance.get(
            "Easy",
            0
        ),

        "Medium": difficulty_performance.get(
            "Medium",
            0
        ),

        "Hard": difficulty_performance.get(
            "Hard",
            0
        ),
    }


    st.bar_chart(
        difficulty_chart,
        height=300
    )


# ==========================================================
# TOPICS + STREAK
# ==========================================================

st.divider()

topics_col, streak_col = st.columns(
    [1.5, 1],
    gap="large"
)


with topics_col:

    st.subheader(
        "📚 Most Studied Topics"
    )

    if top_topics:

        max_count = max(
            count
            for _, count in top_topics
        )

        for topic, count in top_topics:

            st.markdown(
                f"**{topic}**  •  {count} activities"
            )

            st.progress(
                count / max_count
            )

    else:

        st.info(
            "Your frequently studied topics will appear here."
        )


with streak_col:

    st.subheader(
        "🔥 Study Streak"
    )

    current_streak = streak.get(
        "current_streak",
        0
    )

    best_streak = streak.get(
        "best_streak",
        0
    )


    st.metric(
        "Current Streak",
        f"{current_streak} day(s)"
    )

    st.metric(
        "Best Streak",
        f"{best_streak} day(s)"
    )


    if current_streak > 0:

        st.success(
            "🔥 Keep learning every day!"
        )

    else:

        st.info(
            "Start studying today to begin your streak."
        )


# ==========================================================
# RECENT ACTIVITY
# ==========================================================

st.divider()

st.subheader(
    "🕒 Recent Activity"
)


def get_activity_icon(activity_type):

    icons = {

        "chat": "💬",

        "quiz": "🧠",

        "image": "🖼️",

        "youtube": "🎥",

        "saved_note": "📌",
    }

    return icons.get(
        activity_type,
        "📚"
    )


if recent_activity:

    for activity in recent_activity[:10]:

        icon = get_activity_icon(
            activity.get(
                "type",
                ""
            )
        )

        topic = activity.get(
            "topic",
            "General"
        )

        description = activity.get(
            "description",
            ""
        )


        created_at = activity.get(
            "created_at"
        )


        if created_at:

            try:

                if created_at.tzinfo is None:

                    created_at = created_at.replace(
                        tzinfo=timezone.utc
                    )

                date_text = (
                    created_at.astimezone()
                    .strftime(
                        "%d %b %Y • %I:%M %p"
                    )
                )

            except Exception:

                date_text = str(
                    created_at
                )

        else:

            date_text = "Recent"


        with st.container(
            border=True
        ):

            activity_col1, activity_col2 = (
                st.columns(
                    [0.4, 5],
                    gap="small"
                )
            )


            with activity_col1:

                st.markdown(
                    f"### {icon}"
                )


            with activity_col2:

                st.markdown(
                    f"**{topic}**"
                )

                if description:

                    short_description = (
                        description
                    )

                    if len(
                        short_description
                    ) > 100:

                        short_description = (
                            short_description[:100]
                            + "..."
                        )

                    st.caption(
                        short_description
                    )

                st.caption(
                    f"🕒 {date_text}"
                )

else:

    st.info(
        "Your recent learning activity will appear here."
    )


# ==========================================================
# QUICK ACTIONS
# ==========================================================

st.divider()

st.subheader(
    "🚀 Quick Actions"
)


quick1, quick2, quick3, quick4, quick5 = (
    st.columns(
        5,
        gap="small"
    )
)


with quick1:

    if st.button(
        "💬 Chatbot",
        use_container_width=True
    ):

        st.switch_page(
            "pages/Chatbot.py"
        )


with quick2:

    if st.button(
        "🖼️ Image Study",
        use_container_width=True
    ):

        st.switch_page(
            "pages/ImageStudy.py"
        )


with quick3:

    if st.button(
        "🧠 Quiz",
        use_container_width=True
    ):

        st.switch_page(
            "pages/Quiz.py"
        )


with quick4:

    if st.button(
        "🎥 YouTube",
        use_container_width=True
    ):

        st.switch_page(
            "pages/YouTubeResources.py"
        )


with quick5:

    if st.button(
        "📌 Saved Notes",
        use_container_width=True
    ):

        st.switch_page(
            "pages/FavouriteNotes.py"
        )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

footer1, footer2, footer3 = st.columns(3)

with footer1:

    st.caption(
        "📊 My Study Dashboard"
    )

with footer2:

    st.caption(
        "⚡ Firebase • Gemini • Streamlit"
    )

with footer3:

    st.caption(
        "👩‍💻 Academic Notes AI"
    )

# ==========================================================
# PERSONALIZED STUDY INSIGHTS
# ==========================================================

st.divider()

st.markdown(
    "### 🎯 Personalized Study Insights"
)

try:

    response = requests.get(
        f"http://localhost:8000/insights/{current_user['uid']}",
        timeout=5
    )

    if response.status_code == 200:

        insights = response.json()

        # --------------------------------------------------
        # Main recommendation
        # --------------------------------------------------

        st.info(
            f"💡 {insights.get('focus_message', 'Keep studying regularly.')}"
        )

        # --------------------------------------------------
        # Insight cards
        # --------------------------------------------------

        insight1, insight2, insight3, insight4 = st.columns(
            4,
            gap="medium"
        )

        with insight1:

            st.metric(
                "🧠 Quiz Attempts",
                insights.get(
                    "total_quizzes",
                    0
                )
            )

        with insight2:

            st.metric(
                "🎯 Average Score",
                f"{insights.get('average_quiz_score', 0)}%"
            )

        with insight3:

            strongest_topic = (
                insights.get(
                    "strongest_topic"
                )
                or
                "Not Available"
            )

            st.metric(
                "🏆 Strongest Topic",
                strongest_topic
            )

        with insight4:

            weakest_topic = (
                insights.get(
                    "weakest_topic"
                )
                or
                "Not Available"
            )

            st.metric(
                "📚 Focus Topic",
                weakest_topic
            )

        # --------------------------------------------------
        # Detailed insight
        # --------------------------------------------------

        st.markdown(
            "#### 📖 Your Learning Insight"
        )

        insight_col1, insight_col2 = st.columns(
            2,
            gap="large"
        )

        with insight_col1:

            strongest_score = insights.get(
                "strongest_topic_score",
                0
            )

            st.success(
                f"🏆 Strongest Topic: "
                f"{strongest_topic} "
                f"({strongest_score}%)"
            )

        with insight_col2:

            weakest_score = insights.get(
                "weakest_topic_score",
                0
            )

            st.warning(
                f"📚 Needs More Practice: "
                f"{weakest_topic} "
                f"({weakest_score}%)"
            )

    else:

        st.caption(
            "No personalized insights available yet."
        )

except requests.exceptions.RequestException:

    st.caption(
        "Recommendation service is currently unavailable."
    )

# ==========================================================
# PERSONALIZED STUDY PLAN
# ==========================================================

st.divider()

st.markdown(
    "### 📅 Personalized Study Plan"
)

st.caption(
    "This plan is generated by your StudyNova custom API "
    "using your quiz and learning activity."
)

try:

    study_plan_response = requests.get(
        f"http://localhost:8000/study-plan/{current_user['uid']}",
        timeout=5
    )

    if study_plan_response.status_code == 200:

        study_plan_data = (
            study_plan_response.json()
        )

        current_streak = study_plan_data.get(
            "current_streak_days",
            0
        )

        best_streak = study_plan_data.get(
            "best_streak_days",
            0
        )

        # --------------------------------------------------
        # STREAK SUMMARY
        # --------------------------------------------------

        streak_col1, streak_col2 = st.columns(
            2,
            gap="medium"
        )

        with streak_col1:

            st.metric(
                "🔥 Current Streak",
                f"{current_streak} day(s)"
            )

        with streak_col2:

            st.metric(
                "🏆 Best Streak",
                f"{best_streak} day(s)"
            )

        # --------------------------------------------------
        # STUDY PLAN
        # --------------------------------------------------

        plan = study_plan_data.get(
            "study_plan",
            []
        )

        if plan:

            for index, item in enumerate(
                plan,
                start=1
            ):

                priority = item.get(
                    "priority",
                    "Medium"
                )

                action = item.get(
                    "action",
                    "Study"
                )

                topic = item.get(
                    "topic",
                    "General"
                )

                reason = item.get(
                    "reason",
                    ""
                )

                # ------------------------------------------
                # HIGH PRIORITY
                # ------------------------------------------

                if priority == "High":

                    with st.container(
                        border=True
                    ):

                        st.error(
                            f"🔴 Priority {priority}"
                        )

                        st.markdown(
                            f"**{index}. {action}**"
                        )

                        st.write(
                            f"📚 Topic: **{topic}**"
                        )

                        if reason:

                            st.caption(
                                f"Why: {reason}"
                            )

                # ------------------------------------------
                # MEDIUM PRIORITY
                # ------------------------------------------

                elif priority == "Medium":

                    with st.container(
                        border=True
                    ):

                        st.warning(
                            f"🟡 Priority {priority}"
                        )

                        st.markdown(
                            f"**{index}. {action}**"
                        )

                        st.write(
                            f"📚 Topic: **{topic}**"
                        )

                        if reason:

                            st.caption(
                                f"Why: {reason}"
                            )

                # ------------------------------------------
                # LOW PRIORITY
                # ------------------------------------------

                else:

                    with st.container(
                        border=True
                    ):

                        st.success(
                            f"🟢 Priority {priority}"
                        )

                        st.markdown(
                            f"**{index}. {action}**"
                        )

                        st.write(
                            f"📚 Topic: **{topic}**"
                        )

                        if reason:

                            st.caption(
                                f"Why: {reason}"
                            )

        else:

            st.info(
                "No personalized study plan is available yet."
            )

    else:

        st.info(
            "Complete some learning activities to generate "
            "your personalized study plan."
        )


except requests.exceptions.RequestException:

    st.warning(
        "⚠️ Personalized Study Plan service is currently unavailable."
    )