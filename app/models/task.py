from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from typing import Optional

class Task(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    completed_at: Mapped[Optional[datetime]] =mapped_column()
    
    goal_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")


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
        title = data["title"]
        description = data["description"]
        return cls(title=title, description=description)
