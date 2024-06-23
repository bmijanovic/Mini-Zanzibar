import os
import requests
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from app.database import engine, database, get_db
from app.models import Base
from app.schemas import *
import app.crud as crud
from app.models import Base
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.database import engine, database, get_db
from app.insert_initial_data import insert_initial_data
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, HTTPException, Depends, Response, Request
from app.schemas import UserCreate, UserResponse, BoardCreate, BoardResponse, UserLogin
from app.zanzibar_utils import *

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
def update_board(board_dto: BoardContentUpdate, request: Request, db: Session = Depends(get_db)):
    user_email = request.session.get("user_email")
    if user_email is None:
        raise HTTPException(status_code=404, detail="User not found")
    board = crud.get_board(db, board_dto.board_id)
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")

    check_acl_req = check_acl(f"board:{board.name}", "editor", user_email)
    if check_acl_req.status_code != 200:
        raise HTTPException(status_code=404, detail="ACL check failed")
    if not check_acl_req.json().get("authorized"):
        raise HTTPException(status_code=404, detail="Not authorized to edit")
    return crud.update_board_content(db, board_dto.board_id, board_dto.board_content)


@app.get("/boards", response_model=AllBoardsResponse)
def read_boards(request: Request, db: Session = Depends(get_db)):
    user_email = request.session.get("user_email")
    if user_email is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud.find_user_by_email(db, user_email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    relations = crud.get_all_relations(db, user.id)
    my_boards = []
    shared_boards = []
    for relation in relations:
        board = crud.get_board(db, relation.board_id)
        if relation.privilege == "owner":
            my_boards.append(
                BoardForUserResponse(id=board.id, name=board.name, owner_id=board.owner_id, owner_name=user.name,
                                     privilege=relation.privilege))
        else:
            owner = crud.get_user(db, board.owner_id)
            shared_boards.append(
                BoardForUserResponse(id=board.id, name=board.name, owner_id=board.owner_id, owner_name=owner.name,
                                     privilege=relation.privilege))
    return AllBoardsResponse(my_boards=my_boards, shared_boards=shared_boards)


@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    print(user_id)
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/boards/{board_id}", response_model=SingleBoardResponse)
def read_board(board_id: int, request: Request, db: Session = Depends(get_db)):
    user_email = request.session.get("user_email")
    if user_email is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = crud.find_user_by_email(db, user_email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    board = crud.get_board(db, board_id)
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    privilege = 'editor'
    check_acl_req = check_acl(f"board:{board.name}", "editor", user_email)
    if check_acl_req.status_code != 200:
        raise HTTPException(status_code=404, detail="ACL check failed")
    if not check_acl_req.json().get("authorized"):
        check_acl_req = check_acl(f"board:{board.name}", "viewer", user_email)
        if check_acl_req.status_code != 200:
            raise HTTPException(status_code=404, detail="ACL check failed")
        if not check_acl_req.json().get("authorized"):
            raise HTTPException(status_code=404, detail="ACL permission denied")
        privilege = 'viewer'
    board_response = SingleBoardResponse(id=board.id,
                                   name=board.name,
                                   owner_id=board.owner_id,
                                   content=board.content,
                                   privilege="viewer")
    return board_response


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


@app.post("/boards/share")
def share_board(request: Request, share_dto: ShareDTO, db: Session = Depends(get_db)):
    board_id = share_dto.board_id
    email = share_dto.email
    role = share_dto.role.lower()
    user_email = request.session.get("user_email")
    if user_email is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = crud.find_user_by_email(db, user_email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    board = crud.get_board(db, board_id)
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")

    check_acl_req = check_acl(f"board:{board.name}", "owner", user_email)
    if check_acl_req.status_code != 200:
        raise HTTPException(status_code=404, detail="ACL check failed")

    if not check_acl_req.json().get("authorized"):
        raise HTTPException(status_code=404, detail="Not authorized to share")

    shared_user = crud.find_user_by_email(db, email)
    if shared_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    response = create_acl(f"board:{board.name}", role, email)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="ACL not created")
    if crud.get_permissions(db, shared_user.id, board.id) is not None:
        crud.delete_permissions(db, shared_user.id, board.id)
    crud.create_permissions(db, shared_user.id, board.id, role)
    return {"message": "Board shared"}


@app.post("/boards/unshare")
def unshare_board(request: Request, board_id: int, email: str, db: Session = Depends(get_db)):
    user_email = request.session.get("user_email")
    if user_email is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = crud.find_user_by_email(db, user_email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    board = crud.get_board(db, board_id)
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")

    check_acl_req = check_acl(f"board:{board.name}", "owner", user_email)
    if check_acl_req.status_code != 200:
        raise HTTPException(status_code=404, detail="ACL check failed")

    if not check_acl_req.json().get("authorized"):
        raise HTTPException(status_code=404, detail="Not authorized to unshare")

    shared_user = crud.find_user_by_email(db, email)
    if shared_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    response = delete_acl(f"board:{board.name}", email)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="ACL not deleted")
    crud.delete_permissions(db, shared_user.id, board.id)
    return {"message": "Board unshared"}


@app.post("/boards/create", response_model=BoardResponse)
def create_board(board: BoardCreate, request: Request, db: Session = Depends(get_db)):
    user_email = request.session.get("user_email")
    print("User email:", user_email)
    if user_email is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud.find_user_by_email(db, user_email)
    board = crud.create_board(db, board, user.id)
    print("Board:", board)
    response = create_acl(f"board:{board.name}", "owner", user_email)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="ACL not created")
    crud.create_permissions(db, user.id, board.id, "owner")
    return board
