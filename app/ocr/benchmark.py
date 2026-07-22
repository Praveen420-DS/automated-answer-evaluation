"""Ground-truth benchmark for the PP-OCRv5 and PP-StructureV3 pipeline."""

from __future__ import annotations

import csv
import json
import re
import tempfile
from pathlib import Path
from statistics import mean
from typing import Any

import cv2

from app.ocr.extractor import extract_document
from app.ocr.paddle_ocr import extract_text_with_paddle
from app.ocr.preprocessing import preprocess_image


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLES_DIR = PROJECT_ROOT / "tests" / "samples"
EXPECTED_DIR = PROJECT_ROOT / "tests" / "expected"
HISTORICAL_RESULTS_DIR = PROJECT_ROOT / "tests" / "benchmark_results"
HISTORICAL_BASELINE = PROJECT_ROOT / "tests" / "best_per_image_results.csv"
REPORT_PATH = HISTORICAL_RESULTS_DIR / "paddleocr_v5_structure_benchmark.json"
ABLATION_REPORT_PATH = HISTORICAL_RESULTS_DIR / "paddleocr_v5_preprocessing_ablation.json"


ABLATION_CONFIGURATIONS = (
    "original",
    "grayscale_only",
    "upscaling_only",
    "adaptive_threshold_only",
    "grayscale_plus_upscaling",
    "grayscale_plus_adaptive_threshold",
    "upscaling_plus_adaptive_threshold",
    "current_full_pipeline",
)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def character_similarity(expected: str, actual: str) -> float:
    from difflib import SequenceMatcher

    expected_normalized = normalize_text(expected)
    actual_normalized = normalize_text(actual)
    if not expected_normalized or not actual_normalized:
        return 0.0
    return SequenceMatcher(None, expected_normalized, actual_normalized).ratio()


def token_similarity(expected: str, actual: str) -> float:
    expected_tokens = set(normalize_text(expected).split())
    actual_tokens = set(normalize_text(actual).split())
    if not expected_tokens or not actual_tokens:
        return 0.0
    return len(expected_tokens & actual_tokens) / len(expected_tokens | actual_tokens)


def similarity_metrics(expected: str, actual: str) -> dict[str, float]:
    character = character_similarity(expected, actual)
    token = token_similarity(expected, actual)
    return {
        "character_similarity": character,
        "token_similarity": token,
        "overall_similarity": (0.7 * character) + (0.3 * token),
    }


def ground_truth_pairs() -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    for image_path in sorted(SAMPLES_DIR.iterdir()):
        if image_path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        expected_path = EXPECTED_DIR / f"{image_path.stem}.txt"
        if expected_path.exists():
            pairs.append((image_path, expected_path))
    return pairs


def _confidence_statistics(blocks: list[Any]) -> dict[str, float | None]:
    confidences = [block.confidence for block in blocks if block.confidence is not None]
    return {
        "mean_confidence": mean(confidences) if confidences else None,
        "min_confidence": min(confidences) if confidences else None,
        "max_confidence": max(confidences) if confidences else None,
    }


def _result_metrics(expected: str, result: Any) -> dict[str, Any]:
    blocks = [block for page in result.pages for block in page.blocks]
    return {
        **similarity_metrics(expected, result.full_text),
        **_confidence_statistics(blocks),
        "ocr_block_count": len(blocks),
        "ocr_character_count": len(result.full_text),
    }


def _historical_baseline() -> dict[str, dict[str, Any]]:
    baseline: dict[str, dict[str, Any]] = {}
    with HISTORICAL_BASELINE.open(encoding="utf-8", newline="") as csv_file:
        for row in csv.DictReader(csv_file):
            stem = row["Image"]
            actual_path = HISTORICAL_RESULTS_DIR / (
                f"{stem}_{row['Best_Preprocessing'].lower()}_psm{row['Best_PSM']}.txt"
            )
            expected_path = EXPECTED_DIR / f"{stem}.txt"
            if not actual_path.exists() or not expected_path.exists():
                continue
            actual = actual_path.read_text(encoding="utf-8")
            expected = expected_path.read_text(encoding="utf-8")
            baseline[stem] = {
                **similarity_metrics(expected, actual),
                "method": row["Best_Preprocessing"],
                "psm": int(row["Best_PSM"]),
                "historical_character_similarity": float(row["Similarity_Percentage"]) / 100,
            }
    return baseline


