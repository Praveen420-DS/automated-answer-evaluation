import re


def parse_answers(text: str) -> list[dict]:
    """
    Convert OCR text into structured question-answer pairs.

    Supports formats like:
    1. Question
    1) Question
    Q1. Question
    Question 1. Question

    Returns:
        List of dictionaries containing:
        - question_number
        - question
        - answer
    """

    if not text or not text.strip():
        return []

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Detect:
    # 1. Question
    # 1) Question
    # Q1. Question
    # Q1) Question
    pattern = r"(?im)^\s*(?:Q(?:uestion)?\s*)?(\d+)[.)]\s*(.+)$"

    matches = list(re.finditer(pattern, text))

    answers = []

    for index, match in enumerate(matches):

        question_number = int(match.group(1))

        question_text = match.group(2).strip()

        start = match.end()

        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(text)

        answer_text = text[start:end].strip()

        # Remove OCR answer markers
        answer_text = re.sub(
            r"(?im)^\s*(?:Ans|Answer)\s*:\s*",
            "",
            answer_text
        ).strip()

        # Clean excessive blank lines
        answer_text = re.sub(
            r"\n{3,}",
            "\n\n",
            answer_text
        )

        answers.append(
            {
                "question_number": question_number,
                "question": question_text,
                "answer": answer_text,
            }
        )

    return answers