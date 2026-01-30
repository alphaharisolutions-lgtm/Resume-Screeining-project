from app import app
from db.models import db, User, JobDescription, Resume, ScreeningResult

def cleanup():
    with app.app_context():
        print("Starting cleanup of orphaned data...")
        
        # 1. Delete JDs without recruiters
        orphaned_jds = JobDescription.query.filter(~JobDescription.recruiter_id.in_(db.session.query(User.id))).all()
        for jd in orphaned_jds:
            print(f"Deleting orphaned Job: {jd.title}")
            db.session.delete(jd)
            
        # 2. Delete Resumes without students
        orphaned_resumes = Resume.query.filter(~Resume.student_id.in_(db.session.query(User.id))).all()
        for res in orphaned_resumes:
            print(f"Deleting orphaned Resume: {res.filename}")
            db.session.delete(res)
            
        # 3. Delete Screenings without Resume or JD
        orphaned_screenings = ScreeningResult.query.filter(
            (~ScreeningResult.resume_id.in_(db.session.query(Resume.id))) |
            (~ScreeningResult.jd_id.in_(db.session.query(JobDescription.id)))
        ).all()
        for s in orphaned_screenings:
            print(f"Deleting orphaned Screening (Score: {s.score})")
            db.session.delete(s)
            
        db.session.commit()
        print("Cleanup complete!")

if __name__ == "__main__":
    cleanup()
