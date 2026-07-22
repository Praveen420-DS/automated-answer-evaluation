def concept_match(concepts, student_answer):

    student_answer = student_answer.lower()

    covered = []

    missing = []

    for concept in concepts:

        if concept.lower() in student_answer:

            covered.append(concept)

        else:

            missing.append(concept)

    return {

        "covered": covered,

        "missing": missing,

        "coverage": len(covered) / len(concepts) * 100 if concepts else 0

    }
