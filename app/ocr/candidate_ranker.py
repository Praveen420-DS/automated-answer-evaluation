# ============================================================
# CANDIDATE RANKER
# ============================================================
#
# Purpose:
#   Rank OCR candidates based on multiple signals.
#
# Important:
#   Tesseract confidence alone is NOT reliable for code OCR.
#
#   We therefore combine:
#
#       1. OCR confidence
#       2. Code quality
#       3. Syntax quality
#       4. Structure quality
#       5. Token quality
#       6. Readability
#       7. Noise penalty
#
# ============================================================


import re


# ============================================================
# SAFE FLOAT
# ============================================================

def safe_float(
    value,
    default=0.0
):

    try:

        return float(
            value
        )

    except (
        TypeError,
        ValueError
    ):

        return default


# ============================================================
# GET CONFIDENCE
# ============================================================

def get_confidence(
    candidate
):

    if not isinstance(
        candidate,
        dict
    ):

        return 0.0

    confidence = safe_float(

        candidate.get(

            "confidence",

            0.0

        )

    )

    # Tesseract confidence may be:
    #
    # 0 - 100
    #
    # Convert to:
    #
    # 0 - 1

    if confidence > 1.0:

        confidence = (

            confidence

            /

            100.0

        )

    return max(

        0.0,

        min(

            confidence,

            1.0

        )

    )


# ============================================================
# GET TEXT
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
# NORMALIZE TEXT
# ============================================================

def normalize_text(
    text
):

    if not text:

        return ""

    text = str(
        text
    )

    text = text.replace(

        "\r",

        ""

    )

    return text.strip()


# ============================================================
# GET METHOD
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
# GET PSM
# ============================================================

def get_psm(
    candidate
):

    if not isinstance(
        candidate,
        dict
    ):

        return "?"

    return candidate.get(

        "psm",

        "?"

    )


# ============================================================
# CODE QUALITY SCORE
# ============================================================
#
# Detect whether OCR text resembles source code.
#
# This is intentionally lightweight.
#
# We do NOT try to execute OCR code.
#
# ============================================================

def calculate_code_quality(
    text
):

    text = normalize_text(
        text
    )

    if not text:

        return 0.0


    score = 0.0


    # --------------------------------------------------------
    # Programming keywords
    # --------------------------------------------------------

    keywords = [

        "def",

        "function",

        "return",

        "for",

        "while",

        "if",

        "else",

        "elif",

        "int",

        "float",

        "void",

        "main",

        "printf",

        "scanf",

        "print",

        "list",

        "array",

        "range",

        "len",

        "append",

        "sort",

        "include",

    ]


    keyword_hits = 0


    lower_text = text.lower()


    for keyword in keywords:

        if keyword in lower_text:

            keyword_hits += 1


    keyword_score = min(

        keyword_hits

        /

        5.0,

        1.0

    )


    score += (

        keyword_score

        *

        0.35

    )


    # --------------------------------------------------------
    # Programming symbols
    # --------------------------------------------------------

    symbols = [

        "(",

        ")",

        "[",

        "]",

        "{",

        "}",

        "=",

        ":",

        ";",

    ]


    symbol_hits = sum(

        text.count(

            symbol

        )

        for symbol in symbols

    )


    symbol_score = min(

        symbol_hits

        /

        15.0,

        1.0

    )


    score += (

        symbol_score

        *

        0.20

    )


    # --------------------------------------------------------
    # Function-like structure
    # --------------------------------------------------------

    function_patterns = [

        r"\bdef\s+\w+",

        r"\bmain\s*\(",

        r"\bfunction\s+\w+",

        r"\w+\s*\(",

    ]


    function_hits = 0


    for pattern in function_patterns:

        if re.search(

            pattern,

            text,

            flags=re.IGNORECASE

        ):

            function_hits += 1


    function_score = min(

        function_hits

        /

        2.0,

        1.0

    )


    score += (

        function_score

        *

        0.20

    )


    # --------------------------------------------------------
    # Variable assignment
    # --------------------------------------------------------

    assignment_hits = len(

        re.findall(

            r"\b\w+\s*=",

            text

        )

    )


    assignment_score = min(

        assignment_hits

        /

        5.0,

        1.0

    )


    score += (

        assignment_score

        *

        0.15

    )


    # --------------------------------------------------------
    # Numeric/code content
    # --------------------------------------------------------

    number_hits = len(

        re.findall(

            r"\b\d+\b",

            text

        )

    )


    if number_hits > 0:

        score += 0.10


    return max(

        0.0,

        min(

            score,

            1.0

        )

    )


