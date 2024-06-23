from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import engine, database, get_db
from app.models import Base
from app.schemas import UserCreate, UserResponse, BoardCreate, BoardResponse, UserLogin
import app.crud as crud
from app.insert_initial_data import insert_initial_data

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()
    # insert_initial_data()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.post("/boards/", response_model=BoardResponse)
def create_board(board: BoardCreate, db: Session = Depends(get_db)):
    return crud.create_board(db, board)


@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    print(user_id)
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/boards/{board_id}", response_model=BoardResponse)
def read_board(board_id: int, db: Session = Depends(get_db)):
    board = crud.get_board(db, board_id)
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


@app.post("/users/login")
def login(dto: UserLogin, db: Session = Depends(get_db)):
    print(dto)
    user = crud.find_user_by_email_and_password(db, dto.email, dto.password)
    if user in [None, False]:
        raise HTTPException(status_code=404, detail="User not found")
    return user
