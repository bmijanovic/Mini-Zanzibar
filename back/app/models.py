import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()
engine = create_engine(DATABASE_URL)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    boards = relationship("Board", back_populates="owner")


class Board(Base):
    __tablename__ = 'boards'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, index=True)
    content = Column(JSON, nullable=True)

    owner = relationship("User", back_populates="boards")


class Relation(Base):
    __tablename__ = 'relations'
    user_id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer, primary_key=True ,index=True)
    privilege = Column(String, index=True)


Base.metadata.create_all(bind=engine)
