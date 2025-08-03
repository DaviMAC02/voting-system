from typing import List, Optional
from app.modules.users.models import User
from app.modules.users.interfaces.user_repository import UserRepository
from app.shared.database import db


class SQLAlchemyUserRepository(UserRepository):
    def get_by_id(self, id: int) -> Optional[User]:
        return User.query.filter(User.id == id).first()

    def get_all(self) -> List[User]:
        return User.query.all()

    def create(self, user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user: User) -> User:
        db.session.merge(user)
        db.session.commit()
        return user

    def delete(self, id: int) -> bool:
        user = self.get_by_id(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    def get_by_email(self, email: str) -> Optional[User]:
        return User.query.filter(User.email == email).first()
