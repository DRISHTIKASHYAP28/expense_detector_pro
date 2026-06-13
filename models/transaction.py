"""
models/transaction.py
-----------------------
Transaction ORM model for user expense and income records.

Design decisions:
  - Uses `db.Numeric(10, 2)` for amounts to avoid floating point issues.
  - Links to `User` table via foreign key with cascade deletion.
  - Inherits from `TimestampMixin` for automatic created_at and updated_at tracking.
  - Indexes are placed on user_id, category, and date columns for fast filtering and pagination.
"""

from datetime import datetime, timezone
from models.base import TimestampMixin, db


class Transaction(TimestampMixin, db.Model):
    """
    Represents an individual financial transaction (expense/income).
    """

    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(
        db.String(50),
        nullable=False,
        default="Other",
        index=True,
    )
    date = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    def __repr__(self) -> str:
        return f"<Transaction id={self.id} description={self.description!r} amount={self.amount} category={self.category!r}>"
