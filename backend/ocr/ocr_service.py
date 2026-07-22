import easyocr

reader = easyocr.Reader(["en"])

def extract_text(image_path):

    result = reader.readtext(
        image_path,
        detail=0
    )

    text = "\n".join(result)

    return text