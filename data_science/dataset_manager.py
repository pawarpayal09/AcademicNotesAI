import json
from pathlib import Path

import pandas as pd


# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(
    __file__
).resolve().parent.parent

STORAGE_DIR = (
    PROJECT_ROOT / "storage"
)


# ==========================================================
# SOURCE JSON FILES
# ==========================================================

JSON_FILES = [
    "users.json",
    "chat_history.json",
    "favourites.json",
    "quiz_history.json",
    "image_study_history.json",
    "youtube_history.json",
    "activity_history.json",
]


# ==========================================================
# COMMON DATASET COLUMNS
# ==========================================================

DATASET_COLUMNS = [

    "record_id",

    "source_file",

    "record_type",

    "user_uid",

    "user_name",

    "user_email",

    "date",

    "created_at",

    "topic",

    "question",

    "answer",

    "difficulty",

    "score",

    "total_questions",

    "percentage",

    "image_name",

    "instruction",

    "results_count",

    "chat_title",

    "message_count",

    "description",

    "sources",

    "email_verified",

    "disabled",

    # Derived Data Science fields
    "question_length",

    "answer_length",

    "has_question",

    "has_answer",

    "has_source",

    "activity_hour",

]


# ==========================================================
# SAFE JSON LOADER
# ==========================================================

def _load_json_file(
    file_path: Path
):
    """
    Read one JSON file safely.

    Returns:
        list of dictionaries
    """

    if not file_path.exists():

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


    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


    # ------------------------------------------------------
    # Normal format
    # ------------------------------------------------------

    if isinstance(
        data,
        list
    ):

        return [
            item
            for item in data
            if isinstance(
                item,
                dict
            )
        ]


    # ------------------------------------------------------
    # Single dictionary
    # ------------------------------------------------------

    if isinstance(
        data,
        dict
    ):

        return [data]


    return []


# ==========================================================
# VALUE CLEANER
# ==========================================================

def _clean_value(
    value
):
    """
    Convert nested Python values into a
    simple value suitable for a DataFrame.
    """

    if value is None:

        return ""


    if isinstance(
        value,
        (dict, list)
    ):

        return json.dumps(
            value,
            ensure_ascii=False
        )


    return value


# ==========================================================
# RECORD ID
# ==========================================================

def _get_record_id(
    record,
    source_file,
    index
):
    """
    Find the best available ID for a record.
    """

    possible_ids = [

        "record_id",

        "id",

        "uid",

        "quiz_id",

        "activity_id",

        "search_id",

        "chat_id",
    ]


    for key in possible_ids:

        value = record.get(
            key
        )


        if value not in (
            None,
            ""
        ):

            return str(
                value
            )


    return (
        f"{Path(source_file).stem}_"
        f"{index + 1}"
    )


# ==========================================================
# PARSE HOUR FROM DATE
# ==========================================================

def _extract_hour(
    value
):
    """
    Try to extract the hour from a stored date/time string.

    Returns:
        integer hour 0-23
        or empty string
    """

    if not value:

        return ""


    value = str(
        value
    ).strip()


    # ------------------------------------------------------
    # Example:
    # 2026-08-15 09:46:13 UTC
    # ------------------------------------------------------

    try:

        time_part = (
            value.split(" ")[1]
        )

        hour = (
            time_part.split(":")[0]
        )

        return int(
            hour
        )

    except (
        IndexError,
        ValueError
    ):

        pass


    # ------------------------------------------------------
    # Another common format:
    # 2026-08-15T09:46:13
    # ------------------------------------------------------

    try:

        if "T" in value:

            time_part = (
                value.split("T")[1]
            )

            hour = (
                time_part.split(":")[0]
            )

            return int(
                hour
            )

    except (
        IndexError,
        ValueError
    ):

        pass


    return ""


# ==========================================================
# CONVERT ONE RECORD
# ==========================================================

