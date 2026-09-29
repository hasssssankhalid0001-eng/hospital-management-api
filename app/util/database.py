# import json

# def load_data():
#     with open('patients.json','r') as f: 
#         data=json.load(f)

#     return data

# def save_data(data):
#     with open('patients.json', 'w') as f:
#         json.dump(data, f)   

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./patients.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()  

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()