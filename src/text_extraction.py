# text_extraction.py
"""Handles extraction of text from various document formats."""

from pathlib import Path

from PyPDF2 import PdfReader
from docx import Document
from ebooklib import epub
from bs4 import BeautifulSoup


def extract_text(file_path: Path) -> str:
    """
    Extract readable text from supported file formats.
    Returns error message string on failure.
    """
    ext = file_path.suffix.lower()
    try:
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                return f.read()

        elif ext == '.pdf':
            reader = PdfReader(file_path)
            pages_text = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)
            return "\n\n".join(pages_text)

        elif ext == '.docx':
            doc = Document(file_path)
            return "\n".join(para.text for para in doc.paragraphs)

        elif ext == '.epub':
            book = epub.read_epub(str(file_path))
            parts = []
            for itemref in book.spine:
                item_id = itemref[0] if isinstance(itemref, (list, tuple)) else itemref
                item = book.get_item_with_id(item_id)
                if item and item.get_type() == epub.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    for tag in soup(["script", "style", "nav", "header", "footer"]):
                        tag.decompose()
                    chapter_text = soup.get_text(separator="\n", strip=True)
                    if chapter_text.strip():
                        parts.append(chapter_text)
            return "\n\n".join(parts)

        elif ext in ('.html', '.htm'):
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                soup = BeautifulSoup(f, 'html.parser')
                for tag in soup(["script", "style"]):
                    tag.decompose()
                return soup.get_text(separator=" ", strip=True)

        return f"Unsupported file format: {ext}"

    except Exception as e:
        return f"Error reading file: {str(e)}"