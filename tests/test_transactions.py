"""
tests/test_transactions.py
--------------------------
Tests for transaction CRUD, filtering, auto-detection, and authorization rules.
"""

from decimal import Decimal
from models.transaction import Transaction
from models.user import User


def login_user(client):
    """Helper to register and login a test user."""
    client.post(
        "/register",
        data={
            "username": "txuser",
            "email": "tx@example.com",
            "password": "password123",
        },
    )


def test_create_transaction_with_auto_detection(client, app):
    """Verify transaction creation and live keyword category detection."""
    login_user(client)

    # Log expense with "Auto" category selection
    response = client.post(
        "/transactions",
        data={
            "description": "Lunch at McDonald's burger",
            "amount": "14.99",
            "category": "Auto",
            "date": "2026-06-12",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"logged successfully" in response.data.lower()

    with app.app_context():
        tx = Transaction.query.first()
        assert tx is not None
        assert tx.description == "Lunch at McDonald's burger"
        assert tx.amount == Decimal("14.99")
        # Should detect "mcdonald" / "burger" -> Food & Drinks
        assert tx.category == "Food & Drinks"


def test_transaction_api_detect_endpoint(client):
    """Verify the /api/transactions/detect endpoint predicts correctly."""
    login_user(client)

    # Test Uber -> Transport
    response = client.post(
        "/api/transactions/detect", json={"description": "Uber ride home"}
    )
    assert response.status_code == 200
    assert response.get_json() == {"category": "Transport"}

    # Test Netflix -> Entertainment
    response = client.post(
        "/api/transactions/detect",
        json={"description": "Netflix monthly subscription"},
    )
    assert response.status_code == 200
    assert response.get_json() == {"category": "Entertainment"}


def test_edit_transaction(client, app):
    """Verify user can update their transaction details."""
    login_user(client)

    # Create one transaction
    client.post(
        "/transactions",
        data={
            "description": "Gas station bill",
            "amount": "45.00",
            "category": "Transport",
        },
    )

    with app.app_context():
        tx = Transaction.query.first()
        tx_id = tx.id

    # Edit transaction
    response = client.post(
        f"/transactions/{tx_id}/edit",
        data={
            "description": "Gas station bill & snack",
            "amount": "52.50",
            "category": "Food & Drinks",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"updated successfully" in response.data.lower()

    with app.app_context():
        updated_tx = Transaction.query.get(tx_id)
        assert updated_tx.description == "Gas station bill & snack"
        assert updated_tx.amount == Decimal("52.50")
        assert updated_tx.category == "Food & Drinks"


def test_delete_transaction(client, app):
    """Verify user can delete their transaction."""
    login_user(client)

    # Create transaction
    client.post(
        "/transactions",
        data={
            "description": "Internet subscription",
            "amount": "80.00",
            "category": "Utilities",
        },
    )

    with app.app_context():
        tx_id = Transaction.query.first().id

    # Delete transaction
    response = client.post(
        f"/transactions/{tx_id}/delete", follow_redirects=True
    )
    assert response.status_code == 200
    assert b"deleted successfully" in response.data.lower()

    with app.app_context():
        assert Transaction.query.get(tx_id) is None


def test_transaction_owner_authorization(client, app):
    """Verify user cannot edit or delete someone else's transactions."""
    # Register and log in User 1
    client.post(
        "/register",
        data={
            "username": "userone",
            "email": "one@example.com",
            "password": "password123",
        },
    )

    # User 1 creates a transaction
    client.post(
        "/transactions",
        data={
            "description": "User one purchase",
            "amount": "10.00",
            "category": "Other",
        },
    )

    with app.app_context():
        user_one_tx_id = Transaction.query.first().id

    # Log out User 1
    client.get("/logout")

    # Register and log in User 2
    client.post(
        "/register",
        data={
            "username": "usertwo",
            "email": "two@example.com",
            "password": "password123",
        },
    )

    # User 2 attempts to edit User 1's transaction
    response = client.post(
        f"/transactions/{user_one_tx_id}/edit",
        data={
            "description": "Hijacked purchase",
            "amount": "999.00",
            "category": "Other",
        },
        follow_redirects=True,
    )
    # Redirects and alerts access denied (custom exception handler redirects with flash message)
    assert b"access to edit" in response.data.lower()

    # User 2 attempts to delete User 1's transaction
    response = client.post(
        f"/transactions/{user_one_tx_id}/delete", follow_redirects=True
    )
    assert b"access to delete" in response.data.lower()

    # Verify transaction in database remains untouched
    with app.app_context():
        original_tx = Transaction.query.get(user_one_tx_id)
        assert original_tx.description == "User one purchase"
        assert original_tx.amount == Decimal("10.00")
