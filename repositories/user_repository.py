"""
repositories/user_repository.py
-------------------------------
Repository for User-specific database operations.
"""

from typing import Optional
from models.user import User
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Handles user-specific data access routines.
    """

    def __init__(self) -> None:
        super().__init__(User)

    def get_by_email(self, email: str) -> Optional[User]:
        """Find a user by email address (case-insensitive)."""
        return User.query.filter(User.email.ilike(email)).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Find a user by username (case-insensitive)."""
        return User.query.filter(User.username.ilike(username)).first()