# ============================================================
# SYNTAX SCORE
# ============================================================
#
# Lightweight bracket and delimiter validation.
#
# ============================================================

def calculate_syntax_score(
    text
):

    text = normalize_text(
        text
    )

    if not text:

        return 0.0


    score = 0.0


    # --------------------------------------------------------
    # Bracket balance
    # --------------------------------------------------------

    pairs = [

        ("(", ")"),

        ("[", "]"),

        ("{", "}"),

    ]


    total_pairs = 0

    balanced_pairs = 0


    for opening, closing in pairs:

        open_count = text.count(
            opening
        )

        close_count = text.count(
            closing
        )


        if (

            open_count == 0

            and

            close_count == 0

        ):

            continue


        total_pairs += 1


        if open_count == close_count:

            balanced_pairs += 1


    if total_pairs > 0:

        score += (

            balanced_pairs

            /

            total_pairs

        )

        score *= 0.60


    # --------------------------------------------------------
    # Semicolon / colon structure
    # --------------------------------------------------------

    if ";" in text:

        score += 0.15


    if ":" in text:

        score += 0.15


    # --------------------------------------------------------
    # Function parenthesis
    # --------------------------------------------------------

    if re.search(

        r"\w+\s*\(",

        text

    ):

        score += 0.10


    return max(

        0.0,

        min(

            score,

            1.0

        )

    )


# ============================================================
# STRUCTURE SCORE
# ============================================================

def calculate_structure_score(
    text
):

    text = normalize_text(
        text
    )

    if not text:

        return 0.0


    lines = [

        line.strip()

        for line in text.splitlines()

        if line.strip()

    ]


    if not lines:

        return 0.0


    score = 0.0


    # --------------------------------------------------------
    # Multiple lines
    # --------------------------------------------------------

    if len(lines) >= 2:

        score += 0.25


    if len(lines) >= 4:

        score += 0.15


    if len(lines) >= 8:

        score += 0.10


    # --------------------------------------------------------
    # Code indentation
    # --------------------------------------------------------

    indented_lines = sum(

        1

        for line in text.splitlines()

        if line.startswith(

            (

                " ",

                "\t"

            )

        )

    )


    if indented_lines > 0:

        score += 0.20


    # --------------------------------------------------------
    # Code blocks
    # --------------------------------------------------------

    if "{" in text and "}" in text:

        score += 0.15


    # --------------------------------------------------------
    # Function definition
    # --------------------------------------------------------

    if re.search(

        r"\bdef\s+\w+",

        text

    ):

        score += 0.15


    return max(

        0.0,

        min(

            score,

            1.0

        )

    )


# ============================================================
# TOKEN QUALITY
# ============================================================

def calculate_token_quality(
    text
):

    text = normalize_text(
        text
    )

    if not text:

        return 0.0


    tokens = re.findall(

        r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",

        text

    )


    if not tokens:

        return 0.0


    valid_tokens = 0


    for token in tokens:

        if len(token) >= 2:

            valid_tokens += 1


    return (

        valid_tokens

        /

        len(tokens)

    )


# ============================================================
# READABILITY
# ============================================================

