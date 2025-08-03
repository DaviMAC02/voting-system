from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.modules.features.schemas import FeatureCreate, FeatureResponse
from app.modules.features.services.feature_service import FeatureService
from app.modules.features.repositories.sqlalchemy_feature_repository import (
    SQLAlchemyFeatureRepository,
)

features_bp = Blueprint("features", __name__)
feature_service = FeatureService(SQLAlchemyFeatureRepository())


@features_bp.route("/", methods=["POST"])
@jwt_required()
def create_feature():
    user_id = get_jwt_identity()

    try:
        data = request.get_json()
        try:
            feature_create = FeatureCreate(**data)
        except Exception as validation_error:
            return jsonify({"error": "Invalid feature data"}), 400

        try:
            feature = feature_service.create_feature(
                title=feature_create.title,
                description=feature_create.description,
                category=feature_create.category,
                created_by_id=user_id,
            )
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        try:
            response = FeatureResponse.model_validate(feature)
            return jsonify(response.model_dump()), 201
        except Exception as e:
            return jsonify({"error": "Error creating feature response"}), 500
    except Exception as e:
        print(f"Unexpected error in create_feature: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@features_bp.route("/", methods=["GET"])
def get_features():
    try:
        features = feature_service.get_features()
        response = [
            FeatureResponse.model_validate(feature).model_dump() for feature in features
        ]
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@features_bp.route("/<int:feature_id>", methods=["GET"])
def get_feature(feature_id):
    try:
        feature = feature_service.get_feature_by_id(feature_id)
        if not feature:
            return jsonify({"message": "Feature not found"}), 404
        response = FeatureResponse.model_validate(feature).model_dump()
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@features_bp.route("/<int:feature_id>", methods=["PUT"])
@jwt_required()
def update_feature(feature_id):
    user_id = get_jwt_identity()

    try:
        data = request.get_json()
        feature_create = FeatureCreate(**data)

        feature = feature_service.update_feature(
            feature_id=feature_id,
            title=feature_create.title,
            description=feature_create.description,
            category=feature_create.category,
            user_id=user_id,
        )

        response = FeatureResponse.model_validate(feature).model_dump()
        return jsonify(response)
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@features_bp.route("/<int:feature_id>", methods=["DELETE"])
@jwt_required()
def delete_feature(feature_id):
    user_id = get_jwt_identity()

    try:
        feature_service.delete_feature(feature_id, user_id)
        return jsonify({"message": "Feature deleted successfully"})
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
