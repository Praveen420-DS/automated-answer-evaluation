try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    fitz = None


def extract_pdf_text(filepath):
    if fitz is not None:
        document = fitz.open(filepath)
        try:
            text = ""
            for page in document:
                text += page.get_text()
            return text
        finally:
            document.close()

    import pypdfium2 as pdfium

    document = pdfium.PdfDocument(str(filepath))
    try:
        text = ""
        for page in document:
            page_text = page.get_textpage().get_text_range() or ""
            text += page_text
        return text
    finally:
        document.close()