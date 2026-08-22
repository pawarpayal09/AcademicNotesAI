import json
from pathlib import Path
from collections import Counter

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
# CONSISTENT VALUES
# ==========================================================

NOT_APPLICABLE = "Not Applicable"


# ==========================================================
# COMMON DATASET COLUMNS
# ==========================================================

DATASET_COLUMNS = [

    # ------------------------------------------------------
    # Record identification
    # ------------------------------------------------------

    "record_id",
    "source_file",
    "record_type",
    "activity_type",

    # ------------------------------------------------------
    # User information
    # ------------------------------------------------------

    "user_uid",
    "user_name",
    "user_email",

    # ------------------------------------------------------
    # Time
    # ------------------------------------------------------

    "date",
    "created_at",
    "activity_hour",

    # ------------------------------------------------------
    # Academic information
    # ------------------------------------------------------

    "topic",

    # ------------------------------------------------------
    # Text information
    # ------------------------------------------------------

    "question",
    "answer",
    "instruction",
    "description",
    "sources",

    # ------------------------------------------------------
    # Quiz information
    # ------------------------------------------------------

    "difficulty",
    "score",
    "total_questions",
    "percentage",

    # ------------------------------------------------------
    # Image information
    # ------------------------------------------------------

    "image_name",

    # ------------------------------------------------------
    # YouTube information
    # ------------------------------------------------------

    "results_count",

    # ------------------------------------------------------
    # Chat information
    # ------------------------------------------------------

    "chat_title",
    "message_count",

    # ------------------------------------------------------
    # User account information
    # ------------------------------------------------------

    "email_verified",
    "disabled",

    # ------------------------------------------------------
    # Data-science derived features
    # ------------------------------------------------------

    "question_length",
    "answer_length",
    "instruction_length",
    "description_length",

    "has_question",
    "has_answer",
    "has_instruction",
    "has_source",

    # ------------------------------------------------------
    # Activity flags
    # ------------------------------------------------------

    "is_chat",
    "is_quiz",
    "is_image",
    "is_youtube",
    "is_saved_note",
    "is_user_record",

]


# ==========================================================
# SAFE JSON LOADER
# ==========================================================

