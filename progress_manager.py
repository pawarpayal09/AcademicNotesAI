from datetime import datetime, timezone, timedelta
from collections import Counter

from firebase_admin import firestore

from firebase_manager import (
    is_authenticated,
    get_user_document,
    get_firestore_client,
)


# ==========================================================
# DEFAULT STATS
# ==========================================================

DEFAULT_STATS = {
    "total_questions": 0,
    "total_quizzes": 0,
    "quiz_score_sum": 0,
    "total_images": 0,
    "total_saved_notes": 0,
    "total_youtube_searches": 0,
}


# ==========================================================
# GET USER REF
# ==========================================================

def _get_user_ref():

    if not is_authenticated():
        return None

    return get_user_document()


# ==========================================================
# INITIALIZE USER STATS
# ==========================================================

def initialize_user_stats():

    user_ref = _get_user_ref()

    if user_ref is None:
        return False

    user_ref.set(
        {
            "stats": DEFAULT_STATS
        },
        merge=True
    )

    return True


# ==========================================================
# UPDATE USER STATS
# ==========================================================

def _update_stats(updates):

    user_ref = _get_user_ref()

    if user_ref is None:
        return False

    try:

        update_data = {}

        for field, value in updates.items():

            update_data[
                f"stats.{field}"
            ] = value

        user_ref.set(
            {
                "stats": updates
            },
            merge=True
        )

        return True

    except Exception as e:

        print(
            "Stats update error:",
            type(e).__name__,
            str(e)
        )

        return False


# ==========================================================
# LOG ACTIVITY
# ==========================================================

def log_activity(
    activity_type,
    topic="General",
    description="",
    metadata=None
):
    """
    Store one activity for the logged-in user.
    """

    user_ref = _get_user_ref()

    if user_ref is None:
        return False

    try:

        activity_data = {
            "type": activity_type,
            "topic": topic or "General",
            "description": description or "",
            "created_at": datetime.now(timezone.utc),
            "metadata": metadata or {},
        }

        user_ref.collection(
            "activity"
        ).add(
            activity_data
        )

        return True

    except Exception as e:

        print(
            "Activity logging error:",
            type(e).__name__,
            str(e)
        )

        return False


# ==========================================================
# RECORD CHATBOT QUESTION
# ==========================================================

def record_chat_question(
    question,
    topic="Academic Notes"
):

    success = _update_stats(
        {
            "total_questions":
                firestore.Increment(1)
        }
    )

    if success:

        log_activity(
            activity_type="chat",
            topic=topic,
            description=question
        )

    return success


# ==========================================================
# RECORD IMAGE STUDY
# ==========================================================

def record_image_study(
    instruction,
    image_name="Study Image"
):

    success = _update_stats(
        {
            "total_images":
                firestore.Increment(1)
        }
    )

    if success:

        log_activity(
            activity_type="image",
            topic="Image Study",
            description=instruction,
            metadata={
                "image_name": image_name
            }
        )

    return success


# ==========================================================
# RECORD YOUTUBE SEARCH
# ==========================================================

def record_youtube_search(
    topic
):

    success = _update_stats(
        {
            "total_youtube_searches":
                firestore.Increment(1)
        }
    )

    if success:

        log_activity(
            activity_type="youtube",
            topic=topic,
            description=(
                f"YouTube learning search: {topic}"
            )
        )

    return success


# ==========================================================
# RECORD SAVED NOTE
# ==========================================================

def record_saved_note(
    question
):

    success = _update_stats(
        {
            "total_saved_notes":
                firestore.Increment(1)
        }
    )

    if success:

        log_activity(
            activity_type="saved_note",
            topic="Saved Notes",
            description=question
        )

    return success


# ==========================================================
# RECORD QUIZ
# ==========================================================

def record_quiz_result(
    topic,
    difficulty,
    score,
    total_questions
):

    if total_questions <= 0:
        return False

    percentage = round(
        (score / total_questions) * 100
    )

    try:

        user_ref = _get_user_ref()

        if user_ref is None:
            return False

        # ----------------------------------------------
        # Save quiz result
        # ----------------------------------------------

        quiz_data = {
            "topic": topic,
            "difficulty": difficulty,
            "score": score,
            "total_questions": total_questions,
            "percentage": percentage,
            "created_at": datetime.now(timezone.utc),
        }

        user_ref.collection(
            "quizzes"
        ).add(
            quiz_data
        )


        # ----------------------------------------------
        # Update overall stats
        # ----------------------------------------------

        user_ref.set(
            {
                "stats": {
                    "total_quizzes":
                        firestore.Increment(1),

                    "quiz_score_sum":
                        firestore.Increment(
                            percentage
                        ),

                    "total_questions":
                        firestore.Increment(
                            total_questions
                        ),
                }
            },
            merge=True
        )


        # ----------------------------------------------
        # Activity
        # ----------------------------------------------

        log_activity(
            activity_type="quiz",
            topic=topic,
            description=(
                f"{difficulty} quiz: "
                f"{score}/{total_questions} "
                f"({percentage}%)"
            ),
            metadata={
                "difficulty": difficulty,
                "score": score,
                "total_questions": total_questions,
                "percentage": percentage,
            }
        )

        return True

    except Exception as e:

        print(
            "Quiz tracking error:",
            type(e).__name__,
            str(e)
        )

        return False


