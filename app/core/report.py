def generate_report(result):

    report = f"""
========================================
      AI ANSWER EVALUATION REPORT
========================================

Final Score          : {result['final_score']}/10
Grade                : {result['grade']}
Confidence           : {result['confidence']}

----------------------------------------

Semantic Similarity  : {round(result['semantic_similarity']*100,2)}%

Keyword Coverage     : {result['keyword_result']['coverage']}%

Concept Coverage     : {result['concept_result']['coverage']}%

Completeness         : {result['completeness']['percentage']}%

----------------------------------------

Missing Concepts

{', '.join(result['completeness']['missing'])}

----------------------------------------

Feedback
"""

    for item in result["feedback"]:
        report += f"\n• {item}"

    return report