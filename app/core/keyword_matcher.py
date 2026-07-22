def keyword_match(keywords, student_answer):

    student_answer = student_answer.lower()

    matched = []

    missing = []

    for word in keywords:

        if word.lower() in student_answer:

            matched.append(word)

        else:

            missing.append(word)

    coverage = len(matched) / len(keywords) * 100 if keywords else 0

    return {

        "matched": matched,

        "missing": missing,

        "coverage": coverage

    }
