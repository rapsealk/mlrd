from typing import Optional

from sqlalchemy import Column, Integer, String

from mlrd.database import Base
from mlrd.models import MLRDBase, PrimaryKey, TimeStampMixin


class Device(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    address = Column(String(15), nullable=False)
    uuid = Column(String(32), unique=True)
    total_global_memory = Column(Integer, nullable=False)


class DeviceBase(MLRDBase):
    pass


class DeviceCreate(DeviceBase):
    address: str
    uuid: str
    total_global_memory: int


class DeviceRead(DeviceBase):
    id: PrimaryKey
    address: str
    uuid: str
    total_global_memory: int


class DeviceUpdate(DeviceBase):
    id: PrimaryKey
    address: Optional[str] = None
    uuid: Optional[str] = None
    total_global_memory: Optional[int] = None


class DeviceDelete(DeviceBase):
    id: PrimaryKey
