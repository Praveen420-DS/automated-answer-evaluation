import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class LLMEvaluator:

    def __init__(self):
        pass

    def evaluate(
        self,
        question,
        answer_key,
        student_answer,
        total_marks
    ):

        prompt = f"""
You are an experienced university examiner.

Evaluate the student's answer.

Question:
{question}

Official Answer:
{answer_key}

Student Answer:
{student_answer}

Maximum Marks:
{total_marks}

Return ONLY valid JSON in this format:

{{
    "marks": number,
    "percentage": number,
    "feedback": "...",
    "strengths":[...],
    "missing_points":[...],
    "mistakes":[...],
    "grade":"A/B/C/D/F"
}}
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI answer sheet evaluator."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except Exception:
            return {
                "marks": 0,
                "percentage": 0,
                "feedback": content,
                "strengths": [],
                "missing_points": [],
                "mistakes": [],
                "grade": "F"
            }


llm_evaluator = LLMEvaluator()