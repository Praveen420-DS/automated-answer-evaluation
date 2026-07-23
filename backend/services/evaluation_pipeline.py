from services.app_evaluation_adapter import evaluate_parsed_answer

def evaluate_exam(
    questions,
    model_answers,
    student_answers
):

    evaluated = []

    total = 0

    obtained = 0

    for q in questions:

        question = q.get("question", q.get("question_text", ""))

        number = q.get("number", q.get("question_number"))
        model = model_answers.get(number, model_answers.get(str(number), ""))

        student = student_answers.get(
            number,
            ""
        )

        result = evaluate_parsed_answer(
            number,
            question,
            model,
            student,
            q.get("marks", q.get("maximum_score", 0)),
        )

        evaluated.append(result)

        total += result["maximum_score"]
        obtained += result["score"]

    percentage = round(obtained * 100 / total, 2) if total else 0

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
