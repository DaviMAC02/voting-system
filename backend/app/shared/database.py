from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.modules.users.models import User
from app.modules.features.models import Feature
from app.modules.votes.models import Vote

engine = None
db_session = None
Base = declarative_base()


def init_db(app):
    global engine, db_session

    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    Base.query = db_session.query_property()

    Base.metadata.create_all(bind=engine)
