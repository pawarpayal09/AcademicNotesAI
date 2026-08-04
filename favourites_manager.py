import json
import os
import uuid
from datetime import datetime

FAV_FILE = "storage/favourites.json"


def create_favourite_file():

    os.makedirs("storage", exist_ok=True)

    if not os.path.exists(FAV_FILE):

        with open(FAV_FILE, "w", encoding="utf-8") as f:

            json.dump([], f)


create_favourite_file()


# ==========================================
# Load Favourite Notes
# ==========================================

def load_favourites():

    # Create file if missing
    if not os.path.exists(FAV_FILE):

        with open(FAV_FILE, "w", encoding="utf-8") as f:

            json.dump([], f)

    # If file is empty
    if os.path.getsize(FAV_FILE) == 0:

        with open(FAV_FILE, "w", encoding="utf-8") as f:

            json.dump([], f)

    with open(FAV_FILE, "r", encoding="utf-8") as f:

        return json.load(f)


# ==========================================
# Save Favourite
# ==========================================

def add_favourite(question, answer, sources):

    favourites = load_favourites()

    favourites.append({

        "id": str(uuid.uuid4()),

        "question": question,

        "answer": answer,

        "sources": sources,

        "date": datetime.now().strftime("%Y-%m-%d %H:%M")

    })

    with open(FAV_FILE, "w", encoding="utf-8") as f:

        json.dump(
            favourites,
            f,
            indent=4,
            ensure_ascii=False
        )


# ==========================================
# Delete Favourite
# ==========================================

def remove_favourite(fav_id):

    favourites = load_favourites()

    favourites = [

        fav

        for fav in favourites

        if fav["id"] != fav_id

    ]

    with open(FAV_FILE, "w", encoding="utf-8") as f:

        json.dump(
            favourites,
            f,
            indent=4,
            ensure_ascii=False
        )