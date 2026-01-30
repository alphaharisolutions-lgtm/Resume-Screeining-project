import sys
from app import app
from db.models import db, User
from werkzeug.security import generate_password_hash

def create_user_terminal(name, email, password, role):
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        
        if not existing_user:
            hashed_pw = generate_password_hash(password)
            new_user = User(
                name=name,
                email=email,
                password=hashed_pw,
                role=role
            )
            db.session.add(new_user)
            try:
                db.session.commit()
                print(f"\n[SUCCESS] User '{name}' created successfully!")
                print(f"Email: {email}")
                print(f"Password: {password}")
                print(f"Role: {role}")
            except Exception as e:
                db.session.rollback()
                print(f"[ERROR] During creation: {e}")
        else:
            print(f"[WARNING] User with email {email} already exists.")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("\nUsage: python add_user.py <name> <email> <password> <role>")
        print("Example: python add_user.py \"John Doe\" john@example.com mypassword123 recruiter")
        print("\nAvailable Roles: admin, recruiter, student, interviewer")
    else:
        name = sys.argv[1]
        email = sys.argv[2]
        password = sys.argv[3]
        role = sys.argv[4]
        create_user_terminal(name, email, password, role)
