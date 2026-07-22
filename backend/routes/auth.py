from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from middleware.auth_middleware import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

from database.mongodb import users_collection
from utils.student_excel import append_registered_student

# Create Blueprint
auth_bp = Blueprint("auth", __name__)

# ===========================
# Register API
# ===========================

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json(silent=True) or {}

    full_name = data.get("fullName")
    email = (data.get("email") or "").strip().lower()
    username = (data.get("username") or "").strip()
    password = data.get("password")
    role = data.get("role", "student").lower()
    if role == "staff":
        role = "faculty"

    # Validation
    if not full_name or not email or not password or role not in {"student", "faculty", "admin"}:
        return jsonify({
            "success": False,
            "message": "All fields are required."
        }), 400

    users = users_collection()

    # Check existing user
    if users.find_one({"email": email}):

        return jsonify({
            "success": False,
            "message": "Email already exists."
        }), 409

    # Encrypt password
    hashed_password = generate_password_hash(password)

    user = {

        "fullName": full_name,
        "email": email,
        "username": username,
        "password": hashed_password,
        "role": role

    }

    insert_result = users.insert_one(user)

    # Self-service registration is only for students.  Keep the shared
    # Students workbook in sync with each account created through this route.
    excel_details = None
    if role == "student":
        try:
            excel_details = append_registered_student(
                full_name=full_name,
                email=email,
                password_hash=hashed_password,
            )
        except Exception:
            users.delete_one({"_id": insert_result.inserted_id})
            return jsonify({
                "success": False,
                "message": "Unable to save the student registration. Please try again."
            }), 500

    return jsonify({

        "success": True,
        "message": "Registration Successful",
        "student": excel_details,

    }), 201


# ===========================
# Login API
# ===========================

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    identifier = (data.get("email") or data.get("username") or "").strip().lower()
    password = data.get("password")

    if not identifier or not password:
        return jsonify({
            "success": False,
            "message": "Username and password are required."
        }), 400

    users = users_collection()

    user = users.find_one({
        "$or": [
            {"email": identifier},
            {"username": identifier}
        ]
    })

    # Imported users use email addresses as their identifiers. Allow the
    # short form shown in the login screen (for example, "student001").
    if user is None and "@" not in identifier:
        user = users.find_one({"email": f"{identifier}@evalai.com"})

    if user is None:

        return jsonify({

            "success": False,
            "message": "Invalid username or password"

        }), 404

    if not check_password_hash(user["password"], password):

        return jsonify({

            "success": False,
            "message": "Invalid Password"

        }), 401

    token = create_access_token(

        identity=user["email"],
        additional_claims={
            "role": user["role"]
        },
        expires_delta=timedelta(days=1)

    )

    return jsonify({

        "success": True,
        "token": token,
        "role": user["role"],
        "user": {
            "username": user.get("username") or user.get("fullName") or user["email"],
            "email": user["email"],
            "role": user["role"]
        }

    }), 200


# ===========================
# Profile API
# ===========================

@auth_bp.route("/profile", methods=["GET"])
@login_required
def profile():
    user = users_collection().find_one({"email": get_jwt_identity()})
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    return jsonify({
        "success": True,
        "user": {
            "id": str(user["_id"]), "username": user.get("username") or user.get("fullName"),
            "fullName": user.get("fullName"), "email": user["email"], "role": user["role"],
        },
    })
