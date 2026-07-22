from flask import Blueprint, jsonify
from controllers.results_controller import get_latest_result, get_result_by_id

results_bp = Blueprint("results", __name__)

# Latest evaluated answer script
@results_bp.route("/latest", methods=["GET"])
def latest_result():
    return get_latest_result()


# Get evaluation by ID
@results_bp.route("/<result_id>", methods=["GET"])
def result_by_id(result_id):
    return get_result_by_id(result_id)