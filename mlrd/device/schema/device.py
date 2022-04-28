from datetime import datetime
from typing import Optional

from mlrd.models import MLRDBase, PrimaryKey


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
    created_at: datetime
    last_modified_at: datetime


class DeviceUpdate(DeviceBase):
    id: PrimaryKey
    address: Optional[str] = None
    uuid: Optional[str] = None
    total_global_memory: Optional[int] = None


class DeviceDelete(DeviceBase):
    id: PrimaryKey
