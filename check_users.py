from app import app
from db.models import User

with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}, Role: {user.role}")
