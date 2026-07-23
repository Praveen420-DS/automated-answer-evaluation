def extract_text(image_path):
    # Reuse the lazy, Python-3.12-compatible EasyOCR loader used by the
    # question-paper upload flow.
    from parsers.image_parser import extract_image_text
    return extract_image_text(image_path)
