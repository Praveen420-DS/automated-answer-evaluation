import ast


def check_python_syntax(code: str) -> bool:
    """
    Check whether OCR-generated text is valid Python syntax.

    Returns:
        True  -> valid Python syntax
        False -> invalid Python syntax
    """

    if not code or not code.strip():
        return False

    try:
        ast.parse(code)
        return True

    except SyntaxError:
        return False


def syntax_score(code: str) -> float:
    """
    Return a syntax quality score.

    1.0 -> valid Python
    0.0 -> invalid Python
    """

    if check_python_syntax(code):
        return 1.0

    return 0.0


if __name__ == "__main__":

    valid_code = """
def test(array):
    for i in range(len(array)):
        return array[i]
"""

    invalid_code = """
def test(array)
    return array
"""

    print("Valid code:", check_python_syntax(valid_code))
    print("Invalid code:", check_python_syntax(invalid_code))

    print("Valid score:", syntax_score(valid_code))
    print("Invalid score:", syntax_score(invalid_code))