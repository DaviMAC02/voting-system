import os
import sys
from datetime import datetime

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(backend_dir)

from app import create_app
from app.shared.database import db
from app.modules.users.models import User
from app.modules.features.models import Feature
from app.modules.features.schemas import FeatureCategory, FeatureStatus
from app.modules.votes.models import Vote
from werkzeug.security import generate_password_hash


def clear_database():
    """Clear all data from the database."""
    # Delete in order to respect foreign key constraints
    Vote.query.delete()
    Feature.query.delete()
    User.query.delete()
    db.session.commit()
    print("Database cleared successfully!")


def seed_database():
    """Seed the database with mock data."""
    # Clear existing data
    clear_database()

    # Create test users
    users = [
        User(
            name="John Doe",
            email="john@example.com",
            password=generate_password_hash("password123"),
            created_at=datetime.utcnow(),
        ),
        User(
            name="Jane Doe",
            email="jane@example.com",
            password=generate_password_hash("password123"),
            created_at=datetime.utcnow(),
        ),
        User(
            name="Bob Smith",
            email="bob@example.com",
            password=generate_password_hash("password123"),
            created_at=datetime.utcnow(),
        ),
    ]

    # Add users to session
    for user in users:
        db.session.add(user)
    db.session.commit()

    # Create features
    features = [
        Feature(
            title="Dark Mode Support",
            description="Add dark mode to improve visibility in low-light conditions",
            category=FeatureCategory.ENHANCEMENT,
            status=FeatureStatus.OPEN,
            created_at=datetime.utcnow(),
            user_id=users[0].id,
        ),
        Feature(
            title="Mobile App",
            description="Create a native mobile app for iOS and Android",
            category=FeatureCategory.FEATURE,
            status=FeatureStatus.OPEN,
            created_at=datetime.utcnow(),
            user_id=users[1].id,
        ),
        Feature(
            title="Export to PDF",
            description="Allow users to export their data to PDF format",
            category=FeatureCategory.FEATURE,
            status=FeatureStatus.OPEN,
            created_at=datetime.utcnow(),
            user_id=users[2].id,
        ),
        Feature(
            title="Integration with Slack",
            description="Add Slack integration for notifications",
            category=FeatureCategory.ENHANCEMENT,
            status=FeatureStatus.OPEN,
            created_at=datetime.utcnow(),
            user_id=users[0].id,
        ),
    ]

    # Add features to session
    for feature in features:
        db.session.add(feature)
    db.session.commit()

    # Create some initial likes
    votes = [
        # Dark Mode likes
        Vote(user_id=users[1].id, feature_id=features[0].id),
        Vote(user_id=users[2].id, feature_id=features[0].id),
        # Mobile App likes
        Vote(user_id=users[0].id, feature_id=features[1].id),
        Vote(user_id=users[2].id, feature_id=features[1].id),
        # Export to PDF likes
        Vote(user_id=users[0].id, feature_id=features[2].id),
        # Slack Integration likes
        Vote(user_id=users[1].id, feature_id=features[3].id),
    ]

    # Add votes to session
    for vote in votes:
        db.session.add(vote)
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_database()
        print("Database seeded successfully!")
