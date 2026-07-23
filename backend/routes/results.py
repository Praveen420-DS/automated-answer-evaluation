from flask import Blueprint, jsonify
from controllers.results_controller import get_latest_result, get_result_by_id
from middleware.auth_middleware import login_required
from flask_jwt_extended import get_jwt, get_jwt_identity

results_bp = Blueprint("results", __name__)

# Latest evaluated answer script
@results_bp.route("/latest", methods=["GET"])
@login_required
def latest_result():
    student_email = get_jwt_identity() if get_jwt().get("role") == "student" else None
    return get_latest_result(student_email)


# Get evaluation by ID
@results_bp.route("/<result_id>", methods=["GET"])
@login_required
def result_by_id(result_id):
    student_email = get_jwt_identity() if get_jwt().get("role") == "student" else None
    return get_result_by_id(result_id, student_email)
