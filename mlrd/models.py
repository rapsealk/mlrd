from datetime import datetime, timedelta, timezone
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, validator
from pydantic.generics import GenericModel
from pydantic.types import conint
from sqlalchemy import Column, DateTime, event

DataT = TypeVar("DataT")

INT32_MAX = 2 ** 31 - 1

PrimaryKey = conint(gt=0, le=INT32_MAX)

KST = timezone(timedelta(hours=9))


class TimeStampMixin:
    created_at = Column(DateTime, default=lambda: datetime.now(tz=KST))
    created_at._creation_order = 9998
    last_modified_at = Column(DateTime, default=lambda: datetime.now(tz=KST))
    last_modified_at._creation_order = 9998

    @staticmethod
    def _last_modified_at(mapper, connection, target):
        target.last_modified_at = datetime.now(tz=KST)

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._last_modified_at)


class MLRDBase(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        arbitrary_types_allows = True
        anystr_strip_whitespace = True
        json_encoders = {
            datetime: lambda dt: dt.strftime("%Y-%m-%dT%H:%M:%SZ") if dt else None
        }


class Error(BaseModel):
    code: int
    message: str

class Response(GenericModel, Generic[DataT]):
    data: Optional[DataT]
    error: Optional[Error]

    @validator("error", always=True)
    def check_consistency(cls, v, values):
        if v is not None and values["data"] is not None:
            raise ValueError("must not provide both data and error.")
        if v is None and values.get("data") is None:
            raise ValueError("must provide data or error.")
        return v
