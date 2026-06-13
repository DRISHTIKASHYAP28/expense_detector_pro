"""
services/auth_service.py
-------------------------
Business service orchestrating authentication operations.
"""

import logging
from flask_bcrypt import Bcrypt
from models.user import User
from repositories.user_repository import UserRepository
from utils.exceptions import AuthenticationError, ValidationError

logger = logging.getLogger(__name__)


class AuthService:
    """
    Orchestrates user registration and login workflows.
    Decoupled from HTTP controllers.
    """

    def __init__(self, user_repository: UserRepository, bcrypt: Bcrypt) -> None:
        self.user_repo = user_repository
        self.bcrypt = bcrypt

    def register_user(self, username: str, email: str, password: str) -> User:
        """
        Registers a new user, hashes their password, and saves them.
        """
        username = username.strip()
        email = email.strip().lower()

        # Check for duplicates
        if self.user_repo.get_by_email(email):
            raise ValidationError("A user with this email already exists.")

        if self.user_repo.get_by_username(username):
            raise ValidationError("Username is already taken.")

        # Hash password and store
        hashed_password = self.bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )
        user = User(username=username, email=email, password=hashed_password)
        self.user_repo.add(user)

        logger.info(f"Successfully registered user: {username} ({email})")
        return user

    def authenticate_user(self, email_or_username: str, password: str) -> User:
        """
        Authenticates credentials.
        Returns the User object if valid, raises AuthenticationError otherwise.
        """
        credential = email_or_username.strip()
        user = self.user_repo.get_by_email(credential)

        if not user:
            user = self.user_repo.get_by_username(credential)

        if not user or not self.bcrypt.check_password_hash(
            user.password, password
        ):
            logger.warning(
                f"Failed login attempt for credential: {email_or_username}"
            )
            raise AuthenticationError("Invalid username, email, or password.")

        logger.info(f"User authenticated: {user.username}")
        return user
