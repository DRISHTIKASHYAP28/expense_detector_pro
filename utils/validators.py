"""
utils/validators.py
-------------------
Helper functions for request validation.
"""

from datetime import datetime
from email_validator import EmailNotValidError, validate_email
from utils.exceptions import ValidationError


def validate_user_registration(username: str, email: str, password: str) -> None:
    """
    Validate signup parameters.
    Raises ValidationError if any check fails.
    """
    if not username or len(username.strip()) < 3:
        raise ValidationError("Username must be at least 3 characters.")

    if not password or len(password) < 6:
        raise ValidationError("Password must be at least 6 characters.")

    if not email:
        raise ValidationError("Email is required.")

    try:
        validate_email(email.strip(), check_deliverability=False)
    except EmailNotValidError as e:
        raise ValidationError(f"Invalid email format: {str(e)}")



def validate_transaction_data(
    description: str, amount_str: str, category: str, date_str: str = None
) -> float:
    """
    Validate transaction parameters.
    Returns float representation of amount if successful.
    Raises ValidationError if validation fails.
    """
    if not description or len(description.strip()) < 2:
        raise ValidationError("Description must be at least 2 characters.")

    if not category or len(category.strip()) < 1:
        raise ValidationError("Category is required.")

    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        raise ValidationError("Amount must be a numeric value.")

    if amount <= 0:
        raise ValidationError("Amount must be greater than 0.")

    if date_str:
        try:
            # Check ISO format or YYYY-MM-DD
            if "T" in date_str:
                datetime.fromisoformat(date_str)
            else:
                datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValidationError(
                "Invalid date format. Use YYYY-MM-DD or ISO format."
            )

    return amount
