"""
Candidate Ranker V3.1

Purpose:
- Rank OCR candidates using code-aware signals.
- Penalize garbage OCR text.
- Prevent high Tesseract confidence from dominating
  when syntax and code structure are poor.
"""

import ast
import math
import re


# ============================================================
# CONFIGURATION
# ============================================================

MIN_TEXT_LENGTH = 3

CODE_KEYWORDS = {
    "def",
    "return",
    "for",
    "while",
    "if",
    "else",
    "elif",
    "class",
    "import",
    "from",
    "include",
    "int",
    "float",
    "char",
    "void",
    "printf",
    "scanf",
    "main",
    "function",
    "function",
    "array",
    "list",
}

PYTHON_KEYWORDS = {
    "def",
    "return",
    "for",
    "while",
    "if",
    "else",
    "elif",
    "class",
    "import",
    "from",
    "in",
    "range",
    "print",
    "append",
    "sort",
}

C_CPP_KEYWORDS = {
    "include",
    "int",
    "float",
    "double",
    "char",
    "void",
    "main",
    "printf",
    "scanf",
    "return",
    "for",
    "while",
    "if",
    "else",
}

CODE_SYMBOLS = [
    "{",
    "}",
    "(",
    ")",
    "[",
    "]",
    ";",
    "=",
    "<",
    ">",
    "#",
]


# ============================================================
# SAFE FLOAT
# ============================================================

def safe_float(value, default=0.0):

    try:
        value = float(value)

        if math.isnan(value):
            return default

        if math.isinf(value):
            return default

        return value

    except (
        TypeError,
        ValueError,
    ):

        return default


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    if text is None:

        return ""

    text = str(text)

    text = text.replace(
        "\x00",
        " "
    )

    text = text.replace(
        "\r",
        "\n"
    )

    return text.strip()


# ============================================================
# TOKENIZE
# ============================================================

def tokenize(text):

    text = normalize_text(
        text
    )

    return re.findall(
        r"[A-Za-z_][A-Za-z0-9_]*|"
        r"\d+|"
        r"[{}()\[\];,<>=+\-*/#]",
        text
    )


# ============================================================
# CODE KEYWORD SCORE
# ============================================================

def calculate_keyword_score(text):

    tokens = tokenize(
        text
    )

    if not tokens:

        return 0.0

    lowered = [

        token.lower()

        for token in tokens

    ]

    matches = sum(

        1

        for token in lowered

        if token in CODE_KEYWORDS

    )

    return min(

        1.0,

        matches / 4.0

    )


# ============================================================
# CODE SYMBOL SCORE
# ============================================================

def calculate_symbol_score(text):

    text = normalize_text(
        text
    )

    if not text:

        return 0.0

    symbol_count = sum(

        text.count(symbol)

        for symbol in CODE_SYMBOLS

    )

    return min(

        1.0,

        symbol_count / 8.0

    )


# ============================================================
# CODE SIGNAL
# ============================================================

def calculate_code_signal(text):

    text = normalize_text(
        text
    )

    if not text:

        return 0.0

    keyword_score = calculate_keyword_score(
        text
    )

    symbol_score = calculate_symbol_score(
        text
    )

    lines = [

        line.strip()

        for line in text.splitlines()

        if line.strip()

    ]

    line_score = min(

        1.0,

        len(lines) / 8.0

    )

    return min(

        1.0,

        (
            keyword_score * 0.50
            +
            symbol_score * 0.30
            +
            line_score * 0.20
        )

    )


# ============================================================
# PYTHON SYNTAX SCORE
# ============================================================

def python_syntax_score(text):

    text = normalize_text(
        text
    )

    if not text:

        return 0.0

    python_indicators = (

        "def " in text
        or
        "import " in text
        or
        "return " in text
        or
        "for " in text
        or
        "while " in text
        or
        "if " in text

    )

    if not python_indicators:

        return 0.0

    try:

        ast.parse(
            text
        )

        return 1.0

    except SyntaxError:

        # OCR code often contains small
        # syntax errors. Do not immediately
        # discard it.

        score = 0.4

        if "def " in text:

            score += 0.15

        if "return " in text:

            score += 0.15

        if "for " in text:

            score += 0.10

        if "if " in text:

            score += 0.10

        return min(

            1.0,

            score

        )


# ============================================================
# C / C++ SYNTAX SCORE
# ============================================================

