import json
import os

from datetime import (
    datetime,
    timezone,
    timedelta
)

from collections import Counter

from pathlib import Path

import streamlit as st

from firebase_admin import firestore

from firebase_manager import (
    is_authenticated,
    get_current_user,
    get_user_document,
    get_firestore_client,
)


# ==========================================================
# PATHS
# ==========================================================

PROJECT_ROOT = Path(
    __file__
).resolve().parent

STORAGE_DIR = (
    PROJECT_ROOT / "storage"
)


QUIZ_HISTORY_FILE = (
    STORAGE_DIR / "quiz_history.json"
)

IMAGE_STUDY_HISTORY_FILE = (
    STORAGE_DIR / "image_study_history.json"
)

YOUTUBE_HISTORY_FILE = (
    STORAGE_DIR / "youtube_history.json"
)

ACTIVITY_HISTORY_FILE = (
    STORAGE_DIR / "activity_history.json"
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
# CREATE STORAGE DIRECTORY
# ==========================================================

def ensure_storage_directory():

    STORAGE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


ensure_storage_directory()


# ==========================================================
# GENERIC JSON LOAD
# ==========================================================

def _load_json_file(
    file_path
):
    """
    Load a JSON file.

    If the file doesn't exist or is invalid,
    create/reset it as an empty list.
    """

    ensure_storage_directory()

    if not file_path.exists():

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4,
                ensure_ascii=False
            )

        return []


    if file_path.stat().st_size == 0:

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4,
                ensure_ascii=False
            )

        return []


    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )


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

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4,
                ensure_ascii=False
            )

        return []

# ==========================================================
# GENERIC JSON SAVE
# ==========================================================

def _save_json_file(
    file_path,
    data
):
    """
    Save JSON data directly to the requested JSON file.
    """

    ensure_storage_directory()

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

# ==========================================================
# APPEND JSON RECORD
# ==========================================================

def _append_json_record(
    file_path,
    record
):
    """
    Append one record to a JSON list.
    """

    records = _load_json_file(
        file_path
    )

    records.append(
        record
    )

    _save_json_file(
        file_path,
        records
    )


# ==========================================================
# CURRENT USER UID
# ==========================================================

def _get_current_user_uid():

    if not is_authenticated():

        return None


    current_user = (
        get_current_user()
    )


    if not current_user:

        return None


    return current_user.get(
        "uid"
    )


# ==========================================================
# CURRENT USER DETAILS
# ==========================================================

def _get_current_user_details():

    current_user = (
        get_current_user()
    )


    if not current_user:

        return {
            "uid": None,
            "name": "Guest",
            "email": ""
        }


    return {

        "uid": current_user.get(
            "uid"
        ),

        "name": current_user.get(
            "name",
            "Student"
        ),

        "email": current_user.get(
            "email",
            ""
        ),
    }


# ==========================================================
# TIMESTAMP
# ==========================================================

def _current_timestamp():

    return datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )


# ==========================================================
# USER FIRESTORE REFERENCE
# ==========================================================

def _get_user_ref():

    if not is_authenticated():

        return None

    return get_user_document()


# ==========================================================
# UPDATE FIRESTORE STATS
# ==========================================================

