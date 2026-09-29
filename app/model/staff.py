from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.util.database import Base


class Staff(Base):

    __tablename__ = "staff"

    id = Column(String, primary_key=True, index=True)

    name = Column(String)
    role = Column(String)
    department = Column(String)
    phone = Column(String)

