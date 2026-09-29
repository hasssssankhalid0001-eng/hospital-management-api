from app.model.user import User
from app.util.database import SessionLocal

db = SessionLocal()

username = input("Enter the main admin username: ")

user = db.query(User).filter(
    User.username == username
).first()

if not user:
    print("User not found.")
elif user.role != "admin":
    print("User is not an admin.")
else:
    user.is_primary_admin = True
    db.commit()
    print("Main admin set successfully.")

db.close()