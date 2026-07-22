import re

def parse_model_answers(text):

    answers = {}

    pattern = r"Question\s*(\d+)[:.]([\s\S]*?)(?=Question\s*\d+[:.]|$)"

    matches = re.findall(
        pattern,
        text,
        re.IGNORECASE
    )

    for number, answer in matches:

        answers[int(number)] = answer.strip()

    return answers