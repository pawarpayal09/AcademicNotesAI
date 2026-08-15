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
        description="A clear academic multiple-choice question."
    )

    options: list[str] = Field(
        description="Exactly four concise answer options."
    )

    correct_answer: str = Field(
        description="The exact text of the correct option."
    )

    explanation: str = Field(
        description="A short explanation of why the answer is correct."
    )


class QuizResponse(BaseModel):

    topic: str = Field(
        description="The requested quiz topic."
    )

    questions: list[QuizQuestion] = Field(
        description="The generated multiple-choice questions."
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
            "MAIN_CHAT_API_KEY_1"
        )

    except Exception:

        api_key = None


    # ------------------------------------------------------
    # Local .env
    # ------------------------------------------------------

    if not api_key:

        api_key = os.getenv(
            "MAIN_CHAT_API_KEY_1"
        )


    # ------------------------------------------------------
    # Clean key
    # ------------------------------------------------------

    if api_key:

        api_key = api_key.strip()


    return api_key


# ==========================================================
# DIFFICULTY INSTRUCTIONS
# ==========================================================

def get_difficulty_instruction(difficulty):

    if difficulty == "Easy":

        return """
Difficulty requirements:

- Ask basic definition and recognition questions.
- Test fundamental concepts.
- Use direct and simple wording.
- Do not require calculations unless very simple.
- Options should be clearly distinguishable.
"""

    if difficulty == "Medium":

        return """
Difficulty requirements:

- Test understanding, not only memorization.
- Ask conceptual application questions.
- Include comparisons, relationships, or simple scenarios.
- Make distractors plausible but clearly incorrect.
- Avoid overly advanced calculations.
- Keep the questions suitable for MCA/college students.
"""

    return """
Difficulty requirements:

- Test deeper conceptual understanding.
- Use application-based or scenario-based questions.
- Ask students to analyze, compare, infer, or choose the best solution.
- Distractors should be plausible and require careful thinking.
- Avoid ambiguous wording.
- Do not make questions unnecessarily long.
- Keep the questions suitable for MCA/college-level study.
"""


# ==========================================================
# VALIDATE GENERATED QUESTIONS
# ==========================================================

