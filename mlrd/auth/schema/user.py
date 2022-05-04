from mlrd.models import MLRDBase, PrimaryKey


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
