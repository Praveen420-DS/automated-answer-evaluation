from functools import wraps

from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request


def jwt_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            verify_jwt_in_request()
            request.user = get_jwt_identity()
        except Exception:
            return jsonify({
                "success": False,
                "message": "Authentication Required",
            }), 401

        return fn(*args, **kwargs)

    return wrapped
