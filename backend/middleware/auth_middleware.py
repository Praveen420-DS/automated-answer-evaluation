from functools import wraps

from flask import jsonify

from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt
)


# ===============================
# Login Required
# ===============================

def login_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):

        try:

            verify_jwt_in_request()

            return fn(*args, **kwargs)

        except Exception:

            return jsonify({

                "success": False,
                "message": "Authentication Required"

            }), 401

    return wrapper


# ===============================
# Admin Only
# ===============================

def admin_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):

        try:

            verify_jwt_in_request()

            claims = get_jwt()

            if claims["role"] != "admin":

                return jsonify({

                    "success": False,
                    "message": "Admin Access Only"

                }), 403

            return fn(*args, **kwargs)

        except Exception:

            return jsonify({

                "success": False,
                "message": "Invalid Token"

            }), 401

    return wrapper


# ===============================
# Faculty Only
# ===============================

def faculty_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):

        try:

            verify_jwt_in_request()

            claims = get_jwt()

            if claims["role"] != "faculty":

                return jsonify({

                    "success": False,
                    "message": "Faculty Access Only"

                }), 403

            return fn(*args, **kwargs)

        except Exception:

            return jsonify({

                "success": False,
                "message": "Invalid Token"

            }), 401

    return wrapper


# ===============================
# Student Only
# ===============================

def student_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):

        try:

            verify_jwt_in_request()

            claims = get_jwt()

            if claims["role"] != "student":

                return jsonify({

                    "success": False,
                    "message": "Student Access Only"

                }), 403

            return fn(*args, **kwargs)

        except Exception:

            return jsonify({

                "success": False,
                "message": "Invalid Token"

            }), 401

    return wrapper