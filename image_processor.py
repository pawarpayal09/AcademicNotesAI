import os
import streamlit as st
from dotenv import load_dotenv


# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()


# ==========================================================
# GET IMAGE STUDY API KEY
# ==========================================================

def get_image_study_api_key():

    try:
        api_key = st.secrets.get(
            "IMAGE_STUDY_API_KEY_4"
        )
    except Exception:
        api_key = None

    if not api_key:
        api_key = os.getenv(
            "IMAGE_STUDY_API_KEY_4"
        )

    if api_key:
        api_key = api_key.strip()

    return api_key


# ==========================================================
# ANALYZE STUDY IMAGE
# ==========================================================

def analyze_study_image(
    image_bytes,
    mime_type,
    instruction
):

    # ------------------------------------------------------
    # Get API key
    # ------------------------------------------------------

    api_key = get_image_study_api_key()

    if not api_key:
        return (
            "❌ Image Study API key not found.\n\n"
            "Please check IMAGE_STUDY_API_KEY_4 "
            "in your .env file."
        )

    # ------------------------------------------------------
    # Validate image
    # ------------------------------------------------------

    if not image_bytes:
        return "❌ The uploaded image is empty."

    if not mime_type:
        return "❌ The image MIME type could not be detected."

    if not mime_type.startswith("image/"):
        return f"❌ Unsupported image type: {mime_type}"

    try:

        # --------------------------------------------------
        # Import Gemini only when Analyze is clicked
        # --------------------------------------------------

        from google import genai
        from google.genai import types

        # --------------------------------------------------
        # Create Gemini client
        # --------------------------------------------------

        client = genai.Client(
            api_key=api_key
        )

        # --------------------------------------------------
        # Create image part
        # --------------------------------------------------

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        )

        # --------------------------------------------------
        # Study instruction
        # --------------------------------------------------

        prompt = f"""
You are an AI Study Assistant for college students.

Carefully examine the uploaded image.

The image may contain:
- academic notes
- textbook content
- handwritten notes
- questions
- diagrams
- tables
- charts
- mathematical problems
- programming code
- technical concepts
- exam questions

User request:
{instruction}

Rules:

1. Understand the visible content before answering.
2. Answer the user's request directly.
3. Use simple student-friendly language.
4. Keep the answer concise but complete.
5. If the image contains a question, solve or explain it.
6. If the image contains notes, summarize the important concepts.
7. If the image contains a diagram, explain its important components.
8. If the image contains a chart or table, explain the important information.
9. Do not invent information that cannot be identified from the image.
10. If something is unreadable, clearly mention it.
11. Use headings and bullet points when helpful.

Give only the final academic answer.
"""

        # --------------------------------------------------
        # Gemini multimodal request
        # --------------------------------------------------

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                prompt,
                image_part
            ]
        )

        # --------------------------------------------------
        # Extract answer
        # --------------------------------------------------

        if response and response.text:
            return response.text.strip()

        return "❌ Gemini returned no text for this image."

    except Exception as e:

        # IMPORTANT:
        # Show the real error instead of hiding it.

        error_type = type(e).__name__
        error_message = str(e)

        print("\n========== IMAGE STUDY ERROR ==========")
        print("Error Type:", error_type)
        print("Error:", error_message)
        print("=======================================\n")

        return (
            f"❌ Image analysis failed.\n\n"
            f"**Error Type:** `{error_type}`\n\n"
            f"**Details:** `{error_message}`"
        )