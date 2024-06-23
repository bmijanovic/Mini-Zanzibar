from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models import User, Board
from app.schemas import UserCreate, BoardCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        name=user.name,
        surname=user.surname,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_board(db: Session, board: BoardCreate, user_id: int):
    db_board = Board(
        name=board.name,
        owner_id=user_id,
        content=board.content
    )
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def find_user_by_email_and_password(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def get_board(db: Session, board_id: int):
    return db.query(Board).filter(Board.id == board_id).first()


def find_user_by_email(db, user_email):
    return db.query(User).filter(User.email == user_email).first()