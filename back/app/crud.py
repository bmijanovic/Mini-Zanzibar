import json

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models import User, Board, Relation
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
    content = '{"document": {"store": {"document:document": {"gridSize": 10, "name": "", "meta": {}, "id": "document:document", "typeName": "document"}, "page:page": {"meta": {}, "id": "page:page", "name": "Page 1", "index": "a1", "typeName": "page"}}, "schema": {"schemaVersion": 2, "sequences": {"com.tldraw.store": 4, "com.tldraw.asset": 1, "com.tldraw.camera": 1, "com.tldraw.document": 2, "com.tldraw.instance": 25, "com.tldraw.instance_page_state": 5, "com.tldraw.page": 1, "com.tldraw.instance_presence": 5, "com.tldraw.pointer": 1, "com.tldraw.shape": 4, "com.tldraw.asset.bookmark": 2, "com.tldraw.asset.image": 3, "com.tldraw.asset.video": 3, "com.tldraw.shape.group": 0, "com.tldraw.shape.text": 2, "com.tldraw.shape.bookmark": 2, "com.tldraw.shape.draw": 1, "com.tldraw.shape.geo": 8, "com.tldraw.shape.note": 6, "com.tldraw.shape.line": 4, "com.tldraw.shape.frame": 0, "com.tldraw.shape.arrow": 4, "com.tldraw.shape.highlight": 0, "com.tldraw.shape.embed": 4, "com.tldraw.shape.image": 3, "com.tldraw.shape.video": 2, "com.tldraw.binding.arrow": 0}}}, "session": {"version": 0, "currentPageId": "page:page", "exportBackground": true, "isFocusMode": false, "isDebugMode": true, "isToolLocked": false, "isGridMode": false, "pageStates": [{"pageId": "page:page", "camera": {"x": 0, "y": 0, "z": 1}, "selectedShapeIds": [], "focusedGroupId": null}]}}'
    db_board = Board(
        name=board.name,
        owner_id=user_id,
        content=json.loads(content)
    )
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board


def update_board_content(db: Session, board_id: int, new_content: str):
    db_board = db.query(Board).filter(Board.id == board_id).first()

    if not db_board:
        return False
    db_board.content = json.loads(new_content)
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


def create_permissions(db, user_id, board_id, privilege):
    db_relation = Relation(
        user_id=user_id,
        board_id=board_id,
        privilege=privilege
    )
    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)
    return db_relation


def delete_permissions(db, user_id, board_id):
    db.query(Relation).filter(Relation.user_id == user_id, Relation.board_id == board_id).delete()
    db.commit()


def get_permissions(db, user_id, board_id):
    return db.query(Relation).filter(Relation.user_id == user_id, Relation.board_id == board_id).first()


def get_all_relations(db, user_id):
    return db.query(Relation).filter(Relation.user_id == user_id).all()