import os

import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from google import genai
from google.genai import types


# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()


# ==========================================================
# QUIZ DATA MODELS
# ==========================================================

class QuizQuestion(BaseModel):

    question: str = Field(
        description="The multiple-choice question."
    )

    options: list[str] = Field(
        description="Exactly four answer options."
    )

    correct_answer: str = Field(
        description="The exact correct option text."
    )

    explanation: str = Field(
        description="A short explanation of why the answer is correct."
    )


class QuizResponse(BaseModel):

    topic: str = Field(
        description="The quiz topic."
    )

    questions: list[QuizQuestion] = Field(
        description="The generated quiz questions."
    )


# ==========================================================
# GET GEMINI API KEY
# ==========================================================

def get_quiz_api_key():

    # ------------------------------------------------------
    # Streamlit Cloud
    # ------------------------------------------------------

    try:

        api_key = st.secrets.get(
            "MAIN_CHAT_API_KEY_5"
        )

    except Exception:

        api_key = None


    # ------------------------------------------------------
    # Local .env
    # ------------------------------------------------------

    if not api_key:

        api_key = os.getenv(
            "MAIN_CHAT_API_KEY_5"
        )


    # ------------------------------------------------------
    # Clean API key
    # ------------------------------------------------------

    if api_key:

        api_key = api_key.strip()


    return api_key


# ==========================================================
# GENERATE QUIZ
# ==========================================================

def generate_quiz(
    topic,
    number_of_questions=5,
    difficulty="Medium"
):

    # ------------------------------------------------------
    # Validate topic
    # ------------------------------------------------------

    topic = topic.strip()

    if not topic:

        return {
            "success": False,
            "error": "Please enter a topic.",
            "quiz": None
        }


    # ------------------------------------------------------
    # API key
    # ------------------------------------------------------

    api_key = get_quiz_api_key()

    if not api_key:

        return {
            "success": False,
            "error": (
                "MAIN_CHAT_API_KEY_5 is not configured."
            ),
            "quiz": None
        }


    # ------------------------------------------------------
    # Safe question count
    # ------------------------------------------------------

    number_of_questions = max(
        3,
        min(
            int(number_of_questions),
            15
        )
    )


    # ------------------------------------------------------
    # Validate difficulty
    # ------------------------------------------------------

    allowed_difficulties = [
        "Easy",
        "Medium",
        "Hard"
    ]

    if difficulty not in allowed_difficulties:

        difficulty = "Medium"


    try:

        # ==================================================
        # GEMINI CLIENT
        # ==================================================

        client = genai.Client(
            api_key=api_key
        )


        # ==================================================
        # QUIZ PROMPT
        # ==================================================

        prompt = f"""
Create a high-quality academic multiple-choice quiz.

Topic:
{topic}

Number of questions:
{number_of_questions}

Difficulty:
{difficulty}

IMPORTANT RULES:

1. Questions must be directly related to the given topic.
2. Target college/MCA students.
3. Questions must test actual understanding.
4. Create exactly four options for every question.
5. Only one option must be correct.
6. The correct_answer must exactly match one of the four options.
7. Do not create duplicate questions.
8. Avoid ambiguous questions.
9. Keep questions concise and clear.
10. Provide a short explanation for every answer.
11. Do not use information unrelated to the requested topic.
12. Do not include question numbers inside the question text.
13. Return exactly {number_of_questions} questions.
"""


        # ==================================================
        # STRUCTURED GEMINI RESPONSE
        # ==================================================

        response = client.models.generate_content(

            model="gemini-3.6-flash",

            contents=prompt,

            config=types.GenerateContentConfig(

                response_mime_type="application/json",

                response_schema=QuizResponse,

                max_output_tokens=6000
            )
        )


        # ==================================================
        # CHECK RESPONSE
        # ==================================================

        if not response or not response.text:

            return {
                "success": False,
                "error": (
                    "Gemini returned an empty quiz response."
                ),
                "quiz": None
            }


        # ==================================================
        # PARSE STRUCTURED RESPONSE
        # ==================================================

        quiz = QuizResponse.model_validate_json(
            response.text
        )


        # ==================================================
        # VALIDATE QUESTIONS
        # ==================================================

        if len(quiz.questions) == 0:

            return {
                "success": False,
                "error": (
                    "No quiz questions were generated."
                ),
                "quiz": None
            }


        valid_questions = []


        for question in quiz.questions:

            # Must have exactly 4 options
            if len(question.options) != 4:
                continue

            # Correct answer must exist in options
            if question.correct_answer not in question.options:
                continue

            valid_questions.append(
                question
            )


        # --------------------------------------------------
        # Final validation
        # --------------------------------------------------

        if not valid_questions:

            return {
                "success": False,
                "error": (
                    "Gemini generated an invalid quiz format."
                ),
                "quiz": None
            }


        quiz.questions = valid_questions[
            :number_of_questions
        ]


        return {
            "success": True,
            "error": None,
            "quiz": quiz.model_dump()
        }


    except Exception as e:

        print(
            "Quiz Generator Error:",
            type(e).__name__,
            str(e)
        )

        return {
            "success": False,
            "error": (
                "Unable to generate the quiz.\n\n"
                f"{type(e).__name__}: {str(e)}"
            ),
            "quiz": None
        }