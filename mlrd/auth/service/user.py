import abc
from typing import Optional

import bcrypt
from sqlalchemy.orm import Session

from mlrd.auth.domain import User
from mlrd.auth.repositories import UserRepository
from mlrd.auth.schema import UserCreate, UserUpdate, UserDelete


class BaseUserService(abc.ABC):
    @abc.abstractmethod
    async def signup(self, *, user_in: UserCreate) -> Optional[User]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def signin(self, *, email: str, password: str) -> Optional[User]:
        raise NotImplementedError()

    def hash_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt)


class UserService(BaseUserService):
    def __init__(self, session: Session):
        super(UserService, self).__init__()
        self._repository = UserRepository(session=session)

    async def signup(self, *, user_in: UserCreate) -> Optional[User]:
        user_in.password = self.hash_password(password=user_in.password)
        return await self._repository.create(user_in=user_in)

    async def signin(self, *, email: str, password: str) -> Optional[User]:
        if not (user := await self._repository.find(email=email)):
            return None
        if not user.check_password(password):
            return None
        return user

    async def search_by(self, **kwargs) -> Optional[User]:
        return await self._repository.find(**kwargs)

    async def update(self, *, user_in: UserUpdate) -> Optional[User]:
        return await self._repository.update(user_in=user_in)

    async def delete(self, *, user_in: UserDelete) -> bool:
        return await self._repository.delete(user_in=user_in)
