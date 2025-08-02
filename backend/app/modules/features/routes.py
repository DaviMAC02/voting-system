from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.modules.features.schemas import FeatureCreate, FeatureUpdate, FeatureResponse
from app.modules.features.services.feature_service import FeatureService
from app.modules.features.repositories.sqlalchemy_feature_repository import (
    SQLAlchemyFeatureRepository,
)

features_bp = Blueprint("features", __name__)
feature_service = FeatureService(SQLAlchemyFeatureRepository())


@features_bp.route("/", methods=["POST"])
@jwt_required()
def create_feature():
    try:
        user_id = get_jwt_identity()
        feature_data = FeatureCreate(**request.json)
        feature = feature_service.create_feature(feature_data, user_id)
        return jsonify(FeatureResponse.from_orm(feature).dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@features_bp.route("/", methods=["GET"])
def get_features():
    try:
        features_with_votes = feature_service.get_all_features()
        return (
            jsonify(
                [
                    {
                        **FeatureResponse.from_orm(feature).dict(),
                        "vote_count": vote_count,
                    }
                    for feature, vote_count in features_with_votes
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@features_bp.route("/<int:feature_id>", methods=["GET"])
def get_feature(feature_id: int):
    try:
        feature = feature_service.get_feature(feature_id)
        if not feature:
            return jsonify({"error": "Feature not found"}), 404
        return jsonify(FeatureResponse.from_orm(feature).dict()), 200
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@features_bp.route("/<int:feature_id>/status", methods=["PATCH"])
@jwt_required()
def update_feature_status(feature_id: int):
    try:
        update_data = FeatureUpdate(**request.json)
        feature = feature_service.update_feature_status(feature_id, update_data)
        if not feature:
            return jsonify({"error": "Feature not found"}), 404
        return jsonify(FeatureResponse.from_orm(feature).dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
