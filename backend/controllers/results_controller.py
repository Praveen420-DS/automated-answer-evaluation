from flask import jsonify
from services.evaluation_service import (
    latest_evaluation,
    evaluation_by_id
)


def get_latest_result(student_email=None):
    data = latest_evaluation(student_email)

    if not data:
        return jsonify({
            "success": False,
            "message": "No evaluation found"
        }), 404

    return jsonify(data), 200


def get_result_by_id(result_id, student_email=None):
    data = evaluation_by_id(result_id, student_email)

    if not data:
        return jsonify({
            "success": False,
            "message": "Evaluation not found"
        }), 404

    return jsonify(data), 200
