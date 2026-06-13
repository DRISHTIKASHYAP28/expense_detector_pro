"""
repositories/base_repository.py
-------------------------------
Abstract-ish Base Repository defining common CRUD methods.

Provides a unified interface for DB operations, isolating business logic
from raw session management and query syntax.
"""

from typing import Generic, List, Optional, Type, TypeVar
from models.base import db

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Generic repository class containing common CRUD operations.
    """

    def __init__(self, model_class: Type[T]) -> None:
        self.model_class = model_class

    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Fetch a single entity by its primary key ID."""
        return db.session.get(self.model_class, entity_id)

    def get_all(self) -> List[T]:
        """Fetch all entities of this type."""
        return db.session.query(self.model_class).all()

    def add(self, entity: T) -> T:
        """Add a new entity and commit the transaction."""
        db.session.add(entity)
        db.session.commit()
        return entity

    def update(self, entity: T) -> T:
        """Commit current changes to the database."""
        db.session.commit()
        return entity

    def delete(self, entity: T) -> None:
        """Delete an entity and commit the transaction."""
        db.session.delete(entity)
        db.session.commit()
