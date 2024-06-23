import os
import requests
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from app.database import engine, database, get_db
from app.models import Base
from app.schemas import UserCreate, UserResponse, BoardCreate, BoardResponse, UserLogin, BoardContentUpdate
import app.crud as crud
from app.models import Base
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.database import engine, database, get_db
from app.insert_initial_data import insert_initial_data
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, HTTPException, Depends, Response, Request
from app.schemas import UserCreate, UserResponse, BoardCreate, BoardResponse, UserLogin




load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
MINI_ZANZIBAR_URL = os.getenv("MINI_ZANZIBAR_URL")
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    SessionMiddleware, secret_key=SECRET_KEY
)
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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




@app.put("/boards", response_model=BoardResponse)
def update_board(board_dto:BoardContentUpdate, db: Session = Depends(get_db)):
    return crud.update_board_content(db, board_dto.board_id,board_dto.board_content)

@app.get("/boards/{board_id}", response_model=BoardResponse)
def read_board(board_id: int, db: Session = Depends(get_db)):
    board = crud.get_board(db, board_id)
    return board


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
def login(dto: UserLogin, request: Request, db: Session = Depends(get_db)):
    user = crud.find_user_by_email_and_password(db, dto.email, dto.password)
    if user in [None, False]:
        raise HTTPException(status_code=404, detail="User not found")
    request.session["user_email"] = user.email
    return user

@app.post("/users/logout")
def logout(request: Request):
    request.session.pop("user_email", None)
    return {"message": "Logged out"}


@app.get("/whoami")
def whoami(request: Request):
    email = request.session.get("user_email")
    if email is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"email": email}


@app.post("/boards/create", response_model=BoardResponse)
def create_board(board: BoardCreate, request: Request, db: Session = Depends(get_db)):
    user_email = request.session.get("user_email")
    if user_email is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud.find_user_by_email(db, user_email)
    board = crud.create_board(db, board, user.id)
    print("Board:", board)
    response = requests.post(MINI_ZANZIBAR_URL + "/acl", json={
        "object": f"board:{board.name}",
        "relation": "owner",
        "user": user_email
    })
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="ACL not created")
    return board