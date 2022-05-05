import bcrypt
from sqlalchemy import Boolean, Column, Integer, String

from mlrd.database import Base
from mlrd.models import TimeStampMixin


class User(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(4), nullable=False)
    username = Column(String(16), unique=True)
    email = Column(String(256), unique=True)
    password = Column(String(60), nullable=False)
    is_verified = Column(Boolean, default=False)

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def verify(self):
        self.is_verified = True
