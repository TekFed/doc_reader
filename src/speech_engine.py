# speech_engine.py
"""Handles text-to-speech operations using pyttsx3."""

import pyttsx3
from pathlib import Path
from datetime import datetime


def get_available_voices():
    """Return list of available pyttsx3 voices."""
    engine = pyttsx3.init()
    return engine.getProperty('voices')


def prefer_stable_voice(engine, preferred_names=("David", "Zira", "Hazel")):
    """Attempt to select a known more stable voice if available."""
    voices = engine.getProperty('voices')
    for name_part in preferred_names:
        for voice in voices:
            if name_part in voice.name:
                engine.setProperty('voice', voice.id)
                return True
    return False


def save_text_to_mp3(text: str, output_path: Path, rate: int = 150, voice_id=None):
    """
    Convert text to MP3 file using pyttsx3.
    Uses a stable voice preference when no specific voice_id is given.
    """
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)

    if voice_id:
        engine.setProperty('voice', voice_id)
    else:
        prefer_stable_voice(engine)

    engine.save_to_file(text, str(output_path))
    engine.runAndWait()


def create_auto_mp3_filename(original_path: Path) -> Path:
    """Generate automatic output filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    return original_path.with_name(f"{original_path.stem}_spoken_{timestamp}.mp3")