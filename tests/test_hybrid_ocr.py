from pathlib import Path

import cv2
import pytesseract

from app.ocr.code_postprocessor import postprocess_code
from app.ocr.candidate_ranker import rank_candidate


BASE_DIR = Path(__file__).resolve().parent.parent

SAMPLES_DIR = BASE_DIR / "tests" / "samples"
EXPECTED_DIR = BASE_DIR / "tests" / "expected"


def normalize_text(text):
    """
    Normalize text before similarity comparison.
    """

    text = text.lower()

    text = " ".join(
        text.split()
    )

    return text.strip()


def calculate_similarity(expected, actual):
    """
    Calculate similarity between expected
    and OCR output.
    """

    import difflib

    expected = normalize_text(expected)

    actual = normalize_text(actual)

    return (
        difflib.SequenceMatcher(
            None,
            expected,
            actual
        ).ratio()
        * 100
    )


def preprocess_variants(image):
    """
    Generate multiple preprocessing variants.
    """

    variants = {}

    # Original
    variants["Original"] = image

    # Grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    variants["Grayscale"] = gray

    # Upscale
    upscale = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    variants["Upscale"] = upscale

    # CLAHE
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    clahe_image = clahe.apply(
        upscale
    )

    variants["CLAHE"] = clahe_image

    # Otsu threshold
    _, otsu = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY
        + cv2.THRESH_OTSU
    )

    variants["Otsu"] = otsu

    # Adaptive threshold
    adaptive = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    variants["Adaptive"] = adaptive

    return variants


def get_ocr_result(image, psm):
    """
    Run Tesseract OCR and return:
    text + confidence.
    """

    data = pytesseract.image_to_data(
        image,
        config=f"--oem 3 --psm {psm}",
        output_type=pytesseract.Output.DICT
    )

    texts = []

    confidences = []

    for text, confidence in zip(
        data["text"],
        data["conf"]
    ):

        text = text.strip()

        if text:

            texts.append(text)

            try:

                confidence = float(
                    confidence
                )

                if confidence >= 0:

                    confidences.append(
                        confidence
                    )

            except ValueError:

                pass

    result_text = " ".join(
        texts
    )

    if confidences:

        average_confidence = (
            sum(confidences)
            / len(confidences)
        )

    else:

        average_confidence = 0.0

    return (
        result_text,
        average_confidence
    )


def process_image(image_path):
    """
    Process one image using all
    preprocessing + PSM combinations.
    """

    image = cv2.imread(
        str(image_path)
    )

    if image is None:

        raise FileNotFoundError(
            f"Could not read image: {image_path}"
        )

    variants = preprocess_variants(
        image
    )

    candidates = []

    for method, processed_image in variants.items():

        for psm in [6, 11]:

            raw_text, confidence = (
                get_ocr_result(
                    processed_image,
                    psm
                )
            )

            cleaned_text = (
                postprocess_code(
                    raw_text
                )
            )

            ranking_score = (
                rank_candidate(
                    cleaned_text,
                    confidence
                )
            )

            candidates.append(
                {
                    "method": method,
                    "psm": psm,
                    "confidence": confidence,
                    "text": cleaned_text,
                    "ranking_score": ranking_score
                }
            )

    candidates.sort(
        key=lambda x: x["ranking_score"],
        reverse=True
    )

    return candidates


def main():

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
                ".webp"
            }
        ]
    )

    if not image_files:

        print(
            "No images found."
        )

        return

    total_similarity = 0

    processed = 0

    print("=" * 70)

    print(
        "              HYBRID OCR EVALUATION"
    )

    print("=" * 70)

    for image_path in image_files:

        print("\n")

        print(
            "=" * 70
        )

        print(
            f"IMAGE: {image_path.name}"
        )

        print(
            "=" * 70
        )

        try:

            candidates = process_image(
                image_path
            )

            best = candidates[0]

            expected_file = (
                EXPECTED_DIR
                / f"{image_path.stem}.txt"
            )

            if expected_file.exists():

                expected_text = (
                    expected_file.read_text(
                        encoding="utf-8"
                    )
                )

                similarity = (
                    calculate_similarity(
                        expected_text,
                        best["text"]
                    )
                )

            else:

                similarity = 0.0

            total_similarity += similarity

            processed += 1

            print(
                f"Selected Method : "
                f"{best['method']}"
            )

            print(
                f"Selected PSM    : "
                f"{best['psm']}"
            )

            print(
                f"Tesseract Conf. : "
                f"{best['confidence']:.2f}%"
            )

            print(
                f"Ranking Score    : "
                f"{best['ranking_score']:.4f}"
            )

            print(
                f"Actual Similarity: "
                f"{similarity:.2f}%"
            )

            print(
                "\nTop 3 Candidates:"
            )

            for index, candidate in enumerate(
                candidates[:3],
                start=1
            ):

                print(
                    f"{index}. "
                    f"{candidate['method']} "
                    f"| PSM {candidate['psm']} "
                    f"| Confidence "
                    f"{candidate['confidence']:.2f}% "
                    f"| Rank "
                    f"{candidate['ranking_score']:.4f}"
                )

            print(
                "\nSelected OCR Text:"
            )

            print(
                best["text"][:1000]
            )

        except Exception as error:

            print(
                f"ERROR: {error}"
            )

    print("\n")

    print("=" * 70)

    print(
        "              HYBRID OCR SUMMARY"
    )

    print("=" * 70)

    if processed > 0:

        average_similarity = (
            total_similarity
            / processed
        )

        print(
            f"Images evaluated : "
            f"{processed}"
        )

        print(
            f"Hybrid OCR Average: "
            f"{average_similarity:.2f}%"
        )

        print()

        print(
            "Previous Results:"
        )

        print(
            "Single best configuration : 11.24%"
        )

        print(
            "Ground-truth best per image: 17.92%"
        )

        print(
            "Automatic confidence       : 8.59%"
        )

        print()

        difference = (
            average_similarity
            - 11.24
        )

        print(
            f"Hybrid improvement vs "
            f"single configuration: "
            f"{difference:+.2f} percentage points"
        )

    else:

        print(
            "No images evaluated."
        )

    print(
        "=" * 70
    )


if __name__ == "__main__":

    main()