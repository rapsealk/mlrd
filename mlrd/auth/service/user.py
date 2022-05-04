from abc import ABC
from typing import Optional

import bcrypt
from sqlalchemy.orm import Session

from mlrd.auth.domain import User
from mlrd.auth.schema import UserCreate, UserUpdate, UserDelete


class BaseUserService(ABC):
    def hash_password(self, password: str, salt: Optional[str] = None):
        salt = salt or bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt)


class UserService(BaseUserService):
    def __init__(self):
        super(UserService, self).__init__()

    async def create_user(self, *, db_session: Session, user_in: UserCreate, secret: Optional[str] = None) -> Optional[User]:
        user_in.password = self.hash_password(user_in.password, salt=secret)
        try:
            user = User(**user_in.dict())
            db_session.add(user)
            db_session.commit()
        except Exception:
            return None
        return user

    async def find_user(self, *, db_session: Session, **kwargs) -> Optional[User]:
        if user_id := kwargs.get("id"):
            return db_session.query(User).filter(User.id == user_id).first()
        elif username := kwargs.get("username"):
            return db_session.query(User).filter(User.username == username).first()
        elif email := kwargs.get("email"):
            return db_session.query(User).filter(User.email == email).first()
        return None

    async def update_user(self, *, db_session: Session, user_in: UserUpdate) -> Optional[User]:
        if not (user := await self.find_user(db_session=db_session, id=user_in.id)):
            return None

        new_data = user_in.dict(skip_defaults=True, exclude={"id"})

        for field in user.dict():
            if field in new_data:
                setattr(user, field, new_data[field])

        db_session.commit()

        return user

    async def delete_user(self, *, db_session: Session, user_in: UserDelete):
        db_session.query(User).filter(User.id == user_in.id).delete()
        db_session.commit()
