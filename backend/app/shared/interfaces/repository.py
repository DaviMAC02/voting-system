from abc import ABC, abstractmethod
from typing import List, Optional


class Repository(ABC):
    """Base repository interface"""

    @abstractmethod
    def get_by_id(self, id: int):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def create(self, entity):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass
