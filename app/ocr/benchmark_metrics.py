"""Provider-neutral, dependency-free metrics for OCR benchmark results."""

from __future__ import annotations

import json
import math
import re
import unicodedata
from pathlib import Path
from statistics import mean, median
from typing import Any, Sequence, TypeVar


T = TypeVar("T")


def levenshtein_distance(expected: Sequence[T], actual: Sequence[T]) -> int:
    """Return the minimum insertions, deletions and substitutions.

    Strings are character sequences; lists/tuples can be used for token errors.
    Memory usage is linear in the length of the shorter input.
    """
    if len(expected) < len(actual):
        expected, actual = actual, expected
    previous = list(range(len(actual) + 1))
    for row, expected_item in enumerate(expected, 1):
        current = [row]
        for column, actual_item in enumerate(actual, 1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[column] + 1,
                    previous[column - 1] + (expected_item != actual_item),
                )
            )
        previous = current
    return previous[-1]


def normalize_ocr_text(text: str) -> str:
    """NFKC/casefold text and collapse all runs of whitespace.

    Punctuation, digits, formula characters, and technical symbols are retained.
    Newlines are normalized before whitespace is collapsed for explicit and
    platform-independent handling of CRLF/CR/LF input.
    """
    normalized = unicodedata.normalize("NFKC", text).replace("\r\n", "\n").replace("\r", "\n")
    return re.sub(r"\s+", " ", normalized).strip().casefold()


def _error_rate(edits: int, expected_count: int, actual_count: int) -> float:
    if expected_count:
        return edits / expected_count
    return 0.0 if actual_count == 0 else 1.0


# Conservative: only a marker at the beginning of a line is considered. It
# accepts explicit Q/Question markers, or conventional numbered-list markers;
# unmarked numbers elsewhere in answer prose are deliberately ignored.
QUESTION_NUMBER_RE = re.compile(
    r"(?im)^\s*(?:(?:q(?:uestion)?)[ \t]*#?[ \t]*(\d+)[ \t]*[.):\-]?|(\d+)[ \t]*[.)])(?=[ \t]|$)"
)


def extract_question_numbers(text: str) -> list[int]:
    normalized = unicodedata.normalize("NFKC", text).replace("\r\n", "\n").replace("\r", "\n")
    return sorted({int(first or second) for first, second in QUESTION_NUMBER_RE.findall(normalized)})


def question_number_metrics(expected: str, actual: str) -> dict[str, Any]:
    expected_numbers = extract_question_numbers(expected)
    detected_numbers = extract_question_numbers(actual)
    expected_set, detected_set = set(expected_numbers), set(detected_numbers)
    correct = len(expected_set & detected_set)
    precision = correct / len(detected_set) if detected_set else None
    recall = correct / len(expected_set) if expected_set else None
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision is not None and recall is not None and precision + recall
        else (0.0 if precision is not None and recall is not None else None)
    )
    return {
        "expected_question_numbers": expected_numbers,
        "detected_question_numbers": detected_numbers,
        "question_number_precision": precision,
        "question_number_recall": recall,
        "question_number_f1": f1,
    }


def calculate_ocr_metrics(expected: str, actual: str) -> dict[str, Any]:
    """Calculate raw/normalized character metrics and normalized word metrics."""
    normalized_expected = normalize_ocr_text(expected)
    normalized_actual = normalize_ocr_text(actual)
    expected_words = normalized_expected.split()
    actual_words = normalized_actual.split()
    raw_edits = levenshtein_distance(expected, actual)
    character_edits = levenshtein_distance(normalized_expected, normalized_actual)
    word_edits = levenshtein_distance(expected_words, actual_words)
    raw_cer = _error_rate(raw_edits, len(expected), len(actual))
    cer = _error_rate(character_edits, len(normalized_expected), len(normalized_actual))
    wer = _error_rate(word_edits, len(expected_words), len(actual_words))
    return {
        "raw_character_error_rate": raw_cer,
        "normalized_character_error_rate": cer,
        "word_error_rate": wer,
        "character_edit_distance": character_edits,
        "word_edit_distance": word_edits,
        "character_accuracy": max(0.0, 1.0 - cer),
        "word_accuracy": max(0.0, 1.0 - wer),
        "exact_match": expected == actual,
        "normalized_exact_match": normalized_expected == normalized_actual,
        "expected_character_count": len(normalized_expected),
        "actual_character_count": len(normalized_actual),
        "expected_word_count": len(expected_words),
        "actual_word_count": len(actual_words),
        "empty_output": not normalized_actual,
        **question_number_metrics(expected, actual),
    }


# Friendly aliases for callers that prefer a shorter verb.
ocr_metrics = calculate_ocr_metrics
compute_metrics = calculate_ocr_metrics
calculate_metrics = calculate_ocr_metrics


def character_edit_distance(expected: str, actual: str) -> int:
    return levenshtein_distance(normalize_ocr_text(expected), normalize_ocr_text(actual))