def _load_json_file(
    file_path: Path
):
    """
    Safely read one JSON file.

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

            data = json.load(file)


    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


    # ------------------------------------------------------
    # Normal list
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
    # Single object
    # ------------------------------------------------------

    if isinstance(
        data,
        dict
    ):

        return [data]


    return []


# ==========================================================
# TEXT NORMALIZER
# ==========================================================

def _normalize_text(
    value
):
    """
    Convert missing or blank text values into
    a consistent text value.
    """

    if value is None:
        return NOT_APPLICABLE


    if isinstance(
        value,
        str
    ):

        value = value.strip()

        if not value:
            return NOT_APPLICABLE

        return value


    if isinstance(
        value,
        (list, dict, tuple)
    ):

        try:

            return json.dumps(
                value,
                ensure_ascii=False
            )

        except Exception:

            return str(value)


    return str(value)


# ==========================================================
# NUMERIC NORMALIZER
# ==========================================================

def _normalize_number(
    value,
    default=0
):
    """
    Convert a value into a numeric value.

    Missing or invalid values become the supplied
    default. For this dataset, 0 means the metric
    is not applicable or has no recorded value.
    """

    if value is None:
        return default


    if isinstance(
        value,
        str
    ):

        value = value.strip()

        if not value:
            return default


    try:

        number = float(
            value
        )

        if pd.isna(number):
            return default


        if number.is_integer():
            return int(number)


        return number


    except (
        ValueError,
        TypeError
    ):

        return default


# ==========================================================
# BOOLEAN NORMALIZER
# ==========================================================

def _normalize_boolean(
    value
):
    """
    Store boolean values consistently as 0 or 1.
    """

    if isinstance(
        value,
        bool
    ):

        return 1 if value else 0


    if isinstance(
        value,
        str
    ):

        value = value.strip().lower()

        if value in {
            "true",
            "yes",
            "1"
        }:

            return 1


        if value in {
            "false",
            "no",
            "0"
        }:

            return 0


    if value in (
        1,
        0
    ):

        return int(
            value
        )


    return 0


# ==========================================================
# DATE NORMALIZER
# ==========================================================

def _normalize_date(
    value
):
    """
    Return a usable date/time string.
    """

    if value is None:
        return NOT_APPLICABLE


    value = str(
        value
    ).strip()


    if not value:
        return NOT_APPLICABLE


    return value


# ==========================================================
# EXTRACT HOUR
# ==========================================================

def _extract_hour(
    value
):
    """
    Extract hour from common date formats.

    Returns 0 when time is not available.
    """

    if not value:
        return 0


    value = str(
        value
    ).strip()


    # ------------------------------------------------------
    # Format:
    # 2026-08-15 09:46:13 UTC
    # ------------------------------------------------------

    try:

        pieces = value.split()

        if len(pieces) >= 2:

            time_part = pieces[1]

            hour = int(
                time_part.split(":")[0]
            )

            return hour


    except (
        ValueError,
        IndexError
    ):

        pass


    # ------------------------------------------------------
    # Format:
    # 2026-08-15T09:46:13
    # ------------------------------------------------------

    try:

        if "T" in value:

            time_part = (
                value.split("T")[1]
            )

            hour = int(
                time_part.split(":")[0]
            )

            return hour


    except (
        ValueError,
        IndexError
    ):

        pass


    return 0


# ==========================================================
# RECORD ID
# ==========================================================

def _get_record_id(
    record,
    source_file,
    index
):
    """
    Find the best available unique ID.
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
# GET ACTIVITY TYPE
# ==========================================================

def _get_activity_type(
    record,
    source_file
):
    """
    Determine the real activity represented by a record.
    """

    source = (
        Path(
            source_file
        ).stem
    )


    # ------------------------------------------------------
    # Activity history
    # ------------------------------------------------------

    if source == "activity_history":

        activity_type = (
            record.get(
                "type"
            )
        )


        if activity_type:

            return str(
                activity_type
            ).strip().lower()


        return "activity"


    # ------------------------------------------------------
    # Other JSON sources
    # ------------------------------------------------------

    activity_map = {

        "chat_history":
            "chat",

        "quiz_history":
            "quiz",

        "image_study_history":
            "image",

        "youtube_history":
            "youtube",

        "favourites":
            "saved_note",

        "users":
            "user",

    }


    return activity_map.get(
        source,
        source
    )


# ==========================================================
# EXTRACT ACTIVITY METADATA
# ==========================================================

def _get_activity_metadata(
    record,
    source_file
):
    """
    Extract information stored inside activity_history.json
    metadata.
    """

    source = (
        Path(
            source_file
        ).stem
    )


    if source != "activity_history":

        return {}


    metadata = record.get(
        "metadata",
        {}
    )


    if isinstance(
        metadata,
        dict
    ):

        return metadata


    return {}


# ==========================================================
# CONVERT ONE RECORD
# ==========================================================

