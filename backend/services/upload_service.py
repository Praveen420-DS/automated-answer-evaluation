import os

UPLOAD_FOLDER = "uploads"

def process_answer_script(file):
    # OCR and the sentence-transformer model are optional, heavyweight
    # dependencies.  Loading them at module import made every API startup try
    # to download model files, even for unrelated endpoints.
    from ocr.ocr_service import extract_text
    from ai.evaluator import evaluate_answers

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(filepath)

    student_answers = extract_text(filepath)

    evaluation = evaluate_answers(student_answers)

    return evaluation
