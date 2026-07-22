from flask import jsonify


def success(message="", data=None, status=200):

    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), status


def error(message="", status=400):

    return jsonify({
        "success": False,
        "message": message
    }), status