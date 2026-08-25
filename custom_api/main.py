"""
StudyNova — Personalized Study Recommendation API
--------------------------------------------------

This is a separate FastAPI service.

IMPORTANT:
- It does NOT import any Streamlit page.
- It does NOT modify existing project logic.
- It only reads existing JSON files from storage/.
- It returns personalized study information as JSON.

Run:

    cd custom_api
    python -m uvicorn main:app --reload --port 8000

Swagger documentation:

    http://localhost:8000/docs
"""

import json
import os

from collections import defaultdict, Counter
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


# ==========================================================
# FASTAPI APPLICATION
# ==========================================================

app = FastAPI(
    title="StudyNova Personalized Study API",
    description=(
        "Custom API for personalized academic learning "
        "recommendations and study insights."
    ),
    version="1.0.0"
)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# PROJECT PATHS
# ==========================================================

CUSTOM_API_DIR = Path(
    __file__
).resolve().parent

PROJECT_ROOT = CUSTOM_API_DIR.parent

STORAGE_DIR = (
    PROJECT_ROOT / "storage"
)


QUIZ_HISTORY_PATH = (
    STORAGE_DIR / "quiz_history.json"
)

ACTIVITY_HISTORY_PATH = (
    STORAGE_DIR / "activity_history.json"
)


# ==========================================================
# JSON LOADER
# ==========================================================

def load_json(path):
    """
    Safely read a JSON list.
    """

    path = Path(path)

    if not path.exists():

        return []


    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)


        if isinstance(
            data,
            list
        ):

            return data


        return []


    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


# ==========================================================
# GET USER QUIZ DATA
# ==========================================================

def user_quiz_data(
    user_uid
):

    return [

        record

        for record in load_json(
            QUIZ_HISTORY_PATH
        )

        if record.get(
            "user_uid"
        )
        ==
        user_uid
    ]


# ==========================================================
# GET USER ACTIVITY DATA
# ==========================================================

def user_activity_data(
    user_uid
):

    return [

        record

        for record in load_json(
            ACTIVITY_HISTORY_PATH
        )

        if record.get(
            "user_uid"
        )
        ==
        user_uid
    ]


# ==========================================================
# DATE PARSER
# ==========================================================

def parse_activity_date(
    date_value
):
    """
    Convert stored activity date into
    a Python date object.
    """

    if not date_value:

        return None


    date_text = str(
        date_value
    ).strip()


    # ------------------------------------------------------
    # Expected format:
    # 2026-08-25 10:20:40 UTC
    # ------------------------------------------------------

    try:

        return datetime.strptime(
            date_text,
            "%Y-%m-%d %H:%M:%S UTC"
        )

    except ValueError:

        pass


    # ------------------------------------------------------
    # ISO format
    # ------------------------------------------------------

    try:

        return datetime.fromisoformat(
            date_text.replace(
                "Z",
                "+00:00"
            )
        ).replace(
            tzinfo=None
        )

    except ValueError:

        pass


    return None


# ==========================================================
# CALCULATE STREAKS
# ==========================================================

def calculate_streaks(
    activity_data
):
    """
    Return:
        current_streak
        best_streak
    """

    dates = set()


    for row in activity_data:

        date_value = row.get(
            "date"
        )


        parsed_date = (
            parse_activity_date(
                date_value
            )
        )


        if parsed_date:

            dates.add(
                parsed_date.date()
            )


    if not dates:

        return 0, 0


    sorted_dates = sorted(
        dates
    )


    # ======================================================
    # BEST STREAK
    # ======================================================

    best_streak = 1

    running_streak = 1


    for index in range(
        1,
        len(sorted_dates)
    ):

        difference = (
            sorted_dates[index]
            -
            sorted_dates[index - 1]
        ).days


        if difference == 1:

            running_streak += 1

        else:

            running_streak = 1


        best_streak = max(
            best_streak,
            running_streak
        )


    # ======================================================
    # CURRENT STREAK
    # ======================================================

    today = datetime.utcnow().date()

    current_streak = 0

    cursor = today


    while cursor in dates:

        current_streak += 1

        cursor -= timedelta(
            days=1
        )


    return (
        current_streak,
        best_streak
    )


# ==========================================================
# GET TOPIC SCORES
# ==========================================================

