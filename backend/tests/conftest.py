import os
import tempfile
import pytest
from app import create_app
from app.shared.database import db
from app.modules.users.models import User


@pytest.fixture(scope="session")
def app():
    """Create and configure a new app instance for the entire test session."""
    test_db_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(test_db_dir, "test.db")

    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{test_db_path}",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    with app.app_context():
        db.create_all()
        yield app

        db.session.remove()
        db.drop_all()

        if os.path.exists(test_db_path):
            try:
                os.unlink(test_db_path)
            except OSError:
                pass

        if os.path.exists(test_db_dir):
            try:
                os.rmdir(test_db_dir)
            except OSError:
                pass


@pytest.fixture(autouse=True)
def setup_database(app):
    """Reset database before each test."""
    with app.app_context():
        db.session.begin_nested()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
        yield
        db.session.rollback()
        db.session.close()


@pytest.fixture
def client(app):
    """Test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Test runner for CLI commands."""
    return app.test_cli_runner()


@pytest.fixture
def session(app):
    """Create a new database session for a test."""
    with app.app_context():
        s = db.session()
        yield s
        s.close()


@pytest.fixture
def user(app, client, session):
    """Create a test user and return the user instance with access token."""
    with app.app_context():
        register = client.post(
            "/api/users/register",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "password": "testpass123",
            },
        )
        if register.status_code != 201:
            raise ValueError(f"Failed to register user: {register.get_json()}")

        login = client.post(
            "/api/users/login",
            json={"email": "test@example.com", "password": "testpass123"},
        )
        if login.status_code != 200:
            raise ValueError(f"Failed to login user: {login.get_json()}")

        token = login.json["access_token"]
        user = session.query(User).filter_by(email="test@example.com").first()
        user.token = token
        yield user


@pytest.fixture
def auth_header(client):
    """Return Authorization header with a valid Bearer token."""
    register = client.post(
        "/api/users/register",
        json={
            "name": "Auth Test User",
            "email": "auth_test@example.com",
            "password": "testpass123",
        },
    )
    if register.status_code != 201:
        raise ValueError(f"Failed to register user: {register.get_json()}")

    login = client.post(
        "/api/users/login",
        json={"email": "auth_test@example.com", "password": "testpass123"},
    )
    if login.status_code != 200:
        raise ValueError(f"Failed to login user: {login.get_json()}")

    token = login.json["access_token"]
    return {"Authorization": f"Bearer {token}"}
