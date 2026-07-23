from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from middleware.auth_middleware import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

from database.mongodb import mongo, users_collection
from utils.student_excel import append_registered_student
from utils.workbook_users import find_csv_user, find_workbook_user

# Create Blueprint
auth_bp = Blueprint("auth", __name__)


def legacy_imported_user(identifier):
    """Read accounts imported by the original Excel script into separate collections."""
    wanted = identifier.lower()
    for collection_name, role, id_key in (
        ("students", "student", "Student ID"),
        ("staffs", "faculty", "Teacher ID"),
        ("faculty", "faculty", "Teacher ID"),
        ("admin", "admin", "Admin ID"),
        ("admins", "admin", "Admin ID"),
    ):
        document = mongo.db[collection_name].find_one({
            "$or": [{"Email": wanted}, {"email": wanted}, {id_key: {"$regex": f"^{identifier}$", "$options": "i"}}]
        })
        if document is None and "@" not in wanted:
            document = mongo.db[collection_name].find_one({"Email": f"{wanted}@evalai.com"})
        if not document:
            continue
        status = str(document.get("Status", document.get("status", "Active"))).lower()
        if status != "active":
            return None
        email = str(document.get("Email", document.get("email", ""))).strip().lower()
        account_id = str(document.get(id_key, document.get(id_key.replace(" ", "_"), ""))).strip()
        return {
            "fullName": document.get("Name", document.get("name", "")), "email": email,
            "username": account_id or email.split("@", 1)[0],
            "password": document.get("Password", document.get("password", "")),
            "role": role, "status": "Active",
        }
    return None

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

    # The provided CSV files are the demo login source of truth. This checks
    # Student, Staff (Teachers), and Admin files before MongoDB.
    user = find_csv_user(identifier, password)
    if user:
        users.update_one({"email": user["email"]}, {"$set": user}, upsert=True)
    else:
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
        user = legacy_imported_user(identifier)

    # Demo credentials are maintained in the supplied Excel workbook.  On a
    # fresh database, import the matching account on first successful login so
    # Staff and Admin can sign in without manually running an import script.
    if user is None:
        workbook_user = find_workbook_user(identifier, password)
        if workbook_user:
            users.update_one(
                {"email": workbook_user["email"]},
                {"$setOnInsert": workbook_user},
                upsert=True,
            )
            user = users.find_one({"email": workbook_user["email"]}) or workbook_user

    if user is None:

        return jsonify({

            "success": False,
            "message": "Invalid username or password"

        }), 404

    stored_password = str(user.get("password", ""))
    password_matches = (
        check_password_hash(stored_password, password)
        if stored_password.startswith(("pbkdf2:", "scrypt:"))
        else stored_password == password
    )
    if not password_matches:

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
            "fullName": user.get("fullName"), "email": user["email"], "role": user["role"], "photo": user.get("photo", ""),
        },
    })
