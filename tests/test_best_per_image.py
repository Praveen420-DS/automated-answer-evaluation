from pathlib import Path
import csv


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_DIR = (
    BASE_DIR
    / "tests"
    / "benchmark_results"
)

OUTPUT_FILE = (
    BASE_DIR
    / "tests"
    / "best_per_image_results.csv"
)


# ============================================================
# CONFIGURATION
# ============================================================

PREPROCESSING_METHODS = [
    "Original",
    "Grayscale",
    "Upscale",
    "CLAHE",
    "Otsu",
    "Adaptive",
]

PSM_MODES = [
    6,
    11,
]


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():

    print("=" * 70)
    print("             BEST OCR CONFIGURATION PER IMAGE")
    print("=" * 70)

    if not RESULTS_DIR.exists():

        print()
        print(
            "ERROR: Benchmark results directory not found."
        )

        print(
            f"Expected directory: {RESULTS_DIR}"
        )

        print()
        print(
            "Run this command first:"
        )

        print(
            "python -m tests.test_ocr_benchmark"
        )

        return


    # ========================================================
    # FIND ALL OCR RESULT FILES
    # ========================================================

    result_files = list(
        RESULTS_DIR.glob("*.txt")
    )


    if not result_files:

        print()
        print(
            "ERROR: No benchmark OCR result files found."
        )

        return


    # ========================================================
    # STORE RESULTS
    # ========================================================

    all_results = []


    # ========================================================
    # PROCESS EACH IMAGE
    # ========================================================

    for result_file in result_files:

        filename = result_file.stem

        matched_method = None
        matched_psm = None


        # ----------------------------------------------------
        # Identify preprocessing method
        # ----------------------------------------------------

        for method in PREPROCESSING_METHODS:

            method_key = (
                method
                .lower()
                .replace(" ", "_")
            )

            if f"_{method_key}_" in filename:

                matched_method = method

                break


        # ----------------------------------------------------
        # Identify PSM mode
        # ----------------------------------------------------

        if "_psm6" in filename:

            matched_psm = 6

        elif "_psm11" in filename:

            matched_psm = 11


        # ----------------------------------------------------
        # Skip invalid files
        # ----------------------------------------------------

        if (
            matched_method is None
            or matched_psm is None
        ):

            continue


        # ----------------------------------------------------
        # Get image name
        # ----------------------------------------------------

        image_name = filename


        # Remove method name
        method_key = (
            matched_method
            .lower()
            .replace(" ", "_")
        )

        image_name = image_name.replace(
            f"_{method_key}",
            ""
        )


        # Remove PSM name
        image_name = image_name.replace(
            f"_psm{matched_psm}",
            ""
        )


        # ----------------------------------------------------
        # Find expected text
        # ----------------------------------------------------

        expected_file = (
            BASE_DIR
            / "tests"
            / "expected"
            / f"{image_name}.txt"
        )


        if not expected_file.exists():

            continue


        # ----------------------------------------------------
        # Read OCR result
        # ----------------------------------------------------

        actual_text = (
            result_file.read_text(
                encoding="utf-8"
            )
        )


        # ----------------------------------------------------
        # Read expected text
        # ----------------------------------------------------

        expected_text = (
            expected_file.read_text(
                encoding="utf-8"
            )
        )


        # ----------------------------------------------------
        # Calculate similarity
        # ----------------------------------------------------

        import difflib
        import re


        def normalize_text(text):

            text = text.lower()

            text = re.sub(
                r"\s+",
                " ",
                text
            )

            return text.strip()


        expected_normalized = (
            normalize_text(
                expected_text
            )
        )


        actual_normalized = (
            normalize_text(
                actual_text
            )
        )


        similarity = (
            difflib.SequenceMatcher(
                None,
                expected_normalized,
                actual_normalized
            ).ratio()
            * 100
        )


        # ----------------------------------------------------
        # Save result
        # ----------------------------------------------------

        all_results.append(
            {
                "image": image_name,
                "method": matched_method,
                "psm": matched_psm,
                "similarity": similarity,
            }
        )


    # ========================================================
    # FIND BEST CONFIGURATION FOR EACH IMAGE
    # ========================================================

    image_names = sorted(
        set(
            result["image"]
            for result in all_results
        )
    )


    best_results = []


    for image_name in image_names:

        image_results = [
            result
            for result in all_results
            if result["image"] == image_name
        ]


        if not image_results:

            continue


        best = max(
            image_results,
            key=lambda x: x["similarity"]
        )


        best_results.append(
            best
        )


    # ========================================================
    # PRINT RESULTS
    # ========================================================

    print()

    print(
        f"{'Image':<20}"
        f"{'Best Method':<20}"
        f"{'PSM':<8}"
        f"{'Similarity':<12}"
    )

    print("-" * 70)


    total_similarity = 0


    for result in best_results:

        print(
            f"{result['image']:<20}"
            f"{result['method']:<20}"
            f"{result['psm']:<8}"
            f"{result['similarity']:.2f}%"
        )


        total_similarity += (
            result["similarity"]
        )


    # ========================================================
    # CALCULATE ADAPTIVE AVERAGE
    # ========================================================

    if best_results:

        adaptive_average = (
            total_similarity
            / len(best_results)
        )

    else:

        adaptive_average = 0


    print()
    print("=" * 70)

    print(
        f"Images evaluated: "
        f"{len(best_results)}"
    )

    print(
        f"Adaptive OCR average: "
        f"{adaptive_average:.2f}%"
    )

    print("=" * 70)


    # ========================================================
    # SAVE CSV
    # ========================================================

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.writer(
            csv_file
        )


        writer.writerow(
            [
                "Image",
                "Best_Preprocessing",
                "Best_PSM",
                "Similarity_Percentage",
            ]
        )


        for result in best_results:

            writer.writerow(
                [
                    result["image"],
                    result["method"],
                    result["psm"],
                    f"{result['similarity']:.2f}",
                ]
            )


    print()

    print(
        "Results saved to:"
    )

    print(
        OUTPUT_FILE
    )


    # ========================================================
    # COMPARE WITH GLOBAL BEST
    # ========================================================

    global_best = 11.24


    print()
    print("=" * 70)
    print("                  COMPARISON")
    print("=" * 70)

    print(
        f"Single best configuration: "
        f"{global_best:.2f}%"
    )

    print(
        f"Adaptive per-image result: "
        f"{adaptive_average:.2f}%"
    )


    improvement = (
        adaptive_average
        - global_best
    )


    print(
        f"Difference: "
        f"{improvement:+.2f} percentage points"
    )


    if adaptive_average > global_best:

        print()

        print(
            "RESULT: Adaptive strategy is BETTER."
        )

        print(
            "We should consider using "
            "per-image configuration selection."
        )


    elif adaptive_average < global_best:

        print()

        print(
            "RESULT: Single global configuration "
            "is currently BETTER."
        )

        print(
            "Keep Original + PSM 6 "
            "as the current baseline."
        )


    else:

        print()

        print(
            "RESULT: Both strategies have "
            "the same performance."
        )


    print("=" * 70)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()