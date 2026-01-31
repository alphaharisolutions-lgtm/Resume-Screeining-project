from app import app
from db.models import db, User

with app.app_context():
    users = User.query.all()
    print("-" * 50)
    print(f"{'Name':<20} | {'Email':<30} | {'Role':<15}")
    print("-" * 50)
    for user in users:
        print(f"{user.name:<20} | {user.email:<30} | {user.role:<15}")
    print("-" * 50)
