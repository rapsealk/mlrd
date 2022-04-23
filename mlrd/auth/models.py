import bcrypt
from sqlalchemy import Column, Integer, LargeBinary, String

from mlrd.database import Base
from mlrd.models import MLRDBase, PrimaryKey, TimeStampMixin


class User(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(4), nullable=False)
    username = Column(String(16), unique=True)
    email = Column(String(256), unique=True)
    password = Column(LargeBinary, nullable=False)

    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)


class UserBase(MLRDBase):
    pass


class UserCreate(UserBase):
    name: str
    username: str
    email: str
    password: str


class UserRead(UserBase):
    id: PrimaryKey
    name: str
    username: str
    email: str


class UserUpdate(UserBase):
    id: PrimaryKey
    username: str
    password: str


class UserDelete(UserBase):
    id: PrimaryKey
