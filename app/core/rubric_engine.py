def rubric_score(rubric, covered):

    score = 0

    total = sum(rubric.values())

    for concept, mark in rubric.items():

        if concept in covered:

            score += mark

    return score, total