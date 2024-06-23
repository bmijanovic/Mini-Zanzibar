from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DATABASE_URL = "postgresql://postgres:postgres@postgres/postgres"

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


Base.metadata.create_all(bind=engine)
