import json
import csv
from pathlib import Path
from datetime import datetime


# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

STORAGE_DIR = PROJECT_ROOT / "storage"

OUTPUT_FILE = STORAGE_DIR / "combined_student_data.csv"


# ==========================================================
# JSON FILES TO COMBINE
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
# COMMON CSV COLUMNS
# ==========================================================

COMMON_COLUMNS = [
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

    "metadata_json",
]


# ==========================================================
# SAFE JSON READ
# ==========================================================

def load_json_file(file_path):
    """
    Read one JSON file.

    Returns:
        list of records
    """

    if not file_path.exists():

        print(
            f"⚠️ File not found: {file_path.name}"
        )

        return []


    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)


        if isinstance(data, list):

            return data


        # If the JSON contains one dictionary,
        # convert it into a one-record list.

        if isinstance(data, dict):

            return [data]


        print(
            f"⚠️ Unsupported JSON format: "
            f"{file_path.name}"
        )

        return []


    except json.JSONDecodeError as e:

        print(
            f"❌ Invalid JSON in "
            f"{file_path.name}: {e}"
        )

        return []


    except OSError as e:

        print(
            f"❌ Could not read "
            f"{file_path.name}: {e}"
        )

        return []


# ==========================================================
# VALUE CLEANER
# ==========================================================

