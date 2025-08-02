from typing import Optional
import bcrypt
from app.modules.users.interfaces.user_repository import UserRepository
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data: UserCreate) -> User:
        # Check if user exists
        if self.user_repository.get_by_email(user_data.email):
            raise ValueError("User with this email already exists")

        # Hash password
        hashed_password = bcrypt.hashpw(
            user_data.password.encode("utf-8"), bcrypt.gensalt()
        )

        # Create user
        user = User(
            email=user_data.email,
            name=user_data.name,
            password=hashed_password.decode("utf-8"),
        )

        return self.user_repository.create(user)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.user_repository.get_by_email(email)
        if not user:
            return None

        if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return user

        return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.user_repository.get_by_id(user_id)