def _update_stats(
    updates
):
    """
    Update only the supplied Firebase statistics.

    The existing Firestore dashboard functionality
    remains active.
    """

    user_ref = _get_user_ref()


    if user_ref is None:

        return False


    try:

        firestore_updates = {}


        for field, value in updates.items():

            firestore_updates[
                f"stats.{field}"
            ] = value


        user_ref.update(
            firestore_updates
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
# INITIALIZE USER STATS
# ==========================================================

def initialize_user_stats():

    user_ref = _get_user_ref()


    if user_ref is None:

        return False


    try:

        current_document = (
            user_ref.get()
        )


        if not current_document.exists:

            user_ref.set(
                {
                    "stats": DEFAULT_STATS
                },
                merge=True
            )

        else:

            data = (
                current_document.to_dict()
                or {}
            )


            if "stats" not in data:

                user_ref.set(
                    {
                        "stats": DEFAULT_STATS
                    },
                    merge=True
                )


        return True


    except Exception as e:

        print(
            "User stats initialization error:",
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
    Save activity to BOTH:

    1. Firestore
    2. activity_history.json

    The record is linked to the current user's UID.
    """

    user_details = (
        _get_current_user_details()
    )


    uid = user_details["uid"]


    if not uid:

        return False


    timestamp = _current_timestamp()


    activity_record = {

        "activity_id": (
            f"{uid}_"
            f"{int(datetime.now().timestamp() * 1000)}"
        ),

        "user_uid": uid,

        "user_name": user_details["name"],

        "user_email": user_details["email"],

        "type": activity_type,

        "topic": topic or "General",

        "description": description or "",

        "date": timestamp,

        "metadata": metadata or {},
    }


    # ======================================================
    # LOCAL JSON
    # ======================================================

    try:

        _append_json_record(
            ACTIVITY_HISTORY_FILE,
            activity_record
        )

    except Exception as e:

        print(
            "Activity JSON error:",
            type(e).__name__,
            str(e)
        )


    # ======================================================
    # FIRESTORE
    # ======================================================

    try:

        user_ref = _get_user_ref()


        if user_ref is not None:

            user_ref.collection(
                "activity"
            ).add(
                {
                    "type": activity_type,

                    "topic": (
                        topic or "General"
                    ),

                    "description": (
                        description or ""
                    ),

                    "created_at": datetime.now(
                        timezone.utc
                    ),

                    "metadata": (
                        metadata or {}
                    ),
                }
            )


    except Exception as e:

        print(
            "Activity Firestore error:",
            type(e).__name__,
            str(e)
        )


    return True


# ==========================================================
# RECORD CHAT QUESTION
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

        # --------------------------------------------------
        # Image-specific JSON
        # --------------------------------------------------

        user_details = (
            _get_current_user_details()
        )


        uid = user_details["uid"]


        if uid:

            image_record = {

                "activity_id": (
                    f"{uid}_"
                    f"{int(datetime.now().timestamp() * 1000)}"
                ),

                "user_uid": uid,

                "user_name": (
                    user_details["name"]
                ),

                "user_email": (
                    user_details["email"]
                ),

                "image_name": (
                    image_name
                    or
                    "Study Image"
                ),

                "instruction": (
                    instruction
                    or
                    ""
                ),

                "date": (
                    _current_timestamp()
                ),
            }


            _append_json_record(
                IMAGE_STUDY_HISTORY_FILE,
                image_record
            )


        # --------------------------------------------------
        # Overall activity
        # --------------------------------------------------

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
    topic,
    results_count=0
):

    success = _update_stats(
        {
            "total_youtube_searches":
                firestore.Increment(1)
        }
    )


    if success:

        user_details = (
            _get_current_user_details()
        )


        uid = user_details["uid"]


        if uid:

            youtube_record = {

                "search_id": (
                    f"{uid}_"
                    f"{int(datetime.now().timestamp() * 1000)}"
                ),

                "user_uid": uid,

                "user_name": (
                    user_details["name"]
                ),

                "user_email": (
                    user_details["email"]
                ),

                "topic": (
                    topic
                    or
                    "General"
                ),

                "results_count": (
                    int(results_count)
                    if results_count
                    else 0
                ),

                "date": (
                    _current_timestamp()
                ),
            }


            _append_json_record(
                YOUTUBE_HISTORY_FILE,
                youtube_record
            )


        log_activity(
            activity_type="youtube",

            topic=topic,

            description=(
                f"YouTube learning search: "
                f"{topic}"
            ),

            metadata={
                "results_count": (
                    int(results_count)
                    if results_count
                    else 0
                )
            }
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

        user_details = (
            _get_current_user_details()
        )

        uid = user_details["uid"]

        if uid:

            image_record = {

                "activity_id": (
                    f"{uid}_"
                    f"{int(datetime.now().timestamp() * 1000)}"
                ),

                "user_uid": uid,

                "user_name": (
                    user_details["name"]
                ),

                "user_email": (
                    user_details["email"]
                ),

                "image_name": (
                    image_name
                    or
                    "Study Image"
                ),

                "instruction": (
                    instruction
                    or
                    ""
                ),

                "date": (
                    _current_timestamp()
                ),
            }

            _append_json_record(
                IMAGE_STUDY_HISTORY_FILE,
                image_record
            )

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
    topic,
    results_count=0
):
    """
    Save a successful YouTube search for the
    currently logged-in user.

    Data is stored in:
        storage/youtube_history.json

    The same activity is also recorded in:
        Firestore
        activity_history.json
    """

    user_details = (
        _get_current_user_details()
    )

    uid = user_details["uid"]

    if not uid:
        return False

    timestamp = _current_timestamp()

    # ======================================================
    # YOUTUBE JSON RECORD
    # ======================================================

    youtube_record = {

        "search_id": (
            f"{uid}_"
            f"{int(datetime.now().timestamp() * 1000)}"
        ),

        "user_uid": uid,

        "user_name": (
            user_details["name"]
        ),

        "user_email": (
            user_details["email"]
        ),

        "topic": (
            topic
            or
            "General"
        ),

        "results_count": int(
            results_count
            or 0
        ),

        "date": timestamp,
    }

    # ======================================================
    # SAVE TO youtube_history.json
    # ======================================================

    try:

        _append_json_record(
            YOUTUBE_HISTORY_FILE,
            youtube_record
        )

    except Exception as e:

        print(
            "YouTube history JSON error:",
            type(e).__name__,
            str(e)
        )

        return False

    # ======================================================
    # UPDATE FIRESTORE STATS
    # ======================================================

    _update_stats(
        {
            "total_youtube_searches":
                firestore.Increment(1)
        }
    )

    # ======================================================
    # LOG OVERALL ACTIVITY
    # ======================================================

    log_activity(
        activity_type="youtube",

        topic=topic,

        description=(
            f"YouTube learning search: "
            f"{topic}"
        ),

        metadata={
            "results_count": int(
                results_count
                or 0
            )
        }
    )

    return True


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
# RECORD QUIZ RESULT
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
        (
            score
            /
            total_questions
        )
        * 100
    )


    user_details = (
        _get_current_user_details()
    )


    uid = user_details["uid"]


    if not uid:

        return False


    # ======================================================
    # QUIZ JSON
    # ======================================================

    quiz_record = {

        "quiz_id": (
            f"{uid}_"
            f"{int(datetime.now().timestamp() * 1000)}"
        ),

        "user_uid": uid,

        "user_name": (
            user_details["name"]
        ),

        "user_email": (
            user_details["email"]
        ),

        "topic": (
            topic
            or
            "General"
        ),

        "difficulty": (
            difficulty
            or
            "Medium"
        ),

        "score": int(
            score
        ),

        "total_questions": int(
            total_questions
        ),

        "percentage": int(
            percentage
        ),

        "date": _current_timestamp(),
    }


    try:

        _append_json_record(
            QUIZ_HISTORY_FILE,
            quiz_record
        )

    except Exception as e:

        print(
            "Quiz history JSON error:",
            type(e).__name__,
            str(e)
        )


    # ======================================================
    # FIRESTORE QUIZ DATA
    # ======================================================

    try:

        user_ref = _get_user_ref()


        if user_ref is not None:

            user_ref.collection(
                "quizzes"
            ).add(
                {
                    "topic": (
                        topic
                        or
                        "General"
                    ),

                    "difficulty": (
                        difficulty
                        or
                        "Medium"
                    ),

                    "score": int(
                        score
                    ),

                    "total_questions": int(
                        total_questions
                    ),

                    "percentage": int(
                        percentage
                    ),

                    "created_at": datetime.now(
                        timezone.utc
                    ),
                }
            )


    except Exception as e:

        print(
            "Quiz Firestore error:",
            type(e).__name__,
            str(e)
        )


    # ======================================================
    # UPDATE FIRESTORE STATS
    # ======================================================

    _update_stats(
        {
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
    )


    # ======================================================
    # OVERALL ACTIVITY
    # ======================================================

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

            "total_questions": (
                total_questions
            ),

            "percentage": percentage,
        }
    )


    return True


# ==========================================================
# GET DASHBOARD STATS
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


        data = (
            document.to_dict()
            or {}
        )


        stored_stats = (
            data.get(
                "stats",
                {}
            )
        )


        for key in stats:

            if key in stored_stats:

                stats[key] = (
                    stored_stats[key]
                )


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
                direction=(
                    firestore.Query.DESCENDING
                )
            )
            .limit(
                limit
            )
        )


        documents = query.stream()


        results = []


        for document in documents:

            data = document.to_dict()


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

                    "created_at": data.get(
                        "created_at"
                    ),
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
                direction=(
                    firestore.Query.DESCENDING
                )
            )
            .limit(
                limit
            )
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


        topic_counter[
            topic
        ] += 1


    return topic_counter.most_common(
        limit
    )


# ==========================================================
# DIFFICULTY PERFORMANCE
# ==========================================================

def get_difficulty_performance():

    quiz_results = (
        get_quiz_results()
    )


    grouped = {

        "Easy": [],

        "Medium": [],

        "Hard": [],
    }


    for quiz in quiz_results:

        difficulty = (
            quiz.get(
                "difficulty",
                "Medium"
            )
        )


        if difficulty in grouped:

            grouped[
                difficulty
            ].append(
                quiz.get(
                    "percentage",
                    0
                )
            )


    output = {}


    for difficulty, scores in grouped.items():

        if scores:

            output[
                difficulty
            ] = round(
                sum(scores)
                /
                len(scores)
            )

        else:

            output[
                difficulty
            ] = 0


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


    # ======================================================
    # BEST STREAK
    # ======================================================

    best_streak = 1

    current_run = 1


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

            current_run += 1


            best_streak = max(
                best_streak,
                current_run
            )

        else:

            current_run = 1


    # ======================================================
    # CURRENT STREAK
    # ======================================================

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

        "current_streak":
            current_streak,

        "best_streak":
            best_streak,
    }