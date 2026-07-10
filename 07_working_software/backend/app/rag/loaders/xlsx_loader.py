"""XLSX text extraction, flattening each sheet's rows into text."""

import openpyxl


def extract_text_from_xlsx(file_path: str) -> str:
    """Extract cell values from every sheet, flattened row-by-row into text."""
    workbook = openpyxl.load_workbook(file_path, data_only=True, read_only=True)
    sheets_text: list[str] = []

    for sheet in workbook.worksheets:
        parts: list[str] = [f"[Sheet: {sheet.title}]"]
        for row in sheet.iter_rows(values_only=True):
            cells = [str(value) for value in row if value is not None]
            if cells:
                parts.append(" | ".join(cells))
        sheets_text.append("\n".join(parts))

    return "\n\n".join(sheets_text)
