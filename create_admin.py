from app import app
from db.models import db, User
from werkzeug.security import generate_password_hash

def create_admin():
    with app.app_context():
        # Check if admin already exists
        admin_email = "admin@example.com"
        existing_admin = User.query.filter_by(email=admin_email).first()
        
        if not existing_admin:
            hashed_pw = generate_password_hash("admin123")
            admin_user = User(
                name="System Administrator",
                email=admin_email,
                password=hashed_pw,
                role="admin"
            )
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin account created successfully!")
            print(f"Email: {admin_email}")
            print(f"Password: admin123")
        else:
            print("Admin account already exists.")

if __name__ == "__main__":
    create_admin()
