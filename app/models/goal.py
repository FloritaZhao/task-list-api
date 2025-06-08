from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import List

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    tasks: Mapped[List["Task"]] = relationship(back_populates="goal")


    def to_dict(self, include_tasks = False):
        goal_dict = {
            "id": self.id,
            "title": self.title
        }
        if include_tasks:
            goal_dict["tasks"] = [task.to_dict() for task in self.tasks]
            
        return goal_dict

    @classmethod
    def from_dict(cls, data):
        title = data.get("title")
        if title is None:
            raise ValueError("Invalid data")
        return cls(title=title)
