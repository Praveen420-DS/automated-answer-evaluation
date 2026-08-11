import json
from pathlib import Path

import pytest

from app.ocr.benchmark_metrics import (
    aggregate_metrics,
    calculate_ocr_metrics,
    levenshtein_distance,
    load_benchmark_manifest,
    normalize_ocr_text,
)
from app.ocr.provider_result import ProviderResult


def test_exact_match_and_substitution():
    exact = calculate_ocr_metrics("alpha beta", "alpha beta")
    changed = calculate_ocr_metrics("cat", "cut")
    assert exact["normalized_character_error_rate"] == 0
    assert exact["word_error_rate"] == 0
    assert exact["exact_match"] is True
    assert changed["character_edit_distance"] == 1
    assert changed["normalized_character_error_rate"] == pytest.approx(1 / 3)


def test_insertions_deletions_and_accuracy_clamping():
    inserted = calculate_ocr_metrics("a", "aaaa")
    deleted = calculate_ocr_metrics("abcd", "acd")
    assert inserted["normalized_character_error_rate"] == 3
    assert inserted["character_accuracy"] == 0
    assert deleted["character_edit_distance"] == 1


def test_token_distance_counts_repeated_and_reordered_words():
    repeated = calculate_ocr_metrics("go go", "go")
    reordered = calculate_ocr_metrics("one two", "two one")
    assert repeated["word_edit_distance"] == 1
    assert reordered["word_edit_distance"] == 2
    assert levenshtein_distance(["go", "go"], ["go"]) == 1


@pytest.mark.parametrize(
    ("expected", "actual", "cer", "wer", "empty"),
    [("", "", 0, 0, True), ("", "x y", 1, 1, False), ("x y", "", 1, 1, True)],
)
def test_empty_cases(expected, actual, cer, wer, empty):
    metrics = calculate_ocr_metrics(expected, actual)
    assert metrics["normalized_character_error_rate"] == cer
    assert metrics["word_error_rate"] == wer
    assert metrics["empty_output"] is empty


def test_unicode_whitespace_punctuation_and_digits():
    assert normalize_ocr_text("Ａ＋1\r\n\tB!") == "a+1 b!"
    metrics = calculate_ocr_metrics("Ａ＋1\nB!", "a+1   b!")
    assert metrics["normalized_exact_match"] is True
    assert metrics["exact_match"] is False


def test_word_error_rate_can_exceed_one():
    metrics = calculate_ocr_metrics("one", "one two three")
    assert metrics["word_error_rate"] == 2
    assert metrics["word_accuracy"] == 0


def test_macro_and_micro_aggregation_differ():
    short = {**calculate_ocr_metrics("a", "x"), "latency_ms": 10, "page_count": 1, "success": True}
    long = {**calculate_ocr_metrics("abcdefghij", "abcdefghij"), "latency_ms": 30, "page_count": 2, "success": True}
    result = aggregate_metrics([short, long])
    assert result["macro_average_cer"] == 0.5
    assert result["micro_cer"] == pytest.approx(1 / 11)
    assert result["median_latency_ms"] == 20
    assert result["total_pages"] == 3


def test_question_number_precision_and_recall_ignore_inline_numbers():
    result = calculate_ocr_metrics("Q1 answer\n2. answer", "Question 1 answer\nQ3 answer with 42")
    assert result["expected_question_numbers"] == [1, 2]
    assert result["detected_question_numbers"] == [1, 3]
    assert result["question_number_precision"] == 0.5
    assert result["question_number_recall"] == 0.5
    assert result["question_number_f1"] == 0.5


def test_public_manifest_is_valid():
    root = Path(__file__).resolve().parents[1]
    entries = load_benchmark_manifest(root / "tests" / "benchmark_manifest.json", root)
    assert len(entries) == 7
    assert all(entry["ground_truth_verified"] is False for entry in entries)


def _write_manifest(path, entries):
    path.write_text(json.dumps({"samples": entries}), encoding="utf-8")


def test_manifest_rejects_duplicates_missing_empty_absolute_and_escape(tmp_path):
    (tmp_path / "image.jpg").write_bytes(b"image")
    (tmp_path / "truth.txt").write_text("truth", encoding="utf-8")
    valid = {"id": "one", "image_path": "image.jpg", "ground_truth_path": "truth.txt"}
    manifest = tmp_path / "manifest.json"
    _write_manifest(manifest, [valid, valid])
    with pytest.raises(ValueError, match="Duplicate"):
        load_benchmark_manifest(manifest, tmp_path)
    for bad, message in [
        ({**valid, "image_path": "missing.jpg"}, "Missing"),
        ({**valid, "image_path": str((tmp_path / "image.jpg").resolve())}, "relative"),
        ({**valid, "image_path": "../image.jpg"}, "escapes"),
    ]:
        _write_manifest(manifest, [bad])
        with pytest.raises(ValueError, match=message):
            load_benchmark_manifest(manifest, tmp_path)
    (tmp_path / "truth.txt").write_text("  ", encoding="utf-8")
    _write_manifest(manifest, [valid])
    with pytest.raises(ValueError, match="Empty"):
        load_benchmark_manifest(manifest, tmp_path)


def test_provider_result_serialization_is_secret_and_path_safe():
    result = ProviderResult(
        provider="example", model="v1", image_identifier=r"C:\private\student.jpg",
        success=False, error_type="TimeoutError",
        metadata={"api_key": "secret", "source_path": r"C:\private\student.jpg", "traceback": "raw stack"},
    )
    serialized = result.model_dump()
    assert serialized["image_identifier"] == "student.jpg"
    assert serialized["metadata"]["api_key"] == "[REDACTED]"
    assert serialized["metadata"]["source_path"] == "student.jpg"
    assert serialized["metadata"]["traceback"] == "[REDACTED]"
    json.dumps(serialized)
