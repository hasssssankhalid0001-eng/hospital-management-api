from getpass import getpass
from uuid import uuid4

from app.model.user import User
from app.util.database import SessionLocal
from app.util.security import hash_password


username = input("Enter admin username: ")
password = getpass("Enter admin password: ")

db = SessionLocal()

existing_user = db.query(User).filter(
    User.username == username
).first()

if existing_user:
    print("Username already exists.")
else:
    admin = User(
    id=str(uuid4()),
    username=username,
    password_hash=hash_password(password),
    role="admin",
    is_primary_admin=False)

    db.add(admin)
    db.commit()

    print("Admin created successfully.")

db.close()