from app import create_app, db
from app.models.task import Task
from dotenv import load_dotenv
load_dotenv()

app = create_app()


with app.app_context():
    db.session.query(Task).delete()
    db.session.commit()

    demo_tasks = [
        Task(title="buy milk", description="buy bread at the same time"),
        Task(title="write paper", description="finish today's class"),
    ]

    db.session.add_all(demo_tasks)
    db.session.commit()
    
    print("Seeded tasks:", [t.id for t in demo_tasks])
