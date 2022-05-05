import abc
from typing import List, Optional

from sqlalchemy.orm import Session

from mlrd.auth.domain import User
from mlrd.auth.schema import UserCreate, UserDelete, UserUpdate


class BaseUserRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, *, user_in: UserCreate) -> Optional[User]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def find(self, **kwargs) -> Optional[User]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def find_all(self, **kwargs) -> List[User]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def update(self, user_in: UserUpdate) -> Optional[User]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete(self, user_in: UserDelete) -> Optional[User]:
        raise NotImplementedError()


class UserRepository(BaseUserRepository):
    def __init__(self, session: Session):
        super(UserRepository, self).__init__()
        self._session = session

    async def create(self, *, user_in: UserCreate) -> Optional[User]:
        try:
            user = User(**user_in.dict())
            self._session.add(user)
            self._session.commit()
        except TypeError:
            return None
        return user

    async def find(self, **kwargs) -> Optional[User]:
        assert len(kwargs) == 1 and set(kwargs.keys()).issubset(set(["id", "username", "email"]))
        if user_id := kwargs.get("id"):
            return self._session.query(User).filter(User.id == user_id).first()
        elif username := kwargs.get("username"):
            return self._session.query(User).filter(User.username == username).first()
        elif email := kwargs.get("email"):
            return self._session.query(User).filter(User.email == email).first()
        return None

    async def find_all(self, **kwargs) -> List[User]:
        assert len(kwargs) == 1 and set(kwargs.keys()).issubset(set(["id", "username", "email"]))
        if user_id := kwargs.get("id"):
            return self._session.query(User).filter(User.id == user_id).all()
        elif username := kwargs.get("username"):
            return self._session.query(User).filter(User.username == username).all()
        elif email := kwargs.get("email"):
            return self._session.query(User).filter(User.email == email).all()
        return []

    async def update(self, user_in: UserUpdate) -> Optional[User]:
        if not (user := await self.find(id=user_in.id)):
            return None
        new_data = user_in.dict(skip_defaults=True, exclude={"id"})
        for field in user.dict():
            if field in new_data:
                setattr(user, field, new_data[field])
        self._session.commit()
        return user

    async def delete(self, user_in: UserDelete) -> bool:
        rows = self._session.query(User).filter(User.id == user_in.id).delete()
        self._session.commit()
        return rows > 0
