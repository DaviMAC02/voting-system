from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.modules.users.schemas import UserCreate, UserLogin
from app.modules.users.services.user_service import UserService
from app.modules.users.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)

users_bp = Blueprint("users", __name__)
user_service = UserService(SQLAlchemyUserRepository())


@users_bp.route("/register", methods=["POST"])
def register():
    try:
        user_data = UserCreate(**request.json)
        user = user_service.create_user(user_data)
        return jsonify({"message": "User registered successfully", "id": user.id}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@users_bp.route("/login", methods=["POST"])
def login():
    try:
        login_data = UserLogin(**request.json)
        user = user_service.authenticate_user(login_data.email, login_data.password)

        if not user:
            return jsonify({"message": "Invalid credentials"}), 401

        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token}), 200
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = user_service.get_user_by_id(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"id": user.id, "email": user.email, "name": user.name}), 200
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
