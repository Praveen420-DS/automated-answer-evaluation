from flask import Blueprint, jsonify
bp=Blueprint('transcript',__name__,url_prefix='/api/transcripts')
@bp.get('/<exam_id>')
def transcript(exam_id): return jsonify(exam_id=exam_id, text='')
