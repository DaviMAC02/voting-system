from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.users.models import User
from app.modules.users.interfaces.user_repository import UserRepository
from app.shared.database import db_session


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session = db_session):
        self.session = session

    def get_by_id(self, id: int) -> Optional[User]:
        return self.session.query(User).filter(User.id == id).first()

    def get_all(self) -> List[User]:
        return self.session.query(User).all()

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, user: User) -> User:
        self.session.merge(user)
        self.session.commit()
        return user

    def delete(self, id: int) -> bool:
        user = self.get_by_id(id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()
