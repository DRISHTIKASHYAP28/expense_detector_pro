"""
config.py
---------
Centralised configuration management using environment variables.

Follows the 12-Factor App principle: all environment-specific settings live
outside the codebase, loaded from a .env file via python-dotenv.

Three config classes cover the three standard environments:
  - DevelopmentConfig  → local dev with debug mode on
  - TestingConfig      → in-memory SQLite, no CSRF, fast bcrypt rounds
  - ProductionConfig   → strict settings, requires real secrets from env

The `config_by_name` dict lets the app factory select a config by string name,
which is useful for testing and deployment automation.
"""

import os
from dotenv import load_dotenv

# Load .env file from the project root into os.environ
load_dotenv()


class BaseConfig:
    """
    Settings shared across all environments.
    Never instantiate this directly — use a subclass.
    """
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-fallback-secret-change-in-prod")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False  # Suppresses FSADeprecationWarning
    BCRYPT_LOG_ROUNDS: int = 12                   # bcrypt work factor (cost)
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")

    # Database URL is fully configurable — swap SQLite for PostgreSQL with
    # no code changes, just update DATABASE_URL in the environment.
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL",
        "sqlite:///database/expense.db"
    )


class DevelopmentConfig(BaseConfig):
    """Local development environment."""
    DEBUG: bool = True
    BCRYPT_LOG_ROUNDS: int = 4  # Faster hashing in dev for quicker iteration
    LOG_LEVEL: str = "DEBUG"


class TestingConfig(BaseConfig):
    """Isolated test environment — uses an in-memory database."""
    TESTING: bool = True
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
    BCRYPT_LOG_ROUNDS: int = 4   # Minimum rounds keeps test suite fast
    WTF_CSRF_ENABLED: bool = False
    LOG_LEVEL: str = "WARNING"   # Suppress noise during test runs


class ProductionConfig(BaseConfig):
    """
    Production environment.
    SECRET_KEY and DATABASE_URL MUST be set as real environment variables.
    """
    DEBUG: bool = False
    TESTING: bool = False


# Maps string names to config classes — used by the app factory.
config_by_name: dict = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
