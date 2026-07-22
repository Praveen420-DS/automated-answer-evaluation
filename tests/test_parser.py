from app.core.answer_parser import parse_answers


ocr_text = """
1. What is Machine Learning 2

Ans:

Machine Learning is a subset of Artificial Intelligence
that allows computers to learn from data.

2. What is Deep Learning 7

Ans:

Deep Learning is a subset of Machine Learning
that uses artificial neural networks.

3. What are the main types of Machine Learning 4

Ans:

The main types are:
Supervised Learning
Unsupervised Learning
Reinforcement Learning
"""


if __name__ == "__main__":

    result = parse_answers(ocr_text)

    print("\n===== PARSER RESULT =====\n")

    for answer in result:
        print("Question:", answer["question_number"])
        print("Answer:", answer["answer"])
        print("-" * 50)