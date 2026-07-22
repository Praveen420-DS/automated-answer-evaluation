import re

QUESTION_PATTERN = re.compile(
    r"Q(?:uestion)?\s*(\d+)[.:)]\s*(.*?)\s*\((\d+)\s*Marks?\)",
    re.IGNORECASE | re.DOTALL
)

def parse_questions(text):

    questions = []

    matches = QUESTION_PATTERN.findall(text)

    for number, question, marks in matches:

        questions.append({
            "number": int(number),
            "question": question.strip(),
            "marks": int(marks)
        })

    return questions