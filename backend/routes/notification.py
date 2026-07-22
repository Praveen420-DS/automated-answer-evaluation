from flask import Blueprint, jsonify
bp=Blueprint('notification',__name__,url_prefix='/api/notifications')
@bp.get('/')
def notifications(): return jsonify(items=[])
