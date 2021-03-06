from datetime import datetime
from uuid import uuid4
from typing import Optional

from sqlalchemy import Column, String, Boolean, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from utils import text_styles


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    def __init__(
            self, username: str, is_admin: bool, first_name: str, last_name: str,
            password_hash: Optional[str] = None, password_set: Optional[datetime] = None
    ):
        super(User, self).__init__()
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.first_name = first_name
        self.last_name = last_name
        self.password_set = password_set

    def __str__(self):
        return (text_styles.red if self.is_admin else text_styles.green)(repr(self))

    def __repr__(self):
        return f"User(first_name={self.first_name}, last_name={self.last_name}, username={self.username})"

    id = Column(String(36), nullable=False, primary_key=True, default=lambda: str(uuid4()))
    username = Column(String(64), nullable=False)
    password_hash = Column(String(256), nullable=True)
    is_admin = Column(Boolean(), nullable=False)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    password_set = Column(DateTime(), nullable=True)


class Repository:
    def __init__(self, connection_string: str):
        engine = create_engine(connection_string)
        self.session = sessionmaker(bind=engine)()
        Base.metadata.create_all(engine)

    def add_or_update_user(self, user: User):
        self.session.merge(user)
        self.session.commit()

    def delete_user(self, user: User):
        self.session.delete(user)
        self.session.commit()

    def get_user_by_id(self, user_id: str) -> User:
        return self.session.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> User:
        return self.session.query(User).filter(User.username == username).first()