def c_cpp_syntax_score(text):

    text = normalize_text(
        text
    )

    if not text:

        return 0.0

    score = 0.0

    if "#include" in text:

        score += 0.25

    if "main(" in text:

        score += 0.25

    if "int " in text:

        score += 0.10

    if "return" in text:

        score += 0.10

    if "printf" in text:

        score += 0.10

    if "scanf" in text:

        score += 0.10

    if "{" in text and "}" in text:

        score += 0.10

    return min(

        1.0,

        score

    )


# ============================================================
# SYNTAX SCORE
# ============================================================

def calculate_syntax_score(text):

    python_score = python_syntax_score(
        text
    )

    c_cpp_score = c_cpp_syntax_score(
        text
    )

    return max(

        python_score,

        c_cpp_score

    )


# ============================================================
# STRUCTURE SCORE
# ============================================================

def calculate_structure_score(text):

    text = normalize_text(
        text
    )

    if not text:

        return 0.0

    score = 0.0

    lines = [

        line.strip()

        for line in text.splitlines()

        if line.strip()

    ]

    # Multiple lines
    if len(lines) >= 2:

        score += 0.20

    if len(lines) >= 4:

        score += 0.10

    # Function structure
    if (
        "def " in text
        or
        "main(" in text
        or
        "function " in text.lower()
    ):

        score += 0.25

    # Control flow
    if any(

        keyword in text

        for keyword in [

            "for ",
            "while ",
            "if ",
            "else ",
            "elif ",

        ]

    ):

        score += 0.15

    # Return
    if "return" in text:

        score += 0.10

    # Brackets
    if "(" in text and ")" in text:

        score += 0.05

    if "[" in text and "]" in text:

        score += 0.05

    # C/C++ blocks
    if "{" in text and "}" in text:

        score += 0.10

    return min(

        1.0,

        score

    )


# ============================================================
# TOKEN QUALITY
# ============================================================

def calculate_token_quality(text):

    tokens = tokenize(
        text
    )

    if not tokens:

        return 0.0

    meaningful = 0

    for token in tokens:

        if len(token) >= 2:

            meaningful += 1

        elif token.isdigit():

            meaningful += 1

        elif token in CODE_SYMBOLS:

            meaningful += 1

    return min(

        1.0,

        meaningful / max(

            1,

            len(tokens)

        )

    )


# ============================================================
# READABILITY SCORE
# ============================================================

def calculate_readability_score(text):

    text = normalize_text(
        text
    )

    if not text:

        return 0.0

    characters = len(
        text
    )

    if characters == 0:

        return 0.0

    alphanumeric = sum(

        1

        for char in text

        if char.isalnum()

    )

    ratio = (

        alphanumeric

        /

        characters

    )

    return min(

        1.0,

        max(

            0.0,

            ratio

        )

    )


# ============================================================
# NOISE PENALTY
# ============================================================

def calculate_noise_penalty(text):

    text = normalize_text(
        text
    )

    if not text:

        return 1.0

    tokens = tokenize(
        text
    )

    if not tokens:

        return 1.0

    random_short_tokens = 0

    for token in tokens:

        if (

            token.isalpha()

            and

            len(token) <= 2

            and

            token.lower()

            not in {

                "if",
                "in",
                "is",
                "do",
                "or",
                "to",

            }

        ):

            random_short_tokens += 1

    short_token_ratio = (

        random_short_tokens

        /

        max(

            1,

            len(tokens)

        )

    )

    symbol_count = sum(

        1

        for char in text

        if not char.isalnum()

        and not char.isspace()

    )

    symbol_ratio = (

        symbol_count

        /

        max(

            1,

            len(text)

        )

    )

    penalty = (

        short_token_ratio * 0.70

        +

        min(

            1.0,

            symbol_ratio * 2.0

        ) * 0.30

    )

    return min(

        1.0,

        penalty

    )


# ============================================================
# CODE QUALITY
# ============================================================

def calculate_code_quality(

    syntax_score,

    structure_score,

    code_signal,

    token_quality,

    readability,

    noise_penalty

):

    base_score = (

        syntax_score * 0.35

        +

        structure_score * 0.25

        +

        code_signal * 0.20

        +

        token_quality * 0.10

        +

        readability * 0.10

    )

    return max(

        0.0,

        min(

            1.0,

            base_score

            -

            noise_penalty * 0.25

        )

    )


# ============================================================
# RANK CANDIDATE
# ============================================================

