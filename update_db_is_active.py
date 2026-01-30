from app import app
from db.models import db
from sqlalchemy import text

def update_schema():
    with app.app_context():
        try:
            db.session.execute(text('ALTER TABLE job_descriptions ADD COLUMN is_active BOOLEAN DEFAULT 1'))
            db.session.commit()
            print("Added is_active to job_descriptions")
        except Exception as e:
            print(f"Error adding column to job_descriptions: {e}")
            db.session.rollback()

if __name__ == "__main__":
    update_schema()
