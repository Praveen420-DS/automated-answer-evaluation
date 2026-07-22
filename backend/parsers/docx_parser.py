from docx import Document

def extract_docx_text(filepath):

    document = Document(filepath)

    text = "\n".join(
        para.text for para in document.paragraphs
    )

    return text