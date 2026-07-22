from flask import Blueprint, request, jsonify
from datetime import datetime
import os
from pathlib import Path
from werkzeug.utils import secure_filename

from database.mongodb import (
    answer_scripts_collection,
    evaluations_collection
)

from middleware.auth_middleware import faculty_required

evaluation_bp = Blueprint("evaluation", __name__)

UPLOAD_FOLDER = Path(__file__).resolve().parents[1] / "uploads" / "answer_scripts"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@evaluation_bp.route("/start", methods=["POST"])
@faculty_required
def start_evaluation():
    """Start a review batch after answer sheets have been uploaded.

    OCR and semantic evaluation are intentionally queued per uploaded file so
    a slow document never blocks the HTTP request.
    """
    queued = answer_scripts_collection().count_documents({})
    if not queued:
        return jsonify({"success": False, "message": "Upload at least one answer script first."}), 400
    return jsonify({"success": True, "message": "Evaluation batch started", "queuedScripts": queued}), 202


# ==========================================
# Upload Student Answer Sheet
# ==========================================

@evaluation_bp.route("/upload-answer-sheet", methods=["POST"])
@faculty_required
def upload_answer_sheet():

    if "file" not in request.files:

        return jsonify({
            "success": False,
            "message": "No file uploaded"
        }), 400

    file = request.files["file"]

    filename = secure_filename(file.filename)
    if not filename:
        return jsonify({"success": False, "message": "Invalid filename"}), 400

    filepath = UPLOAD_FOLDER / filename

    file.save(filepath)

    answer_scripts_collection().insert_one({

        "filename": filename,
        "path": str(filepath),
        "uploadedAt": datetime.utcnow()

    })

    return jsonify({

        "success": True,
        "message": "Answer Sheet Uploaded Successfully",
        "file": filename

    })


# ==========================================
# OCR Extraction
# ==========================================

@evaluation_bp.route("/ocr/<filename>", methods=["GET"])
@faculty_required
def run_ocr(filename):

    filename = secure_filename(filename)
    filepath = UPLOAD_FOLDER / filename

    if not os.path.exists(filepath):

        return jsonify({

            "success": False,
            "message": "File Not Found"

        }), 404

    try:
        import easyocr
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(filepath)
    except ImportError:
        return jsonify({
            "success": False,
            "message": "OCR is not installed. Install the optional AI requirements first."
        }), 503

    extracted_text = ""

    for item in result:

        extracted_text += item[1] + "\n"

    evaluations_collection().insert_one({

        "filename": filename,
        "ocrText": extracted_text,
        "createdAt": datetime.utcnow()

    })

    return jsonify({

        "success": True,
        "filename": filename,
        "text": extracted_text

    })


# ==========================================
# View OCR Result
# ==========================================

@evaluation_bp.route("/ocr-results", methods=["GET"])
@faculty_required
def get_results():

    data = []

    for doc in evaluations_collection().find():

        doc["_id"] = str(doc["_id"])

        data.append(doc)

    return jsonify({

        "success": True,
        "count": len(data),
        "data": data

    })