def validate_questions(
    questions,
    requested_count
):

    valid_questions = []

    seen_questions = set()


    for question in questions:

        # --------------------------------------------------
        # Clean values
        # --------------------------------------------------

        question.question = question.question.strip()

        question.correct_answer = (
            question.correct_answer.strip()
        )

        question.explanation = (
            question.explanation.strip()
        )

        question.options = [
            option.strip()
            for option in question.options
        ]


        # --------------------------------------------------
        # Exactly four options
        # --------------------------------------------------

        if len(question.options) != 4:
            continue


        # --------------------------------------------------
        # Remove empty options
        # --------------------------------------------------

        if any(
            not option
            for option in question.options
        ):
            continue


        # --------------------------------------------------
        # Correct answer must exist
        # --------------------------------------------------

        if (
            question.correct_answer
            not in question.options
        ):
            continue


        # --------------------------------------------------
        # Avoid duplicate questions
        # --------------------------------------------------

        normalized_question = (
            question.question.lower()
            .strip()
        )

        if normalized_question in seen_questions:
            continue

        seen_questions.add(
            normalized_question
        )

        valid_questions.append(
            question
        )


        if len(valid_questions) >= requested_count:
            break


    return valid_questions


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

    topic = str(topic).strip()


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
                "MAIN_CHAT_API_KEY_1 is not configured."
            ),
            "quiz": None
        }


    # ------------------------------------------------------
    # Safe question count
    # ------------------------------------------------------

    try:

        number_of_questions = int(
            number_of_questions
        )

    except (TypeError, ValueError):

        number_of_questions = 5


    number_of_questions = max(
        3,
        min(
            number_of_questions,
            15
        )
    )


    # ------------------------------------------------------
    # Validate difficulty
    # ------------------------------------------------------

    allowed_difficulties = {
        "Easy",
        "Medium",
        "Hard"
    }


    if difficulty not in allowed_difficulties:

        difficulty = "Medium"


    difficulty_instruction = (
        get_difficulty_instruction(
            difficulty
        )
    )


    try:

        # ==================================================
        # GEMINI CLIENT
        # ==================================================

        client = genai.Client(
            api_key=api_key
        )


        # ==================================================
        # PROMPT
        # ==================================================

        prompt = f"""
Create an academic multiple-choice quiz.

TOPIC:
{topic}

QUESTION COUNT:
{number_of_questions}

DIFFICULTY:
{difficulty}

{difficulty_instruction}

GENERAL RULES:

1. Create exactly four options per question.
2. Only one option can be correct.
3. The correct_answer must exactly match one option.
4. Do not repeat questions.
5. Do not create trick questions.
6. Do not use ambiguous wording.
7. Questions must stay focused on the requested topic.
8. Use concise wording.
9. Keep each explanation short and useful.
10. Do not include question numbers in the question field.
11. Do not add any text outside the requested structured output.
12. Return as many valid questions as possible, up to the requested count.
13. The quiz is for MCA/college students.
"""


        # ==================================================
        # STRUCTURED RESPONSE
        # ==================================================

        response = client.models.generate_content(

            model="gemini-3.6-flash",

            contents=prompt,

            config=types.GenerateContentConfig(

                response_mime_type="application/json",

                response_schema=QuizResponse,

                temperature=0.3,

                max_output_tokens=8000
            )
        )


        # ==================================================
        # EMPTY RESPONSE
        # ==================================================

        if not response:

            return {
                "success": False,
                "error": (
                    "Gemini returned no response."
                ),
                "quiz": None
            }


        if not response.text:

            return {
                "success": False,
                "error": (
                    "Gemini returned an empty quiz response. "
                    "Please try again."
                ),
                "quiz": None
            }


        # ==================================================
        # PARSE RESPONSE
        # ==================================================

        try:

            quiz = QuizResponse.model_validate_json(
                response.text
            )

        except Exception as parse_error:

            print(
                "Quiz parsing error:",
                parse_error
            )

            return {
                "success": False,
                "error": (
                    "Gemini generated an invalid quiz format. "
                    "Please try again."
                ),
                "quiz": None
            }


        # ==================================================
        # VALIDATE QUESTIONS
        # ==================================================

        valid_questions = validate_questions(
            quiz.questions,
            number_of_questions
        )


        # ==================================================
        # NO VALID QUESTIONS
        # ==================================================

        if not valid_questions:

            return {
                "success": False,
                "error": (
                    "No valid quiz questions were generated. "
                    "Please try again."
                ),
                "quiz": None
            }


        # ==================================================
        # UPDATE QUIZ
        # ==================================================

        quiz.questions = valid_questions


        # ==================================================
        # RETURN
        # ==================================================

        return {
            "success": True,
            "error": None,
            "quiz": quiz.model_dump()
        }


    # ======================================================
    # GEMINI / SYSTEM ERROR
    # ======================================================

    except Exception as e:

        error_type = type(e).__name__
        error_message = str(e)


        print(
            "\n========== QUIZ GENERATOR ERROR =========="
        )

        print(
            "Error Type:",
            error_type
        )

        print(
            "Error:",
            error_message
        )

        print(
            "==========================================\n"
        )


        # --------------------------------------------------
        # Quota error
        # --------------------------------------------------

        if (
            "429" in error_message
            or
            "RESOURCE_EXHAUSTED" in error_message
            or
            "quota" in error_message.lower()
        ):

            return {
                "success": False,
                "error": (
                    "⚠️ Gemini quota is currently "
                    "exhausted for this model/API key.\n\n"
                    "Please wait for the quota to reset "
                    "or use another available Gemini model."
                ),
                "quiz": None
            }


        # --------------------------------------------------
        # Other errors
        # --------------------------------------------------

        return {
            "success": False,
            "error": (
                f"Unable to generate the quiz.\n\n"
                f"{error_type}: {error_message}"
            ),
            "quiz": None
        }