def _average(rows: list[dict[str, Any]], keys: tuple[str, ...]) -> dict[str, float]:
    return {key: mean(row[key] for row in rows) for key in keys}


def _upscale(image: Any) -> Any:
    height, width = image.shape[:2]
    if max(height, width) < 1600:
        return cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    return image


def _adaptive_threshold(image: Any) -> Any:
    gray = (
        cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if len(image.shape) == 3
        else image
    )
    return cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10,
    )


def _ablation_image(image_path: Path, configuration: str, output_dir: Path) -> Path:
    """Write one independently transformed image for the requested ablation."""
    if configuration == "original":
        return image_path
    if configuration == "current_full_pipeline":
        return preprocess_image(image_path, enabled=True, output_dir=output_dir)

    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Invalid or unreadable image: {image_path}")

    grayscale = configuration in {
        "grayscale_only",
        "grayscale_plus_upscaling",
        "grayscale_plus_adaptive_threshold",
    }
    upscaling = configuration in {
        "upscaling_only",
        "grayscale_plus_upscaling",
        "upscaling_plus_adaptive_threshold",
    }
    thresholding = configuration in {
        "adaptive_threshold_only",
        "grayscale_plus_adaptive_threshold",
        "upscaling_plus_adaptive_threshold",
    }
    if grayscale:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if upscaling:
        image = _upscale(image)
    if thresholding:
        image = _adaptive_threshold(image)

    destination = output_dir / f"{image_path.stem}-{configuration}.png"
    if not cv2.imwrite(str(destination), image):
        raise OSError(f"Could not write ablation image: {destination}")
    return destination


