from datetime import datetime

from sqlalchemy_utils import EmailType

from main import db


class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(EmailType, unique=True, index=True, nullable=False)
    hashed_password = db.Column(db.String(72), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UserModel(id={self.id}, name={self.name}, email={self.email})>"
