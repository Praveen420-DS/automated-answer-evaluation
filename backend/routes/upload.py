from flask import Blueprint
from controllers.upload_controller import upload_answer_script

upload_bp = Blueprint("upload", __name__)

upload_bp.route(
    "/answer-script",
    methods=["POST"]
)(upload_answer_script)