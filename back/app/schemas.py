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
    owner_id: int
    content: Optional[dict]


class BoardResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    content: Optional[dict]

    class Config:
        orm_mode = True