# ==========================================================
# GET USER STATISTICS
# ==========================================================

def get_dashboard_stats():

    user_ref = _get_user_ref()

    stats = DEFAULT_STATS.copy()

    if user_ref is None:
        return stats

    try:

        document = user_ref.get()

        if not document.exists:
            return stats

        data = document.to_dict()

        stored_stats = data.get(
            "stats",
            {}
        )

        for key in stats:

            if key in stored_stats:

                stats[key] = stored_stats[key]

        return stats

    except Exception as e:

        print(
            "Dashboard stats error:",
            type(e).__name__,
            str(e)
        )

        return stats


# ==========================================================
# GET QUIZ RESULTS
# ==========================================================

def get_quiz_results(
    limit=100
):

    user_ref = _get_user_ref()

    if user_ref is None:
        return []

    try:

        query = (
            user_ref
            .collection("quizzes")
            .order_by(
                "created_at",
                direction=firestore.Query.DESCENDING
            )
            .limit(limit)
        )

        documents = query.stream()

        results = []

        for document in documents:

            data = document.to_dict()

            created_at = data.get(
                "created_at"
            )

            results.append(
                {
                    "topic": data.get(
                        "topic",
                        "General"
                    ),

                    "difficulty": data.get(
                        "difficulty",
                        "Medium"
                    ),

                    "score": data.get(
                        "score",
                        0
                    ),

                    "total_questions": data.get(
                        "total_questions",
                        0
                    ),

                    "percentage": data.get(
                        "percentage",
                        0
                    ),

                    "created_at": created_at,
                }
            )

        return results

    except Exception as e:

        print(
            "Quiz results error:",
            type(e).__name__,
            str(e)
        )

        return []


# ==========================================================
# GET RECENT ACTIVITY
# ==========================================================

def get_recent_activity(
    limit=12
):

    user_ref = _get_user_ref()

    if user_ref is None:
        return []

    try:

        query = (
            user_ref
            .collection("activity")
            .order_by(
                "created_at",
                direction=firestore.Query.DESCENDING
            )
            .limit(limit)
        )

        documents = query.stream()

        activities = []

        for document in documents:

            data = document.to_dict()

            activities.append(
                {
                    "type": data.get(
                        "type",
                        "activity"
                    ),

                    "topic": data.get(
                        "topic",
                        "General"
                    ),

                    "description": data.get(
                        "description",
                        ""
                    ),

                    "created_at": data.get(
                        "created_at"
                    ),
                }
            )

        return activities

    except Exception as e:

        print(
            "Recent activity error:",
            type(e).__name__,
            str(e)
        )

        return []


# ==========================================================
# TOP STUDIED TOPICS
# ==========================================================

def get_top_topics(
    limit=6
):

    activities = get_recent_activity(
        limit=100
    )

    topic_counter = Counter()

    ignored_topics = {
        "",
        "General",
        "Saved Notes",
        "Image Study",
    }

    for activity in activities:

        topic = activity.get(
            "topic",
            "General"
        )

        if topic in ignored_topics:
            continue

        topic_counter[topic] += 1

    return topic_counter.most_common(
        limit
    )


# ==========================================================
# DIFFICULTY PERFORMANCE
# ==========================================================

def get_difficulty_performance():

    quiz_results = get_quiz_results()

    grouped = {
        "Easy": [],
        "Medium": [],
        "Hard": [],
    }

    for quiz in quiz_results:

        difficulty = quiz.get(
            "difficulty",
            "Medium"
        )

        if difficulty in grouped:

            grouped[difficulty].append(
                quiz.get(
                    "percentage",
                    0
                )
            )

    output = {}

    for difficulty, scores in grouped.items():

        if scores:

            output[difficulty] = round(
                sum(scores) / len(scores)
            )

        else:

            output[difficulty] = 0

    return output


# ==========================================================
# STUDY STREAK
# ==========================================================

def get_study_streak():

    activities = get_recent_activity(
        limit=100
    )

    if not activities:

        return {
            "current_streak": 0,
            "best_streak": 0,
        }


    dates = set()

    for activity in activities:

        created_at = activity.get(
            "created_at"
        )

        if not created_at:
            continue

        if hasattr(
            created_at,
            "date"
        ):

            dates.add(
                created_at.date()
            )


    if not dates:

        return {
            "current_streak": 0,
            "best_streak": 0,
        }


    sorted_dates = sorted(
        dates
    )


    # ------------------------------------------------------
    # Best streak
    # ------------------------------------------------------

    best_streak = 1
    current_run = 1


    for index in range(
        1,
        len(sorted_dates)
    ):

        difference = (
            sorted_dates[index]
            - sorted_dates[index - 1]
        ).days

        if difference == 1:

            current_run += 1

            best_streak = max(
                best_streak,
                current_run
            )

        else:

            current_run = 1


    # ------------------------------------------------------
    # Current streak
    # ------------------------------------------------------

    today = datetime.now(
        timezone.utc
    ).date()


    current_streak = 0
    check_date = today


    while check_date in dates:

        current_streak += 1

        check_date -= timedelta(
            days=1
        )


    return {
        "current_streak": current_streak,
        "best_streak": best_streak,
    }