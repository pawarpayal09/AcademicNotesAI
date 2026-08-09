import speech_recognition as sr
import tempfile
import os


def speech_to_text(audio_bytes):

    if not audio_bytes:
        return None

    try:

        # Create temporary WAV file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as temp_audio:

            temp_audio.write(audio_bytes)

            audio_path = temp_audio.name

        # Speech Recognition
        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_path) as source:

            audio = recognizer.record(source)

        # Convert speech to text
        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        # Remove temporary file
        os.remove(audio_path)

        return text.strip()

    except sr.UnknownValueError:

        return None

    except sr.RequestError:

        return None

    except Exception as e:

        print("Speech-to-text error:", e)

        return None