import os
import tempfile
from gtts import gTTS
import speech_recognition as sr

# ==========================================================
# TEXT TO SPEECH
# ==========================================================

def text_to_speech(text):

    if not text.strip():
        return None

    temp_dir = tempfile.gettempdir()

    audio_path = os.path.join(
        temp_dir,
        "academic_notes_answer.mp3"
    )

    tts = gTTS(
        text=text,
        lang="en",
        slow=False
    )

    tts.save(audio_path)

    return audio_path


# ==========================================================
# SPEECH TO TEXT
# ==========================================================

def speech_to_text(audio_file):

    recognizer = sr.Recognizer()

    try:

        with sr.AudioFile(audio_file) as source:

            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        return text.strip()

    except sr.UnknownValueError:

        return ""

    except sr.RequestError as e:

        print(
            "Speech recognition service error:",
            e
        )

        return ""

    except Exception as e:

        print(
            "Speech-to-text error:",
            e
        )

        return ""

# =====================================================
# SPEECH TO TEXT
# =====================================================

def speech_to_text(audio_file):

    try:

        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_file) as source:

            audio = recognizer.record(source)

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        return text.strip()

    except sr.UnknownValueError:

        return ""

    except sr.RequestError as e:

        print("Speech recognition service error:", e)

        return ""

    except Exception as e:

        print("Speech-to-text error:", e)

        return ""