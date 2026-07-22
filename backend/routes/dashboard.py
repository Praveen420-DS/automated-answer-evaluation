from flask import Blueprint, jsonify
bp=Blueprint('dashboard',__name__,url_prefix='/api/dashboard')
@bp.get('/')
def dashboard(): return jsonify(active_exams=0, scripts_evaluated=0, students=0)