def _convert_record(
    record,
    source_file,
    index
):
    """
    Convert one JSON record into a standard
    dataset row.
    """

    row = {

        "record_id": (
            _get_record_id(
                record,
                source_file,
                index
            )
        ),

        "source_file": (
            source_file
        ),

        "record_type": (
            Path(
                source_file
            ).stem
        ),

        # --------------------------------------------------
        # USER
        # --------------------------------------------------

        "user_uid": (
            record.get(
                "user_uid",
                record.get(
                    "uid",
                    ""
                )
            )
        ),

        "user_name": (
            record.get(
                "user_name",
                record.get(
                    "name",
                    ""
                )
            )
        ),

        "user_email": (
            record.get(
                "user_email",
                record.get(
                    "email",
                    ""
                )
            )
        ),

        # --------------------------------------------------
        # TIME
        # --------------------------------------------------

        "date": _clean_value(
            record.get(
                "date",
                ""
            )
        ),

        "created_at": _clean_value(
            record.get(
                "created_at",
                ""
            )
        ),

        # --------------------------------------------------
        # ACADEMIC CONTENT
        # --------------------------------------------------

        "topic": _clean_value(
            record.get(
                "topic",
                ""
            )
        ),

        "question": _clean_value(
            record.get(
                "question",
                ""
            )
        ),

        "answer": _clean_value(
            record.get(
                "answer",
                ""
            )
        ),

        # --------------------------------------------------
        # QUIZ
        # --------------------------------------------------

        "difficulty": _clean_value(
            record.get(
                "difficulty",
                ""
            )
        ),

        "score": _clean_value(
            record.get(
                "score",
                ""
            )
        ),

        "total_questions": _clean_value(
            record.get(
                "total_questions",
                ""
            )
        ),

        "percentage": _clean_value(
            record.get(
                "percentage",
                ""
            )
        ),

        # --------------------------------------------------
        # IMAGE
        # --------------------------------------------------

        "image_name": _clean_value(
            record.get(
                "image_name",
                ""
            )
        ),

        "instruction": _clean_value(
            record.get(
                "instruction",
                ""
            )
        ),

        # --------------------------------------------------
        # YOUTUBE
        # --------------------------------------------------

        "results_count": _clean_value(
            record.get(
                "results_count",
                ""
            )
        ),

        # --------------------------------------------------
        # CHAT
        # --------------------------------------------------

        "chat_title": _clean_value(
            record.get(
                "title",
                record.get(
                    "chat_title",
                    ""
                )
            )
        ),

        # --------------------------------------------------
        # ACTIVITY
        # --------------------------------------------------

        "description": _clean_value(
            record.get(
                "description",
                ""
            )
        ),

        # --------------------------------------------------
        # SOURCES
        # --------------------------------------------------

        "sources": _clean_value(
            record.get(
                "sources",
                ""
            )
        ),

        # --------------------------------------------------
        # USER STATUS
        # --------------------------------------------------

        "email_verified": _clean_value(
            record.get(
                "email_verified",
                ""
            )
        ),

        "disabled": _clean_value(
            record.get(
                "disabled",
                ""
            )
        ),
    }


    # ======================================================
    # MESSAGE COUNT
    # ======================================================

    messages = record.get(
        "messages",
        []
    )


    if isinstance(
        messages,
        list
    ):

        row["message_count"] = len(
            messages
        )

    else:

        row["message_count"] = ""


    # ======================================================
    # DATA SCIENCE DERIVED FEATURES
    # ======================================================

    question_text = str(
        row["question"]
        or
        ""
    )


    answer_text = str(
        row["answer"]
        or
        ""
    )


    sources_text = str(
        row["sources"]
        or
        ""
    )


    row["question_length"] = len(
        question_text.strip()
    )


    row["answer_length"] = len(
        answer_text.strip()
    )


    row["has_question"] = (
        1
        if question_text.strip()
        else 0
    )


    row["has_answer"] = (
        1
        if answer_text.strip()
        else 0
    )


    row["has_source"] = (
        1
        if sources_text.strip()
        else 0
    )


    row["activity_hour"] = (
        _extract_hour(
            row["date"]
        )
    )


    return row


