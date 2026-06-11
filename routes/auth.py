import jwt
import re
from datetime import datetime, timedelta, timezone
from flask import Blueprint, request, jsonify, current_app
from extensions import db, bcrypt
from models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api")


def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return re.match(pattern, email) is not None


def validate_mobile(mobile):
    return mobile.isdigit() and 7 <= len(mobile) <= 15


# ── Register ──────────────────────────────────────────────────────────────────
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = (data.get("name") or "").strip()
    mobile = (data.get("mobile") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    confirm_password = data.get("confirm_password") or ""

    # Validations
    if not all([name, mobile, email, password, confirm_password]):
        return jsonify({"error": "All fields are required."}), 400

    if not validate_email(email):
        return jsonify({"error": "Invalid email format."}), 400

    if not validate_mobile(mobile):
        return jsonify({"error": "Mobile number must be 7–15 digits."}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters."}), 400

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email already exists."}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(name=name, mobile=mobile, email=email, password=hashed_pw)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Account created successfully! Please log in."}), 201


# ── Login ─────────────────────────────────────────────────────────────────────
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password."}), 401

    payload = {
        "user_id": user.id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")

    return jsonify({"token": token, "message": "Login successful!"}), 200


# ── Me (Get current user) ─────────────────────────────────────────────────────
@auth_bp.route("/me", methods=["GET"])
def me():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization token missing."}), 401

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(
            token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Session expired. Please log in again."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token."}), 401

    user = User.query.get(payload["user_id"])
    if not user:
        return jsonify({"error": "User not found."}), 404

    return jsonify({"user": user.to_dict()}), 200
