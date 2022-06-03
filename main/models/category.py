from datetime import datetime

from main import db


class CategoryModel(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    author = db.relationship("UserModel", uselist=False)
    items = db.relationship(
        "ItemModel", backref="category", cascade="all,delete", lazy="dynamic"
    )

    def __repr__(self):
        return f"<CategoryModel(id={self.id}, name={self.name})>"
