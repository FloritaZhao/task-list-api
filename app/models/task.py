from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from typing import Optional

class Task(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=False)
    completed_at: Mapped[datetime] =mapped_column(nullable=True)
    goal_id: Mapped[int] = mapped_column(db.ForeignKey("goal.id"))
    goal: Mapped[Optional[list["Goal"]]] = relationship(back_populates="task")


    def to_dict(self):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
    
        if self.goal_id is not None:
            task_dict["goal_id"] = self.goal_id
        return task_dict


    @classmethod
    def from_dict(cls, data):
        title = data.get("title")
        description = data.get("description")
        if title is None or description is None:
            raise ValueError("Invalid data")
        return cls(title=title, description=description)
