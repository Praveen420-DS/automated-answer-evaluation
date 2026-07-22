from pathlib import Path
import sys
from types import SimpleNamespace

import cv2
import numpy as np
from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas

from app.evaluation.deterministic_evaluator import evaluate_answers
from app.feedback.feedback_generator import generate_feedback
from app.main import app
from app.core.config import RUNTIME_HOME, configure_runtime_environment
from app.ocr.extractor import extract_document
from app.ocr.input_handler import input_to_images
from app.ocr.models import OCRPage, OCRResult
from app.ocr.paddle_ocr import get_paddle_ocr_engine
from app.ocr.preprocessing import preprocess_image
from app.ocr.pp_structure import _extract_blocks, get_pp_structure_engine
from app.parser.answer_parser import parse_ocr_result


SAMPLE_IMAGE = Path("tests/samples/Closest10.JPEG")


def test_paddleocr_import_and_version():
    configure_runtime_environment()
    import paddle
    import paddleocr

    assert paddle.__version__
    assert paddleocr.__version__.startswith("3.")


def test_paddleocr_initializes_with_project_runtime_cache():
    configure_runtime_environment()

    runtime_probe = RUNTIME_HOME / "runtime-write-test.txt"
    runtime_probe.write_text("ok", encoding="utf-8")
    assert runtime_probe.read_text(encoding="utf-8") == "ok"
    runtime_probe.unlink()

    get_paddle_ocr_engine.cache_clear()
    engine = get_paddle_ocr_engine()

    assert engine is not None


def test_pp_structure_initializes_with_project_runtime_cache(monkeypatch):
    class FakePPStructureV3:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    monkeypatch.setitem(
        sys.modules,
        "paddleocr",
        SimpleNamespace(PPStructureV3=FakePPStructureV3),
    )
    get_pp_structure_engine.cache_clear()
    engine = get_pp_structure_engine()

    assert engine is not None
    assert engine.kwargs["device"] == "cpu"
    assert engine.kwargs["use_table_recognition"] is False
    get_pp_structure_engine.cache_clear()


def test_paddleocr_image_ocr_schema():
    result = extract_document(SAMPLE_IMAGE)

    assert isinstance(result, OCRResult)
    assert result.metadata["engine"] == "PaddleOCR"
    assert result.metadata["model"] == "PP-OCRv5"
    assert len(result.pages) == 1
    assert isinstance(result.full_text, str)


def test_preprocessing_disabled_returns_original_image(tmp_path):
    image_path = tmp_path / "answer.png"
    assert cv2.imwrite(str(image_path), np.full((100, 200, 3), 255, dtype=np.uint8))

    assert preprocess_image(image_path, enabled=False) == image_path


