"""
routes/auth_routes.py
---------------------
Controller for authentication routes (login, register, logout).
"""

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from utils.exceptions import AuthenticationError, ValidationError
from utils.validators import validate_user_registration

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Renders register template or performs user signup."""
    if current_user.is_authenticated:
        return redirect(url_for("transaction.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        try:
            # Validate input arguments
            validate_user_registration(username, email, password)

            # Retrieve auth service from app context container
            auth_service = current_app.extensions["auth_service"]
            user = auth_service.register_user(username, email, password)

            # Keep user logged in immediately
            login_user(user)
            flash("Account registered successfully! Welcome.", "success")
            return redirect(url_for("transaction.dashboard"))

        except ValidationError as e:
            flash(str(e), "danger")
        except Exception as e:
            current_app.logger.error(f"Signup error: {str(e)}")
            flash("An unexpected error occurred during signup. Please try again.", "danger")

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Renders login template or processes user authentication."""
    if current_user.is_authenticated:
        return redirect(url_for("transaction.dashboard"))

    if request.method == "POST":
        email_or_username = request.form.get("email_or_username", "").strip()
        password = request.form.get("password", "")

        try:
            auth_service = current_app.extensions["auth_service"]
            user = auth_service.authenticate_user(email_or_username, password)

            login_user(user)
            flash("Login successful! Welcome back.", "success")
            return redirect(url_for("transaction.dashboard"))

        except (ValidationError, AuthenticationError) as e:
            flash(str(e), "danger")
        except Exception as e:
            current_app.logger.error(f"Login error: {str(e)}")
            flash("An error occurred. Please verify your credentials and try again.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """Closes user session and redirects."""
    logout_user()
    flash("You have logged out successfully.", "info")
    return redirect(url_for("auth.login"))
