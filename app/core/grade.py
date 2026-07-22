def get_grade(score):
    """
    Convert final score into grade.
    """

    if score >= 9:
        return "A+"

    elif score >= 8:
        return "A"

    elif score >= 7:
        return "B"

    elif score >= 6:
        return "C"

    elif score >= 5:
        return "D"

    else:
        return "F"