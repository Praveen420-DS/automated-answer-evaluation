from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from database.mongodb import init_db
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.evaluation import evaluation_bp
from routes.results import results_bp
from routes.student import student_bp
from routes.teacher import faculty_bp
from routes.upload import upload_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    origins = app.config.get("CORS_ORIGINS", "*").split(",")
    CORS(app, resources={r"/api/*": {"origins": origins}})
    JWTManager(app)
    init_db(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(student_bp, url_prefix="/api/student")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(faculty_bp, url_prefix="/api/faculty")
    app.register_blueprint(evaluation_bp, url_prefix="/api/evaluation")
    app.register_blueprint(upload_bp, url_prefix="/api/upload")
    app.register_blueprint(results_bp, url_prefix="/api/results")

    @app.get("/")
    def home():
        return jsonify(project="EvalAI", status="Backend Running Successfully")

    @app.get("/api/health")
    def health():
        return jsonify(success=True, database="MongoDB", server="Running")

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify(success=False, message="Route Not Found"), 404

    @app.errorhandler(500)
    def internal_server_error(_error):
        return jsonify(success=False, message="Internal Server Error"), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
