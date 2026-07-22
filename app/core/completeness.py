def completeness_score(expected_concepts, covered_concepts):

    total = len(expected_concepts)

    covered = len(covered_concepts)

    if total == 0:
        return {
            "percentage": 0,
            "missing": []
        }

    missing = []

    for concept in expected_concepts:

        if concept not in covered_concepts:

            missing.append(concept)

    percentage = round((covered / total) * 100, 2)

    return {

        "percentage": percentage,

        "missing": missing

    }