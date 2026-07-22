from pathlib import Path

import cv2
import pytesseract


# ---------------------------------------------------------
# IMAGE PREPROCESSING METHODS
# ---------------------------------------------------------

def preprocess_original(image):
    """
    Keep the original image unchanged.
    """
    return image


def preprocess_grayscale(image):
    """
    Convert image to grayscale.
    """
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    return gray


def preprocess_upscale(image):
    """
    Convert to grayscale and upscale image.
    """
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    upscaled = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    return upscaled


def preprocess_clahe(image):
    """
    Grayscale + Upscaling + CLAHE
    for contrast enhancement.
    """
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    upscaled = cv2.resize(
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

    enhanced = clahe.apply(
        upscaled
    )

    return enhanced


def preprocess_otsu(image):
    """
    Grayscale + Upscaling + Otsu thresholding.
    """
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    upscaled = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    _, thresholded = cv2.threshold(
        upscaled,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresholded


def preprocess_adaptive(image):
    """
    Grayscale + Upscaling + Adaptive Thresholding.
    """
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    upscaled = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    thresholded = cv2.adaptiveThreshold(
        upscaled,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return thresholded


# ---------------------------------------------------------
# OCR CONFIGURATIONS
# ---------------------------------------------------------

OCR_CONFIGURATIONS = [
    {
        "method": "Original",
        "psm": 6,
        "preprocess": preprocess_original
    },
    {
        "method": "Original",
        "psm": 11,
        "preprocess": preprocess_original
    },
    {
        "method": "Grayscale",
        "psm": 6,
        "preprocess": preprocess_grayscale
    },
    {
        "method": "Grayscale",
        "psm": 11,
        "preprocess": preprocess_grayscale
    },
    {
        "method": "Upscale",
        "psm": 6,
        "preprocess": preprocess_upscale
    },
    {
        "method": "Upscale",
        "psm": 11,
        "preprocess": preprocess_upscale
    },
    {
        "method": "CLAHE",
        "psm": 6,
        "preprocess": preprocess_clahe
    },
    {
        "method": "CLAHE",
        "psm": 11,
        "preprocess": preprocess_clahe
    },
    {
        "method": "Otsu",
        "psm": 6,
        "preprocess": preprocess_otsu
    },
    {
        "method": "Otsu",
        "psm": 11,
        "preprocess": preprocess_otsu
    },
    {
        "method": "Adaptive",
        "psm": 6,
        "preprocess": preprocess_adaptive
    },
    {
        "method": "Adaptive",
        "psm": 11,
        "preprocess": preprocess_adaptive
    }
]


# ---------------------------------------------------------
# OCR CONFIDENCE CALCULATION
# ---------------------------------------------------------

def calculate_ocr_confidence(
    processed_image,
    psm
):
    """
    Run Tesseract and calculate average OCR confidence.

    Returns:
        text
        confidence
    """

    config = (
        f"--oem 3 --psm {psm}"
    )

    data = pytesseract.image_to_data(
        processed_image,
        config=config,
        output_type=pytesseract.Output.DICT
    )

    text_parts = []
    confidence_values = []

    for index, text in enumerate(
        data["text"]
    ):

        text = text.strip()

        try:
            confidence = float(
                data["conf"][index]
            )

        except (
            ValueError,
            TypeError
        ):
            confidence = -1

        if text:

            text_parts.append(
                text
            )

            if confidence >= 0:

                confidence_values.append(
                    confidence
                )

    final_text = " ".join(
        text_parts
    )

    if confidence_values:

        average_confidence = (
            sum(confidence_values)
            / len(confidence_values)
        )

    else:

        average_confidence = 0.0

    return (
        final_text,
        average_confidence
    )


# ---------------------------------------------------------
# RUN ALL OCR CANDIDATES
# ---------------------------------------------------------

def run_all_ocr_candidates(
    image_path: str
):
    """
    Run all OCR preprocessing and PSM configurations.

    This function generates 12 OCR candidates:

        6 preprocessing methods
        ×
        2 PSM modes

    Returns:
        List of dictionaries containing:

        {
            "text": OCR extracted text,
            "method": preprocessing method,
            "psm": PSM mode,
            "confidence": Tesseract confidence
        }
    """

    image_path = Path(
        image_path
    )

    if not image_path.exists():

        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    # -----------------------------------------------------
    # READ IMAGE
    # -----------------------------------------------------

    image = cv2.imread(
        str(image_path)
    )

    if image is None:

        raise ValueError(
            f"Could not read image: {image_path}"
        )

    # -----------------------------------------------------
    # STORE ALL CANDIDATES
    # -----------------------------------------------------

    candidates = []

    # -----------------------------------------------------
    # RUN EVERY OCR CONFIGURATION
    # -----------------------------------------------------

    for configuration in OCR_CONFIGURATIONS:

        method = configuration[
            "method"
        ]

        psm = configuration[
            "psm"
        ]

        preprocess = configuration[
            "preprocess"
        ]

        # Apply preprocessing
        processed_image = preprocess(
            image
        )

        # Run OCR
        text, confidence = (
            calculate_ocr_confidence(
                processed_image,
                psm
            )
        )

        # Create candidate
        candidate = {
            "text": text,
            "method": method,
            "psm": psm,
            "confidence": confidence
        }

        # Add candidate to list
        candidates.append(
            candidate
        )

    return candidates


# ---------------------------------------------------------
# ADAPTIVE OCR
# ---------------------------------------------------------

def extract_text_adaptive(
    image_path: str
):
    """
    Automatically test multiple OCR configurations
    and select the configuration with the highest
    Tesseract confidence.

    Returns:
        {
            "text": OCR text,
            "method": preprocessing method,
            "psm": PSM mode,
            "confidence": confidence score
        }
    """

    image_path = Path(
        image_path
    )

    if not image_path.exists():

        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    # -----------------------------------------------------
    # READ IMAGE
    # -----------------------------------------------------

    image = cv2.imread(
        str(image_path)
    )

    if image is None:

        raise ValueError(
            f"Could not read image: {image_path}"
        )

    # -----------------------------------------------------
    # BEST RESULT
    # -----------------------------------------------------

    best_result = None

    print(
        "=" * 60
    )

    print(
        f"ADAPTIVE OCR: "
        f"{image_path.name}"
    )

    print(
        "=" * 60
    )

    # -----------------------------------------------------
    # TEST EVERY OCR CONFIGURATION
    # -----------------------------------------------------

    for configuration in OCR_CONFIGURATIONS:

        method = configuration[
            "method"
        ]

        psm = configuration[
            "psm"
        ]

        preprocess = configuration[
            "preprocess"
        ]

        # Apply preprocessing
        processed_image = preprocess(
            image
        )

        # Run OCR
        text, confidence = (
            calculate_ocr_confidence(
                processed_image,
                psm
            )
        )

        print(
            f"{method:<12} "
            f"PSM {psm:<2} "
            f"Confidence: "
            f"{confidence:.2f}%"
        )

        # -------------------------------------------------
        # SELECT HIGHEST CONFIDENCE
        # -------------------------------------------------

        if (
            best_result is None
            or confidence
            > best_result[
                "confidence"
            ]
        ):

            best_result = {

                "text": text,

                "method": method,

                "psm": psm,

                "confidence": confidence
            }

    # -----------------------------------------------------
    # DISPLAY BEST RESULT
    # -----------------------------------------------------

    print(
        "-" * 60
    )

    print(
        f"SELECTED METHOD : "
        f"{best_result['method']}"
    )

    print(
        f"SELECTED PSM    : "
        f"{best_result['psm']}"
    )

    print(
        f"CONFIDENCE      : "
        f"{best_result['confidence']:.2f}%"
    )

    print(
        "=" * 60
    )

    return best_result


# ---------------------------------------------------------
# SIMPLE TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    # -----------------------------------------------------
    # PROJECT ROOT
    # -----------------------------------------------------

    sample_image = (
        Path(__file__).resolve().parents[2]
        / "tests"
        / "samples"
        / "Closest10.JPEG"
    )

    # -----------------------------------------------------
    # RUN ADAPTIVE OCR
    # -----------------------------------------------------

    result = extract_text_adaptive(
        str(sample_image)
    )

    # -----------------------------------------------------
    # PRINT FINAL OCR TEXT
    # -----------------------------------------------------

    print(
        "\nFINAL OCR TEXT"
    )

    print(
        "=" * 60
    )

    print(
        result["text"]
    )