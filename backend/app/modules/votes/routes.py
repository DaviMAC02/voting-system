from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.modules.votes.schemas import VoteCreate, VoteResponse
from app.modules.votes.services.vote_service import VoteService
from app.modules.votes.repositories.sqlalchemy_vote_repository import (
    SQLAlchemyVoteRepository,
)

votes_bp = Blueprint("votes", __name__)
vote_service = VoteService(SQLAlchemyVoteRepository())


@votes_bp.route("/", methods=["POST"])
@jwt_required()
def toggle_vote():
    try:
        user_id = get_jwt_identity()
        vote_data = VoteCreate(**request.json)
        vote = vote_service.toggle_vote(vote_data, user_id)

        if vote is None:
            return jsonify({"message": "Vote removed"}), 200

        return jsonify(VoteResponse.model_validate(vote).model_dump()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@votes_bp.route("/features/<int:feature_id>/count", methods=["GET"])
def get_vote_count(feature_id: int):
    try:
        # First check if feature exists
        feature = vote_service.feature_service.get_feature_by_id(feature_id)
        if not feature:
            return jsonify({"error": "Feature not found"}), 404

        count = vote_service.get_vote_count(feature_id)
        return jsonify({"count": count}), 200
    except Exception as e:
        print(f"Error getting vote count: {e}")
        return jsonify({"error": "Internal server error"}), 500


@votes_bp.route("/", methods=["GET"])
def get_all_votes():
    try:
        votes = vote_service.get_all_votes()
        return (
            jsonify([VoteResponse.model_validate(vote).model_dump() for vote in votes]),
            200,
        )
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@votes_bp.route("/features/<int:feature_id>/user-vote", methods=["GET"])
@jwt_required()
def get_user_vote(feature_id: int):
    try:
        # First check if feature exists
        feature = vote_service.feature_service.get_feature_by_id(feature_id)
        if not feature:
            return jsonify({"error": "Feature not found"}), 404

        user_id = get_jwt_identity()
        vote = vote_service.get_user_vote(feature_id, user_id)

        if not vote:
            return jsonify({"message": "No vote found"}), 404

        return jsonify(VoteResponse.model_validate(vote).model_dump()), 200
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
