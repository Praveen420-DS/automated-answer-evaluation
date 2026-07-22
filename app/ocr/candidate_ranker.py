from app.ocr.code_quality import code_quality_score
from app.ocr.syntax_validator import syntax_score


def normalize_confidence(confidence):
    """
    Convert Tesseract confidence from percentage
    into a 0-1 range.
    """

    return max(0.0, min(confidence / 100.0, 1.0))


def rank_candidate(
    text: str,
    confidence: float
) -> float:
    """
    Calculate a code-aware ranking score.

    Components:
    1. OCR confidence
    2. Code quality
    3. Python syntax validity
    """

    confidence_score = normalize_confidence(
        confidence
    )

    quality_score = code_quality_score(
        text
    )

    syntax_quality = syntax_score(
        text
    )

    # Weighted ranking
    final_score = (
        0.30 * confidence_score
        + 0.35 * quality_score
        + 0.35 * syntax_quality
    )

    return final_score


def rank_candidates(candidates):
    """
    Rank multiple OCR candidates.

    Expected candidate format:

    {
        "method": "Otsu",
        "psm": 6,
        "text": "...",
        "confidence": 45.5
    }

    Returns candidates sorted by ranking score.
    """

    ranked = []

    for candidate in candidates:

        score = rank_candidate(
            candidate["text"],
            candidate["confidence"]
        )

        result = candidate.copy()

        result["ranking_score"] = score

        ranked.append(result)

    ranked.sort(
        key=lambda item: item["ranking_score"],
        reverse=True
    )

    return ranked


if __name__ == "__main__":

    candidates = [
        {
            "method": "Original",
            "psm": 6,
            "text": "def test(array): return array",
            "confidence": 50
        },
        {
            "method": "Otsu",
            "psm": 11,
            "text": "random unreadable text",
            "confidence": 70
        }
    ]

    results = rank_candidates(
        candidates
    )

    for result in results:
        print(
            result["method"],
            result["ranking_score"]
        )