import re

from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import Session
from starlette.requests import Request
from sqlalchemy_utils import create_database, database_exists


def get_db(request: Request) -> Session:
    return request.state.db


def resolve_table_name(name: str):
    names = re.split("(?=[A-Z])", name)
    return "_".join([x.lower() for x in names if x])


class CustomBase:
    __repr_attrs__ = []
    __repr_max_length__ = 15

    @declared_attr
    def __tablename__(self):
        return resolve_table_name(self.__name__)

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__tablename__.columns}

    @property
    def _id_str(self):
        if ids := inspect(self).identity:
            return "-".join([str(x) for x in ids]) if len(ids) > 1 else str(ids[0])
        return "None"

    @property
    def _repr_attrs_str(self):
        max_length = self.__repr_max_length__
        values = []
        single = len(self.__repr_attrs__) == 1
        for key in self.__repr_attrs__:
            if not hasattr(self, key):
                raise KeyError(f"{self.__class__} has incorrect attribute '{key}' in __repr_attrs__.")
            value = getattr(self, key)
            wrap_in_quote = isinstance(value, str)

            value = str(value)
            if len(value) > max_length:
                value = value[:max_length] + "..."

            if wrap_in_quote:
                value = f"'{value}'"

            values.append(value if single else f"{key}:{value}")

        return " ".join(values)

    def __repr__(self):
        # get id like "#123"
        id_str = ("#" + self._id_str) if self._id_str else ""
        # join class name, id and repr_attrs
        return f"<{self.__class__.__name__} {id_str}{' ' + self._repr_attrs_str if self._repr_attrs_str else ''}>"


Base = declarative_base(cls=CustomBase)


class Database:
    def __init__(self, url):
        if not database_exists(url):
            create_database(url)

        self._engine = create_engine(url)

    def initialize(self):
        from mlrd.auth.models import User   # noqa: F401

        Base.metadata.create_all(self.engine)

    @property
    def engine(self) -> Engine:
        return self._engine