def _convert_record(
    record,
    source_file,
    index
):
    """
    Convert one JSON record into one consistent
    machine-learning-friendly row.
    """

    activity_type = (
        _get_activity_type(
            record,
            source_file
        )
    )


    activity_metadata = (
        _get_activity_metadata(
            record,
            source_file
        )
    )


    # ======================================================
    # USER INFORMATION
    # ======================================================

    user_uid = _normalize_text(
        record.get(
            "user_uid",
            record.get(
                "uid"
            )
        )
    )


    user_name = _normalize_text(
        record.get(
            "user_name",
            record.get(
                "name"
            )
        )
    )


    user_email = _normalize_text(
        record.get(
            "user_email",
            record.get(
                "email"
            )
        )
    )


    # ======================================================
    # DATE
    # ======================================================

    date_value = _normalize_date(
        record.get(
            "date",
            record.get(
                "created_at"
            )
        )
    )


    created_at_value = _normalize_date(
        record.get(
            "created_at",
            record.get(
                "date"
            )
        )
    )


    # ======================================================
    # ACADEMIC TEXT
    # ======================================================

    topic = _normalize_text(
        record.get(
            "topic"
        )
    )


    question = _normalize_text(
        record.get(
            "question"
        )
    )


    answer = _normalize_text(
        record.get(
            "answer"
        )
    )


    instruction = _normalize_text(
        record.get(
            "instruction"
        )
    )


    description = _normalize_text(
        record.get(
            "description"
        )
    )


    sources = _normalize_text(
        record.get(
            "sources"
        )
    )


    # ======================================================
    # CHAT HISTORY
    # ======================================================

    chat_title = _normalize_text(
        record.get(
            "title",
            record.get(
                "chat_title"
            )
        )
    )


    messages = record.get(
        "messages",
        []
    )


    if isinstance(
        messages,
        list
    ):

        message_count = len(
            messages
        )

    else:

        message_count = 0


    # ======================================================
    # QUIZ DATA
    # ======================================================

    difficulty = record.get(
        "difficulty"
    )


    score = record.get(
        "score"
    )


    total_questions = record.get(
        "total_questions"
    )


    percentage = record.get(
        "percentage"
    )


    # ------------------------------------------------------
    # Extract quiz values from activity metadata
    # ------------------------------------------------------

    if activity_type == "quiz":

        if difficulty in (
            None,
            ""
        ):

            difficulty = (
                activity_metadata.get(
                    "difficulty"
                )
            )


        if score in (
            None,
            ""
        ):

            score = (
                activity_metadata.get(
                    "score"
                )
            )


        if total_questions in (
            None,
            ""
        ):

            total_questions = (
                activity_metadata.get(
                    "total_questions"
                )
            )


        if percentage in (
            None,
            ""
        ):

            percentage = (
                activity_metadata.get(
                    "percentage"
                )
            )


    difficulty = _normalize_text(
        difficulty
    )


    score = _normalize_number(
        score
    )


    total_questions = _normalize_number(
        total_questions
    )


    percentage = _normalize_number(
        percentage
    )


    # ======================================================
    # IMAGE DATA
    # ======================================================

    image_name = record.get(
        "image_name"
    )


    if (
        image_name in (
            None,
            ""
        )
        and activity_type == "image"
    ):

        image_name = (
            activity_metadata.get(
                "image_name"
            )
        )


    image_name = _normalize_text(
        image_name
    )


    # ======================================================
    # YOUTUBE DATA
    # ======================================================

    results_count = record.get(
        "results_count"
    )


    if (
        results_count in (
            None,
            ""
        )
        and activity_type == "youtube"
    ):

        results_count = (
            activity_metadata.get(
                "results_count"
            )
        )


    results_count = _normalize_number(
        results_count
    )


    # ======================================================
    # USER ACCOUNT DATA
    # ======================================================

    email_verified = _normalize_boolean(
        record.get(
            "email_verified"
        )
    )


    disabled = _normalize_boolean(
        record.get(
            "disabled"
        )
    )


    # ======================================================
    # DERIVED TEXT FEATURES
    # ======================================================

    question_length = (
        0
        if question == NOT_APPLICABLE
        else len(
            question
        )
    )


    answer_length = (
        0
        if answer == NOT_APPLICABLE
        else len(
            answer
        )
    )


    instruction_length = (
        0
        if instruction == NOT_APPLICABLE
        else len(
            instruction
        )
    )


    description_length = (
        0
        if description == NOT_APPLICABLE
        else len(
            description
        )
    )


    # ======================================================
    # SOURCE FLAGS
    # ======================================================

    has_question = (
        1
        if question != NOT_APPLICABLE
        else 0
    )


    has_answer = (
        1
        if answer != NOT_APPLICABLE
        else 0
    )


    has_instruction = (
        1
        if instruction != NOT_APPLICABLE
        else 0
    )


    has_source = (
        1
        if sources != NOT_APPLICABLE
        else 0
    )


    # ======================================================
    # ACTIVITY FLAGS
    # ======================================================

    is_chat = (
        1
        if activity_type == "chat"
        else 0
    )


    is_quiz = (
        1
        if activity_type == "quiz"
        else 0
    )


    is_image = (
        1
        if activity_type == "image"
        else 0
    )


    is_youtube = (
        1
        if activity_type == "youtube"
        else 0
    )


    is_saved_note = (
        1
        if activity_type == "saved_note"
        else 0
    )


    is_user_record = (
        1
        if activity_type == "user"
        else 0
    )


    # ======================================================
    # CREATE ROW
    # ======================================================

    row = {

        "record_id": _get_record_id(
            record,
            source_file,
            index
        ),

        "source_file":
            source_file,

        "record_type":
            Path(
                source_file
            ).stem,

        "activity_type":
            activity_type,

        "user_uid":
            user_uid,

        "user_name":
            user_name,

        "user_email":
            user_email,

        "date":
            date_value,

        "created_at":
            created_at_value,

        "topic":
            topic,

        "question":
            question,

        "answer":
            answer,

        "difficulty":
            difficulty,

        "score":
            score,

        "total_questions":
            total_questions,

        "percentage":
            percentage,

        "image_name":
            image_name,

        "instruction":
            instruction,

        "results_count":
            results_count,

        "chat_title":
            chat_title,

        "message_count":
            message_count,

        "description":
            description,

        "sources":
            sources,

        "email_verified":
            email_verified,

        "disabled":
            disabled,

        "question_length":
            question_length,

        "answer_length":
            answer_length,

        "instruction_length":
            instruction_length,

        "description_length":
            description_length,

        "has_question":
            has_question,

        "has_answer":
            has_answer,

        "has_instruction":
            has_instruction,

        "has_source":
            has_source,

        "is_chat":
            is_chat,

        "is_quiz":
            is_quiz,

        "is_image":
            is_image,

        "is_youtube":
            is_youtube,

        "is_saved_note":
            is_saved_note,

        "is_user_record":
            is_user_record,

        "activity_hour":
            _extract_hour(
                date_value
            ),
    }


    return row


