import os

from parsers.pdf_parser import extract_pdf_text
from parsers.docx_parser import extract_docx_text
from parsers.image_parser import extract_image_text

def extract_document(filepath):

    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".pdf":
        return extract_pdf_text(filepath)

    elif extension == ".docx":
        return extract_docx_text(filepath)

    elif extension in [".png", ".jpg", ".jpeg"]:
        return extract_image_text(filepath)

    raise ValueError("Unsupported File Type")