def clean_value(value):
    """
    Convert dictionaries/lists into JSON strings
    so they can safely be stored inside one CSV cell.
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
# GENERATE RECORD ID
# ==========================================================

def get_record_id(record, source_file, index):

    possible_ids = [
        "id",
        "uid",
        "quiz_id",
        "activity_id",
        "search_id",
        "chat_id",
        "record_id",
    ]


    for key in possible_ids:

        value = record.get(key)

        if value not in (
            None,
            ""
        ):

            return str(value)


    return (
        f"{Path(source_file).stem}_"
        f"{index + 1}"
    )


# ==========================================================
# EXTRACT COMMON DATA
# ==========================================================

def convert_record(
    record,
    source_file,
    index
):
    """
    Convert one JSON record into one CSV row.
    """

    row = {}

    # ------------------------------------------------------
    # BASIC INFORMATION
    # ------------------------------------------------------

    row["record_id"] = get_record_id(
        record,
        source_file,
        index
    )

    row["source_file"] = source_file

    row["record_type"] = Path(
        source_file
    ).stem


    # ------------------------------------------------------
    # USER INFORMATION
    # ------------------------------------------------------

    row["user_uid"] = record.get(
        "user_uid",
        record.get(
            "uid",
            ""
        )
    )

    row["user_name"] = record.get(
        "user_name",
        record.get(
            "name",
            ""
        )
    )

    row["user_email"] = record.get(
        "user_email",
        record.get(
            "email",
            ""
        )
    )


    # ------------------------------------------------------
    # TIME
    # ------------------------------------------------------

    row["date"] = record.get(
        "date",
        ""
    )

    row["created_at"] = clean_value(
        record.get(
            "created_at",
            ""
        )
    )


    # ------------------------------------------------------
    # ACADEMIC CONTENT
    # ------------------------------------------------------

    row["topic"] = record.get(
        "topic",
        ""
    )

    row["question"] = record.get(
        "question",
        ""
    )

    row["answer"] = record.get(
        "answer",
        ""
    )


    # ------------------------------------------------------
    # QUIZ
    # ------------------------------------------------------

    row["difficulty"] = record.get(
        "difficulty",
        ""
    )

    row["score"] = record.get(
        "score",
        ""
    )

    row["total_questions"] = record.get(
        "total_questions",
        ""
    )

    row["percentage"] = record.get(
        "percentage",
        ""
    )


    # ------------------------------------------------------
    # IMAGE STUDY
    # ------------------------------------------------------

    row["image_name"] = record.get(
        "image_name",
        ""
    )

    row["instruction"] = record.get(
        "instruction",
        ""
    )


    # ------------------------------------------------------
    # YOUTUBE
    # ------------------------------------------------------

    row["results_count"] = record.get(
        "results_count",
        ""
    )


    # ------------------------------------------------------
    # CHAT HISTORY
    # ------------------------------------------------------

    row["chat_title"] = record.get(
        "title",
        record.get(
            "chat_title",
            ""
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

        row["message_count"] = len(
            messages
        )

    else:

        row["message_count"] = ""


    # ------------------------------------------------------
    # ACTIVITY
    # ------------------------------------------------------

    row["description"] = record.get(
        "description",
        ""
    )


    # ------------------------------------------------------
    # SOURCES
    # ------------------------------------------------------

    row["sources"] = clean_value(
        record.get(
            "sources",
            ""
        )
    )


    # ------------------------------------------------------
    # USER ACCOUNT FIELDS
    # ------------------------------------------------------

    row["email_verified"] = record.get(
        "email_verified",
        ""
    )

    row["disabled"] = record.get(
        "disabled",
        ""
    )


    # ------------------------------------------------------
    # NESTED / EXTRA DATA
    # ------------------------------------------------------

    known_keys = {
        "id",
        "uid",
        "quiz_id",
        "activity_id",
        "search_id",
        "chat_id",
        "record_id",
        "user_uid",
        "user_name",
        "user_email",
        "name",
        "email",
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
        "title",
        "chat_title",
        "messages",
        "description",
        "sources",
        "email_verified",
        "disabled",
    }


    extra_data = {
        key: value
        for key, value in record.items()
        if key not in known_keys
    }


    row["metadata_json"] = (
        json.dumps(
            extra_data,
            ensure_ascii=False
        )
        if extra_data
        else ""
    )


    # ------------------------------------------------------
    # STORE CHAT MESSAGES WITHOUT LOSING THEM
    # ------------------------------------------------------

    if messages:

        row["metadata_json"] = json.dumps(
            {
                "messages": messages,
                **extra_data,
            },
            ensure_ascii=False
        )


    return row


# ==========================================================
# COMBINE ALL JSON FILES
# ==========================================================

def combine_json_to_csv():
    """
    Read all project JSON files and create one CSV file.

    The CSV is completely regenerated every time the
    function runs, so newly added JSON records are included.
    """

    STORAGE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    all_rows = []


    print(
        "\n========================================"
    )

    print(
        " Academic Notes AI - JSON → CSV"
    )

    print(
        "========================================\n"
    )


    for json_name in JSON_FILES:

        json_path = STORAGE_DIR / json_name


        print(
            f"📂 Reading: {json_name}"
        )


        records = load_json_file(
            json_path
        )


        print(
            f"   Records found: {len(records)}"
        )


        for index, record in enumerate(
            records
        ):

            if not isinstance(
                record,
                dict
            ):

                print(
                    f"⚠️ Skipping invalid "
                    f"record {index + 1} "
                    f"in {json_name}"
                )

                continue


            row = convert_record(
                record,
                json_name,
                index
            )


            all_rows.append(
                row
            )


    # ======================================================
    # WRITE CSV
    # ======================================================

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=COMMON_COLUMNS,
            extrasaction="ignore"
        )


        writer.writeheader()


        writer.writerows(
            all_rows
        )


    print(
        "\n========================================"
    )

    print(
        "✅ CSV CREATED SUCCESSFULLY"
    )

    print(
        "========================================"
    )


    print(
        f"📄 File: {OUTPUT_FILE}"
    )

    print(
        f"📊 Total records: {len(all_rows)}"
    )

    print(
        f"📋 Total columns: {len(COMMON_COLUMNS)}"
    )


    print(
        "========================================\n"
    )


    return OUTPUT_FILE


# ==========================================================
# RUN SCRIPT
# ==========================================================

if __name__ == "__main__":

    combine_json_to_csv()