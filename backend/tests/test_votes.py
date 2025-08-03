from app.modules.features.models import Feature, FeatureCategory
from app.modules.users.models import User
from app.modules.votes.models import Vote


def test_create_vote(client, session, user: User, auth_header):
    create_feature_response = client.post(
        "/api/features",
        headers=auth_header,
        json={
            "title": "Test Feature",
            "description": "Test Description",
            "category": "FEATURE",
        },
    )
    assert create_feature_response.status_code == 201
    feature = create_feature_response.json
    feature_id = feature["id"]

    # Create a like
    response = client.post(
        "/api/votes",
        json={"feature_id": feature_id},
        headers=auth_header,
    )

    assert response.status_code == 201
    json_data = response.get_json()
    assert "id" in json_data
    assert json_data["feature_id"] == feature_id


def test_get_like_count(client, session, user: User, auth_header):
    # Create a feature
    feature = Feature(
        title="Test Feature",
        description="Test Description",
        category=FeatureCategory.FEATURE,
        user_id=user.id,
    )
    session.add(feature)
    session.commit()

    # Create a like
    response = client.post(
        "/api/votes",
        json={"feature_id": feature.id},
        headers=auth_header,
    )
    assert response.status_code == 201

    # Get vote count
    response = client.get(f"/api/votes/features/{feature.id}/count")
    assert response.status_code == 200
    json_data = response.get_json()
    assert "count" in json_data
    assert json_data["count"] == 1


def test_toggle_like(client, session, user: User, auth_header):
    # Create a feature
    feature = Feature(
        title="Test Feature",
        description="Test Description",
        category=FeatureCategory.FEATURE,
        user_id=user.id,
    )
    session.add(feature)
    session.commit()

    # Add a like
    response = client.post(
        "/api/votes",
        json={"feature_id": feature.id},
        headers=auth_header,
    )
    assert response.status_code == 201
    vote_id = response.json["id"]

    # Toggle like (removes it)
    response = client.post(
        "/api/votes",
        json={"feature_id": feature.id},
        headers=auth_header,
    )
    assert response.status_code == 200
    assert response.json["message"] == "Vote removed"

    # Verify like is deleted
    assert session.query(Vote).filter_by(id=vote_id).first() is None


def test_multiple_users_like(client, session, user: User, auth_header):
    other_user = User(
        email="other@example.com", name="Other User", password="password123"
    )
    session.add(other_user)
    session.commit()

    feature_response = client.post(
        "/api/features",
        headers=auth_header,
        json={
            "title": "Test Feature",
            "description": "Test Description",
            "category": "FEATURE",
        },
    )
    assert feature_response.status_code == 201
    feature = feature_response.json
    feature_id = feature["id"]

    response1 = client.post(
        "/api/votes",
        json={"feature_id": feature_id},
        headers=auth_header,
    )
    assert response1.status_code == 201
    count_response = client.get(f"/api/votes/features/{feature_id}/count")
    assert count_response.status_code == 200
    assert count_response.json["count"] == 1
