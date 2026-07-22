from flask import Blueprint, jsonify, request
bp=Blueprint('exam',__name__,url_prefix='/api/exams')
@bp.get('/')
def list_exams(): return jsonify(items=[])
@bp.post('/')
def create_exam(): return jsonify(message='Exam created', exam=request.get_json(silent=True) or {}), 201
