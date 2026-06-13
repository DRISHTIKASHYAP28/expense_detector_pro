"""
routes/transaction_routes.py
----------------------------
Controller for transaction operations (CRUD dashboard views and REST APIs).
"""

from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from utils.exceptions import ForbiddenError, ResourceNotFoundError, ValidationError
from utils.validators import validate_transaction_data

transaction_bp = Blueprint("transaction", __name__)


@transaction_bp.route("/dashboard")
@login_required
def dashboard():
    """Renders the personal dashboard with metric cards and transaction tables."""
    tx_service = current_app.extensions["transaction_service"]

    # Read filtering parameters from query arguments
    category = request.args.get("category", "All")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")
    search_query = request.args.get("search_query", "")

    try:
        transactions = tx_service.get_user_transactions(
            user_id=current_user.id,
            category=category if category != "All" else None,
            start_date_str=start_date if start_date else None,
            end_date_str=end_date if end_date else None,
            search_query=search_query if search_query else None,
        )
        stats = tx_service.get_transaction_stats(current_user.id)
    except Exception as e:
        current_app.logger.error(f"Error generating dashboard values: {str(e)}")
        transactions = []
        stats = {
            "total_income": 0.0,
            "total_expense": 0.0,
            "balance": 0.0,
            "top_category": "None",
            "category_spending": {},
        }

    categories = [
        "Food & Drinks",
        "Transport",
        "Entertainment",
        "Utilities",
        "Shopping",
        "Health & Medical",
        "Salary / Income",
        "Other",
    ]

    return render_template(
        "dashboard.html",
        transactions=transactions,
        stats=stats,
        categories=categories,
        selected_category=category,
        start_date=start_date,
        end_date=end_date,
        search_query=search_query,
    )


@transaction_bp.route("/transactions", methods=["POST"])
@login_required
def create():
    """Handles adding a transaction."""
    tx_service = current_app.extensions["transaction_service"]

    description = request.form.get("description", "").strip()
    amount_str = request.form.get("amount", "")
    category = request.form.get("category", "")
    date_str = request.form.get("date", "")

    try:
        amount = validate_transaction_data(description, amount_str, category, date_str)
        tx_service.create_transaction(
            user_id=current_user.id,
            description=description,
            amount=amount,
            category=category,
            date_str=date_str if date_str else None,
        )
        flash("Transaction logged successfully!", "success")
    except ValidationError as e:
        flash(str(e), "danger")
    except Exception as e:
        current_app.logger.error(f"Error creating transaction: {str(e)}")
        flash("An unexpected error occurred while saving the transaction.", "danger")

    return redirect(url_for("transaction.dashboard"))


@transaction_bp.route("/transactions/<int:tx_id>/edit", methods=["POST"])
@login_required
def edit(tx_id):
    """Handles updating a transaction."""
    tx_service = current_app.extensions["transaction_service"]

    description = request.form.get("description", "").strip()
    amount_str = request.form.get("amount", "")
    category = request.form.get("category", "")
    date_str = request.form.get("date", "")

    try:
        amount = validate_transaction_data(description, amount_str, category, date_str)
        tx_service.update_transaction(
            user_id=current_user.id,
            tx_id=tx_id,
            description=description,
            amount=amount,
            category=category,
            date_str=date_str if date_str else None,
        )
        flash("Transaction updated successfully!", "success")
    except ValidationError as e:
        flash(str(e), "danger")
    except (ResourceNotFoundError, ForbiddenError) as e:
        flash(str(e), "danger")
    except Exception as e:
        current_app.logger.error(f"Error updating transaction: {str(e)}")
        flash("An unexpected error occurred while modifying the transaction.", "danger")

    return redirect(url_for("transaction.dashboard"))


@transaction_bp.route("/transactions/<int:tx_id>/delete", methods=["POST"])
@login_required
def delete(tx_id):
    """Handles deleting a transaction."""
    tx_service = current_app.extensions["transaction_service"]

    try:
        tx_service.delete_transaction(user_id=current_user.id, tx_id=tx_id)
        flash("Transaction deleted successfully.", "success")
    except (ResourceNotFoundError, ForbiddenError) as e:
        flash(str(e), "danger")
    except Exception as e:
        current_app.logger.error(f"Error deleting transaction: {str(e)}")
        flash("An unexpected error occurred while deleting the transaction.", "danger")

    return redirect(url_for("transaction.dashboard"))


# ─── REST API endpoints ───────────────────────────────────────────────────────


@transaction_bp.route("/api/transactions/detect", methods=["POST"])
@login_required
def detect_category():
    """
    POST API endpoint returning the auto-detected category of a description string.
    Expected JSON payload: {"description": "uber ride"}
    """
    tx_service = current_app.extensions["transaction_service"]
    data = request.get_json() or {}
    description = data.get("description", "")
    category = tx_service.detect_category(description)
    return jsonify({"category": category})
