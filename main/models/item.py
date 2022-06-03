from datetime import datetime

from main import db


class ItemModel(db.Model):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(1000))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    author = db.relationship("UserModel", uselist=False)

    def __repr__(self):
        return f"<ItemModel(\
                    id={self.id}, \
                    name={self.name}, \
                    category={repr(self.category)})>"
