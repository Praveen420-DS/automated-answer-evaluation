from flask import request, jsonify
from services.upload_service import process_answer_script

def upload_answer_script():

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file uploaded"
        }), 400

    file = request.files["file"]

    result = process_answer_script(file)

    return jsonify(result)