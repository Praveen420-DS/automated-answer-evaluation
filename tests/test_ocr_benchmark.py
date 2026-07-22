from pathlib import Path
import cv2
import pytesseract
import difflib
import re


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SAMPLES_DIR = BASE_DIR / "tests" / "samples"
EXPECTED_DIR = BASE_DIR / "tests" / "expected"
RESULTS_DIR = BASE_DIR / "tests" / "benchmark_results"


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Normalize text before comparison.

    This reduces differences caused by:
    - Uppercase/lowercase
    - Extra spaces
    - Line breaks
    """

    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# SIMILARITY CALCULATION
# ============================================================

def calculate_similarity(expected, actual):
    """
    Calculate similarity between expected text
    and OCR-generated text.
    """

    expected_normalized = normalize_text(expected)
    actual_normalized = normalize_text(actual)

    return (
        difflib.SequenceMatcher(
            None,
            expected_normalized,
            actual_normalized
        ).ratio()
        * 100
    )


# ============================================================
# PREPROCESSING METHODS
# ============================================================

def preprocess_original(image):
    """
    Original image without preprocessing.
    """
    return image


def preprocess_grayscale(image):
    """
    Convert image to grayscale.
    """
    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


def preprocess_upscale(image):
    """
    Convert to grayscale and upscale 2x.
    """

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    scaled = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    return scaled


def preprocess_clahe(image):
    """
    Grayscale + 2x upscaling + CLAHE.
    """

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    scaled = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(scaled)

    return enhanced


def preprocess_otsu(image):
    """
    Grayscale + 2x upscaling + Otsu thresholding.
    """

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    scaled = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    _, thresholded = cv2.threshold(
        scaled,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresholded


def preprocess_adaptive(image):
    """
    Grayscale + 2x upscaling +
    adaptive thresholding.
    """

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    scaled = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    thresholded = cv2.adaptiveThreshold(
        scaled,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return thresholded


# ============================================================
# PREPROCESSING CONFIGURATIONS
# ============================================================

PREPROCESSING_METHODS = {
    "Original": preprocess_original,
    "Grayscale": preprocess_grayscale,
    "Upscale": preprocess_upscale,
    "CLAHE": preprocess_clahe,
    "Otsu": preprocess_otsu,
    "Adaptive": preprocess_adaptive,
}


# ============================================================
# OCR FUNCTION
# ============================================================

def run_ocr(image, psm_mode):
    """
    Run Tesseract OCR using selected PSM mode.
    """

    config = f"--oem 3 --psm {psm_mode}"

    text = pytesseract.image_to_string(
        image,
        config=config
    )

    return text


# ============================================================
# MAIN BENCHMARK
# ============================================================

def main():

    print("=" * 70)
    print("                 OCR CONFIGURATION BENCHMARK")
    print("=" * 70)

    # Create benchmark result directory
    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Find sample images
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
            "ERROR: No images found in tests/samples/"
        )

        return

    # PSM modes to test
    psm_modes = [
        6,
        11,
    ]

    # Store benchmark results
    benchmark_results = []

    # ========================================================
    # LOOP THROUGH PREPROCESSING METHODS
    # ========================================================

    for method_name, preprocess_function in PREPROCESSING_METHODS.items():

        for psm_mode in psm_modes:

            print()
            print("-" * 70)

            print(
                f"Testing: {method_name} + PSM {psm_mode}"
            )

            print("-" * 70)

            total_similarity = 0
            processed_images = 0

            # =================================================
            # PROCESS EACH IMAGE
            # =================================================

            for image_path in image_files:

                expected_file = (
                    EXPECTED_DIR
                    / f"{image_path.stem}.txt"
                )

                if not expected_file.exists():

                    print(
                        f"SKIPPED: No expected file "
                        f"for {image_path.name}"
                    )

                    continue

                # Read original image
                image = cv2.imread(
                    str(image_path)
                )

                if image is None:

                    print(
                        f"FAILED: Could not read "
                        f"{image_path.name}"
                    )

                    continue

                # Apply preprocessing
                processed_image = preprocess_function(
                    image
                )

                # Run OCR
                actual_text = run_ocr(
                    processed_image,
                    psm_mode
                )

                # Read expected text
                expected_text = (
                    expected_file.read_text(
                        encoding="utf-8"
                    )
                )

                # Calculate similarity
                similarity = calculate_similarity(
                    expected_text,
                    actual_text
                )

                total_similarity += similarity

                processed_images += 1

                print(
                    f"{image_path.name:<20} "
                    f"{similarity:>7.2f}%"
                )

                # Save individual OCR result
                safe_method_name = (
                    method_name
                    .lower()
                    .replace(" ", "_")
                )

                output_filename = (
                    f"{image_path.stem}_"
                    f"{safe_method_name}_"
                    f"psm{psm_mode}.txt"
                )

                output_path = (
                    RESULTS_DIR
                    / output_filename
                )

                output_path.write_text(
                    actual_text,
                    encoding="utf-8"
                )

            # =================================================
            # CALCULATE AVERAGE
            # =================================================

            if processed_images > 0:

                average_similarity = (
                    total_similarity
                    / processed_images
                )

            else:

                average_similarity = 0

            # Store result
            benchmark_results.append(
                {
                    "method": method_name,
                    "psm": psm_mode,
                    "accuracy": average_similarity,
                }
            )

            print()
            print(
                f"Average Similarity: "
                f"{average_similarity:.2f}%"
            )


    # ========================================================
    # FINAL RESULTS
    # ========================================================

    print()
    print("=" * 70)
    print("                 FINAL BENCHMARK RESULTS")
    print("=" * 70)

    # Sort from highest to lowest
    benchmark_results.sort(
        key=lambda x: x["accuracy"],
        reverse=True
    )

    print()

    print(
        f"{'Rank':<6}"
        f"{'Method':<20}"
        f"{'PSM':<8}"
        f"{'Similarity':<12}"
    )

    print("-" * 70)

    for index, result in enumerate(
        benchmark_results,
        start=1
    ):

        print(
            f"{index:<6}"
            f"{result['method']:<20}"
            f"{result['psm']:<8}"
            f"{result['accuracy']:.2f}%"
        )

    # ========================================================
    # BEST CONFIGURATION
    # ========================================================

    if benchmark_results:

        best = benchmark_results[0]

        print()
        print("=" * 70)
        print("                 BEST CONFIGURATION")
        print("=" * 70)

        print(
            f"Preprocessing : {best['method']}"
        )

        print(
            f"PSM Mode      : {best['psm']}"
        )

        print(
            f"Similarity    : "
            f"{best['accuracy']:.2f}%"
        )

        print("=" * 70)

        print()
        print(
            "Benchmark completed successfully."
        )

        print(
            "OCR results saved in:"
        )

        print(
            RESULTS_DIR
        )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()