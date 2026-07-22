import os
import re


_model = None
_model_load_failed = False


def _fallback_similarity(expected: str, student: str) -> float:
    """Return a lightweight similarity score when the embedding model is unavailable."""
    expected_terms = set(re.findall(r"\w+", expected.lower()))
    student_terms = set(re.findall(r"\w+", student.lower()))
    if not expected_terms or not student_terms:
        return 0.0
    return len(expected_terms & student_terms) / len(expected_terms | student_terms)


def semantic_score(expected: str, student: str) -> float:
    """Calculate semantic similarity without making application startup depend on Hugging Face."""
    global _model, _model_load_failed

    # Opt in to model loading because downloading it at request time makes an API
    # unusable in offline and certificate-restricted deployments.
    if os.getenv("ENABLE_EMBEDDING_MODEL", "").lower() in {"1", "true", "yes"} and not _model_load_failed:
        try:
            if _model is None:
                from sentence_transformers import SentenceTransformer

                _model = SentenceTransformer("all-MiniLM-L6-v2")
            emb1 = _model.encode(expected, convert_to_tensor=True)
            emb2 = _model.encode(student, convert_to_tensor=True)
            from sentence_transformers import util

            return float(util.cos_sim(emb1, emb2))
        except Exception:
            # The service remains usable in offline or certificate-restricted environments.
            _model_load_failed = True

    return _fallback_similarity(expected, student)
