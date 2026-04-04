from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    existing = User.query.filter_by(email=data["email"]).first()
    if existing:
        return jsonify({"message": "Email already registered"}), 400
    user = User(
        student_id=data["student_id"],
        fullname=data["full_name"],
        email=data["email"],
        password=data["password"]
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if not user or user.password != data["password"]:
        return jsonify({"message": "Invalid credentials"}), 401
    token = create_access_token(identity=str(user.user_id))
    return jsonify({"access_token": token, "fullname": user.fullname})