import json

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas import UserCreate, BoardCreate
import app.crud as crud


def insert_initial_data():
    db: Session = SessionLocal()
    try:
        # Create users
        user1 = UserCreate(name="John", surname="Doe", email="john@example.com", password="password123")
        user2 = UserCreate(name="Jane", surname="Smith", email="jane@example.com", password="password123")

        crud.create_user(db, user1)
        crud.create_user(db, user2)

    finally:
        db.close()