def get_topic_scores(
    quiz_data
):

    topic_scores = defaultdict(
        list
    )


    for row in quiz_data:

        topic = (
            row.get(
                "topic"
            )
            or
            "Unknown"
        )


        percentage = row.get(
            "percentage"
        )


        try:

            percentage = float(
                percentage
            )

        except (
            TypeError,
            ValueError
        ):

            continue


        topic_scores[
            topic
        ].append(
            percentage
        )


    return topic_scores


# ==========================================================
# GET TOPIC BREAKDOWN
# ==========================================================

def get_topic_breakdown(
    quiz_data
):

    topic_scores = (
        get_topic_scores(
            quiz_data
        )
    )


    result = []


    for topic, scores in (
        topic_scores.items()
    ):

        if not scores:

            continue


        average_score = (
            sum(scores)
            /
            len(scores)
        )


        result.append(
            {
                "topic": topic,
                "attempts": len(
                    scores
                ),
                "average_score": round(
                    average_score,
                    1
                ),
            }
        )


    result.sort(
        key=lambda item:
        item["average_score"]
    )


    return result


# ==========================================================
# ACTIVITY COUNTS
# ==========================================================

def get_activity_counts(
    activity_data
):

    counts = Counter()


    for row in activity_data:

        activity_type = (
            row.get(
                "type"
            )
            or
            row.get(
                "activity_type"
            )
            or
            "other"
        )


        counts[
            activity_type
        ] += 1


    return counts


# ==========================================================
# LAST ACTIVITY
# ==========================================================

def get_latest_activity(
    activity_data
):

    parsed_records = []


    for row in activity_data:

        parsed_date = (
            parse_activity_date(
                row.get(
                    "date"
                )
            )
        )


        if parsed_date:

            parsed_records.append(
                (
                    parsed_date,
                    row
                )
            )


    if not parsed_records:

        return None


    parsed_records.sort(
        key=lambda item:
        item[0],
        reverse=True
    )


    latest_date, latest_record = (
        parsed_records[0]
    )


    return {
        "type": (
            latest_record.get(
                "type",
                "other"
            )
        ),

        "topic": (
            latest_record.get(
                "topic",
                "General"
            )
        ),

        "description": (
            latest_record.get(
                "description",
                ""
            )
        ),

        "date": (
            latest_record.get(
                "date",
                ""
            )
        ),
    }


# ==========================================================
# ROOT ENDPOINT
# ==========================================================

@app.get("/")
def root():

    return {
        "status":
            "StudyNova Recommendation API is running",

        "version":
            "1.0.0",

        "service":
            "Personalized Study Recommendation API",
    }


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.get("/health")
def health_check():

    return {

        "status": "healthy",

        "quiz_history_exists":
            QUIZ_HISTORY_PATH.exists(),

        "activity_history_exists":
            ACTIVITY_HISTORY_PATH.exists(),

        "storage_directory":
            str(
                STORAGE_DIR
            ),
    }


# ==========================================================
# ENDPOINT 1
# PERSONALIZED RECOMMENDATION
# ==========================================================

@app.get(
    "/recommend/{user_uid}"
)
def recommend(
    user_uid: str
):

    quiz_data = (
        user_quiz_data(
            user_uid
        )
    )


    activity_data = (
        user_activity_data(
            user_uid
        )
    )


    if not quiz_data and not activity_data:

        raise HTTPException(
            status_code=404,
            detail=(
                "No activity found for this user yet."
            )
        )


    topic_breakdown = (
        get_topic_breakdown(
            quiz_data
        )
    )


    weakest_topic = None

    weakest_average = None


    if topic_breakdown:

        weakest_topic = (
            topic_breakdown[0]["topic"]
        )

        weakest_average = (
            topic_breakdown[0]["average_score"]
        )


    current_streak, best_streak = (
        calculate_streaks(
            activity_data
        )
    )


    if weakest_topic:

        message = (
            f'You are currently weakest in '
            f'"{weakest_topic}" '
            f'with an average score of '
            f'{weakest_average}%. '
            f'Consider revising this topic next.'
        )

    else:

        message = (
            "Take a quiz to get a personalized "
            "topic recommendation."
        )


    return {

        "user_uid":
            user_uid,

        "weakest_topic":
            weakest_topic,

        "weakest_topic_avg_score":
            weakest_average,

        "current_streak_days":
            current_streak,

        "best_streak_days":
            best_streak,

        "message":
            message,
    }


