from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models to ensure they're known to Flask-Migrate
    from app.modules.users.models import User
    from app.modules.features.models import Feature
    from app.modules.votes.models import Vote

    with app.app_context():
        db.create_all()
