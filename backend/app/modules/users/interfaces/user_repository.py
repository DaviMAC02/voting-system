from abc import ABC, abstractmethod
from typing import List, Optional
from app.modules.users.models import User
from app.shared.interfaces.repository import Repository


class UserRepository(Repository):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass
