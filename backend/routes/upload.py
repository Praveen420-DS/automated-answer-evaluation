from flask import Blueprint, jsonify, request
from services.upload_service import save_upload
bp=Blueprint('upload',__name__,url_prefix='/api/uploads')
@bp.post('/')
def upload(): return jsonify(save_upload(request.files.get('file')))
