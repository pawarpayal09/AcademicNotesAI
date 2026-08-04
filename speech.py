import os
import tempfile
from gtts import gTTS


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