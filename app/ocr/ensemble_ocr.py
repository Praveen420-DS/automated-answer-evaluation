from pathlib import Path
from typing import List, Dict, Any

from app.ocr.adaptive_ocr import run_all_ocr_candidates
from app.ocr.code_postprocessor import postprocess_code
from app.ocr.code_quality import code_quality_score
from app.ocr.candidate_ranker import rank_candidate


def select_best_candidate(
    candidates: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Select the best OCR candidate using:
    1. OCR confidence
    2. Code quality
    3. Candidate ranking score
    """

    if not candidates:
        raise ValueError("No OCR candidates available")

    ranked_candidates = []

    for candidate in candidates:
        text = candidate.get("text", "")

        confidence = candidate.get(
            "confidence",
            candidate.get("conf", 0.0)
        )

        method = candidate.get(
            "method",
            "Unknown"
        )

        psm = candidate.get(
            "psm",
            6
        )

        # Clean OCR text
        processed_text = postprocess_code(text)

        # Calculate code quality
        quality = code_quality_score(processed_text)

        # Calculate final ranking
        ranking = rank_candidate(
            processed_text,
            confidence
        )

        # Add code quality influence
        final_score = (
            0.50 * ranking
            + 0.30 * quality
            + 0.20 * (confidence / 100.0)
        )

        ranked_candidates.append(
            {
                "method": method,
                "psm": psm,
                "confidence": confidence,
                "original_text": text,
                "processed_text": processed_text,
                "quality": quality,
                "ranking_score": final_score,
            }
        )

    ranked_candidates.sort(
        key=lambda item: item["ranking_score"],
        reverse=True
    )

    return ranked_candidates[0]


def extract_text_ensemble(
    image_path: str
) -> Dict[str, Any]:
    """
    Run multiple OCR configurations,
    rank all candidates,
    and return the best result.
    """

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    print("=" * 60)
    print(
        f"ENSEMBLE OCR: {image_path.name}"
    )
    print("=" * 60)

    # Run all OCR configurations
    candidates = run_all_ocr_candidates(
        str(image_path)
    )

    # Safety check
    if not candidates:
        raise ValueError(
            "OCR engine returned no candidates"
        )

    print(
        f"Total OCR candidates: {len(candidates)}"
    )

    # Select best candidate
    best = select_best_candidate(
        candidates
    )

    print("-" * 60)
    print(
        f"SELECTED METHOD : "
        f"{best['method']}"
    )
    print(
        f"SELECTED PSM    : "
        f"{best['psm']}"
    )
    print(
        f"Tesseract Conf. : "
        f"{best['confidence']:.2f}%"
    )
    print(
        f"Code Quality    : "
        f"{best['quality']:.4f}"
    )
    print(
        f"Ranking Score   : "
        f"{best['ranking_score']:.4f}"
    )
    print("=" * 60)

    return best


if __name__ == "__main__":

    # Project root
    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    # Sample image
    image_path = (
        PROJECT_ROOT
        / "tests"
        / "samples"
        / "Closest10.JPEG"
    )

    try:

        result = extract_text_ensemble(
            str(image_path)
        )

        print()
        print("=" * 60)
        print("FINAL ENSEMBLE OCR TEXT")
        print("=" * 60)

        print(
            result["processed_text"]
        )

    except Exception as error:

        print()
        print("=" * 60)
        print("ENSEMBLE OCR FAILED")
        print("=" * 60)

        print(
            f"Error: {error}"
        )