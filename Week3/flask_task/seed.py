from app import create_app
from app.models import db, Task

app = create_app()

with app.app_context():
    if Task.query.count() == 0:
        sample = [
            Task(title="Learn Flask", description="JWT, Swagger, SQLAlchemy", status="pending"),
            Task(title="Connect React App", description="Use fetch or axios", status="completed"),
            Task(title="Test Swagger Docs", status="pending")
        ]
        db.session.bulk_save_objects(sample)
        db.session.commit()
        print("✅ Database seeded with sample tasks")
    else:
        print("ℹ️ Tasks already exist, skipping seed")
