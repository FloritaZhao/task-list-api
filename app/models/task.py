from ..db import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'), nullable=True)
    goal = db.relationship('Goal', back_populates='tasks')


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
