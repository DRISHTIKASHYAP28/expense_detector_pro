"""
models/user.py
--------------
User ORM model and Flask-Login integration.

Design decisions:
  - `UserMixin` from Flask-Login provides default implementations of
    is_authenticated, is_active, is_anonymous, and get_id() so the login
    manager works out of the box.
  - Password is stored as a bcrypt hash — the raw password is NEVER persisted.
  - `__repr__` is defined for clean debugging output in logs/shell.
  - Columns are indexed where they are used in WHERE clauses (email, username)
    to ensure O(log n) lookups as the user table grows.
"""

from flask_login import UserMixin

from models.base import TimestampMixin, db


class User(UserMixin, TimestampMixin, db.Model):
    """
    Represents a registered application user.

    Relationships:
        transactions: One-to-many → a user owns many transactions.
                      `lazy='dynamic'` returns a query object instead of
                      loading all rows at once — essential for large datasets.
                      `cascade='all, delete-orphan'` ensures transactions are
                      deleted when the user account is removed.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(128), nullable=False)  # bcrypt hash

    # One-to-many: User → Transactions
    transactions = db.relationship(
        "Transaction",
        backref="owner",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"
