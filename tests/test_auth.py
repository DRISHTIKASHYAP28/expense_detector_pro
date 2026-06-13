"""
tests/test_auth.py
------------------
Tests for authentication flows (registration, login, logout).
"""

from models.user import User


def test_register_user_success(client, app):
    """Verify that a user can register successfully with valid details."""
    response = client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"registered successfully" in response.data.lower()

    with app.app_context():
        user = User.query.filter_by(username="testuser").first()
        assert user is not None
        assert user.email == "test@example.com"


def test_register_duplicate_validations(client):
    """Verify registration fails when username or email is already in use."""
    # First registration
    client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123",
        },
    )

    # Log out user session
    client.get("/logout")

    # Duplicate email registration
    response = client.post(
        "/register",
        data={
            "username": "newuser",
            "email": "test@example.com",
            "password": "securepassword123",
        },
        follow_redirects=True,
    )
    assert b"email already exists" in response.data.lower()

    # Log out user session (in case it succeeded/sends cookies)
    client.get("/logout")

    # Duplicate username registration
    response = client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "newemail@example.com",
            "password": "securepassword123",
        },
        follow_redirects=True,
    )
    assert b"username is already taken" in response.data.lower()



def test_register_validation_failures(client):
    """Verify registration validation constraints (length, format)."""
    # Short username
    response = client.post(
        "/register",
        data={
            "username": "ab",
            "email": "valid@email.com",
            "password": "password",
        },
        follow_redirects=True,
    )
    assert b"username must be at least" in response.data.lower()

    # Short password
    response = client.post(
        "/register",
        data={
            "username": "validuser",
            "email": "valid@email.com",
            "password": "123",
        },
        follow_redirects=True,
    )
    assert b"password must be at least" in response.data.lower()

    # Invalid email format
    response = client.post(
        "/register",
        data={
            "username": "validuser",
            "email": "not-an-email",
            "password": "password",
        },
        follow_redirects=True,
    )
    assert b"invalid email format" in response.data.lower()


def test_login_logout_flow(client):
    """Verify that a user can login and logout successfully."""
    # Register first
    client.post(
        "/register",
        data={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "password123",
        },
    )

    # Log out session from registration
    client.get("/logout")

    # Attempt login with correct password
    response = client.post(
        "/login",
        data={"email_or_username": "loginuser", "password": "password123"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"login successful" in response.data.lower()

    # Attempt log out
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"logged out successfully" in response.data.lower()
