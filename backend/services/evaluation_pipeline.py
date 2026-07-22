from ai.evaluator import evaluate_question

def evaluate_exam(
    questions,
    model_answers,
    student_answers
):

    evaluated = []

    total = 0

    obtained = 0

    for q in questions:

        question = q["question"]

        model = model_answers[q["number"]]

        student = student_answers.get(
            q["number"],
            ""
        )

        result = evaluate_question(
            question,
            model,
            student,
            q["marks"]
        )

        result["question_number"] = q["number"]

        evaluated.append(result)

        total += q["marks"]

        obtained += result["obtained_marks"]

    percentage = round(
        obtained * 100 / total,
        2
    )

    if percentage >= 90:
        grade = "O"
    elif percentage >= 80:
        grade = "A+"
    elif percentage >= 70:
        grade = "A"
    elif percentage >= 60:
        grade = "B+"
    elif percentage >= 50:
        grade = "B"
    else:
        grade = "RA"

    return {
        "summary":{
            "total_marks":obtained,
            "maximum_marks":total,
            "percentage":percentage,
            "grade":grade
        },
        "questions":evaluated
    }