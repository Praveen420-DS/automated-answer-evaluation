def apply_rubric(score,rubric): return min(score,rubric.get('max_marks',score))
