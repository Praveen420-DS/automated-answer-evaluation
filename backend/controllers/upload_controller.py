from flask import request, jsonify
from services.upload_service import process_answer_script
from services.app_ocr_adapter import OCRProcessingError
from middleware.auth_middleware import faculty_required

@faculty_required
def upload_answer_script():

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file uploaded"
        }), 400

    file = request.files["file"]

    try:
        result = process_answer_script(file)
    except (ValueError, OCRProcessingError) as error:
        return jsonify({"success": False, "message": str(error)}), 422

    return jsonify(result)
