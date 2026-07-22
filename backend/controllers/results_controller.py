from flask import jsonify
from services.evaluation_service import (
    latest_evaluation,
    evaluation_by_id
)


def get_latest_result():
    data = latest_evaluation()

    if not data:
        return jsonify({
            "success": False,
            "message": "No evaluation found"
        }), 404

    return jsonify(data), 200


def get_result_by_id(result_id):
    data = evaluation_by_id(result_id)

    if not data:
        return jsonify({
            "success": False,
            "message": "Evaluation not found"
        }), 404

    return jsonify(data), 200