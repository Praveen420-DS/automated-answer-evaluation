import easyocr

reader = easyocr.Reader(["en"])

def extract_image_text(filepath):

    result = reader.readtext(
        filepath,
        detail=0
    )

    return "\n".join(result)