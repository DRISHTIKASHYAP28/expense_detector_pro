"""
services/transaction_service.py
--------------------------------
Business service managing transaction CRUD operations and auto-category mapping.
"""

from datetime import datetime, timezone
from decimal import Decimal
import logging
from typing import Dict, List, Optional
from models.transaction import Transaction
from repositories.transaction_repository import TransactionRepository
from utils.exceptions import ForbiddenError, ResourceNotFoundError

logger = logging.getLogger(__name__)


class TransactionService:
    """
    Manages transaction lifecycle and applies category auto-detection logic.
    """

    def __init__(self, transaction_repository: TransactionRepository) -> None:
        self.tx_repo = transaction_repository

    def detect_category(self, description: str) -> str:
        """
        Detects transaction category based on common text keywords.
        """
        desc_lower = description.lower()
        rules = {
            "Food & Drinks": [
                "starbucks",
                "mcdonald",
                "burger",
                "pizza",
                "cafe",
                "grocery",
                "supermarket",
                "din",
                "lunch",
                "breakfast",
                "restaurant",
                "kfc",
                "subway",
                "food",
                "eat",
            ],
            "Transport": [
                "uber",
                "taxi",
                "grab",
                "bus",
                "train",
                "metro",
                "flight",
                "airline",
                "fuel",
                "gas",
                "petrol",
                "commute",
                "ride",
                "lyft",
                "bolt",
            ],
            "Entertainment": [
                "netflix",
                "spotify",
                "movie",
                "cinema",
                "ticket",
                "concert",
                "game",
                "play",
                "theater",
                "show",
                "club",
                "bar",
                "pub",
                "steam",
                "disney",
                "hulu",
            ],
            "Utilities": [
                "bill",
                "electric",
                "water",
                "internet",
                "wifi",
                "phone",
                "mobile",
                "rent",
                "power",
                "trash",
                "telecom",
            ],
            "Shopping": [
                "amazon",
                "ebay",
                "shop",
                "clothes",
                "shoes",
                "electronics",
                "target",
                "walmart",
                "mall",
                "purchase",
                "nike",
                "adidas",
                "zara",
            ],
            "Health & Medical": [
                "hospital",
                "pharmacy",
                "drug",
                "doctor",
                "medicine",
                "clinic",
                "dentist",
                "gym",
                "fitness",
                "pharm",
                "medical",
            ],
            "Salary / Income": [
                "salary",
                "payroll",
                "payout",
                "refund",
                "dividend",
                "bonus",
                "wage",
                "deposit",
                "interest",
            ],
        }

        for category, keywords in rules.items():
            for kw in keywords:
                if kw in desc_lower:
                    return category

        return "Other"

    def get_user_transactions(
        self,
        user_id: int,
        category: Optional[str] = None,
        start_date_str: Optional[str] = None,
        end_date_str: Optional[str] = None,
        search_query: Optional[str] = None,
    ) -> List[Transaction]:
        """
        Retrieves user transactions with optional filters applied.
        """
        start_date = None
        end_date = None

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            except ValueError:
                pass

        if end_date_str:
            try:
                # Add end of day components so filtering includes transactions on that date
                end_date = datetime.strptime(
                    f"{end_date_str} 23:59:59", "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                pass

        return self.tx_repo.get_by_user_id(
            user_id=user_id,
            category=category,
            start_date=start_date,
            end_date=end_date,
            search_query=search_query,
        )

    def create_transaction(
        self,
        user_id: int,
        description: str,
        amount: float,
        category: str,
        date_str: Optional[str] = None,
    ) -> Transaction:
        """
        Creates a transaction. Auto-detects category if set to 'Auto'.
        """
        if not category or category.strip().lower() == "auto":
            category = self.detect_category(description)

        date_val = datetime.now(timezone.utc)
        if date_str:
            try:
                if "T" in date_str:
                    date_val = datetime.fromisoformat(date_str)
                else:
                    date_val = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                pass

        tx = Transaction(
            user_id=user_id,
            description=description.strip(),
            amount=Decimal(str(amount)),
            category=category,
            date=date_val,
        )

        self.tx_repo.add(tx)
        logger.info(
            f"Created transaction: {tx.description} ({tx.category}) for User: {user_id}"
        )
        return tx

    def update_transaction(
        self,
        user_id: int,
        tx_id: int,
        description: str,
        amount: float,
        category: str,
        date_str: Optional[str] = None,
    ) -> Transaction:
        """
        Updates transaction properties after validation.
        """
        tx = self.tx_repo.get_by_id(tx_id)
        if not tx:
            raise ResourceNotFoundError("Transaction not found.")

        if tx.user_id != user_id:
            raise ForbiddenError(
                "You do not have access to edit this transaction."
            )

        if not category or category.strip().lower() == "auto":
            category = self.detect_category(description)

        if date_str:
            try:
                if "T" in date_str:
                    tx.date = datetime.fromisoformat(date_str)
                else:
                    tx.date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                pass

        tx.description = description.strip()
        tx.amount = Decimal(str(amount))
        tx.category = category

        self.tx_repo.update(tx)
        logger.info(f"Updated transaction: {tx_id} for User: {user_id}")
        return tx

    def delete_transaction(self, user_id: int, tx_id: int) -> None:
        """
        Deletes transaction if owned by the user.
        """
        tx = self.tx_repo.get_by_id(tx_id)
        if not tx:
            raise ResourceNotFoundError("Transaction not found.")

        if tx.user_id != user_id:
            raise ForbiddenError(
                "You do not have access to delete this transaction."
            )

        self.tx_repo.delete(tx)
        logger.info(f"Deleted transaction: {tx_id} for User: {user_id}")

    def get_transaction_stats(self, user_id: int) -> Dict:
        """
        Computes transaction summaries (total income, total expense, balance, and breakdown).
        """
        txs = self.tx_repo.get_by_user_id(user_id)
        total_income = Decimal("0.00")
        total_expense = Decimal("0.00")
        category_spending: Dict[str, Decimal] = {}

        for tx in txs:
            if tx.category == "Salary / Income":
                total_income += tx.amount
            else:
                total_expense += tx.amount
                category_spending[tx.category] = (
                    category_spending.get(tx.category, Decimal("0.00"))
                    + tx.amount
                )

        balance = total_income - total_expense

        # Format breakdown
        formatted_spending = {
            k: float(v)
            for k, v in sorted(
                category_spending.items(), key=lambda item: item[1], reverse=True
            )
        }
        top_category = list(formatted_spending.keys())[0] if formatted_spending else "None"

        return {
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "balance": float(balance),
            "top_category": top_category,
            "category_spending": formatted_spending,
        }
