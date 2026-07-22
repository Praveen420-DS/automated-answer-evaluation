def confidence_level(similarity):

    if similarity >= 0.90:
        return "High"

    elif similarity >= 0.70:
        return "Medium"

    else:
        return "Low"