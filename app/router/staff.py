from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.util.database import get_db
from app.model.staff import Staff
from app.schema.staff import StaffCreate, StaffUpdate
from app.util.auth import require_admin

router = APIRouter(

    prefix="/staff",

    tags=["Staff"],

    dependencies=[Depends(require_admin)]

)


@router.post("/staff")
def create_staff(
    staff: StaffCreate,
    db: Session = Depends(get_db)
):
    new_staff = Staff(
        id=staff.id,
        name=staff.name,
        role=staff.role,
        department=staff.department,
        phone=staff.phone
    )

    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)

    return new_staff


@router.get("/staff")
def get_all_staff(
    db: Session = Depends(get_db)
):
    staff = db.query(Staff).all()

    return staff


@router.get("/staff/{staff_id}")
def get_staff(
    staff_id: str,
    db: Session = Depends(get_db)
):
    staff = db.query(Staff).filter(
        Staff.id == staff_id
    ).first()

    if not staff:
        raise HTTPException(
            status_code=404,
            detail="Staff not found"
        )

    return staff


@router.put("/staff/{staff_id}")
def update_staff(
    staff_id: str,
    staff_update: StaffUpdate,
    db: Session = Depends(get_db)
):
    staff = db.query(Staff).filter(
        Staff.id == staff_id
    ).first()

    if not staff:
        raise HTTPException(
            status_code=404,
            detail="Staff not found"
        )

    updated_data = staff_update.model_dump(
        exclude_unset=True
    )

    for key, value in updated_data.items():
        setattr(staff, key, value)

    db.commit()
    db.refresh(staff)

    return staff


@router.delete("/staff/{staff_id}")
def delete_staff(
    staff_id: str,
    db: Session = Depends(get_db)
):
    staff = db.query(Staff).filter(
        Staff.id == staff_id
    ).first()

    if not staff:
        raise HTTPException(
            status_code=404,
            detail="Staff not found"
        )

    db.delete(staff)
    db.commit()

    return {
        "message": "Staff deleted successfully"
    }