# ==========================================================
# ENDPOINT 2
# TOPIC BREAKDOWN
# ==========================================================

@app.get(
    "/topics/{user_uid}"
)
def topic_breakdown(
    user_uid: str
):

    quiz_data = (
        user_quiz_data(
            user_uid
        )
    )


    if not quiz_data:

        raise HTTPException(
            status_code=404,
            detail=(
                "No quiz history found "
                "for this user yet."
            )
        )


    breakdown = (
        get_topic_breakdown(
            quiz_data
        )
    )


    return {

        "user_uid":
            user_uid,

        "topic_count":
            len(
                breakdown
            ),

        "topics":
            breakdown,
    }


# ==========================================================
# ENDPOINT 3
# STREAK DETAILS
# ==========================================================

@app.get(
    "/streak/{user_uid}"
)
def streak_details(
    user_uid: str
):

    activity_data = (
        user_activity_data(
            user_uid
        )
    )


    if not activity_data:

        raise HTTPException(
            status_code=404,
            detail=(
                "No activity found "
                "for this user yet."
            )
        )


    current_streak, best_streak = (
        calculate_streaks(
            activity_data
        )
    )


    return {

        "user_uid":
            user_uid,

        "current_streak_days":
            current_streak,

        "best_streak_days":
            best_streak,
    }


# ==========================================================
# ENDPOINT 4
# ACTIVITY SUMMARY
# ==========================================================

@app.get(
    "/summary/{user_uid}"
)
def activity_summary(
    user_uid: str
):

    activity_data = (
        user_activity_data(
            user_uid
        )
    )


    if not activity_data:

        raise HTTPException(
            status_code=404,
            detail=(
                "No activity found "
                "for this user yet."
            )
        )


    counts = (
        get_activity_counts(
            activity_data
        )
    )


    return {

        "user_uid":
            user_uid,

        "total_activities":
            len(
                activity_data
            ),

        "by_type":
            dict(
                counts
            ),
    }


# ==========================================================
# ENDPOINT 5
# PERSONALIZED INSIGHTS
# ==========================================================

@app.get(
    "/insights/{user_uid}"
)
def personalized_insights(
    user_uid: str
):

    quiz_data = (
        user_quiz_data(
            user_uid
        )
    )


    activity_data = (
        user_activity_data(
            user_uid
        )
    )


    if not quiz_data and not activity_data:

        raise HTTPException(
            status_code=404,
            detail=(
                "No activity found "
                "for this user yet."
            )
        )


    # ------------------------------------------------------
    # Quiz statistics
    # ------------------------------------------------------

    quiz_scores = []


    for quiz in quiz_data:

        try:

            score = float(
                quiz.get(
                    "percentage",
                    0
                )
            )

            quiz_scores.append(
                score
            )

        except (
            TypeError,
            ValueError
        ):

            pass


    average_quiz_score = 0


    if quiz_scores:

        average_quiz_score = round(
            sum(
                quiz_scores
            )
            /
            len(
                quiz_scores
            ),
            1
        )


    # ------------------------------------------------------
    # Topic information
    # ------------------------------------------------------

    topics = (
        get_topic_breakdown(
            quiz_data
        )
    )


    weakest_topic = None

    weakest_score = None

    strongest_topic = None

    strongest_score = None


    if topics:

        weakest_topic = (
            topics[0]["topic"]
        )

        weakest_score = (
            topics[0]["average_score"]
        )


        strongest = max(
            topics,
            key=lambda item:
            item["average_score"]
        )


        strongest_topic = (
            strongest["topic"]
        )

        strongest_score = (
            strongest["average_score"]
        )


    # ------------------------------------------------------
    # Activity information
    # ------------------------------------------------------

    activity_counts = (
        get_activity_counts(
            activity_data
        )
    )


    most_used_activity = None


    if activity_counts:

        most_used_activity = (
            activity_counts
            .most_common(1)[0][0]
        )


    # ------------------------------------------------------
    # Streak
    # ------------------------------------------------------

    current_streak, best_streak = (
        calculate_streaks(
            activity_data
        )
    )


    # ------------------------------------------------------
    # Latest activity
    # ------------------------------------------------------

    latest_activity = (
        get_latest_activity(
            activity_data
        )
    )


    # ------------------------------------------------------
    # Recommendation
    # ------------------------------------------------------

    if weakest_topic and weakest_score < 50:

        focus_message = (
            f"Focus on {weakest_topic}. "
            f"Your average score is only "
            f"{weakest_score}%. "
            f"Revise this topic and take another quiz."
        )


    elif weakest_topic and weakest_score < 70:

        focus_message = (
            f"Your next focus should be "
            f"{weakest_topic}. "
            f"Your average score is "
            f"{weakest_score}%. "
            f"More practice can improve your result."
        )


    elif current_streak == 0:

        focus_message = (
            "You have no active study streak. "
            "Try to study at least one topic today."
        )


    elif average_quiz_score >= 80:

        focus_message = (
            "Your quiz performance is strong. "
            "Try a harder topic or difficulty level."
        )


    else:

        focus_message = (
            "Keep studying regularly and "
            "continue practicing with quizzes."
        )


    return {

        "user_uid":
            user_uid,

        "total_quizzes":
            len(
                quiz_data
            ),

        "average_quiz_score":
            average_quiz_score,

        "strongest_topic":
            strongest_topic,

        "strongest_topic_score":
            strongest_score,

        "weakest_topic":
            weakest_topic,

        "weakest_topic_score":
            weakest_score,

        "most_used_activity":
            most_used_activity,

        "current_streak_days":
            current_streak,

        "best_streak_days":
            best_streak,

        "latest_activity":
            latest_activity,

        "focus_message":
            focus_message,
    }


