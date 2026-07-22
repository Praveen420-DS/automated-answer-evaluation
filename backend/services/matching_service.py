def match_questions_with_answers(
        questions,
        model_answers
):

    matched = []

    for question in questions:

        number = question["number"]

        matched.append({

            "number": number,

            "question": question["question"],

            "marks": question["marks"],

            "model_answer": model_answers.get(
                number,
                ""
            )

        })

    return matched