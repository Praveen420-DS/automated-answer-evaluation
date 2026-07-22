from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load AI model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


class AnswerEvaluator:

    def __init__(self):
        pass

    # ===========================
    # Clean Text
    # ===========================
    def clean_text(self, text):

        if text is None:
            return ""

        text = text.lower()

        text = text.replace("\n", " ")

        text = text.strip()

        return text

    # ===========================
    # Semantic Similarity
    # ===========================
    def similarity_score(
        self,
        answer_key,
        student_answer
    ):

        answer_key = self.clean_text(answer_key)

        student_answer = self.clean_text(student_answer)

        embeddings = model.encode(
            [
                answer_key,
                student_answer
            ]
        )

        similarity = cosine_similarity(

            [embeddings[0]],
            [embeddings[1]]

        )[0][0]

        return float(similarity)

    # ===========================
    # Marks Calculation
    # ===========================
    def calculate_marks(
        self,
        similarity,
        total_marks
    ):

        marks = similarity * total_marks

        return round(marks, 2)

    # ===========================
    # AI Feedback
    # ===========================
    def feedback(
        self,
        similarity
    ):

        if similarity >= 0.90:

            return "Excellent Answer"

        elif similarity >= 0.75:

            return "Very Good Answer"

        elif similarity >= 0.60:

            return "Good Answer"

        elif similarity >= 0.40:

            return "Average Answer"

        else:

            return "Needs Improvement"

    # ===========================
    # Complete Evaluation
    # ===========================
    def evaluate(
        self,
        answer_key,
        student_answer,
        total_marks
    ):

        similarity = self.similarity_score(

            answer_key,
            student_answer

        )

        marks = self.calculate_marks(

            similarity,
            total_marks

        )

        feedback = self.feedback(

            similarity

        )

        return {

            "similarity": round(
                similarity,
                4
            ),

            "marks": marks,

            "feedback": feedback

        }


evaluator = AnswerEvaluator()