# ==========================================================
# ENDPOINT 6
# PERSONALIZED STUDY PLAN
# ==========================================================

@app.get(
    "/study-plan/{user_uid}"
)
def personalized_study_plan(
    user_uid: str
):

    quiz_data = (
        user_quiz_data(
            user_uid
        )
    )


    activity_data = (
        user_activity_data(
            user_uid
        )
    )


    if not quiz_data and not activity_data:

        raise HTTPException(
            status_code=404,
            detail=(
                "No activity found "
                "for this user yet."
            )
        )


    topics = (
        get_topic_breakdown(
            quiz_data
        )
    )


    current_streak, best_streak = (
        calculate_streaks(
            activity_data
        )
    )


    plan = []


    # ======================================================
    # PLAN ITEM 1
    # ======================================================

    if topics:

        weakest = topics[0]

        plan.append(
            {
                "priority": "High",

                "action":
                    "Revise weak topic",

                "topic":
                    weakest["topic"],

                "reason":
                    (
                        f'Average quiz score is '
                        f'{weakest["average_score"]}%.'
                    )
            }
        )

    else:

        plan.append(
            {
                "priority": "High",

                "action":
                    "Take your first quiz",

                "topic":
                    "Choose any academic topic",

                "reason":
                    (
                        "Quiz data is needed to "
                        "identify weak topics."
                    )
            }
        )


    # ======================================================
    # PLAN ITEM 2
    # ======================================================

    if current_streak == 0:

        plan.append(
            {
                "priority": "Medium",

                "action":
                    "Start a study streak",

                "topic":
                    "Any academic topic",

                "reason":
                    (
                        "No activity was recorded "
                        "for today."
                    )
            }
        )

    else:

        plan.append(
            {
                "priority": "Medium",

                "action":
                    "Maintain your study streak",

                "topic":
                    "Continue today's study",

                "reason":
                    (
                        f"Current streak: "
                        f"{current_streak} day(s)."
                    )
            }
        )


    # ======================================================
    # PLAN ITEM 3
    # ======================================================

    plan.append(
        {
            "priority": "Medium",

            "action":
                "Practice with a quiz",

            "topic":
                (
                    topics[0]["topic"]
                    if topics
                    else "Choose a topic"
                ),

            "reason":
                (
                    "Quiz practice helps measure "
                    "your understanding."
                )
        }
    )


    # ======================================================
    # PLAN ITEM 4
    # ======================================================

    plan.append(
        {
            "priority": "Low",

            "action":
                "Use another learning resource",

            "topic":
                (
                    topics[0]["topic"]
                    if topics
                    else "Current study topic"
                ),

            "reason":
                (
                    "Use Image Study or YouTube "
                    "Resources for additional learning."
                )
        }
    )


    return {

        "user_uid":
            user_uid,

        "current_streak_days":
            current_streak,

        "best_streak_days":
            best_streak,

        "study_plan":
            plan,
    }