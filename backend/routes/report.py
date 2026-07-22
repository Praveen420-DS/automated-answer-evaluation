from flask import Blueprint, jsonify
bp=Blueprint('report',__name__,url_prefix='/api/reports')
@bp.get('/<report_id>')
def get_report(report_id): return jsonify(id=report_id, status='pending')
