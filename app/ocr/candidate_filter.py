# ============================================================
# CANDIDATE FILTER V3
# ============================================================

import re


# ============================================================
# CODE KEYWORDS
# ============================================================

CODE_KEYWORDS = [
    "def",
    "return",
    "for",
    "while",
    "if",
    "else",
    "elif",
    "import",
    "from",
    "class",
    "print",
    "range",
    "len",
    "list",
    "array",
    "minimum",
    "maximum",
    "min",
    "max",
]


# ============================================================
# CODE SYMBOLS
# ============================================================

CODE_SYMBOLS = [
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
    "_",
]


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    if text is None:
        return ""

    return str(text).strip()


# ============================================================
# CODE KEYWORD SCORE
# ============================================================

def calculate_keyword_score(text):

    text = normalize_text(text).lower()

    if not text:
        return 0.0

    found_keywords = 0

    for keyword in CODE_KEYWORDS:

        # Word boundary style matching without regex
        words = text.replace(
            "(",
            " "
        ).replace(
            ")",
            " "
        ).replace(
            "[",
            " "
        ).replace(
            "]",
            " "
        ).replace(
            ":",
            " "
        ).replace(
            "=",
            " "
        ).split()

        if keyword in words:

            found_keywords += 1

    score = min(
        found_keywords / 5.0,
        1.0
    )

    return round(
        score,
        4
    )


# ============================================================
# CODE SYMBOL SCORE
# ============================================================

def calculate_symbol_score(text):

    text = normalize_text(text)

    if not text:
        return 0.0

    found_symbols = 0

    for symbol in CODE_SYMBOLS:

        if symbol in text:

            found_symbols += 1

    score = min(
        found_symbols / 5.0,
        1.0
    )

    return round(
        score,
        4
    )


# ============================================================
# STRUCTURE SCORE
# ============================================================

def calculate_structure_score(text):

    text = normalize_text(text)

    if not text:
        return 0.0

    score = 0.0

    text_lower = text.lower()

    # Function definition
    if "def " in text_lower:

        score += 0.25

    # Return statement
    if "return " in text_lower:

        score += 0.20

    # Loop
    if "for " in text_lower or "while " in text_lower:

        score += 0.15

    # Condition
    if "if " in text_lower:

        score += 0.15

    # Function brackets
    if "(" in text and ")" in text:

        score += 0.10

    # Assignment
    if "=" in text:

        score += 0.10

    # List / array structure
    if "[" in text and "]" in text:

        score += 0.05

    return round(
        min(
            score,
            1.0
        ),
        4
    )


# ============================================================
# TOKEN QUALITY SCORE
# ============================================================

def calculate_token_quality(text):

    text = normalize_text(text)

    if not text:
        return 0.0

    tokens = text.split()

    if not tokens:
        return 0.0

    valid_tokens = 0

    for token in tokens:

        clean_token = token.strip(
            ".,;:!?\"'`()[]{}"
        )

        if not clean_token:
            continue

        has_alpha = False

        for character in clean_token:

            if character.isalpha():

                has_alpha = True

                break

        if has_alpha:

            valid_tokens += 1

    score = (
        valid_tokens
        /
        len(tokens)
    )

    return round(
        score,
        4
    )


# ============================================================
# READABILITY SCORE
# ============================================================

def calculate_readability_score(text):

    text = normalize_text(text)

    if not text:
        return 0.0

    tokens = text.split()

    if not tokens:
        return 0.0

    # Extremely short text
    if len(text) < 5:

        return 0.1

    # Count suspicious repeated characters
    repeated_noise = 0

    for i in range(
        len(text) - 2
    ):

        if (
            text[i]
            ==
            text[i + 1]
            ==
            text[i + 2]
        ):

            repeated_noise += 1

    noise_ratio = min(
        repeated_noise / 5.0,
        1.0
    )

    readability = 1.0 - (
        noise_ratio * 0.5
    )

    return round(
        max(
            readability,
            0.0
        ),
        4
    )


# ============================================================
# NOISE PENALTY
# ============================================================

def calculate_noise_penalty(text):

    text = normalize_text(text)

    if not text:
        return 1.0

    tokens = text.split()

    if not tokens:
        return 1.0

    suspicious_tokens = 0

    for token in tokens:

        alpha_count = 0
        digit_count = 0
        symbol_count = 0

        for character in token:

            if character.isalpha():

                alpha_count += 1

            elif character.isdigit():

                digit_count += 1

            else:

                symbol_count += 1

        # Token containing only strange symbols
        if (
            alpha_count == 0
            and digit_count == 0
            and symbol_count > 0
        ):

            suspicious_tokens += 1

    penalty = (
        suspicious_tokens
        /
        len(tokens)
    )

    return round(
        min(
            penalty,
            1.0
        ),
        4
    )


