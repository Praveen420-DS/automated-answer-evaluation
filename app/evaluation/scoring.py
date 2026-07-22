from __future__ import annotations

import difflib
import re


def normalize_text(text: str | None) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text).lower()).strip()


def character_similarity(actual: str, expected: str) -> float:
    actual_normalized = normalize_text(actual)
    expected_normalized = normalize_text(expected)
    if not actual_normalized or not expected_normalized:
        return 0.0
    return difflib.SequenceMatcher(None, actual_normalized, expected_normalized).ratio()


def token_similarity(actual: str, expected: str) -> float:
    actual_tokens = set(normalize_text(actual).split())
    expected_tokens = set(normalize_text(expected).split())
    if not actual_tokens or not expected_tokens:
        return 0.0
    return len(actual_tokens & expected_tokens) / len(actual_tokens | expected_tokens)


def overall_similarity(actual: str, expected: str) -> float:
    return (0.7 * character_similarity(actual, expected)) + (
        0.3 * token_similarity(actual, expected)
    )


def score_similarity(actual: str, expected: str, maximum_score: float) -> float:
    return round(overall_similarity(actual, expected) * maximum_score, 2)
