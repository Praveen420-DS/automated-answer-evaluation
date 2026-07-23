import sys
from pathlib import Path

# ``backend/app.py`` has the same module name as the internal ``app`` package.
# The repository root must come first so the shared library package ``app`` is
# imported from the project root. The backend folder follows so local backend
# modules such as ``routes`` and ``services`` remain importable.
BACKEND_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_ROOT.parent
for path in (PROJECT_ROOT, BACKEND_ROOT):
    if str(path) in sys.path:
        sys.path.remove(str(path))
    sys.path.insert(0, str(path))

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
from routes.analytics import analytics_bp
from routes.dashboard import bp as dashboard_bp
from routes.exam import bp as exam_bp
from routes.notification import bp as notification_bp
from routes.profile import bp as profile_bp
from routes.report import bp as report_bp
from routes.transcript import bp as transcript_bp


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
    # These blueprints already include their /api path in the route module.
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(transcript_bp)

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