# ============================================================
# CODE SIGNAL
# ============================================================

def calculate_code_signal(text):

    keyword_score = calculate_keyword_score(
        text
    )

    symbol_score = calculate_symbol_score(
        text
    )

    structure_score = calculate_structure_score(
        text
    )

    code_signal = (

        keyword_score
        * 0.40

        +

        symbol_score
        * 0.20

        +

        structure_score
        * 0.40

    )

    return round(
        min(
            code_signal,
            1.0
        ),
        4
    )


# ============================================================
# MAIN FILTER
# ============================================================

def filter_candidate(candidate):

    # --------------------------------------------------------
    # Normalize input
    # --------------------------------------------------------

    if isinstance(
        candidate,
        dict
    ):

        result = dict(
            candidate
        )

    else:

        result = {

            "text":
                str(candidate),

            "confidence":
                0.0,

        }

    # --------------------------------------------------------
    # Extract text
    # --------------------------------------------------------

    text = normalize_text(
        result.get(
            "text",
            ""
        )
    )

    # --------------------------------------------------------
    # Calculate metrics
    # --------------------------------------------------------

    code_signal = calculate_code_signal(
        text
    )

    token_quality = calculate_token_quality(
        text
    )

    structure_score = calculate_structure_score(
        text
    )

    readability_score = calculate_readability_score(
        text
    )

    noise_penalty = calculate_noise_penalty(
        text
    )

    # --------------------------------------------------------
    # Store metrics
    # --------------------------------------------------------

    result[
        "code_signal"
    ] = code_signal

    result[
        "token_quality_score"
    ] = token_quality

    result[
        "structure_score"
    ] = structure_score

    result[
        "readability_score"
    ] = readability_score

    result[
        "noise_penalty"
    ] = noise_penalty

    # --------------------------------------------------------
    # Acceptance score
    # --------------------------------------------------------

    acceptance_score = (

        code_signal
        * 0.40

        +

        token_quality
        * 0.20

        +

        structure_score
        * 0.20

        +

        readability_score
        * 0.20

        -

        noise_penalty
        * 0.30

    )

    acceptance_score = max(
        0.0,
        min(
            acceptance_score,
            1.0
        )
    )

    result[
        "filter_score"
    ] = round(
        acceptance_score,
        4
    )

    # --------------------------------------------------------
    # Acceptance decision
    # --------------------------------------------------------

    # Strong rejection:
    # Almost no code signal

    if code_signal < 0.10:

        result[
            "accepted"
        ] = False

        result[
            "reason"
        ] = (
            "Very low code signal"
        )

        return result

    # Strong rejection:
    # High noise

    if noise_penalty > 0.70:

        result[
            "accepted"
        ] = False

        result[
            "reason"
        ] = (
            "High OCR noise"
        )

        return result

    # Normal acceptance threshold

    if acceptance_score >= 0.25:

        result[
            "accepted"
        ] = True

        result[
            "reason"
        ] = (
            "Candidate contains "
            "sufficient code structure"
        )

    else:

        result[
            "accepted"
        ] = False

        result[
            "reason"
        ] = (
            "Insufficient candidate quality"
        )

    return result


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "=" * 60
    )

    print(
        "CANDIDATE FILTER V3 TEST"
    )

    print(
        "=" * 60
    )

    test_candidates = [

        {
            "text":
                "def test(array): return array",

            "confidence":
                50,
        },

        {
            "text":
                "hello random text",

            "confidence":
                80,
        },

        {
            "text":
                """
                def find_minimum(array):

                    minimum = array[0]

                    for i in range(len(array)):

                        if array[i] < minimum:

                            minimum = array[i]

                    return minimum
                """,

            "confidence":
                45,
        },

        {
            "text":
                "a i ak ny ii Be th wn ue",

            "confidence":
                31,
        },

    ]

    for candidate in test_candidates:

        result = filter_candidate(
            candidate
        )

        print()

        print(
            "Text:"
        )

        print(
            result[
                "text"
            ]
        )

        print()

        print(
            "Accepted :",
            result[
                "accepted"
            ]
        )

        print(
            "Reason   :",
            result[
                "reason"
            ]
        )

        print(
            "Filter Score :",
            result[
                "filter_score"
            ]
        )

        print(
            "Code Signal :",
            result[
                "code_signal"
            ]
        )

        print(
            "Structure   :",
            result[
                "structure_score"
            ]
        )

        print(
            "Token Quality :",
            result[
                "token_quality_score"
            ]
        )

        print(
            "Noise Penalty :",
            result[
                "noise_penalty"
            ]
        )

    print()

    print(
        "=" * 60
    )

    print(
        "FILTER V3 TEST COMPLETE"
    )

    print(
        "=" * 60
    )