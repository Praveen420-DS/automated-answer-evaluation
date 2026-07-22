import sys
import cv2
import pytesseract
import traceback

from pathlib import Path


# ============================================================
# IMPORT FILTER AND RANKER
# ============================================================

try:
    from app.ocr.candidate_filter import filter_candidate
except ImportError:
    filter_candidate = None


try:
    from app.ocr.candidate_ranker import (
        rank_candidate,
        get_candidate_details
    )
except ImportError:
    rank_candidate = None
    get_candidate_details = None


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]


# ============================================================
# DEFAULT IMAGE PATH
# ============================================================

DEFAULT_IMAGE_PATH = (
    PROJECT_ROOT
    / "tests"
    / "samples"
    / "Closest10.JPEG"
)


# ============================================================
# PREPROCESSING METHODS
# ============================================================

def preprocess_original(image):

    return image


def preprocess_grayscale(image):

    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


def preprocess_otsu(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY
        + cv2.THRESH_OTSU
    )

    return thresh


def preprocess_adaptive(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    result = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return result


def preprocess_clahe(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    return clahe.apply(
        gray
    )


def preprocess_upscale(image):

    height, width = image.shape[:2]

    return cv2.resize(
        image,
        (
            width * 2,
            height * 2
        ),
        interpolation=cv2.INTER_CUBIC
    )


# ============================================================
# PREPROCESSING PIPELINE
# ============================================================

PREPROCESSORS = {

    "Original":
        preprocess_original,

    "Grayscale":
        preprocess_grayscale,

    "Otsu":
        preprocess_otsu,

    "Adaptive":
        preprocess_adaptive,

    "CLAHE":
        preprocess_clahe,

    "Upscale":
        preprocess_upscale,

}


# ============================================================
# OCR CONFIGURATION
# ============================================================

PSM_MODES = [

    6,

    11,

]


# ============================================================
# TESSERACT OCR
# ============================================================

def run_tesseract(
    image,
    psm
):

    config = (
        f"--psm {psm}"
    )

    data = pytesseract.image_to_data(

        image,

        config=config,

        output_type=
            pytesseract.Output.DICT

    )

    texts = []

    confidences = []


    for index in range(

        len(
            data["text"]
        )

    ):

        text = (

            data["text"][index]

            .strip()

        )

        confidence = (

            data["conf"][index]

        )


        if not text:

            continue


        texts.append(
            text
        )


        try:

            confidence = float(
                confidence
            )


            if confidence >= 0:

                confidences.append(

                    confidence

                )


        except (

            ValueError,

            TypeError

        ):

            pass


    final_text = " ".join(

        texts

    )


    if confidences:

        avg_confidence = (

            sum(
                confidences
            )

            /

            len(
                confidences
            )

        )

    else:

        avg_confidence = 0.0


    return (

        final_text,

        avg_confidence

    )


# ============================================================
# NORMALIZE CANDIDATE
# ============================================================

def normalize_candidate(

    candidate,

    method=None,

    psm=None,

    confidence=None

):

    # --------------------------------------------------------
    # Dictionary candidate
    # --------------------------------------------------------

    if isinstance(

        candidate,

        dict

    ):

        normalized = dict(

            candidate

        )


        normalized.setdefault(

            "text",

            ""

        )


        normalized.setdefault(

            "method",

            method

        )


        normalized.setdefault(

            "psm",

            psm

        )


        normalized.setdefault(

            "confidence",

            (

                confidence

                if confidence is not None

                else 0.0

            )

        )


        return normalized


    # --------------------------------------------------------
    # String candidate
    # --------------------------------------------------------

    if isinstance(

        candidate,

        str

    ):

        return {

            "text":
                candidate,

            "method":
                method,

            "psm":
                psm,

            "confidence":
                (

                    confidence

                    if confidence is not None

                    else 0.0

                ),

        }


    # --------------------------------------------------------
    # Unknown candidate
    # --------------------------------------------------------

    return {

        "text":
            str(
                candidate
            ),

        "method":
            method,

        "psm":
            psm,

        "confidence":
            (

                confidence

                if confidence is not None

                else 0.0

            ),

    }


# ============================================================
# FALLBACK CODE SIGNAL
# ============================================================

def calculate_code_signal(
    text
):

    if not text:

        return 0.0


    text_lower = (

        text.lower()

    )


    code_keywords = [

        "def ",

        "return ",

        "for ",

        "while ",

        "if ",

        "else",

        "elif ",

        "import ",

        "from ",

        "class ",

        "print(",

        "range(",

        "len(",

        "array",

        "list",

        "minimum",

        "maximum",

    ]


    symbols = [

        "(",

        ")",

        "[",

        "]",

        "{",

        "}",

        ":",

        "=",

        "<",

        ">",

    ]


    keyword_count = 0


    for keyword in code_keywords:

        if keyword in text_lower:

            keyword_count += 1


    symbol_count = 0


    for symbol in symbols:

        if symbol in text:

            symbol_count += 1


    keyword_score = min(

        keyword_count / 4,

        1.0

    )


    symbol_score = min(

        symbol_count / 5,

        1.0

    )


    return round(

        (

            keyword_score
            * 0.7

        )

        +

        (

            symbol_score
            * 0.3

        ),

        4

    )


# ============================================================
# FALLBACK FILTER
# ============================================================

def fallback_filter(

    candidate

):

    candidate = normalize_candidate(

        candidate

    )


    text = candidate.get(

        "text",

        ""

    )


    code_signal = (

        calculate_code_signal(

            text

        )

    )


    candidate[

        "code_signal"

    ] = code_signal


    if code_signal < 0.15:

        candidate[

            "accepted"

        ] = False


        candidate[

            "rejection_reason"

        ] = (

            "Insufficient code signal"

        )


    else:

        candidate[

            "accepted"

        ] = True


        candidate[

            "rejection_reason"

        ] = ""


    return candidate


# ============================================================
# FALLBACK RANKER
# ============================================================

def fallback_ranker(

    candidate

):

    candidate = normalize_candidate(

        candidate

    )


    text = candidate.get(

        "text",

        ""

    )


    confidence = candidate.get(

        "confidence",

        0.0

    )


    if confidence > 1:

        confidence_score = (

            confidence / 100

        )

    else:

        confidence_score = confidence


    code_signal = candidate.get(

        "code_signal",

        calculate_code_signal(

            text

        )

    )


    readability = 1.0


    if len(

        text.strip()

    ) < 5:

        readability = 0.2


    rank_score = (

        confidence_score
        * 0.4

        +

        code_signal
        * 0.4

        +

        readability
        * 0.2

    )


    candidate[

        "confidence_score"

    ] = round(

        confidence_score,

        4

    )


    candidate[

        "syntax_score"

    ] = 0.0


    candidate[

        "code_quality_score"

    ] = round(

        code_signal,

        4

    )


    candidate[

        "structure_score"

    ] = 0.0


    candidate[

        "token_quality_score"

    ] = 1.0


    candidate[

        "readability_score"

    ] = round(

        readability,

        4

    )


    candidate[

        "noise_penalty"

    ] = 0.0


    candidate[

        "rank_score"

    ] = round(

        rank_score,

        4

    )


    return candidate


# ============================================================
# APPLY FILTER
# ============================================================

def apply_filter(

    candidate

):

    candidate = normalize_candidate(

        candidate

    )


    # --------------------------------------------------------
    # Use real candidate filter
    # --------------------------------------------------------

    if filter_candidate is not None:

        try:

            result = filter_candidate(

                candidate

            )


            if isinstance(

                result,

                dict

            ):

                merged = dict(

                    candidate

                )


                merged.update(

                    result

                )


                return merged


            if isinstance(

                result,

                bool

            ):

                candidate[

                    "accepted"

                ] = result


                return candidate


        except Exception as error:

            print(

                "Filter warning: "

                f"{error}"

            )


    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    return fallback_filter(

        candidate

    )


# ============================================================
# APPLY RANKER
# ============================================================

def apply_ranker(

    candidate

):

    candidate = normalize_candidate(

        candidate

    )


    # --------------------------------------------------------
    # Use real candidate ranker
    # --------------------------------------------------------

    if rank_candidate is not None:

        try:

            text = candidate.get(

                "text",

                ""

            )


            confidence = candidate.get(

                "confidence",

                0.0

            )


            # ------------------------------------------------
            # Get final ranking score
            # ------------------------------------------------

            result = rank_candidate(

                text,

                confidence

            )


            # ------------------------------------------------
            # IMPORTANT:
            # rank_candidate returns a number
            # ------------------------------------------------

            if isinstance(

                result,

                (

                    int,

                    float

                )

            ):

                candidate[

                    "rank_score"

                ] = float(

                    result

                )


            # ------------------------------------------------
            # Get detailed metrics
            # ------------------------------------------------

            if get_candidate_details is not None:

                details = (

                    get_candidate_details(

                        text,

                        confidence

                    )

                )


                if isinstance(

                    details,

                    dict

                ):

                    candidate.update(

                        details

                    )


                    # Keep rank_candidate's
                    # final score authoritative

                    candidate[

                        "rank_score"

                    ] = float(

                        result

                    )


                return candidate


            return candidate


        except Exception as error:

            print(

                "Ranker warning: "

                f"{error}"

            )


    # --------------------------------------------------------
    # Fallback ranker
    # --------------------------------------------------------

    return fallback_ranker(

        candidate

    )


# ============================================================
# GENERATE OCR CANDIDATES
# ============================================================

def generate_candidates(

    image

):

    candidates = []


    for (

        method_name,

        processor

    ) in PREPROCESSORS.items():


        try:

            processed_image = (

                processor(

                    image

                )

            )


        except Exception as error:

            print(

                f"Preprocessing failed: "

                f"{method_name} -> "

                f"{error}"

            )

            continue


        for psm in PSM_MODES:


            try:

                text, confidence = (

                    run_tesseract(

                        processed_image,

                        psm

                    )

                )


                candidate = {

                    "text":
                        text,

                    "method":
                        method_name,

                    "psm":
                        psm,

                    "confidence":
                        confidence,

                }


                candidates.append(

                    candidate

                )


            except Exception as error:

                print(

                    f"OCR failed: "

                    f"{method_name} | "

                    f"PSM {psm} -> "

                    f"{error}"

                )


    return candidates


# ============================================================
# PROCESS CANDIDATES
# ============================================================

def process_candidates(

    candidates

):

    processed = []


    for candidate in candidates:


        candidate = normalize_candidate(

            candidate

        )


        # ----------------------------------------------------
        # APPLY FILTER
        # ----------------------------------------------------

        filtered = apply_filter(

            candidate

        )


        filtered = normalize_candidate(

            filtered

        )


        if "accepted" not in filtered:

            filtered[

                "accepted"

            ] = True


        # ----------------------------------------------------
        # RANK ONLY ACCEPTED CANDIDATES
        # ----------------------------------------------------

        if filtered.get(

            "accepted",

            False

        ):

            ranked = apply_ranker(

                filtered

            )


            ranked = normalize_candidate(

                ranked

            )


            processed.append(

                ranked

            )


    return processed


# ============================================================
# SELECT BEST CANDIDATE
# ============================================================

def select_best_candidate(

    candidates

):

    if not candidates:

        return None


    return max(

        candidates,

        key=lambda candidate:

            candidate.get(

                "rank_score",

                0.0

            )

    )


# ============================================================
# PRINT CANDIDATE
# ============================================================

def print_candidate(

    candidate

):

    print(

        f"{candidate.get('method', 'Unknown')} "

        f"| PSM "

        f"{candidate.get('psm', '?')} "

        f"| Confidence "

        f"{candidate.get('confidence', 0.0):.2f}% "

        f"| Rank "

        f"{candidate.get('rank_score', 0.0):.4f}"

    )


# ============================================================
# PRINT DETAILED CANDIDATE
# ============================================================

def print_candidate_details(

    candidate

):

    print(

        f"Confidence Score : "

        f"{candidate.get('confidence_score', 0.0):.4f}"

    )


    print(

        f"Syntax Score     : "

        f"{candidate.get('syntax_score', 0.0):.4f}"

    )


    print(

        f"Code Quality     : "

        f"{candidate.get('code_quality_score', 0.0):.4f}"

    )


    print(

        f"Structure Score   : "

        f"{candidate.get('structure_score', 0.0):.4f}"

    )


    print(

        f"Token Quality     : "

        f"{candidate.get('token_quality_score', 0.0):.4f}"

    )


    print(

        f"Readability       : "

        f"{candidate.get('readability_score', 0.0):.4f}"

    )


    print(

        f"Noise Penalty     : "

        f"{candidate.get('noise_penalty', 0.0):.4f}"

    )


    print(

        f"Ranking Score     : "

        f"{candidate.get('rank_score', 0.0):.4f}"

    )


# ============================================================
# MAIN ENSEMBLE OCR
# ============================================================

def run_ensemble_ocr(

    image_path

):

    image_path = Path(

        image_path

    ).resolve()


    # --------------------------------------------------------
    # Validate image path
    # --------------------------------------------------------

    if not image_path.exists():

        raise FileNotFoundError(

            f"Image does not exist: "

            f"{image_path}"

        )


    print(

        f"Loading image: "

        f"{image_path}"

    )


    # --------------------------------------------------------
    # Load image
    # --------------------------------------------------------

    image = cv2.imread(

        str(

            image_path

        )

    )


    if image is None:

        raise FileNotFoundError(

            f"Could not load image: "

            f"{image_path}"

        )


    image_name = image_path.name


    print(

        "=" * 60

    )


    print(

        f"ENSEMBLE OCR V4: "

        f"{image_name}"

    )


    print(

        "=" * 60

    )


    # --------------------------------------------------------
    # Generate candidates
    # --------------------------------------------------------

    candidates = generate_candidates(

        image

    )


    print(

        f"Total OCR candidates: "

        f"{len(candidates)}"

    )


    # --------------------------------------------------------
    # Process candidates
    # --------------------------------------------------------

    processed_candidates = (

        process_candidates(

            candidates

        )

    )


    # --------------------------------------------------------
    # Count rejected
    # --------------------------------------------------------

    rejected_count = (

        len(

            candidates

        )

        -

        len(

            processed_candidates

        )

    )


    print(

        f"Accepted candidates: "

        f"{len(processed_candidates)}"

    )


    print(

        f"Rejected candidates: "

        f"{rejected_count}"

    )


    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    if not processed_candidates:

        print()

        print(

            "WARNING: "

            "No candidates passed filter."

        )


        print(

            "Using all OCR candidates "

            "for ranking."

        )


        processed_candidates = []


        for candidate in candidates:


            candidate = (

                normalize_candidate(

                    candidate

                )

            )


            candidate = fallback_ranker(

                candidate

            )


            processed_candidates.append(

                candidate

            )


    # --------------------------------------------------------
    # Select best
    # --------------------------------------------------------

    best_candidate = (

        select_best_candidate(

            processed_candidates

        )

    )


    if best_candidate is None:

        raise RuntimeError(

            "No OCR candidate available."

        )


    # --------------------------------------------------------
    # Sort candidates
    # --------------------------------------------------------

    sorted_candidates = sorted(

        processed_candidates,

        key=lambda candidate:

            candidate.get(

                "rank_score",

                0.0

            ),

        reverse=True

    )


    # ========================================================
    # SELECTED CANDIDATE
    # ========================================================

    print()

    print(

        "-" * 60

    )


    print(

        f"SELECTED METHOD : "

        f"{best_candidate.get('method')}"

    )


    print(

        f"SELECTED PSM    : "

        f"{best_candidate.get('psm')}"

    )


    print(

        f"Tesseract Conf. : "

        f"{best_candidate.get('confidence', 0.0):.2f}%"

    )


    print_candidate_details(

        best_candidate

    )


    # ========================================================
    # TOP 3
    # ========================================================

    print()

    print(

        "-" * 60

    )


    print(

        "TOP 3 OCR CANDIDATES"

    )


    print(

        "-" * 60

    )


    for (

        index,

        candidate

    ) in enumerate(

        sorted_candidates[:3],

        start=1

    ):


        print(

            f"{index}. ",

            end=""

        )


        print_candidate(

            candidate

        )


    # ========================================================
    # FINAL OCR TEXT
    # ========================================================

    print()

    print(

        "=" * 60

    )


    print(

        "FINAL ENSEMBLE OCR TEXT"

    )


    print(

        "=" * 60

    )


    print(

        best_candidate.get(

            "text",

            ""

        )

    )


    print(

        "=" * 60

    )


    return {
    "best_candidate": best_candidate,
    "candidates": sorted_candidates
    }


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    try:

        run_ensemble_ocr(

            str(

                DEFAULT_IMAGE_PATH

            )

        )


    except Exception as error:


        print()

        print(

            "=" * 60

        )


        print(

            "ENSEMBLE OCR FAILED"

        )


        print(

            "=" * 60

        )


        print(

            f"Error: "

            f"{error}"

        )


        print()


        traceback.print_exc()


        sys.exit(1)