def test_preprocessing_enabled_writes_transformed_image(tmp_path):
    image_path = tmp_path / "answer.png"
    image = np.full((100, 200, 3), 255, dtype=np.uint8)
    cv2.putText(image, "42", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
    assert cv2.imwrite(str(image_path), image)

    processed_path = preprocess_image(
        image_path,
        enabled=True,
        output_dir=tmp_path / "processed",
    )
    processed = cv2.imread(str(processed_path), cv2.IMREAD_UNCHANGED)

    assert processed_path != image_path
    assert processed_path.exists()
    assert processed.ndim == 2
    assert processed.shape == (150, 300)
    assert set(np.unique(processed)).issubset({0, 255})


def test_paddle_wrapper_uses_preprocessed_image_and_normalizes_all_results(
    tmp_path,
    monkeypatch,
):
    from app.ocr import paddle_ocr

    image_path = tmp_path / "answer.png"
    assert cv2.imwrite(str(image_path), np.full((100, 200, 3), 255, dtype=np.uint8))
    inputs: list[Path] = []

    class FakeEngine:
        def predict(self, input: str):
            inputs.append(Path(input))
            return [
                SimpleNamespace(
                    json={
                        "res": {
                            "rec_texts": ["first", "second"],
                            "rec_scores": [0.9, 0.8],
                            "rec_polys": [
                                [[0, 0], [1, 0], [1, 1], [0, 1]],
                                [[2, 2], [3, 2], [3, 3], [2, 3]],
                            ],
                        }
                    }
                ),
                SimpleNamespace(
                    json={
                        "res": {
                            "rec_texts": ["third"],
                            "rec_scores": [0.7],
                            "rec_boxes": [[4, 4, 5, 5]],
                        }
                    }
                ),
            ]

    monkeypatch.setattr(paddle_ocr, "get_paddle_ocr_engine", lambda: FakeEngine())
    result = paddle_ocr.extract_text_with_paddle(
        [image_path],
        preprocess=True,
        workspace=tmp_path,
    )

    assert inputs[0] != image_path
    assert inputs[0].parent == tmp_path / "preprocessed"
    assert inputs[0].exists()
    assert [page.page_number for page in result.pages] == [1, 2]
    assert [block.text for block in result.pages[0].blocks] == ["first", "second"]
    assert result.pages[0].blocks[1].order == 1
    assert result.pages[1].blocks[0].bbox == [4.0, 4.0, 5.0, 5.0]


def test_pp_structure_normalizes_layout_regions_and_tables():
    raw_page = SimpleNamespace(
        json={
            "res": {
                "parsing_res_list": [
                    {
                        "block_label": "title",
                        "block_content": "Question 1",
                        "block_bbox": [0, 0, 100, 20],
                        "block_order": 3,
                        "block_score": 0.98,
                    },
                    {
                        "block_label": "table",
                        "block_content": "",
                        "block_bbox": [0, 30, 100, 80],
                    },
                ],
                "table_res_list": [
                    {
                        "block_bbox": [0, 30, 100, 80],
                        "pred_html": "<table><tr><td>A</td></tr></table>",
                        "cell_box_list": [[0, 30, 100, 80]],
                    }
                ],
            }
        }
    )

    blocks = _extract_blocks(raw_page)

    assert [(block.type, block.text, block.order) for block in blocks] == [
        ("title", "Question 1", 3),
        ("table", "", 1),
    ]
    assert blocks[0].confidence == 0.98
    assert blocks[1].table["pred_html"].startswith("<table>")


def test_pp_structure_normalizes_observed_pp_structurev3_schema():
    raw_page = SimpleNamespace(
        json={
            "res": {
                "page_index": 0,
                "parsing_res_list": [
                    {
                        "block_label": "formula",
                        "block_content": "x = y + 1",
                        "block_bbox": [0, 0, 200, 40],
                        "block_id": 0,
                        "block_order": 1,
                    }
                ],
            }
        }
    )

    blocks = _extract_blocks(raw_page)

    assert len(blocks) == 1
    assert blocks[0].type == "formula"
    assert blocks[0].text == "x = y + 1"
    assert blocks[0].bbox == [0.0, 0.0, 200.0, 40.0]
    assert blocks[0].order == 1
    assert blocks[0].confidence is None


def test_extractor_attaches_structure_without_replacing_ocr_blocks(
    tmp_path,
    monkeypatch,
):
    from app.ocr import extractor

    image_path = tmp_path / "answer.png"
    assert cv2.imwrite(str(image_path), np.full((100, 200, 3), 255, dtype=np.uint8))
    ocr_result = OCRResult(
        pages=[OCRPage(
            page_number=1,
            text="OCR text",
            blocks=[],
        )],
        full_text="OCR text",
    )
    structure_result = OCRResult(
        pages=[OCRPage(
            page_number=1,
            text="Structured text",
            structure_blocks=[],
            blocks=[{"text": "Structured text", "type": "paragraph", "order": 0}],
        )],
        metadata={"model": "PP-StructureV3"},
    )
    monkeypatch.setattr(extractor, "PADDLE_ENABLE_STRUCTURE", True)
    monkeypatch.setattr(extractor, "extract_text_with_paddle", lambda *args, **kwargs: ocr_result)
    monkeypatch.setattr(extractor, "analyze_structure", lambda paths: structure_result)

    result = extractor.extract_document(image_path)

    assert result.full_text == "OCR text"
    assert result.pages[0].blocks == []
    assert result.pages[0].structure_blocks[0].type == "paragraph"
    assert result.metadata["structure_available"] is True


def test_multi_page_pdf_reaches_ocr_pipeline(tmp_path, monkeypatch):
    from app.ocr import extractor

    pdf_path = tmp_path / "sample.pdf"
    page = canvas.Canvas(str(pdf_path))
    page.drawString(100, 750, "Page one")
    page.showPage()
    page.drawString(100, 750, "Page two")
    page.save()
    captured: dict[str, object] = {}

    def fake_extract(image_paths, preprocess, workspace):
        assert all(path.exists() for path in image_paths)
        captured["paths"] = image_paths
        captured["preprocess"] = preprocess
        captured["workspace"] = workspace
        return OCRResult()

    monkeypatch.setattr(extractor, "extract_text_with_paddle", fake_extract)
    monkeypatch.setattr(extractor, "PADDLE_ENABLE_STRUCTURE", False)
    extractor.extract_document(pdf_path, preprocess=True)

    assert len(captured["paths"]) == 2
    assert captured["preprocess"] is True


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
