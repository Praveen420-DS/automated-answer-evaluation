from app.core.answer_parser import parse_answers


OCR_TEXT = """
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


def test_parse_answers_extracts_all_questions():
    results = parse_answers(OCR_TEXT)

    assert len(results) == 3
    assert [str(item["question_number"]) for item in results] == [
        "1",
        "2",
        "3",
    ]


def test_parse_answers_extracts_correct_content():
    results = parse_answers(OCR_TEXT)

    assert "subset of Artificial Intelligence" in results[0]["answer"]
    assert "artificial neural networks" in results[1]["answer"]
    assert "Supervised Learning" in results[2]["answer"]
    assert "Reinforcement Learning" in results[2]["answer"]


def test_parse_answers_removes_answer_label():
    results = parse_answers(OCR_TEXT)

    for result in results:
        assert not result["answer"].strip().lower().startswith("ans:")