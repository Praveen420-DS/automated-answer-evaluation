from flask import Blueprint, jsonify
bp=Blueprint('profile',__name__,url_prefix='/api/profile')
@bp.get('/')
def profile(): return jsonify(user=None)
