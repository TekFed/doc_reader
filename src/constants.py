# constants.py
"""Application-wide constants and configuration values."""

APP_TITLE = "Document Reader - Text to Speech"
WINDOW_BG = "#f0f0f0"
HEADER_BG = "#2c3e50"
HEADER_FG = "white"
FONT_FAMILY = "Segoe UI"

SUPPORTED_FORMATS = [
    ("All supported", "*.txt *.pdf *.docx *.epub *.html *.htm"),
    ("Text", "*.txt"),
    ("PDF", "*.pdf"),
    ("Word", "*.docx"),
    ("EPUB", "*.epub"),
    ("HTML", "*.html *.htm"),
]

DEFAULT_RATE = 150
RATE_MIN = 100
RATE_MAX = 220

PROGRESS_LENGTH = 800
PREVIEW_HEIGHT = 10