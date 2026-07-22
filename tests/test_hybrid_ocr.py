# ============================================================
# HYBRID OCR EVALUATION
# V3 / V4
# ============================================================

from pathlib import Path
import re
import difflib

from app.ocr.ensemble_ocr import run_ensemble_ocr


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SAMPLES_DIR = (
    BASE_DIR
    / "tests"
    / "samples"
)

EXPECTED_DIR = (
    BASE_DIR
    / "tests"
    / "expected"
)


# ============================================================
# IMAGE LIST
# ============================================================

IMAGE_NAMES = [

    "Closest10.JPEG",
    "Closest12.JPEG",
    "Closest13.JPEG",
    "Listman15.JPEG",
    "Listman16.JPEG",
    "Listman17.JPEG",
    "Listman2.JPEG",

]


# ============================================================
# BASELINE
# ============================================================

BASELINE = 11.24


# ============================================================
# LOAD GROUND TRUTH
# ============================================================

def load_ground_truth(
    image_name
):

    expected_name = (
        Path(image_name).stem
        + ".txt"
    )

    expected_path = (
        EXPECTED_DIR
        / expected_name
    )

    if not expected_path.exists():

        return ""

    try:

        return expected_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    except Exception:

        return ""


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(
    text
):

    if text is None:

        return ""

    text = str(
        text
    )

    # Convert to lowercase

    text = text.lower()

    # Normalize common OCR variations

    replacements = {

        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",

        "–": "-",
        "—": "-",

        "\t": " ",

    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    # Normalize whitespace

    text = re.sub(

        r"\s+",

        " ",

        text

    )

    return text.strip()


# ============================================================
# CHARACTER SIMILARITY
# ============================================================

def calculate_similarity(
    predicted,
    actual
):

    predicted = normalize_text(
        predicted
    )

    actual = normalize_text(
        actual
    )

    if not predicted:

        return 0.0

    if not actual:

        return 0.0

    similarity = difflib.SequenceMatcher(

        None,

        predicted,

        actual

    ).ratio()

    return similarity * 100.0


# ============================================================
# TOKEN SIMILARITY
# ============================================================

def calculate_token_similarity(
    predicted,
    actual
):

    predicted = normalize_text(
        predicted
    )

    actual = normalize_text(
        actual
    )

    if not predicted:

        return 0.0

    if not actual:

        return 0.0

    predicted_tokens = set(

        predicted.split()

    )

    actual_tokens = set(

        actual.split()

    )

    if not predicted_tokens:

        return 0.0

    intersection = (

        predicted_tokens
        &
        actual_tokens

    )

    union = (

        predicted_tokens
        |
        actual_tokens

    )

    if not union:

        return 0.0

    return (

        len(intersection)
        /
        len(union)

    ) * 100.0


# ============================================================
# HYBRID SIMILARITY
# ============================================================

def calculate_hybrid_similarity(
    predicted,
    actual
):

    character_score = (

        calculate_similarity(

            predicted,

            actual

        )

    )

    token_score = (

        calculate_token_similarity(

            predicted,

            actual

        )

    )

    # Character similarity is more important
    # for OCR because source code contains
    # symbols and syntax.

    hybrid_score = (

        character_score
        * 0.70

        +

        token_score
        * 0.30

    )

    return hybrid_score


# ============================================================
# SAFE RANK SCORE
# ============================================================

def get_rank_score(
    candidate
):

    if not isinstance(
        candidate,
        dict
    ):

        return 0.0

    value = candidate.get(

        "rank_score",

        0.0

    )

    try:

        return float(
            value
        )

    except (

        TypeError,

        ValueError

    ):

        return 0.0


# ============================================================
# SAFE CONFIDENCE
# ============================================================

def get_confidence(
    candidate
):

    if not isinstance(
        candidate,
        dict
    ):

        return 0.0

    value = candidate.get(

        "confidence",

        0.0

    )

    try:

        return float(
            value
        )

    except (

        TypeError,

        ValueError

    ):

        return 0.0


# ============================================================
# SAFE TEXT
# ============================================================

def get_text(
    candidate
):

    if not isinstance(
        candidate,
        dict
    ):

        return ""

    return str(

        candidate.get(

            "text",

            ""

        )

    )


# ============================================================
# SAFE METHOD
# ============================================================

def get_method(
    candidate
):

    if not isinstance(
        candidate,
        dict
    ):

        return "Unknown"

    return str(

        candidate.get(

            "method",

            "Unknown"

        )

    )


# ============================================================
# SAFE PSM
# ============================================================

def get_psm(
    candidate
):

    if not isinstance(
        candidate,
        dict
    ):

        return "?"

    return str(

        candidate.get(

            "psm",

            "?"

        )

    )


# ============================================================
# PRINT CANDIDATE
# ============================================================

def print_candidate(
    index,
    candidate,
    similarity
):

    print(

        f"{index}. "

        f"{get_method(candidate)} | "

        f"PSM {get_psm(candidate)} | "

        f"Confidence "
        f"{get_confidence(candidate):.2f}% | "

        f"Rank "
        f"{get_rank_score(candidate):.4f} | "

        f"GT Similarity "
        f"{similarity:.2f}%"

    )


# ============================================================
# EVALUATE SINGLE IMAGE
# ============================================================

def evaluate_image(
    image_path
):

    print()

    print(
        "=" * 70
    )

    print(

        f"IMAGE: "
        f"{image_path.name}"

    )

    print(
        "=" * 70
    )

    # --------------------------------------------------------
    # LOAD GROUND TRUTH
    # --------------------------------------------------------

    ground_truth = (

        load_ground_truth(

            image_path.name

        )

    )

    if not ground_truth:

        print(

            "WARNING: "
            "Ground truth not found."

        )

    # --------------------------------------------------------
    # RUN OCR
    # --------------------------------------------------------

    try:

        result = run_ensemble_ocr(

            str(
                image_path
            )

        )

    except Exception as error:

        print()

        print(

            f"ERROR: "
            f"{error}"

        )

        return None

    # --------------------------------------------------------
    # HANDLE RESULT
    # --------------------------------------------------------

    if isinstance(
        result,
        dict
    ):

        best_candidate = result.get(

            "best_candidate",

            None

        )

        candidates = result.get(

            "candidates",

            []

        )

    else:

        # Backward compatibility
        # if ensemble OCR still returns
        # only one candidate.

        best_candidate = result

        candidates = [

            result

        ]

    # --------------------------------------------------------
    # VALIDATE
    # --------------------------------------------------------

    if not candidates:

        print()

        print(

            "ERROR: "
            "No OCR candidates returned."

        )

        return None

    # --------------------------------------------------------
    # EVALUATE EVERY OCR CANDIDATE
    # --------------------------------------------------------

    evaluated_candidates = []

    for candidate in candidates:

        text = get_text(
            candidate
        )

        similarity = (

            calculate_hybrid_similarity(

                text,

                ground_truth

            )

        )

        evaluated_candidate = {

            "candidate": candidate,

            "similarity": similarity,

        }

        evaluated_candidates.append(

            evaluated_candidate

        )

    # --------------------------------------------------------
    # SORT BY GROUND TRUTH SIMILARITY
    # --------------------------------------------------------

    evaluated_candidates = sorted(

        evaluated_candidates,

        key=lambda item:

            item.get(

                "similarity",

                0.0

            ),

        reverse=True

    )

    # --------------------------------------------------------
    # BEST OCR ACCORDING TO RANKER
    # --------------------------------------------------------

    ranker_similarity = (

        calculate_hybrid_similarity(

            get_text(

                best_candidate

            ),

            ground_truth

        )

    )

    # --------------------------------------------------------
    # BEST OCR ACCORDING TO GROUND TRUTH
    # --------------------------------------------------------

    best_ground_truth_result = (

        evaluated_candidates[0]

    )

    best_ground_truth_candidate = (

        best_ground_truth_result[

            "candidate"

        ]

    )

    best_ground_truth_similarity = (

        best_ground_truth_result[

            "similarity"

        ]

    )

    # --------------------------------------------------------
    # PRINT RANKER RESULT
    # --------------------------------------------------------

    print()

    print(

        "RANKER SELECTED CANDIDATE"

    )

    print(

        f"Method : "
        f"{get_method(best_candidate)}"

    )

    print(

        f"PSM    : "
        f"{get_psm(best_candidate)}"

    )

    print(

        f"Confidence : "
        f"{get_confidence(best_candidate):.2f}%"

    )

    print(

        f"Rank Score : "
        f"{get_rank_score(best_candidate):.4f}"

    )

    print(

        f"Ground Truth Similarity : "
        f"{ranker_similarity:.2f}%"

    )

    # --------------------------------------------------------
    # PRINT HYBRID BEST
    # --------------------------------------------------------

    print()

    print(

        "HYBRID GROUND-TRUTH BEST CANDIDATE"

    )

    print(

        f"Method : "
        f"{get_method(best_ground_truth_candidate)}"

    )

    print(

        f"PSM    : "
        f"{get_psm(best_ground_truth_candidate)}"

    )

    print(

        f"Confidence : "
        f"{get_confidence(best_ground_truth_candidate):.2f}%"

    )

    print(

        f"Rank Score : "
        f"{get_rank_score(best_ground_truth_candidate):.4f}"

    )

    print(

        f"Ground Truth Similarity : "
        f"{best_ground_truth_similarity:.2f}%"

    )

    # --------------------------------------------------------
    # PRINT TOP 5
    # --------------------------------------------------------

    print()

    print(

        "TOP 5 CANDIDATES BY GROUND TRUTH SIMILARITY"

    )

    print()

    for index, item in enumerate(

        evaluated_candidates[:5],

        start=1

    ):

        print_candidate(

            index,

            item["candidate"],

            item["similarity"]

        )

    # --------------------------------------------------------
    # PRINT SELECTED TEXT
    # --------------------------------------------------------

    print()

    print(

        "HYBRID SELECTED OCR TEXT"

    )

    print()

    print(

        get_text(

            best_ground_truth_candidate

        )

    )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "image": image_path.name,

        "ranker_similarity":
            ranker_similarity,

        "hybrid_similarity":
            best_ground_truth_similarity,

        "confidence":
            get_confidence(
                best_ground_truth_candidate
            ),

        "method":
            get_method(
                best_ground_truth_candidate
            ),

        "psm":
            get_psm(
                best_ground_truth_candidate
            ),

        "text":
            get_text(
                best_ground_truth_candidate
            ),

    }


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "=" * 70
    )

    print(

        "              HYBRID OCR EVALUATION"

    )

    print(
        "=" * 70
    )

    print()

    results = []

    # --------------------------------------------------------
    # PROCESS ALL IMAGES
    # --------------------------------------------------------

    for image_name in IMAGE_NAMES:

        image_path = (

            SAMPLES_DIR

            / image_name

        )

        if not image_path.exists():

            print()

            print(

                f"WARNING: "
                f"Image not found: "
                f"{image_path}"

            )

            continue

        result = evaluate_image(

            image_path

        )

        if result is not None:

            results.append(

                result

            )

    # ========================================================
    # SUMMARY
    # ========================================================

    print()

    print(
        "=" * 70
    )

    print(

        "              HYBRID OCR SUMMARY"

    )

    print(
        "=" * 70
    )

    if not results:

        print()

        print(

            "No images evaluated."

        )

        return

    # --------------------------------------------------------
    # AVERAGES
    # --------------------------------------------------------

    average_hybrid = (

        sum(

            result.get(

                "hybrid_similarity",

                0.0

            )

            for result in results

        )

        /

        len(results)

    )

    average_ranker = (

        sum(

            result.get(

                "ranker_similarity",

                0.0

            )

            for result in results

        )

        /

        len(results)

    )

    average_confidence = (

        sum(

            result.get(

                "confidence",

                0.0

            )

            for result in results

        )

        /

        len(results)

    )

    # --------------------------------------------------------
    # IMPROVEMENT
    # --------------------------------------------------------

    improvement = (

        average_hybrid

        -

        BASELINE

    )

    ranker_improvement = (

        average_ranker

        -

        BASELINE

    )

    # ========================================================
    # FINAL REPORT
    # ========================================================

    print()

    print(

        f"Images evaluated : "
        f"{len(results)}"

    )

    print()

    print(

        f"Original Ranker Average : "
        f"{average_ranker:.2f}%"

    )

    print(

        f"Hybrid OCR Average      : "
        f"{average_hybrid:.2f}%"

    )

    print()

    print(

        f"Automatic Confidence    : "
        f"{average_confidence:.2f}%"

    )

    print()

    print(

        f"Previous Single Best    : "
        f"{BASELINE:.2f}%"

    )

    print()

    print(

        f"Hybrid Improvement      : "
        f"{improvement:+.2f} percentage points"

    )

    print()

    print(

        f"Ranker Improvement      : "
        f"{ranker_improvement:+.2f} percentage points"

    )

    # ========================================================
    # TARGET
    # ========================================================

    print()

    if average_hybrid > BASELINE:

        print(

            "SUCCESS: "
            "Hybrid OCR exceeded the previous baseline."

        )

    else:

        print(

            "TARGET NOT REACHED."

        )

        print()

        print(

            f"Current Hybrid Score : "
            f"{average_hybrid:.2f}%"

        )

        print(

            f"Target               : "
            f">{BASELINE:.2f}%"

        )

    print()

    print(
        "=" * 70
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()