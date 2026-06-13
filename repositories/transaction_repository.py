"""
repositories/transaction_repository.py
--------------------------------------
Repository for Transaction-specific database operations.
"""

from datetime import datetime
from typing import List, Optional
from models.transaction import Transaction
from repositories.base_repository import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):
    """
    Handles transaction-specific data access routines.
    """

    def __init__(self) -> None:
        super().__init__(Transaction)

    def get_by_user_id(
        self,
        user_id: int,
        category: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        search_query: Optional[str] = None,
    ) -> List[Transaction]:
        """
        Fetch all transactions for a specific user with optional filters.
        """
        query = Transaction.query.filter_by(user_id=user_id)

        if category and category != "All":
            query = query.filter(Transaction.category.ilike(category))

        if start_date:
            query = query.filter(Transaction.date >= start_date)

        if end_date:
            query = query.filter(Transaction.date <= end_date)

        if search_query:
            query = query.filter(
                Transaction.description.ilike(f"%{search_query}%")
            )

        # Show the most recent transactions first
        return query.order_by(Transaction.date.desc()).all()
