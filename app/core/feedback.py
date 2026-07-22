def generate_feedback(result):
    """
    Generate feedback based on evaluation result.
    """

    feedback = []

    # -------- Semantic Similarity --------
    similarity = result["semantic_similarity"]

    if similarity >= 0.85:
        feedback.append("✅ Excellent understanding of the answer.")
    elif similarity >= 0.70:
        feedback.append("✅ Good understanding, but there is room for improvement.")
    else:
        feedback.append("❌ The answer is significantly different from the expected answer.")

    # -------- Keyword Coverage --------
    keyword_coverage = result["keyword_result"]["coverage"]

    if keyword_coverage == 100:
        feedback.append("✅ All important keywords are covered.")
    elif keyword_coverage >= 70:
        feedback.append("✅ Most important keywords are covered.")
    else:
        feedback.append("❌ Many important keywords are missing.")

    # -------- Completeness --------
    completeness = result["completeness"]["percentage"]

    if completeness == 100:
        feedback.append("✅ The answer is complete.")
    elif completeness >= 70:
        feedback.append("✅ The answer is mostly complete.")
    else:
        feedback.append("❌ The answer is incomplete.")

    # -------- Missing Concepts --------
    missing = result["completeness"]["missing"]

    if len(missing) > 0:
        feedback.append(
            "📌 Missing Concepts: " + ", ".join(missing)
        )
        feedback.append(
            "💡 Suggestion: Include the missing concepts to improve your score."
        )
    else:
        feedback.append("🎉 Excellent! No concepts are missing.")

    return feedback