# ==========================================================
# LOAD ALL DATA
# ==========================================================

def load_combined_dataset(
    user_uid=None
):
    """
    Read all seven JSON files and return one
    combined Pandas DataFrame.

    Parameters:
        user_uid:
            If supplied, only that user's records
            are returned.

    Returns:
        Pandas DataFrame
    """

    all_rows = []


    # ======================================================
    # READ EACH JSON
    # ======================================================

    for json_name in JSON_FILES:

        json_path = (
            STORAGE_DIR / json_name
        )


        records = _load_json_file(
            json_path
        )


        for index, record in enumerate(
            records
        ):

            row = _convert_record(
                record,
                json_name,
                index
            )


            all_rows.append(
                row
            )


    # ======================================================
    # CREATE DATAFRAME
    # ======================================================

    dataframe = pd.DataFrame(
        all_rows,
        columns=DATASET_COLUMNS
    )


    # ======================================================
    # USER FILTER
    # ======================================================

    if user_uid:

        dataframe = (
            dataframe[
                dataframe[
                    "user_uid"
                ].astype(str)
                ==
                str(user_uid)
            ]
            .copy()
        )


    # ======================================================
    # RESET INDEX
    # ======================================================

    dataframe = (
        dataframe
        .reset_index(
            drop=True
        )
    )


    # ======================================================
    # SORT
    # ======================================================

    if not dataframe.empty:

        # Create temporary sorting field.

        dataframe["_sort_date"] = (
            pd.to_datetime(
                dataframe["date"],
                errors="coerce",
                utc=True
            )
        )


        dataframe = (
            dataframe
            .sort_values(
                by="_sort_date",
                ascending=False,
                na_position="last"
            )
            .drop(
                columns="_sort_date"
            )
            .reset_index(
                drop=True
            )
        )


    return dataframe


# ==========================================================
# GET ALL DATA
# ==========================================================

def get_all_data():

    return load_combined_dataset()


# ==========================================================
# GET CURRENT USER DATA
# ==========================================================

def get_current_user_dataset(
    user_uid
):

    if not user_uid:

        return pd.DataFrame(
            columns=DATASET_COLUMNS
        )


    return load_combined_dataset(
        user_uid=user_uid
    )


# ==========================================================
# DATASET SUMMARY
# ==========================================================

def get_dataset_summary(
    dataframe
):
    """
    Calculate basic summary information.
    """

    if dataframe is None:

        dataframe = pd.DataFrame(
            columns=DATASET_COLUMNS
        )


    summary = {

        "total_records": (
            len(dataframe)
        ),

        "total_users": (
            dataframe[
                "user_uid"
            ]
            .replace(
                "",
                pd.NA
            )
            .nunique()
        ),

        "total_questions": (
            (
                dataframe[
                    "record_type"
                ]
                == "chat_history"
            )
            .sum()
        ),

        "total_quizzes": (
            (
                dataframe[
                    "record_type"
                ]
                == "quiz_history"
            )
            .sum()
        ),

        "total_images": (
            (
                dataframe[
                    "record_type"
                ]
                == "image_study_history"
            )
            .sum()
        ),

        "total_youtube_searches": (
            (
                dataframe[
                    "record_type"
                ]
                == "youtube_history"
            )
            .sum()
        ),

        "total_saved_notes": (
            (
                dataframe[
                    "record_type"
                ]
                == "favourites"
            )
            .sum()
        ),
    }


    # ======================================================
    # AVERAGE QUIZ SCORE
    # ======================================================

    if (
        "percentage" in dataframe.columns
        and not dataframe.empty
    ):

        quiz_percentages = pd.to_numeric(
            dataframe.loc[
                dataframe[
                    "record_type"
                ] == "quiz_history",
                "percentage"
            ],
            errors="coerce"
        ).dropna()


        if not quiz_percentages.empty:

            summary[
                "average_quiz_percentage"
            ] = round(
                quiz_percentages.mean(),
                2
            )

        else:

            summary[
                "average_quiz_percentage"
            ] = 0

    else:

        summary[
            "average_quiz_percentage"
        ] = 0


    return summary


