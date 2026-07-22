from app.ocr.extractor import extract_text_from_image
from app.core.answer_parser import parse_answers


def process_answer_script(file_path: str):
    # Step 1: OCR
    extracted_text = extract_text_from_image(file_path)

    print("\n===== RAW OCR TEXT =====")
    print(extracted_text)

    # Step 2: Parse answers
    answers = parse_answers(extracted_text)

    print("\n===== STRUCTURED ANSWERS =====")

    for answer in answers:
        print(answer)

    return answers


if __name__ == "__main__":
    process_answer_script("data/sample_answer.jpg")