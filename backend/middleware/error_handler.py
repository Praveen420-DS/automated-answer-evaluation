from flask import jsonify
def register_error_handlers(app):
 @app.errorhandler(Exception)
 def handle_error(error): return jsonify(error=str(error)),500
