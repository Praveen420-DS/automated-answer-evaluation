from pathlib import Path

from app.ocr.adaptive_ocr import extract_text_adaptive
import difflib
import re
def normalize_text(text):
    """
    Normalize text before comparison.
    """

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def calculate_similarity(expected, actual):
    """
    Calculate similarity between expected
    ground-truth text and OCR text.
    """

    expected_normalized = normalize_text(
        expected
    )

    actual_normalized = normalize_text(
        actual
    )

    return (
        difflib.SequenceMatcher(
            None,
            expected_normalized,
            actual_normalized
        ).ratio()
        * 100
    )
# ---------------------------------------------------------
# PROJECT DIRECTORIES
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

SAMPLES_DIR = BASE_DIR / "tests" / "samples"

EXPECTED_DIR = BASE_DIR / "tests" / "expected"


# ---------------------------------------------------------
# MAIN TEST
# ---------------------------------------------------------

def main():

    print("=" * 70)
    print("           AUTOMATIC ADAPTIVE OCR TEST")
    print("=" * 70)

    image_files = sorted(
        [
            file
            for file in SAMPLES_DIR.iterdir()
            if file.is_file()
            and file.suffix.lower()
            in {
                ".jpg",
                ".jpeg",
                ".png",
                ".bmp",
                ".tiff",
                ".webp",
            }
        ]
    )

    if not image_files:

        print(
            "ERROR: No sample images found."
        )

        return


    total_similarity = 0

    processed = 0


    # -----------------------------------------------------
    # PROCESS EVERY IMAGE
    # -----------------------------------------------------

    for image_path in image_files:

        print("\n")
        print("=" * 70)

        print(
            f"PROCESSING IMAGE: "
            f"{image_path.name}"
        )

        print("=" * 70)


        # ---------------------------------------------
        # Find expected ground truth
        # ---------------------------------------------

        expected_file = (
            EXPECTED_DIR
            / f"{image_path.stem}.txt"
        )


        if not expected_file.exists():

            print(
                "SKIPPED: Ground-truth file "
                "not found."
            )

            continue


        # ---------------------------------------------
        # Run adaptive OCR
        # ---------------------------------------------

        result = extract_text_adaptive(
            str(image_path)
        )


        # ---------------------------------------------
        # Read ground truth
        # ---------------------------------------------

        expected_text = (
            expected_file.read_text(
                encoding="utf-8"
            )
        )


        actual_text = result["text"]


        # ---------------------------------------------
        # Calculate actual similarity
        # ---------------------------------------------

        similarity = calculate_similarity(
            expected_text,
            actual_text
        )


        # ---------------------------------------------
        # Display result
        # ---------------------------------------------

        print()

        print(
            f"Automatically selected method: "
            f"{result['method']}"
        )

        print(
            f"Automatically selected PSM: "
            f"{result['psm']}"
        )

        print(
            f"Tesseract confidence: "
            f"{result['confidence']:.2f}%"
        )

        print(
            f"Actual ground-truth similarity: "
            f"{similarity:.2f}%"
        )


        total_similarity += similarity

        processed += 1


    # -----------------------------------------------------
    # FINAL RESULT
    # -----------------------------------------------------

    if processed > 0:

        average_similarity = (
            total_similarity
            / processed
        )


        print("\n")

        print("=" * 70)

        print(
            "          AUTOMATIC ADAPTIVE OCR RESULTS"
        )

        print("=" * 70)

        print(
            f"Images evaluated: "
            f"{processed}"
        )

        print(
            f"Average actual similarity: "
            f"{average_similarity:.2f}%"
        )

        print("=" * 70)


        print()

        print(
            "COMPARISON"
        )

        print("-" * 70)

        print(
            "Best single configuration : "
            "11.24%"
        )

        print(
            "Ground-truth adaptive      : "
            "17.92%"
        )

        print(
            "Automatic confidence       : "
            f"{average_similarity:.2f}%"
        )

        print("=" * 70)


    else:

        print(
            "\nNo images were evaluated."
        )


# ---------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":

    main()