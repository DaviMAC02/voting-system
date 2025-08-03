import pytest
from app.modules.features.models import Feature


def test_create_feature(client, auth_header):
    """Test feature creation."""
    response = client.post(
        "/api/features",
        headers=auth_header,
        json={
            "title": "Test Feature",
            "description": "This is a test feature",
            "category": "BUG",
        },
    )
    assert response.status_code == 201
    assert response.json["title"] == "Test Feature"
    assert response.json["description"] == "This is a test feature"
    assert response.json["category"] == "BUG"


def test_create_feature_unauthorized(client):
    """Test feature creation without authentication."""
    response = client.post(
        "/api/features",
        json={
            "title": "Test Feature",
            "description": "This is a test feature",
            "category": "Feature",
        },
    )
    assert response.status_code == 401


def test_get_all_features(client):
    """Test getting all features."""
    # Create a test feature first
    auth_response = client.post(
        "/api/users/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpass123",
        },
    )
    login_response = client.post(
        "/api/users/login",
        json={"email": "test@example.com", "password": "testpass123"},
    )
    auth_header = {"Authorization": f'Bearer {login_response.json["access_token"]}'}

    client.post(
        "/api/features",
        headers=auth_header,
        json={
            "title": "Test Feature",
            "description": "This is a test feature",
            "category": "FEATURE",
        },
    )

    # Get all features
    response = client.get("/api/features")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    assert response.json[0]["title"] == "Test Feature"


def test_get_feature_by_id(client, auth_header):
    """Test getting a specific feature."""
    # Create a test feature first
    create_response = client.post(
        "/api/features",
        headers=auth_header,
        json={
            "title": "Test Feature",
            "description": "This is a test feature",
            "category": "FEATURE",
        },
    )
    feature_id = create_response.json["id"]

    # Get the feature
    response = client.get(f"/api/features/{feature_id}")
    assert response.status_code == 200
    assert response.json["id"] == feature_id
    assert response.json["title"] == "Test Feature"


def test_get_nonexistent_feature(client):
    """Test getting a feature that doesn't exist."""
    response = client.get("/api/features/999")
    assert response.status_code == 404