# ==========================================================
# REMOVE DUPLICATE ACTIVITY-HISTORY RECORDS
# ==========================================================

def _remove_duplicate_activity_records(
    dataframe
):
    """
    Remove duplicate summary records created because
    detailed history and activity_history.json both
    contain the same event.

    Detailed sources are preferred:

        quiz_history.json
        image_study_history.json
        youtube_history.json

    activity_history.json is retained for:
        chat
        saved_note
        user
        other activities
    """

    if dataframe.empty:
        return dataframe


    detailed_types = {
        "quiz",
        "image",
        "youtube",
    }


    detailed_source_files = {
        "quiz_history.json",
        "image_study_history.json",
        "youtube_history.json",
    }


    # ------------------------------------------------------
    # Separate detailed records
    # ------------------------------------------------------

    detailed = dataframe[
        dataframe["source_file"].isin(
            detailed_source_files
        )
    ].copy()


    # ------------------------------------------------------
    # Activity-history records
    # ------------------------------------------------------

    activity_history = dataframe[
        dataframe["source_file"]
        ==
        "activity_history.json"
    ].copy()


    # ------------------------------------------------------
    # Keep activity history only for activities without
    # detailed duplicate sources.
    # ------------------------------------------------------

    if not activity_history.empty:

        activity_history = activity_history[
            ~activity_history[
                "activity_type"
            ].isin(
                detailed_types
            )
        ].copy()


    # ------------------------------------------------------
    # Other sources
    # ------------------------------------------------------

    other_sources = dataframe[
        ~dataframe["source_file"].isin(
            detailed_source_files
            |
            {
                "activity_history.json"
            }
        )
    ].copy()


    # ------------------------------------------------------
    # Combine without duplicate summary records
    # ------------------------------------------------------

    cleaned = pd.concat(
        [
            other_sources,
            detailed,
            activity_history
        ],
        ignore_index=True
    )


    return cleaned


