"""
models/base.py
--------------
Shared SQLAlchemy declarative base and metadata.

All ORM models import `Base` from here. Centralising the Base means:
  - A single metadata object tracks all tables across the app.
  - `db.create_all()` only needs one import to find every model.
  - Migrating to Alembic (for PostgreSQL) is straightforward because
    Alembic targets the same `Base.metadata`.

`TimestampMixin` is a reusable mixin that injects `created_at` and
`updated_at` columns into any model that needs them — keeps models DRY.
"""

from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

# Single shared SQLAlchemy instance — imported and initialised by app.py
db = SQLAlchemy()


class TimestampMixin:
    """
    Mixin that adds `created_at` and `updated_at` columns to a model.

    Inherit from this alongside `db.Model` to automatically track when
    records are created and last modified. Timezone-aware UTC timestamps
    are used so there is no ambiguity across regions.
    """
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
