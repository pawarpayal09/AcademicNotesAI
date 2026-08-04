import json
import os
import uuid
from datetime import datetime

# ==========================================
# Chat History File
# ==========================================

CHAT_FILE = "storage/chat_history.json"


# ==========================================
# Create File Automatically
# ==========================================

def initialize_chat_history():

    if not os.path.exists("storage"):
        os.makedirs("storage")

    if not os.path.exists(CHAT_FILE):

        with open(CHAT_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)


# ==========================================
# Load Chats
# ==========================================

def load_chat_history():

    initialize_chat_history()

    with open(CHAT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ==========================================
# Save Chats
# ==========================================

def save_chat_history(history):

    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)


# ==========================================
# Add New Chat
# ==========================================

def add_chat(title, messages):

    history = load_chat_history()

    history.append(
        {
            "id": str(uuid.uuid4()),
            "title": title,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "messages": messages
        }
    )

    save_chat_history(history)


# ==========================================
# Update Existing Chat
# ==========================================

def update_chat(chat_id, messages):

    history = load_chat_history()

    for chat in history:

        if chat["id"] == chat_id:

            chat["messages"] = messages
            break

    save_chat_history(history)


# ==========================================
# Delete Chat
# ==========================================

def delete_chat(chat_id):

    history = load_chat_history()

    history = [
        chat
        for chat in history
        if chat["id"] != chat_id
    ]

    save_chat_history(history)