def run_preprocessing_ablation(
    report_path: Path = ABLATION_REPORT_PATH,
) -> dict[str, Any]:
    """Benchmark each requested preprocessing operation independently.

    The report is additive and intentionally does not update the historical
    Tesseract baseline or the existing PaddleOCR/structure benchmark report.
    """
    pairs = ground_truth_pairs()
    per_configuration: dict[str, list[dict[str, Any]]] = {
        configuration: [] for configuration in ABLATION_CONFIGURATIONS
    }

    with tempfile.TemporaryDirectory() as temporary_workspace:
        workspace = Path(temporary_workspace)
        for image_path, expected_path in pairs:
            expected = expected_path.read_text(encoding="utf-8")
            for configuration in ABLATION_CONFIGURATIONS:
                prepared_path = _ablation_image(image_path, configuration, workspace)
                result = extract_text_with_paddle([prepared_path], preprocess=False)
                per_configuration[configuration].append(
                    {
                        "image": image_path.name,
                        "ground_truth": expected_path.name,
                        **_result_metrics(expected, result),
                    }
                )

    metric_keys = (
        "character_similarity",
        "token_similarity",
        "overall_similarity",
        "mean_confidence",
    )
    configurations = {
        configuration: {
            "per_image": rows,
            "averages": _average(rows, metric_keys),
        }
        for configuration, rows in per_configuration.items()
    }
    best_by_image = []
    for image_path, _ in pairs:
        candidates = [
            (configuration, next(row for row in rows if row["image"] == image_path.name))
            for configuration, rows in per_configuration.items()
        ]
        configuration, result = max(
            candidates, key=lambda item: item[1]["overall_similarity"]
        )
        best_by_image.append(
            {
                "image": image_path.name,
                "best_configuration": configuration,
                **{key: result[key] for key in metric_keys},
            }
        )

    ranked = sorted(
        configurations.items(),
        key=lambda item: item[1]["averages"]["overall_similarity"],
        reverse=True,
    )
    report = {
        "pipeline": {
            "ocr_model": "PP-OCRv5_server_det + PP-OCRv5_server_rec",
            "device": "cpu",
        },
        "image_count": len(pairs),
        "configurations": configurations,
        "per_image_best": best_by_image,
        "best_overall_configuration": ranked[0][0],
        "worst_overall_configuration": ranked[-1][0],
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def run_benchmark(report_path: Path = REPORT_PATH) -> dict[str, Any]:
    """Run all configured PaddleOCR variants and write an additive JSON report."""
    pairs = ground_truth_pairs()
    baseline = _historical_baseline()
    images: list[dict[str, Any]] = []

    for image_path, expected_path in pairs:
        expected = expected_path.read_text(encoding="utf-8")
        original = extract_text_with_paddle([image_path], preprocess=False)
        preprocessed = extract_text_with_paddle([image_path], preprocess=True)
        structured = extract_document(image_path, preprocess=True)
        structure_blocks = [
            block for page in structured.pages for block in page.structure_blocks
        ]
        images.append(
            {
                "image": image_path.name,
                "ground_truth": expected_path.name,
                "original": _result_metrics(expected, original),
                "preprocessed": _result_metrics(expected, preprocessed),
                "preprocessed_with_structure": {
                    **_result_metrics(expected, structured),
                    "structure_available": structured.metadata.get("structure_available", False),
                    "structure_block_count": len(structure_blocks),
                    "structure_block_types": sorted({block.type for block in structure_blocks}),
                    "table_block_count": sum(block.type == "table" for block in structure_blocks),
                },
                "historical_tesseract": baseline.get(image_path.stem),
            }
        )

    metric_keys = ("character_similarity", "token_similarity", "overall_similarity")
    original_rows = [image["original"] for image in images]
    preprocessed_rows = [image["preprocessed"] for image in images]
    structured_rows = [image["preprocessed_with_structure"] for image in images]
    baseline_rows = [
        image["historical_tesseract"] for image in images if image["historical_tesseract"]
    ]
    best = max(preprocessed_rows, key=lambda row: row["overall_similarity"])
    worst = min(preprocessed_rows, key=lambda row: row["overall_similarity"])
    best_image = images[preprocessed_rows.index(best)]["image"]
    worst_image = images[preprocessed_rows.index(worst)]["image"]
    paddle_average = _average(preprocessed_rows, metric_keys)
    baseline_average = _average(baseline_rows, metric_keys)

    report = {
        "pipeline": {
            "ocr_model": "PP-OCRv5_server_det + PP-OCRv5_server_rec",
            "structure_model": "PP-StructureV3 / PP-DocLayout_plus-L",
            "device": "cpu",
        },
        "image_count": len(images),
        "images": images,
        "averages": {
            "original": _average(original_rows, metric_keys),
            "preprocessed": paddle_average,
            "preprocessed_with_structure": _average(structured_rows, metric_keys),
            "historical_tesseract": baseline_average,
            "preprocessed_vs_tesseract_percentage_points": {
                key: (paddle_average[key] - baseline_average[key]) * 100
                for key in metric_keys
            },
            "confidence": {
                "mean_of_image_means": mean(
                    row["mean_confidence"]
                    for row in preprocessed_rows
                    if row["mean_confidence"] is not None
                )
            },
            "structure": {
                "total_blocks": sum(row["structure_block_count"] for row in structured_rows),
                "images_with_structure": sum(row["structure_available"] for row in structured_rows),
                "total_table_blocks": sum(row["table_block_count"] for row in structured_rows),
            },
        },
        "best_preprocessed_image": {"image": best_image, **best},
        "worst_preprocessed_image": {"image": worst_image, **worst},
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(run_benchmark(), indent=2))