def calculate_readability(
    text
):

    text = normalize_text(
        text
    )

    if not text:

        return 0.0


    total_chars = len(
        text
    )


    if total_chars == 0:

        return 0.0


    alphanumeric_chars = sum(

        1

        for char in text

        if char.isalnum()

    )


    ratio = (

        alphanumeric_chars

        /

        total_chars

    )


    return max(

        0.0,

        min(

            ratio,

            1.0

        )

    )


# ============================================================
# NOISE PENALTY
# ============================================================

def calculate_noise_penalty(
    text
):

    text = normalize_text(
        text
    )

    if not text:

        return 1.0


    penalty = 0.0


    # --------------------------------------------------------
    # Excessive unusual symbols
    # --------------------------------------------------------

    unusual_symbols = len(

        re.findall(

            r"[^a-zA-Z0-9\s_\[\]\(\)\{\}\+\-\*\/=%:;,.<>#'\"&|]",

            text

        )

    )


    if unusual_symbols > 5:

        penalty += 0.20


    if unusual_symbols > 15:

        penalty += 0.20


    # --------------------------------------------------------
    # Excessive repeated characters
    # --------------------------------------------------------

    repeated_patterns = re.findall(

        r"(.)\1{3,}",

        text

    )


    if repeated_patterns:

        penalty += 0.20


    # --------------------------------------------------------
    # Very short text
    # --------------------------------------------------------

    if len(text) < 20:

        penalty += 0.20


    # --------------------------------------------------------
    # Extremely long single line
    # --------------------------------------------------------

    if (

        len(text.splitlines()) == 1

        and

        len(text) > 500

    ):

        penalty += 0.20


    return max(

        0.0,

        min(

            penalty,

            1.0

        )

    )


# ============================================================
# RANK SCORE
# ============================================================
#
# IMPORTANT:
#
# Confidence is NOT dominant.
#
# The previous system appears to select candidates with
# higher OCR confidence even when their actual text quality
# is poor.
#
# New weights:
#
# Confidence       15%
# Code Quality     25%
# Syntax           15%
# Structure        15%
# Token Quality    10%
# Readability      10%
# Noise Penalty    -10%
#
# ============================================================

def calculate_rank_score(
    candidate
):

    if not isinstance(
        candidate,
        dict
    ):

        return 0.0


    text = get_text(
        candidate
    )


    confidence = get_confidence(

        candidate

    )


    code_quality = calculate_code_quality(

        text

    )


    syntax_score = calculate_syntax_score(

        text

    )


    structure_score = calculate_structure_score(

        text

    )


    token_quality = calculate_token_quality(

        text

    )


    readability = calculate_readability(

        text

    )


    noise_penalty = calculate_noise_penalty(

        text

    )


    # --------------------------------------------------------
    # Weighted ranking
    # --------------------------------------------------------

    rank_score = (

        confidence

        *

        0.15

    )


    rank_score += (

        code_quality

        *

        0.25

    )


    rank_score += (

        syntax_score

        *

        0.15

    )


    rank_score += (

        structure_score

        *

        0.15

    )


    rank_score += (

        token_quality

        *

        0.10

    )


    rank_score += (

        readability

        *

        0.10

    )


    rank_score -= (

        noise_penalty

        *

        0.10

    )


    rank_score = max(

        0.0,

        min(

            rank_score,

            1.0

        )

    )


    # --------------------------------------------------------
    # Store metrics
    # --------------------------------------------------------

    candidate[

        "confidence_score"

    ] = confidence


    candidate[

        "code_quality"

    ] = code_quality


    candidate[

        "syntax_score"

    ] = syntax_score


    candidate[

        "structure_score"

    ] = structure_score


    candidate[

        "token_quality"

    ] = token_quality


    candidate[

        "readability"

    ] = readability


    candidate[

        "noise_penalty"

    ] = noise_penalty


    candidate[

        "rank_score"

    ] = rank_score


    return rank_score


# ============================================================
# RANK CANDIDATES
# ============================================================

