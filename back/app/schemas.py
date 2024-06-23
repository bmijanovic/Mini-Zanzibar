from pydantic import BaseModel, Field
from typing import Optional


class UserCreate(BaseModel):
    name: str
    surname: str
    email: str
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str = Field(..., min_length=8)


class BoardCreate(BaseModel):
    name: str
    content: Optional[dict]


class BoardContentUpdate(BaseModel):
    board_content: str
    board_id: int


class BoardResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    content: Optional[dict]

    class Config:
        orm_mode = True
class SingleBoardResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    content: dict
    privilege: str

    class Config:
        orm_mode = True



class BoardForUserResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    owner_name: str
    privilege: str

    class Config:
        orm_mode = True


class AllBoardsResponse(BaseModel):
    my_boards: list[BoardForUserResponse]
    shared_boards: list[BoardForUserResponse]

    class Config:
        orm_mode = True


class ShareDTO(BaseModel):
    email: str
    board_id: int
    role: str
