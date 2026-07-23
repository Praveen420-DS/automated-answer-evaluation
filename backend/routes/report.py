from flask import Blueprint, jsonify, send_file
from pathlib import Path
from flask_jwt_extended import get_jwt, get_jwt_identity
from middleware.auth_middleware import login_required
from database.mongodb import reports_collection
bp=Blueprint('report',__name__,url_prefix='/api/reports')
@bp.get('/<report_id>')
@login_required
def get_report(report_id):
    report = reports_collection().find_one({"$or": [{"_id": report_id}, {"evaluationId": report_id}]})
    if not report:
        return jsonify(success=False, message="Report not found"), 404
    if get_jwt().get("role") == "student" and report.get("studentEmail") != get_jwt_identity():
        return jsonify(success=False, message="Report not found"), 404
    path = report.get("path")
    if not path or not Path(path).is_file():
        return jsonify(success=False, message="Report file is unavailable"), 404
    return send_file(path, as_attachment=True)
