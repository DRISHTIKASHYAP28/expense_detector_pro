"""
app.py
------
Application Factory for the Flask Expense Tracker.

Configures database, authentications, blueprints, logging, and unified
global exception handlers.
"""

import logging
import os
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from config import config_by_name
from logging_config import setup_logging
from models.base import db
from repositories.transaction_repository import TransactionRepository
from repositories.user_repository import UserRepository
from routes.auth_routes import auth_bp
from routes.transaction_routes import transaction_bp
from services.auth_service import AuthService
from services.transaction_service import TransactionService
from utils.exceptions import AppException


def create_app(config_name: str = None) -> Flask:
    """
    Creates and configures a Flask application instance.
    """
    if not config_name:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Configure logging
    setup_logging(app.config["LOG_LEVEL"])
    logger = logging.getLogger(__name__)
    logger.info(f"Initializing app factory in '{config_name}' environment.")

    # Initialize database
    db.init_app(app)

    # Initialize bcrypt
    bcrypt = Bcrypt(app)

    # Initialize Flask-Login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    # Dependency Injection Setup
    user_repo = UserRepository()
    tx_repo = TransactionRepository()
    auth_service = AuthService(user_repo, bcrypt)
    tx_service = TransactionService(tx_repo)

    # Register in extensions dict for clean access from Blueprints
    app.extensions["user_repository"] = user_repo
    app.extensions["transaction_repository"] = tx_repo
    app.extensions["auth_service"] = auth_service
    app.extensions["transaction_service"] = tx_service

    @login_manager.user_loader
    def load_user(user_id):
        """Callback to load User object by ID."""
        return user_repo.get_by_id(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(transaction_bp)

    @app.route("/")
    def index():
        """Root route redirecting user based on auth state."""
        if current_user.is_authenticated:
            return redirect(url_for("transaction.dashboard"))
        return redirect(url_for("auth.login"))

    # Global Exception Handling
    @app.errorhandler(AppException)
    def handle_app_exception(error):
        """Catches custom AppExceptions and returns styled JSON/HTML."""
        logger.warning(
            f"AppException raised: '{error.message}' (HTTP {error.status_code})"
        )
        if (
            request.path.startswith("/api/")
            or request.headers.get("Accept") == "application/json"
        ):
            return jsonify(error.to_dict()), error.status_code

        # For browser sessions, show flash and redirect
        flash(error.message, "danger")
        return redirect(url_for("transaction.dashboard"))

    @app.errorhandler(404)
    def page_not_found(error):
        """Catches 404 errors."""
        if (
            request.path.startswith("/api/")
            or request.headers.get("Accept") == "application/json"
        ):
            return jsonify({"error": "Resource not found"}), 404
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """Catches 500 errors."""
        logger.error(f"Internal Server Error: {str(error)}")
        if (
            request.path.startswith("/api/")
            or request.headers.get("Accept") == "application/json"
        ):
            return jsonify({"error": "An internal server error occurred"}), 500
        return render_template("errors/500.html"), 500

    # Automatically create tables (SQLite helper)
    with app.app_context():
        db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
        if db_uri.startswith("sqlite:///"):
            # Ensure folder containing SQLite database exists
            db_path = db_uri.replace("sqlite:///", "")
            # Handle absolute paths vs relative paths
            if not os.path.isabs(db_path):
                db_path = os.path.join(app.instance_path, db_path)
            db_dir = os.path.dirname(db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)


        db.create_all()
        logger.info("Database schemas generated successfully.")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
