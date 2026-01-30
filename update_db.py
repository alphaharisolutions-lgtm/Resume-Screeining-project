from app import app
from db.models import db
from sqlalchemy import text

def update_schema():
    with app.app_context():
        try:
            db.session.execute(text('ALTER TABLE job_descriptions ADD COLUMN auto_shortlist_threshold FLOAT DEFAULT 80.0'))
            db.session.commit()
            print("Added auto_shortlist_threshold to job_descriptions")
        except Exception as e:
            print(f"Error adding column to job_descriptions: {e}")
            db.session.rollback()

        try:
            db.session.execute(text('ALTER TABLE screening_results ADD COLUMN interviewer_id INTEGER REFERENCES users(id)'))
            db.session.commit()
            print("Added interviewer_id to screening_results")
        except Exception as e:
            print(f"Error adding column to screening_results: {e}")
            db.session.rollback()

if __name__ == "__main__":
    update_schema()