def word_edit_distance(expected: str, actual: str) -> int:
    return levenshtein_distance(normalize_ocr_text(expected).split(), normalize_ocr_text(actual).split())


def raw_character_error_rate(expected: str, actual: str) -> float:
    return _error_rate(levenshtein_distance(expected, actual), len(expected), len(actual))


def normalized_character_error_rate(expected: str, actual: str) -> float:
    normalized_expected, normalized_actual = normalize_ocr_text(expected), normalize_ocr_text(actual)
    return _error_rate(levenshtein_distance(normalized_expected, normalized_actual), len(normalized_expected), len(normalized_actual))


def word_error_rate(expected: str, actual: str) -> float:
    expected_words, actual_words = normalize_ocr_text(expected).split(), normalize_ocr_text(actual).split()
    return _error_rate(levenshtein_distance(expected_words, actual_words), len(expected_words), len(actual_words))


def _micro_rate(edits: int, expected: int, actual: int) -> float:
    return _error_rate(edits, expected, actual)


def _percentile(values: list[float], percentile: float) -> float | None:
    """Linear-interpolated percentile (the common R-7/NumPy default)."""
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * percentile
    lower, upper = math.floor(position), math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def aggregate_metrics(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate per-image metrics, optionally including operational fields."""
    if not rows:
        return {
            "macro_average_cer": None, "macro_average_wer": None,
            "micro_cer": None, "micro_wer": None, "success_rate": None,
            "empty_output_rate": None, "median_latency_ms": None,
            "p95_latency_ms": None, "total_pages": 0,
            "total_expected_characters": 0, "total_expected_words": 0,
        }
    char_count = sum(int(row.get("expected_character_count", 0)) for row in rows)
    word_count = sum(int(row.get("expected_word_count", 0)) for row in rows)
    actual_chars = sum(int(row.get("actual_character_count", 0)) for row in rows)
    actual_words = sum(int(row.get("actual_word_count", 0)) for row in rows)
    latencies = [float(row["latency_ms"]) for row in rows if row.get("latency_ms") is not None]
    result = {
        "macro_average_cer": mean(float(row["normalized_character_error_rate"]) for row in rows),
        "macro_average_wer": mean(float(row["word_error_rate"]) for row in rows),
        "micro_cer": _micro_rate(sum(int(row["character_edit_distance"]) for row in rows), char_count, actual_chars),
        "micro_wer": _micro_rate(sum(int(row["word_edit_distance"]) for row in rows), word_count, actual_words),
        "success_rate": sum(bool(row.get("success", True)) for row in rows) / len(rows),
        "empty_output_rate": sum(bool(row.get("empty_output", False)) for row in rows) / len(rows),
        "median_latency_ms": median(latencies) if latencies else None,
        "p95_latency_ms": _percentile(latencies, 0.95),
        "total_pages": sum(int(row.get("page_count", 0)) for row in rows),
        "total_expected_characters": char_count,
        "total_expected_words": word_count,
    }
    # Concise aliases make report consumption less coupled to display wording.
    result["macro_cer"] = result["macro_average_cer"]
    result["macro_wer"] = result["macro_average_wer"]
    result["total_expected_character_count"] = result["total_expected_characters"]
    result["total_expected_word_count"] = result["total_expected_words"]
    return result


def load_benchmark_manifest(
    manifest_path: str | Path,
    repository_root: str | Path | None = None,
) -> list[dict[str, Any]]:
    """Load and validate a benchmark manifest without reading image contents."""
    path = Path(manifest_path).resolve()
    root = Path(repository_root).resolve() if repository_root else path.parent.parent.resolve()
    payload = json.loads(path.read_text(encoding="utf-8"))
    entries = payload.get("samples") if isinstance(payload, dict) else payload
    if not isinstance(entries, list):
        raise ValueError("Benchmark manifest must be a list or contain a 'samples' list")
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValueError(f"Manifest entry {index} must be an object")
        sample_id = entry.get("id") or entry.get("sample_id")
        if not isinstance(sample_id, str) or not sample_id.strip():
            raise ValueError(f"Manifest entry {index} has no stable ID")
        if sample_id in seen:
            raise ValueError(f"Duplicate benchmark sample ID: {sample_id}")
        seen.add(sample_id)
        for field in ("image_path", "ground_truth_path"):
            relative = Path(entry.get(field, ""))
            if not str(relative) or relative.is_absolute():
                raise ValueError(f"{field} for {sample_id} must be a relative path")
            resolved = (root / relative).resolve()
            try:
                resolved.relative_to(root)
            except ValueError as exc:
                raise ValueError(f"{field} for {sample_id} escapes the repository") from exc
            if not resolved.is_file():
                raise ValueError(f"Missing {field} for {sample_id}: {relative}")
            if field == "ground_truth_path" and not resolved.read_text(encoding="utf-8").strip():
                raise ValueError(f"Empty ground truth for {sample_id}: {relative}")
    return entries


load_manifest = load_benchmark_manifest
