from datetime import datetime
from models.base import db


class LoginHistory(db.Model):
    __tablename__ = "login_history"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    login_time = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    ip_address = db.Column(
        db.String(50)
    )

    user_agent = db.Column(
        db.String(255)
    )