def rank_candidate(candidate):

    if not isinstance(
        candidate,
        dict
    ):

        return {

            "text": str(
                candidate
            ),

            "confidence": 0.0,

            "rank_score": 0.0,

        }

    text = normalize_text(

        candidate.get(

            "text",

            ""

        )

    )

    confidence = safe_float(

        candidate.get(

            "confidence",

            0.0

        )

    )

    # Convert percentage to 0-1
    if confidence > 1.0:

        confidence_score = (

            confidence / 100.0

        )

    else:

        confidence_score = confidence

    code_signal = calculate_code_signal(
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

    readability_score = calculate_readability_score(
        text
    )

    noise_penalty = calculate_noise_penalty(
        text
    )

    code_quality_score = calculate_code_quality(

        syntax_score,

        structure_score,

        code_signal,

        token_quality,

        readability_score,

        noise_penalty

    )

    # ========================================================
    # BASE RANK
    # ========================================================

    rank_score = (

        confidence_score * 0.20

        +

        syntax_score * 0.25

        +

        code_quality_score * 0.25

        +

        structure_score * 0.15

        +

        token_quality * 0.05

        +

        readability_score * 0.05

        -

        noise_penalty * 0.15

    )

    # ========================================================
    # HARD PENALTY
    #
    # High OCR confidence alone must not win.
    # ========================================================

    if (

        syntax_score == 0.0

        and

        structure_score == 0.0

        and

        code_signal < 0.20

    ):

        rank_score *= 0.35

    elif (

        syntax_score == 0.0

        and

        structure_score == 0.0

    ):

        rank_score *= 0.60

    # Strong code candidate bonus
    if (

        syntax_score >= 0.8

        and

        structure_score >= 0.7

    ):

        rank_score += 0.10

    rank_score = max(

        0.0,

        min(

            1.0,

            rank_score

        )

    )

    result = dict(
        candidate
    )

    result.update({

        "confidence_score":
            confidence_score,

        "syntax_score":
            syntax_score,

        "code_signal":
            code_signal,

        "code_quality_score":
            code_quality_score,

        "structure_score":
            structure_score,

        "token_quality_score":
            token_quality,

        "readability_score":
            readability_score,

        "noise_penalty":
            noise_penalty,

        "rank_score":
            rank_score,

    })

    return result


# ============================================================
# RANK ALL CANDIDATES
# ============================================================

def rank_candidates(
    candidates
):

    if not candidates:

        return []

    ranked = [

        rank_candidate(
            candidate
        )

        for candidate in candidates

    ]

    return sorted(

        ranked,

        key=lambda candidate:

            safe_float(

                candidate.get(

                    "rank_score",

                    0.0

                )

            ),

        reverse=True

    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_candidates = [

        {

            "text":
                "def test(array): return array",

            "confidence":
                50.0,

        },

        {

            "text":
                "hello random text",

            "confidence":
                80.0,

        },

        {

            "text":
                """
def test(array):
    for i in range(len(array)):
        return i
                """,

            "confidence":
                45.0,

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
                45.0,

        },

        {

            "text":
                "a i ak ny ii Be th wn ue",

            "confidence":
                90.0,

        },

    ]

    print(
        "=" * 60
    )

    print(
        "CANDIDATE RANKER V3.1 TEST"
    )

    print(
        "=" * 60
    )

    ranked = rank_candidates(

        test_candidates

    )

    for candidate in ranked:

        print()

        print(
            "Text:"
        )

        print(

            candidate.get(

                "text",

                ""

            )

        )

        print()

        print(

            f"Confidence : "
            f"{candidate.get('confidence', 0):.0f}%"

        )

        print(

            f"Rank Score : "
            f"{candidate.get('rank_score', 0):.4f}"

        )

        print(
            "Details:"
        )

        print(

            f"  confidence_score      : "
            f"{candidate.get('confidence_score', 0):.4f}"

        )

        print(

            f"  syntax_score          : "
            f"{candidate.get('syntax_score', 0):.4f}"

        )

        print(

            f"  code_signal           : "
            f"{candidate.get('code_signal', 0):.4f}"

        )

        print(

            f"  code_quality_score    : "
            f"{candidate.get('code_quality_score', 0):.4f}"

        )

        print(

            f"  structure_score       : "
            f"{candidate.get('structure_score', 0):.4f}"

        )

        print(

            f"  token_quality_score   : "
            f"{candidate.get('token_quality_score', 0):.4f}"

        )

        print(

            f"  readability_score     : "
            f"{candidate.get('readability_score', 0):.4f}"

        )

        print(

            f"  noise_penalty         : "
            f"{candidate.get('noise_penalty', 0):.4f}"

        )

    print()

    print(
        "=" * 60
    )

    print(
        "RANKER V3.1 TEST COMPLETE"
    )

    print(
        "=" * 60
    )