"""PDF text extraction, including OCR fallback for image-only pages."""

import logging

import pypdf
import pytesseract
from pdf2image import convert_from_path

logger = logging.getLogger(__name__)

MIN_CHARS_BEFORE_OCR_FALLBACK = 20


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF. Falls back to OCR for pages with no embedded text."""
    pages: list[str] = []
    reader = pypdf.PdfReader(file_path)

    for page_number, page in enumerate(reader.pages):
        text = (page.extract_text() or "").strip()
        if len(text) < MIN_CHARS_BEFORE_OCR_FALLBACK:
            text = _ocr_page(file_path, page_number)
        pages.append(f"[Page {page_number + 1}]\n{text}")

    return "\n\n".join(pages)


def _ocr_page(file_path: str, page_number: int) -> str:
    try:
        images = convert_from_path(file_path, first_page=page_number + 1, last_page=page_number + 1)
        if not images:
            return ""
        return pytesseract.image_to_string(images[0]).strip()
    except Exception:
        logger.exception("OCR fallback failed for %s page %d", file_path, page_number + 1)
        return ""
