from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.util.database import get_db
from app.util.security import verify_password, create_access_token
from app.model.user import User
from app.schema.user import UserLogin

from uuid import uuid4

from app.util.auth import require_main_admin
from app.util.security import hash_password
from app.schema.user import UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token({
        "sub": db_user.username,
        "role": db_user.role
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/admin")
def create_admin(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_main_admin)
):
    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_admin = User(
        id=str(uuid4()),
        username=user.username,
        password_hash=hash_password(user.password),
        role="admin",
        is_primary_admin=False
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {
        "message": "Admin created successfully",
        "username": new_admin.username
    }

@router.delete("/admin/{admin_id}")
def delete_admin(
    admin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_main_admin)
):
    admin = db.query(User).filter(
        User.id == admin_id
    ).first()

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    if admin.is_primary_admin:
        raise HTTPException(
            status_code=403,
            detail="Main admin cannot be deleted"
        )

    if admin.id == current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete yourself"
        )

    db.delete(admin)
    db.commit()

    return {
        "message": "Admin deleted successfully"
    }

@router.get("/admins")
def get_admins(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_main_admin)
):
    admins = db.query(User).all()

    return [
        {
            "id": admin.id,
            "username": admin.username,
            "role": admin.role,
            "is_primary_admin": admin.is_primary_admin
        }
        for admin in admins
    ]