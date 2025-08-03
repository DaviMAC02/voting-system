import pytest
from app.modules.users.models import User


def test_register(client):
    """Test user registration."""
    response = client.post(
        "/api/users/register",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    assert response.json["message"] == "User registered successfully"


def test_register_duplicate_email(client):
    """Test registration with duplicate email."""
    # First registration
    client.post(
        "/api/users/register",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        },
    )

    # Second registration with same email
    response = client.post(
        "/api/users/register",
        json={
            "name": "Jane Doe",
            "email": "john@example.com",
            "password": "password456",
        },
    )
    assert response.status_code == 400
    assert "already exists" in response.json["message"].lower()


def test_login_success(client):
    """Test successful login."""
    # Register a user first
    client.post(
        "/api/users/register",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        },
    )

    # Try to login
    response = client.post(
        "/api/users/login",
        json={"email": "john@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json


def test_login_wrong_password(client):
    """Test login with wrong password."""
    # Register a user first
    client.post(
        "/api/users/register",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        },
    )

    # Try to login with wrong password
    response = client.post(
        "/api/users/login",
        json={"email": "john@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "invalid credentials" in response.json["message"].lower()


def test_get_current_user(client, auth_header):
    """Test getting current user information."""
    response = client.get("/api/users/me", headers=auth_header)
    assert response.status_code == 200
    assert response.json["email"] == "auth_test@example.com"
