"""
models/__init__.py
------------------
Exposes all models from a single import point.

Usage inside the app:
    from models import User, Transaction
"""

from models.base import db
from models.user import User
from models.transaction import Transaction

__all__ = ["db", "User", "Transaction"]
