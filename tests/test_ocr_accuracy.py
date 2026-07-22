from pathlib import Path
import difflib
import re


BASE_DIR = Path(__file__).resolve().parent.parent
OCR_DIR = BASE_DIR / "tests" / "ocr_results"
EXPECTED_DIR = BASE_DIR / "tests" / "expected"


def normalize_text(text):
    """
    Normalize text before comparison.
    This removes differences caused by:
    - uppercase/lowercase
    - extra spaces
    - line breaks
    """
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def calculate_similarity(expected, actual):
    """
    Calculate text similarity using SequenceMatcher.
    Returns a percentage from 0 to 100.
    """
    expected_normalized = normalize_text(expected)
    actual_normalized = normalize_text(actual)

    return difflib.SequenceMatcher(
        None,
        expected_normalized,
        actual_normalized
    ).ratio() * 100


def main():

    expected_files = sorted(EXPECTED_DIR.glob("*.txt"))

    if not expected_files:
        print("ERROR: No expected ground-truth files found.")
        return

    total_accuracy = 0
    processed = 0

    print("=" * 60)
    print("OCR ACCURACY EVALUATION")
    print("=" * 60)

    for expected_file in expected_files:

        image_name = expected_file.stem

        ocr_file = OCR_DIR / f"{image_name}_ocr.txt"

        if not ocr_file.exists():
            print(f"\nSKIPPED: {image_name}")
            print("OCR result file not found.")
            continue

        expected_text = expected_file.read_text(
            encoding="utf-8"
        )

        actual_text = ocr_file.read_text(
            encoding="utf-8"
        )

        accuracy = calculate_similarity(
            expected_text,
            actual_text
        )

        total_accuracy += accuracy
        processed += 1

        print(f"\nImage: {image_name}")
        print(f"Expected characters: {len(expected_text)}")
        print(f"OCR characters:      {len(actual_text)}")
        print(f"Similarity:          {accuracy:.2f}%")

    if processed > 0:

        overall_accuracy = total_accuracy / processed

        print("\n" + "=" * 60)
        print(f"Images evaluated: {processed}")
        print(f"Overall OCR similarity: {overall_accuracy:.2f}%")
        print("=" * 60)

    else:

        print("\nNo images were evaluated.")


if __name__ == "__main__":
    main()