from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database.mongodb import init_db
from routes.auth import auth_bp
from routes.student import student_bp
from routes.admin import admin_bp
from routes.faculty import faculty_bp
from routes.evaluation import evaluation_bp

# Create Flask application
app = Flask(__name__)

# ==============================
# Configuration
# ==============================

app.config.from_object(Config)

# ==============================
# Initialize Extensions
# ==============================

CORS(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*").split(",")}})

jwt = JWTManager(app)

init_db(app)

# API blueprints used by the React frontend.
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(student_bp, url_prefix="/api/student")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(faculty_bp, url_prefix="/api/faculty")
app.register_blueprint(evaluation_bp, url_prefix="/api/evaluation")

# ==============================
# Health Check Routes
# ==============================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "project": "EvalAI",
        "title": "AI Automated Answer Script Evaluation System",
        "version": "1.0.0",
        "status": "Backend Running Successfully"
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "database": "MongoDB",
        "server": "Running"
    })


# ==============================
# Error Handlers
# ==============================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "message": "Route Not Found"
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "message": "Internal Server Error"
    }), 500


# ==============================
# Run Server
# ==============================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
