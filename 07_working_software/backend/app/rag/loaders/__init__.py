"""Format-aware document loaders. Dispatches on file_type to the correct extractor."""

from app.rag.loaders.docx_loader import extract_text_from_docx
from app.rag.loaders.eml_loader import extract_text_from_eml
from app.rag.loaders.pdf_loader import extract_text_from_pdf
from app.rag.loaders.pptx_loader import extract_text_from_pptx
from app.rag.loaders.xlsx_loader import extract_text_from_xlsx

LOADER_DISPATCH = {
    "pdf": extract_text_from_pdf,
    "docx": extract_text_from_docx,
    "pptx": extract_text_from_pptx,
    "xlsx": extract_text_from_xlsx,
    "eml": extract_text_from_eml,
}


def extract_text(file_path: str, file_type: str) -> str:
    """Extract plain text from a document, dispatching by file_type (FR-1.2)."""
    loader = LOADER_DISPATCH.get(file_type)
    if loader is None:
        raise ValueError(f"Unsupported file_type: {file_type}")
    return loader(file_path)
