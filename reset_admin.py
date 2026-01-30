from app import app
from db.models import db, User
from werkzeug.security import generate_password_hash

def reset_password(email, new_password):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            print(f"[SUCCESS] Password for {email} has been reset to: {new_password}")
        else:
            print(f"[ERROR] User with email {email} not found.")

if __name__ == "__main__":
    reset_password("admin@example.com", "admin123")