# ==========================================================
# TOP TOPICS
# ==========================================================

def get_top_topics(
    dataframe,
    limit=10
):
    """
    Return most frequently used topics.
    """

    if dataframe is None:

        return pd.DataFrame(
            columns=[
                "topic",
                "count"
            ]
        )


    topics = (
        dataframe[
            "topic"
        ]
        .astype(str)
        .str.strip()
    )


    topics = topics[
        ~topics.isin(
            [
                "",
                "General",
                "Image Study",
                "Saved Notes"
            ]
        )
    ]


    if topics.empty:

        return pd.DataFrame(
            columns=[
                "topic",
                "count"
            ]
        )


    result = (
        topics
        .value_counts()
        .head(limit)
        .reset_index()
    )


    result.columns = [
        "topic",
        "count"
    ]


    return result


# ==========================================================
# ACTIVITY SUMMARY
# ==========================================================

def get_activity_summary(
    dataframe
):
    """
    Count records by activity type.
    """

    if dataframe is None:

        return pd.DataFrame(
            columns=[
                "record_type",
                "count"
            ]
        )


    result = (
        dataframe[
            "record_type"
        ]
        .value_counts()
        .reset_index()
    )


    result.columns = [
        "record_type",
        "count"
    ]


    return result


# ==========================================================
# QUIZ PERFORMANCE
# ==========================================================

def get_quiz_performance(
    dataframe
):
    """
    Return quiz records and useful numeric values.
    """

    if dataframe is None:

        return pd.DataFrame()


    quiz_data = (
        dataframe[
            dataframe[
                "record_type"
            ]
            == "quiz_history"
        ]
        .copy()
    )


    if quiz_data.empty:

        return quiz_data


    quiz_data[
        "score"
    ] = pd.to_numeric(
        quiz_data[
            "score"
        ],
        errors="coerce"
    )


    quiz_data[
        "total_questions"
    ] = pd.to_numeric(
        quiz_data[
            "total_questions"
        ],
        errors="coerce"
    )


    quiz_data[
        "percentage"
    ] = pd.to_numeric(
        quiz_data[
            "percentage"
        ],
        errors="coerce"
    )


    return quiz_data


# ==========================================================
# DATE-WISE ACTIVITY
# ==========================================================

def get_daily_activity(
    dataframe
):
    """
    Return daily record counts.
    """

    if dataframe is None:

        return pd.DataFrame(
            columns=[
                "date",
                "count"
            ]
        )


    if dataframe.empty:

        return pd.DataFrame(
            columns=[
                "date",
                "count"
            ]
        )


    dates = pd.to_datetime(
        dataframe["date"],
        errors="coerce",
        utc=True
    )


    valid_dates = dates.dropna()


    if valid_dates.empty:

        return pd.DataFrame(
            columns=[
                "date",
                "count"
            ]
        )


    date_only = (
        valid_dates
        .dt.date
        .astype(str)
    )


    result = (
        date_only
        .value_counts()
        .sort_index()
        .reset_index()
    )


    result.columns = [
        "date",
        "count"
    ]


    return result


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    dataframe = (
        load_combined_dataset()
    )


    print(
        "\n========================================"
    )

    print(
        "Academic Notes AI Dataset Manager"
    )

    print(
        "========================================"
    )


    print(
        f"Records : {len(dataframe)}"
    )


    print(
        f"Columns : {len(dataframe.columns)}"
    )


    print(
        "\nColumns:"
    )


    for column in dataframe.columns:

        print(
            f" - {column}"
        )


    print(
        "\n========================================"
    )

    print(
        "Dataset loaded successfully."
    )

    print(
        "========================================"
    )