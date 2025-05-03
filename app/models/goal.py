from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Goal(db.Model):
    __tablename__ = 'goals'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    tasks = db.relationship('Task', back_populates='goal', lazy=True)


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }

    @classmethod
    def from_dict(cls, data):
        title = data.get("title")
        if title is None:
            raise ValueError("Invalid data")
        return cls(title=title)
