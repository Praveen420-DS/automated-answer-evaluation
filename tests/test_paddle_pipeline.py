from pathlib import Path

from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas

from app.evaluation.deterministic_evaluator import evaluate_answers
from app.feedback.feedback_generator import generate_feedback
from app.main import app
from app.ocr.extractor import extract_document
from app.ocr.input_handler import input_to_images
from app.ocr.models import OCRResult
from app.parser.answer_parser import parse_ocr_result


SAMPLE_IMAGE = Path("tests/samples/Closest10.JPEG")


def test_paddleocr_import_and_version():
    import paddle
    import paddleocr

    assert paddle.__version__
    assert paddleocr.__version__.startswith("3.")


def test_paddleocr_image_ocr_schema():
    result = extract_document(SAMPLE_IMAGE)

    assert isinstance(result, OCRResult)
    assert result.metadata["engine"] == "PaddleOCR"
    assert result.metadata["model"] == "PP-OCRv5"
    assert len(result.pages) == 1
    assert isinstance(result.full_text, str)


def test_pdf_to_images(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    page = canvas.Canvas(str(pdf_path))
    page.drawString(100, 750, "1. Test answer")
    page.showPage()
    page.drawString(100, 750, "2. Second page")
    page.save()

    image_paths = input_to_images(pdf_path, tmp_path)

    assert len(image_paths) == 2
    assert all(path.exists() for path in image_paths)


def test_invalid_input_extension(tmp_path):
    invalid = tmp_path / "bad.txt"
    invalid.write_text("not an image", encoding="utf-8")

    try:
        input_to_images(invalid, tmp_path)
    except Exception as error:
        assert "supported" in str(error)
    else:
        raise AssertionError("Invalid extension was accepted")


def test_parser_evaluator_scoring_feedback():
    result = OCRResult(
        pages=[],
        full_text="1. Example\nAns: def add(a, b):\n    return a + b",
        metadata={"engine": "test"},
    )

    parsed = parse_ocr_result(result)
    evaluation = evaluate_answers(
        parsed,
        expected_answer="def add(a, b):\n    return a + b",
        maximum_score=5,
    )
    feedback = generate_feedback(evaluation)

    assert parsed["answers"]
    assert evaluation["score"] > 0
    assert feedback["score"] == evaluation["score"]


def test_api_rejects_invalid_file():
    client = TestClient(app)
    response = client.post(
        "/api/ocr",
        files={"file": ("bad.txt", b"hello", "text/plain")},
    )

    assert response.status_code == 400