# ==========================================================
# LOAD COMPLETE DATASET
# ==========================================================

def load_combined_dataset(
    user_uid=None
):
    """
    Read all seven JSON files and create one
    clean, consistent dataset.

    user_uid is optional.

    When user_uid is None:
        all users are returned.

    When user_uid is supplied:
        only that user is returned.
    """

    all_rows = []


    # ======================================================
    # READ ALL JSON FILES
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

            if not isinstance(
                record,
                dict
            ):

                continue


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
        all_rows
    )


    # ======================================================
    # ENSURE ALL COLUMNS EXIST
    # ======================================================

    for column in DATASET_COLUMNS:

        if column not in dataframe.columns:

            if column in {
                "score",
                "total_questions",
                "percentage",
                "results_count",
                "message_count",
                "question_length",
                "answer_length",
                "instruction_length",
                "description_length",
                "activity_hour",
                "has_question",
                "has_answer",
                "has_instruction",
                "has_source",
                "is_chat",
                "is_quiz",
                "is_image",
                "is_youtube",
                "is_saved_note",
                "is_user_record",
            }:

                dataframe[column] = 0

            else:

                dataframe[column] = (
                    NOT_APPLICABLE
                )


    # ======================================================
    # COLUMN ORDER
    # ======================================================

    dataframe = dataframe[
        DATASET_COLUMNS
    ]


    # ======================================================
    # REMOVE DUPLICATE SUMMARY EVENTS
    # ======================================================

    dataframe = (
        _remove_duplicate_activity_records(
            dataframe
        )
    )


    # ======================================================
    # FILTER USER WHEN REQUESTED
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
    # CLEAN TEXT COLUMNS AGAIN
    # ======================================================

    text_columns = [

        "record_id",
        "source_file",
        "record_type",
        "activity_type",
        "user_uid",
        "user_name",
        "user_email",
        "date",
        "created_at",
        "topic",
        "question",
        "answer",
        "difficulty",
        "image_name",
        "instruction",
        "chat_title",
        "description",
        "sources",

    ]


    for column in text_columns:

        dataframe[column] = (
            dataframe[column]
            .apply(
                _normalize_text
            )
        )


    # ======================================================
    # NUMERIC COLUMNS
    # ======================================================

    numeric_columns = [

        "score",
        "total_questions",
        "percentage",
        "results_count",
        "message_count",
        "question_length",
        "answer_length",
        "instruction_length",
        "description_length",
        "activity_hour",

        "has_question",
        "has_answer",
        "has_instruction",
        "has_source",

        "is_chat",
        "is_quiz",
        "is_image",
        "is_youtube",
        "is_saved_note",
        "is_user_record",

        "email_verified",
        "disabled",

    ]


    for column in numeric_columns:

        dataframe[column] = (
            pd.to_numeric(
                dataframe[column],
                errors="coerce"
            )
            .fillna(0)
        )


    # ======================================================
    # SORT BY DATE
    # ======================================================

    if not dataframe.empty:

        dataframe["_sort_date"] = (
            pd.to_datetime(
                dataframe[
                    "date"
                ],
                errors="coerce",
                utc=True
            )
        )


        dataframe = (
            dataframe
            .sort_values(
                by="_sort_date",
                ascending=True,
                na_position="last"
            )
            .drop(
                columns="_sort_date"
            )
            .reset_index(
                drop=True
            )
        )


    # ======================================================
    # FINAL SAFETY CHECK
    # ======================================================

    for column in dataframe.columns:

        if column in numeric_columns:

            dataframe[column] = (
                dataframe[column]
                .fillna(0)
            )

        else:

            dataframe[column] = (
                dataframe[column]
                .replace(
                    "",
                    NOT_APPLICABLE
                )
                .fillna(
                    NOT_APPLICABLE
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

    if dataframe is None:

        dataframe = pd.DataFrame(
            columns=DATASET_COLUMNS
        )


    summary = {

        "total_records":
            len(dataframe),

        "total_users":
            dataframe[
                "user_uid"
            ]
            .replace(
                NOT_APPLICABLE,
                pd.NA
            )
            .nunique(),

        "total_questions":
            (
                dataframe[
                    "activity_type"
                ]
                == "chat"
            ).sum(),

        "total_quizzes":
            (
                dataframe[
                    "activity_type"
                ]
                == "quiz"
            ).sum(),

        "total_images":
            (
                dataframe[
                    "activity_type"
                ]
                == "image"
            ).sum(),

        "total_youtube_searches":
            (
                dataframe[
                    "activity_type"
                ]
                == "youtube"
            ).sum(),

        "total_saved_notes":
            (
                dataframe[
                    "activity_type"
                ]
                == "saved_note"
            ).sum(),
    }


    quiz_percentages = pd.to_numeric(
        dataframe.loc[
            dataframe[
                "activity_type"
            ]
            ==
            "quiz",
            "percentage"
        ],
        errors="coerce"
    )


    quiz_percentages = (
        quiz_percentages[
            quiz_percentages > 0
        ]
    )


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


    return summary


# ==========================================================
# TOP TOPICS
# ==========================================================

def get_top_topics(
    dataframe,
    limit=10
):

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
                NOT_APPLICABLE,
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

    if dataframe is None:

        return pd.DataFrame(
            columns=[
                "activity_type",
                "count"
            ]
        )


    result = (
        dataframe[
            "activity_type"
        ]
        .value_counts()
        .reset_index()
    )


    result.columns = [
        "activity_type",
        "count"
    ]


    return result


# ==========================================================
# QUIZ PERFORMANCE
# ==========================================================

def get_quiz_performance(
    dataframe
):

    if dataframe is None:

        return pd.DataFrame()


    quiz_data = (
        dataframe[
            dataframe[
                "activity_type"
            ]
            ==
            "quiz"
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
    ).fillna(0)


    quiz_data[
        "total_questions"
    ] = pd.to_numeric(
        quiz_data[
            "total_questions"
        ],
        errors="coerce"
    ).fillna(0)


    quiz_data[
        "percentage"
    ] = pd.to_numeric(
        quiz_data[
            "percentage"
        ],
        errors="coerce"
    ).fillna(0)


    return quiz_data


# ==========================================================
# DAILY ACTIVITY
# ==========================================================

def get_daily_activity(
    dataframe
):

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
        dataframe[
            "date"
        ],
        errors="coerce",
        utc=True
    )


    valid_dates = (
        dates.dropna()
    )


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
        get_all_data()
    )


    print(
        "\n========================================"
    )

    print(
        "Academic Notes AI - ML Dataset"
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
        "\nUsers:"
    )


    users = (
        dataframe[
            [
                "user_uid",
                "user_name",
                "user_email"
            ]
        ]
        .drop_duplicates()
    )


    print(
        users.to_string(
            index=False
        )
    )


    print(
        "\nActivity distribution:"
    )


    print(
        dataframe[
            "activity_type"
        ]
        .value_counts()
        .to_string()
    )


    print(
        "\nMissing values:"
    )


    missing_values = (
        dataframe.isna().sum()
    )


    print(
        missing_values.to_string()
    )


    print(
        "\n========================================"
    )

    print(
        "Dataset loaded successfully."
    )

    print(
        "No blank/NaN values should remain."
    )

    print(
        "========================================"
    )