def rank_candidates(
    candidates
):

    if not candidates:

        return []


    processed = []


    for candidate in candidates:

        if not isinstance(

            candidate,

            dict

        ):

            continue


        candidate = candidate.copy()


        calculate_rank_score(

            candidate

        )


        processed.append(

            candidate

        )


    return sorted(

        processed,

        key=lambda candidate:

            candidate.get(

                "rank_score",

                0.0

            ),

        reverse=True

    )


# ============================================================
# GET BEST CANDIDATE
# ============================================================

def get_best_candidate(
    candidates
):

    ranked = rank_candidates(

        candidates

    )


    if not ranked:

        return None


    return ranked[0]


# ============================================================
# GET TOP CANDIDATES
# ============================================================

def get_top_candidates(
    candidates,
    count=3
):

    ranked = rank_candidates(

        candidates

    )


    return ranked[

        :count

    ]


# ============================================================
# FALLBACK RANKER
# ============================================================

def fallback_ranker(
    candidate
):

    if not isinstance(

        candidate,

        dict

    ):

        return candidate


    candidate = candidate.copy()


    calculate_rank_score(

        candidate

    )


    return candidate


# ============================================================
# NORMALIZE CANDIDATE
# ============================================================

def normalize_candidate(
    candidate
):

    if not isinstance(

        candidate,

        dict

    ):

        return {

            "text": str(

                candidate

            ),

            "method": "Unknown",

            "psm": "?",

            "confidence": 0.0,

        }


    candidate = candidate.copy()


    candidate.setdefault(

        "text",

        ""

    )


    candidate.setdefault(

        "method",

        "Unknown"

    )


    candidate.setdefault(

        "psm",

        "?"

    )


    candidate.setdefault(

        "confidence",

        0.0

    )


    return candidate


# ============================================================
# PRINT CANDIDATE
# ============================================================

def print_candidate(
    candidate,
    index=None
):

    if not isinstance(

        candidate,

        dict

    ):

        return


    prefix = ""


    if index is not None:

        prefix = f"{index}. "


    print(

        f"{prefix}"

        f"{get_method(candidate)} | "

        f"PSM {get_psm(candidate)} | "

        f"Confidence "

        f"{safe_float(candidate.get('confidence', 0.0)):.2f}% | "

        f"Code "

        f"{safe_float(candidate.get('code_quality', 0.0)):.4f} | "

        f"Syntax "

        f"{safe_float(candidate.get('syntax_score', 0.0)):.4f} | "

        f"Structure "

        f"{safe_float(candidate.get('structure_score', 0.0)):.4f} | "

        f"Rank "

        f"{safe_float(candidate.get('rank_score', 0.0)):.4f}"

    )


# ============================================================
# PRINT CANDIDATE DETAILS
# ============================================================

def print_candidate_details(
    candidate
):

    if not isinstance(

        candidate,

        dict

    ):

        return


    print(

        f"Confidence Score : "

        f"{safe_float(candidate.get('confidence_score', 0.0)):.4f}"

    )


    print(

        f"Syntax Score     : "

        f"{safe_float(candidate.get('syntax_score', 0.0)):.4f}"

    )


    print(

        f"Code Quality     : "

        f"{safe_float(candidate.get('code_quality', 0.0)):.4f}"

    )


    print(

        f"Structure Score   : "

        f"{safe_float(candidate.get('structure_score', 0.0)):.4f}"

    )


    print(

        f"Token Quality     : "

        f"{safe_float(candidate.get('token_quality', 0.0)):.4f}"

    )


    print(

        f"Readability       : "

        f"{safe_float(candidate.get('readability', 0.0)):.4f}"

    )


    print(

        f"Noise Penalty     : "

        f"{safe_float(candidate.get('noise_penalty', 0.0)):.4f}"

    )


    print(

        f"Ranking Score     : "

        f"{safe_float(candidate.get('rank_score', 0.0)):.4f}"

    )
